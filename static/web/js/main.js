document.documentElement.classList.add('js-ready');

function setPiMotionState(enabled, persist = false) {
  document.documentElement.classList.toggle('pi-motion-enabled', enabled);
  document.documentElement.classList.toggle('pi-motion-disabled', !enabled);

  if (persist) {
    try {
      window.localStorage.setItem('pi-motion', enabled ? 'on' : 'off');
    } catch (error) {
      // The visual preference still works for this page when storage is unavailable.
    }
  }

  document.querySelectorAll('[data-motion-toggle]').forEach((button) => {
    button.setAttribute('aria-pressed', String(enabled));
    button.setAttribute('aria-label', enabled ? 'Pause animation' : 'Enable animation');
    const label = button.querySelector('[data-motion-label]');
    if (label) label.textContent = enabled ? 'MOTION ON' : 'MOTION OFF';
  });
}

function isPiMotionEnabled() {
  return document.documentElement.classList.contains('pi-motion-enabled');
}

function initPiMotionPreference() {
  // Keep old preview links on the same canonical experience, preserving other parameters.
  try {
    const pageUrl = new URL(window.location.href);
    if (pageUrl.searchParams.has('motion')) {
      pageUrl.searchParams.delete('motion');
      window.history.replaceState(window.history.state, '', pageUrl.pathname + pageUrl.search + pageUrl.hash);
    }
  } catch (error) {
    // URL cleanup must never prevent the site from loading.
  }
  if (document.body.classList.contains('home-page')) {
    setPiMotionState(true);
    return;
  }
  let stored = null;
  try { stored = window.localStorage.getItem('pi-motion'); } catch (error) {}
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  setPiMotionState(!reduced && stored !== 'off');
}

initPiMotionPreference();

function cssColorToNumber(name, fallback) {
  const value = getComputedStyle(document.documentElement).getPropertyValue(name).trim().replace('#', '');
  return /^[0-9a-fA-F]{6}$/.test(value) ? parseInt(value, 16) : fallback;
}

function initVanta() {
  if (!window.VANTA || typeof window.VANTA.GLOBE !== 'function') return;
  const el = document.getElementById('vanta-hero');
  if (!el) return;

  if (el.__vanta) {
    el.__vanta.destroy();
    el.__vanta = null;
  }

  const primaryColor = cssColorToNumber('--color-primary', 0x2d6cdf);
  const accentColor = cssColorToNumber('--color-accent', 0x0ea5e9);
  const bgColor = cssColorToNumber('--color-bg', 0x0b0f14);

  el.__vanta = window.VANTA.GLOBE({
    el,
    mouseControls: true,
    touchControls: true,
    gyroControls: true,
    minHeight: 200.0,
    minWidth: 200.0,
    scale: 1.0,
    scaleMobile: 1.0,
    color: primaryColor,
    color2: accentColor,
    backgroundColor: bgColor
  });
}

function initNavbar() {
  const nav = document.getElementById('Topnav');
  const navLinks = document.getElementById('navLinks');
  const menuBtn = document.querySelector('.menu-icon');
  const progressBar = document.getElementById('progress-bar');
  const fadeText = document.getElementById('fade-text');
  const hero = document.querySelector('.company-hero, .showcase');
  const socialLinks = document.querySelector('.social');
  let scrollThreshold = hero ? window.innerHeight * 0.8 : 0;
  let docHeight = 0;
  let scrollPending = false;

  function updateDocumentHeight() {
    docHeight = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
  }

  function syncNavbarState() {
    if (!nav) return;
    const shouldShowSolid = !hero || window.scrollY > scrollThreshold || nav.classList.contains('menu-open');
    nav.classList.toggle('scrolled', shouldShowSolid);
  }

  function syncHeroEffects() {
    if (!hero) return;

    const heroHeight = Math.max(hero.offsetHeight, window.innerHeight);
    const isMobileHero = window.innerWidth <= 769;
    const textProgress = Math.min(window.scrollY / (heroHeight * 0.58), 1);
    const socialProgress = Math.min(window.scrollY / (heroHeight * 0.42), 1);

    if (fadeText) {
      if (isMobileHero) {
        fadeText.style.opacity = '1';
        fadeText.style.transform = 'translate3d(0, 0, 0)';
      } else {
        fadeText.style.opacity = String(1 - textProgress);
        fadeText.style.transform = `translate3d(0, ${textProgress * 18}px, 0)`;
      }
    }

    if (socialLinks) {
      if (isMobileHero) {
        socialLinks.style.opacity = '1';
        socialLinks.style.transform = 'translate3d(0, 0, 0)';
        socialLinks.style.filter = 'blur(0)';
      } else {
        socialLinks.style.opacity = String(1 - socialProgress * 0.75);
        socialLinks.style.transform = `translate3d(0, ${socialProgress * 10}px, 0)`;
        socialLinks.style.filter = `blur(${socialProgress * 2.2}px)`;
      }
    }
  }

  function syncProgressBar() {
    if (!progressBar) return;

    const scrollTop = window.scrollY;
    const progress = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    progressBar.style.width = `${progress}%`;
  }

  function closeMenu() {
    if (navLinks) {
      navLinks.classList.remove('active');
    }
    if (menuBtn) {
      menuBtn.setAttribute('aria-expanded', 'false');
      menuBtn.setAttribute('aria-label', 'Open navigation');
    }
    if (nav) {
      nav.classList.remove('menu-open');
    }
    syncNavbarState();
  }

  function toggleMenu() {
    if (!navLinks || !menuBtn) return;
    const isOpen = navLinks.classList.toggle('active');
    menuBtn.setAttribute('aria-expanded', String(isOpen));
    menuBtn.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    if (nav) {
      nav.classList.toggle('menu-open', isOpen);
    }
    syncNavbarState();
    if (isOpen) {
      navLinks.querySelector('a')?.focus();
    }
  }

  if (menuBtn) {
    menuBtn.addEventListener('click', toggleMenu);
  }

  if (navLinks) {
    navLinks.querySelectorAll('a').forEach((link) => {
      link.addEventListener('click', closeMenu);
    });
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && navLinks?.classList.contains('active')) {
      closeMenu();
      menuBtn?.focus();
    }
  });

  document.addEventListener('click', (event) => {
    if (!nav?.classList.contains('menu-open') || nav.contains(event.target)) return;
    closeMenu();
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) {
      closeMenu();
    }
    scrollThreshold = hero ? window.innerHeight * 0.8 : 0;
    updateDocumentHeight();
    syncHeroEffects();
    syncNavbarState();
    syncProgressBar();
  });

  window.addEventListener('scroll', () => {
    if (scrollPending) return;
    scrollPending = true;
    requestAnimationFrame(() => {
      scrollPending = false;
      syncNavbarState();
      syncHeroEffects();
      syncProgressBar();
    });
  }, { passive: true });

  updateDocumentHeight();
  window.addEventListener('load', () => { updateDocumentHeight(); syncProgressBar(); }, { once: true });
  document.fonts?.ready.then(() => { updateDocumentHeight(); syncProgressBar(); });
  syncHeroEffects();
  syncProgressBar();
  syncNavbarState();
}

function initProcesoAnimation() {
  const procesoSteps = document.querySelectorAll('.proceso-step');
  if (!procesoSteps.length) return;

  function revealSteps() {
    const trigger = window.innerHeight * 0.85;
    procesoSteps.forEach((step, i) => {
      const top = step.getBoundingClientRect().top;
      if (top < trigger) {
        setTimeout(() => {
          step.classList.add('visible');
        }, i * 200);
      }
    });
  }

  window.addEventListener('scroll', revealSteps);
  window.addEventListener('load', revealSteps);
}

function initAnalyzeForms() {
  const forms = document.querySelectorAll('[data-analyze-form]');
  if (!forms.length) return;

  forms.forEach((form) => {
    form.addEventListener('submit', (event) => {
      if (form.dataset.browserTool) return;
      const submitButton = event.submitter || form.querySelector('button[type="submit"]');
      if (!submitButton || submitButton.disabled || submitButton.name) return;

      submitButton.disabled = true;
      submitButton.dataset.originalText = submitButton.textContent;
      submitButton.textContent = submitButton.dataset.loadingText || 'Analyzing...';
    });
  });
}

function initCopyButtons() {
  const copyButtons = document.querySelectorAll('[data-copy-button]');
  if (!copyButtons.length) return;

  copyButtons.forEach((button) => {
    button.addEventListener('click', async () => {
      const targetId = button.dataset.copyTarget;
      const target = targetId ? document.getElementById(targetId) : null;
      if (!target) return;

      const value = target.value || target.textContent || '';
      const feedback = button.closest('[data-copy-group]')?.querySelector('[data-copy-feedback]')
        || button.parentElement?.querySelector('[data-copy-feedback]');
      const originalText = button.dataset.originalText || button.textContent;
      button.dataset.originalText = originalText;

      try {
        await navigator.clipboard.writeText(value);
        button.textContent = button.dataset.copiedText || 'Copied';
        if (feedback) {
          feedback.textContent = button.dataset.copySuccess || 'Copied to clipboard.';
        }
        sendAnalyticsEvent('tool_result_copy', {
          tool_name: button.closest('form[data-browser-tool]')?.dataset.browserTool || 'utm-builder'
        });
      } catch (error) {
        if (feedback) {
          feedback.textContent = 'Could not copy automatically. Please copy the text manually.';
        }
      }

      window.setTimeout(() => {
        button.textContent = originalText;
      }, 1800);
    });
  });
}

function initPiCore() {
  const core = document.querySelector('[data-pi-core]');
  if (!core) return;

  function resetCore() {
    core.style.setProperty('--core-rx', '0deg');
    core.style.setProperty('--core-ry', '0deg');
    core.style.setProperty('--glow-x', '50%');
    core.style.setProperty('--glow-y', '48%');
  }

  core.addEventListener('pointermove', (event) => {
    if (!isPiMotionEnabled()) return;
    const bounds = core.getBoundingClientRect();
    const x = Math.max(0, Math.min(1, (event.clientX - bounds.left) / bounds.width));
    const y = Math.max(0, Math.min(1, (event.clientY - bounds.top) / bounds.height));

    core.style.setProperty('--core-rx', `${((0.5 - y) * 4.5).toFixed(2)}deg`);
    core.style.setProperty('--core-ry', `${((x - 0.5) * 5.5).toFixed(2)}deg`);
    core.style.setProperty('--glow-x', `${(x * 100).toFixed(1)}%`);
    core.style.setProperty('--glow-y', `${(y * 100).toFixed(1)}%`);
  });

  core.addEventListener('pointerleave', resetCore);
  core.addEventListener('blur', resetCore);
}

function initAudienceCascade() {
  const items = [...document.querySelectorAll('[data-cascade-item]')];
  if (!items.length) return;
  let replayTimer = null;
  let visible = false;

  function replayCascade() {
    if (!isPiMotionEnabled() || !visible || document.hidden) return;
    items.forEach((item) => item.classList.remove('is-cascading'));
    void items[0].offsetWidth;

    items
      .map((item) => ({ item, order: Math.random() }))
      .sort((a, b) => a.order - b.order)
      .forEach(({ item }, index) => {
        item.style.setProperty('--cascade-delay', `${index * 155 + Math.round(Math.random() * 130)}ms`);
        item.classList.add('is-cascading');
      });

    replayTimer = window.setTimeout(replayCascade, 5600 + Math.round(Math.random() * 2600));
  }

  document.addEventListener('pi:motionchange', (event) => {
    window.clearTimeout(replayTimer);
    if (event.detail?.enabled && visible) {
      replayCascade();
    } else {
      items.forEach((item) => item.classList.remove('is-cascading'));
    }
  });

  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      window.clearTimeout(replayTimer);
      if (visible) replayCascade();
    }, { rootMargin: '100px' }).observe(items[0].parentElement);
  } else {
    visible = true;
    replayCascade();
  }
  document.addEventListener('visibilitychange', () => {
    window.clearTimeout(replayTimer);
    if (!document.hidden) replayCascade();
  });
}

function initMetricBoards() {
  const boards = document.querySelectorAll('[data-metric-board]');
  if (!boards.length) return;

  const glyphs = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';

  function animateMetric(metric, metricIndex) {
    const target = metric.dataset.metricValue || metric.textContent.trim();
    const characters = [...target];
    metric.setAttribute('aria-label', target);
    metric.textContent = '';

    characters.forEach((targetCharacter, characterIndex) => {
      const character = document.createElement('span');
      character.setAttribute('aria-hidden', 'true');
      character.textContent = targetCharacter;

      if (!/[0-9A-Z]/i.test(targetCharacter)) {
        metric.appendChild(character);
        return;
      }

      character.className = 'pi-flip-char is-flipping';
      metric.appendChild(character);
      const turns = 7 + metricIndex * 2 + characterIndex;
      let turn = 0;

      const timer = window.setInterval(() => {
        character.textContent = glyphs[Math.floor(Math.random() * glyphs.length)];
        turn += 1;

        if (turn >= turns) {
          window.clearInterval(timer);
          character.textContent = targetCharacter;
          character.classList.remove('is-flipping');
          window.setTimeout(() => character.classList.add('is-settled'), 420);
        }
      }, 48 + characterIndex * 5);
    });
  }

  function animateBoard(board) {
    if (board.dataset.metricAnimated === 'true' || !isPiMotionEnabled()) return;
    board.dataset.metricAnimated = 'true';
    board.querySelectorAll('.pi-metric-value').forEach((metric, index) => {
      window.setTimeout(() => animateMetric(metric, index), index * 125);
    });
  }

  if (!('IntersectionObserver' in window)) {
    boards.forEach(animateBoard);
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      if (!isPiMotionEnabled()) return;
      animateBoard(entry.target);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.34 });

  boards.forEach((board) => observer.observe(board));

  document.addEventListener('pi:motionchange', (event) => {
    if (!event.detail?.enabled) return;
    boards.forEach((board) => {
      const bounds = board.getBoundingClientRect();
      if (bounds.top < window.innerHeight && bounds.bottom > 0) animateBoard(board);
    });
  });
}

function initPiMotionControls() {
  const buttons = document.querySelectorAll('[data-motion-toggle]');
  if (!buttons.length) return;

  setPiMotionState(isPiMotionEnabled());
  buttons.forEach((button) => {
    button.addEventListener('click', () => {
      const enabled = !isPiMotionEnabled();
      setPiMotionState(enabled, true);
      document.dispatchEvent(new CustomEvent('pi:motionchange', { detail: { enabled } }));
    });
  });
}

function initProjectPreviews() {
  const previews = document.querySelectorAll('[data-project-preview]');
  if (!previews.length) return;

  previews.forEach((preview) => {
    const iframe = preview.querySelector('iframe[data-preview-src]');
    const liveRegion = preview.querySelector('[data-preview-live]');
    const loading = preview.querySelector('[data-preview-loading]');
    const launch = preview.querySelector('[data-preview-launch]');
    const launchLabel = preview.querySelector('[data-preview-launch-label]');
    const sizeButtons = preview.querySelectorAll('[data-preview-size-button]');
    const projectName = preview.dataset.projectName || 'unknown';
    let live = false;

    function setSize(size) {
      preview.dataset.previewSize = size;
      const selectedImage = preview.querySelector(`[data-preview-image="${size}"]`);
      if (selectedImage && !selectedImage.getAttribute('src')) {
        selectedImage.src = selectedImage.dataset.previewImageSrc;
      }
      sizeButtons.forEach((button) => {
        button.setAttribute('aria-pressed', String(button.dataset.previewSizeButton === size));
      });
    }

    function setLive(nextLive) {
      if (!iframe || !liveRegion || !launch || !launchLabel) return;
      live = nextLive;
      preview.classList.toggle('is-live', live);
      liveRegion.setAttribute('aria-hidden', String(!live));
      launch.setAttribute('aria-pressed', String(live));
      launchLabel.textContent = live ? 'Close preview' : 'Live preview';

      if (live) {
        preview.classList.remove('is-preview-loaded');
        if (loading) loading.textContent = 'Loading live project…';
        if (!iframe.src || iframe.src === 'about:blank') iframe.src = iframe.dataset.previewSrc;
        sendAnalyticsEvent('project_preview_open', { project_name: projectName });
      } else {
        iframe.src = 'about:blank';
        preview.classList.remove('is-preview-loaded');
      }
    }

    sizeButtons.forEach((button) => {
      button.addEventListener('click', () => setSize(button.dataset.previewSizeButton));
    });

    launch?.addEventListener('click', () => setLive(!live));
    iframe?.addEventListener('load', () => {
      if (!live || iframe.src === 'about:blank') return;
      preview.classList.add('is-preview-loaded');
      if (loading) loading.textContent = 'Live project loaded';
    });

    setSize(window.innerWidth <= 620 ? 'mobile' : 'desktop');
  });
}

function sendAnalyticsEvent(eventName, parameters = {}) {
  return window.PiAnalytics?.track(eventName, parameters) || false;
}

function analyticsIsMeasuring() {
  return window.PiAnalytics?.isMeasuring?.() ?? window.PiAnalytics?.isEnabled?.() ?? false;
}

const EDITORIAL_ORIGIN_KEY = 'pi-editorial-origin-v1';
const EDITORIAL_READER_KEY = 'pi-editorial-reader-v1';

function editorialContext() {
  const article = document.querySelector('[data-editorial-article]');
  if (!article) return null;
  return {
    element: article,
    slug: article.dataset.articleSlug || 'unknown',
    type: article.dataset.articleType || 'article',
    cluster: article.dataset.articleCluster || 'uncategorized'
  };
}

function readStoredEditorialOrigin() {
  if (!window.PiAnalytics?.isEnabled()) return null;
  try {
    const value = JSON.parse(window.localStorage.getItem(EDITORIAL_ORIGIN_KEY) || 'null');
    if (!value || !value.slug || !value.recorded_at) return null;
    const thirtyDays = 30 * 24 * 60 * 60 * 1000;
    return Date.now() - Number(value.recorded_at) <= thirtyDays ? value : null;
  } catch (error) {
    return null;
  }
}

function storeEditorialOrigin(context) {
  if (!window.PiAnalytics?.isEnabled()) return;
  try {
    window.localStorage.setItem(EDITORIAL_ORIGIN_KEY, JSON.stringify({
      slug: context.slug,
      cluster: context.cluster,
      recorded_at: Date.now()
    }));
  } catch (error) {
    // Measurement remains functional when storage is unavailable.
  }
}

function editorialCommercialDestination(pathname) {
  const destinations = [
    ['/contact/', 'contact'],
    ['/soluciones-para-negocios/', 'business_solutions'],
    ['/planes-web/', 'web_plans'],
    ['/solutions/', 'solutions'],
    ['/adtech/', 'adtech'],
    ['/work/', 'work'],
    ['/products/', 'products'],
    ['/company/', 'company']
  ];
  const match = destinations.find(([prefix]) => pathname.startsWith(prefix));
  return match ? match[1] : null;
}

function editorialAttributionParameters() {
  const origin = readStoredEditorialOrigin();
  return origin ? { origin_article_slug: origin.slug, origin_article_cluster: origin.cluster } : {};
}

function initEditorialAnalytics() {
  const context = editorialContext();
  if (!context) return;

  let returningReader = false;
  if (window.PiAnalytics?.isEnabled()) {
    try {
      returningReader = window.localStorage.getItem(EDITORIAL_READER_KEY) === 'seen';
      window.localStorage.setItem(EDITORIAL_READER_KEY, 'seen');
    } catch (error) {
      returningReader = false;
    }
  }

  storeEditorialOrigin(context);
  sendAnalyticsEvent('editorial_article_view', {
    article_slug: context.slug,
    article_type: context.type,
    article_cluster: context.cluster,
    returning_reader: returningReader ? 'yes' : 'no'
  });

  const reachedDepths = new Set();
  const depthThresholds = [25, 50, 75, 90];
  const reportDepth = () => {
    if (!analyticsIsMeasuring()) return;
    const articleTop = window.scrollY + context.element.getBoundingClientRect().top;
    const articleHeight = Math.max(context.element.offsetHeight, 1);
    const viewportBottom = window.scrollY + window.innerHeight;
    const progress = Math.max(0, Math.min(100, ((viewportBottom - articleTop) / articleHeight) * 100));
    depthThresholds.forEach((threshold) => {
      if (progress < threshold || reachedDepths.has(threshold)) return;
      reachedDepths.add(threshold);
      sendAnalyticsEvent('editorial_read_progress', {
        article_slug: context.slug,
        article_cluster: context.cluster,
        read_percent: threshold
      });
    });
  };

  let activeSeconds = 0;
  const reachedTimeMilestones = new Set();
  const timeMilestones = [30, 60, 120, 300];
  window.setInterval(() => {
    if (!analyticsIsMeasuring() || document.visibilityState !== 'visible' || !document.hasFocus()) return;
    activeSeconds += 5;
    timeMilestones.forEach((milestone) => {
      if (activeSeconds < milestone || reachedTimeMilestones.has(milestone)) return;
      reachedTimeMilestones.add(milestone);
      sendAnalyticsEvent('editorial_engaged_time', {
        article_slug: context.slug,
        article_cluster: context.cluster,
        milestone_seconds: milestone
      });
    });
  }, 5000);

  reportDepth();
  window.addEventListener('scroll', reportDepth, { passive: true });
  window.addEventListener('resize', reportDepth);
}

function analyticsLinkLocation(link) {
  if (link.closest('nav')) return 'navigation';
  if (link.closest('footer')) return 'footer';
  if (link.closest('.pi-home-hero, .business-hero, .plans-hero')) return 'hero';
  if (link.closest('.company-cta, .business-final-cta')) return 'page_cta';
  if (link.closest('[data-plan]')) return 'plan_card';
  if (link.closest('.company-contact-layout')) return 'contact_details';
  return 'content';
}

function initAnalyticsEvents() {
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a[href]');
    if (!link) return;

    let destination;
    try {
      destination = new URL(link.href, window.location.href);
    } catch (error) {
      return;
    }

    const location = analyticsLinkLocation(link);
    const label = (
      link.dataset.analyticsLabel
      || link.getAttribute('aria-label')
      || link.textContent
      || ''
    ).trim().slice(0, 100);
    const explicitEvent = link.dataset.analyticsEvent;
    const planName = link.closest('[data-plan]')?.dataset.plan;
    const contactContext = { ...editorialAttributionParameters(), ...(planName ? { plan_name: planName } : {}) };

    const currentArticle = editorialContext();
    const commercialDestination = destination.origin === window.location.origin
      ? editorialCommercialDestination(destination.pathname)
      : null;
    if (currentArticle && commercialDestination) {
      sendAnalyticsEvent('editorial_to_pi', {
        article_slug: currentArticle.slug,
        article_cluster: currentArticle.cluster,
        destination_section: commercialDestination,
        link_location: location
      });
    }

    if (explicitEvent) {
      sendAnalyticsEvent(explicitEvent, { link_location: location, link_text: label });
      return;
    }

    if (destination.protocol === 'mailto:') {
      sendAnalyticsEvent('contact_start', {
        contact_method: 'email',
        link_location: location,
        ...contactContext
      });
      return;
    }

    if (destination.protocol === 'tel:' || destination.hostname === 'wa.me') {
      sendAnalyticsEvent('contact_start', {
        contact_method: destination.hostname === 'wa.me' ? 'whatsapp' : 'phone',
        link_location: location,
        ...contactContext
      });
      return;
    }

    if (destination.origin === window.location.origin && destination.pathname === '/contact/') {
      sendAnalyticsEvent('contact_cta_click', {
        link_location: location,
        link_text: label,
        ...contactContext
      });
      return;
    }

    if (destination.protocol.startsWith('http') && destination.origin !== window.location.origin) {
      sendAnalyticsEvent('outbound_click', {
        link_domain: destination.hostname,
        link_location: location,
        link_text: label
      });
    }
  });

  document.addEventListener('pi:tool-complete', (event) => {
    sendAnalyticsEvent('tool_use', { tool_name: event.detail?.tool_name || 'unknown' });
  });

  document.addEventListener('pi:tool-error', (event) => {
    sendAnalyticsEvent('tool_error', {
      tool_name: event.detail?.tool_name || 'unknown',
      error_type: event.detail?.error_type || 'unknown'
    });
  });

  document.addEventListener('pi:tool-copy', (event) => {
    sendAnalyticsEvent('tool_result_copy', { tool_name: event.detail?.tool_name || 'unknown' });
  });

  document.addEventListener('pi:utm-preset', (event) => {
    sendAnalyticsEvent('utm_preset_select', { preset_name: event.detail?.preset_name || 'unknown' });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initVanta();
  initNavbar();
  initProcesoAnimation();
  initAnalyzeForms();
  initCopyButtons();
  initPiMotionControls();
  initPiCore();
  initAudienceCascade();
  initMetricBoards();
  initProjectPreviews();
  initAnalyticsEvents();
  let editorialStarted = false;
  function startEditorialMeasurement() {
    if (editorialStarted || !analyticsIsMeasuring()) return;
    editorialStarted = true;
    initEditorialAnalytics();
  }
  window.addEventListener('pi:analyticsready', startEditorialMeasurement);
  startEditorialMeasurement();
});
