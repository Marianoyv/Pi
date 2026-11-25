(function () {
  'use strict';

  function cleanLine(value) {
    return String(value || '').replace(/\s+/g, ' ').trim();
  }

  function cleanParagraph(value) {
    return String(value || '')
      .split(/\r?\n/)
      .map(cleanLine)
      .filter(Boolean)
      .join('\n');
  }

  function buildBrief(values) {
    const projectType = cleanLine(values.project_type);
    const currentStage = cleanLine(values.current_stage);
    const outcome = cleanParagraph(values.outcome);
    const timeline = cleanLine(values.timeline);

    return [
      'Hello Mariano,',
      '',
      'I would like to discuss a possible Pi Development project.',
      '',
      `Project type: ${projectType}`,
      `Current stage: ${currentStage}`,
      '',
      'What should work better:',
      outcome,
      '',
      `Timing: ${timeline}`
    ].join('\n');
  }

  function buildLinks(brief, whatsappBaseUrl, email) {
    const whatsappBase = cleanLine(whatsappBaseUrl);
    let whatsappUrl = '';
    if (whatsappBase) {
      const whatsapp = new URL(whatsappBase);
      whatsapp.searchParams.set('text', brief);
      whatsappUrl = whatsapp.href;
    }
    const subject = 'Project inquiry | Pi Development';
    const emailAddress = cleanLine(email);
    return {
      whatsapp: whatsappUrl,
      email: emailAddress ? `mailto:${emailAddress}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(brief)}` : ''
    };
  }

  function valuesFrom(form) {
    return Object.fromEntries(new FormData(form).entries());
  }

  async function copyText(value) {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(value);
      return;
    }
    const helper = document.createElement('textarea');
    helper.value = value;
    helper.setAttribute('readonly', '');
    helper.style.position = 'fixed';
    helper.style.opacity = '0';
    document.body.appendChild(helper);
    helper.select();
    const copied = document.execCommand('copy');
    helper.remove();
    if (!copied) throw new Error('Copy was not available');
  }

  function initialize(form) {
    const result = form.parentElement.querySelector('[data-contact-brief-result]');
    const preview = result?.querySelector('[data-contact-brief-preview]');
    const whatsapp = result?.querySelector('[data-contact-brief-whatsapp]');
    const email = result?.querySelector('[data-contact-brief-email]');
    const copy = result?.querySelector('[data-contact-brief-copy]');
    const status = result?.querySelector('[data-contact-brief-status]');
    if (!result || !preview || !whatsapp || !email || !copy || !status) return;

    let currentBrief = '';

    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      currentBrief = buildBrief(valuesFrom(form));
      const links = buildLinks(currentBrief, form.dataset.whatsappUrl, form.dataset.contactEmail);
      preview.textContent = currentBrief;
      whatsapp.href = links.whatsapp;
      whatsapp.hidden = !links.whatsapp;
      email.href = links.email;
      email.hidden = !links.email;
      status.textContent = '';
      result.hidden = false;
      result.focus({ preventScroll: true });
      result.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });

    copy.addEventListener('click', async () => {
      if (!currentBrief) return;
      try {
        await copyText(currentBrief);
        status.textContent = 'Brief copied.';
      } catch (_error) {
        status.textContent = 'Copy was not available. Select the brief above and copy it manually.';
      }
    });
  }

  window.PiContactBrief = Object.freeze({ buildBrief, buildLinks });
  document.querySelectorAll('[data-contact-brief]').forEach(initialize);
}());
