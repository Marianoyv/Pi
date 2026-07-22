document.documentElement.classList.add('js-ready');

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
    const docHeight = document.body.scrollHeight - window.innerHeight;
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
    syncHeroEffects();
    syncNavbarState();
  });

  window.addEventListener('scroll', () => {
    syncNavbarState();
    syncHeroEffects();
    syncProgressBar();
  }, { passive: true });

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
    form.addEventListener('submit', () => {
      const submitButton = form.querySelector('button[type="submit"]');
      if (!submitButton || submitButton.disabled) return;

      submitButton.disabled = true;
      submitButton.dataset.originalText = submitButton.textContent;
      submitButton.textContent = submitButton.dataset.loadingText || 'Analizando...';
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
        button.textContent = button.dataset.copiedText || 'Copiado';
        if (feedback) {
          feedback.textContent = button.dataset.copySuccess || 'Copiado al portapapeles.';
        }
      } catch (error) {
        if (feedback) {
          feedback.textContent = 'No se pudo copiar automáticamente. Copia el texto manualmente.';
        }
      }

      window.setTimeout(() => {
        button.textContent = originalText;
      }, 1800);
    });
  });
}

window.handleContact = function (e) {
  e.preventDefault();

  const nombre = document.getElementById('nombre')?.value?.trim();
  const email = document.getElementById('correo_electronico')?.value?.trim();
  const proyecto = document.getElementById('proyecto')?.value?.trim();

  if (!nombre || !email || !proyecto) {
    alert('Completa nombre, correo y una descripción del problema.');
    return;
  }

  const phone = document.body.dataset.whatsappPhone || '5491170619703';
  const message = `Hola. Soy ${nombre}. Mi correo es ${email}. Necesito revisar o construir: ${proyecto}. Llego desde pidevelopment.web.app`;
  const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;

  window.open(url, '_blank', 'noopener,noreferrer');

  if (typeof gtag === 'function') {
    gtag('event', 'contact_submit', {
      method: 'whatsapp'
    });
  }
};

document.addEventListener('DOMContentLoaded', () => {
  initVanta();
  initNavbar();
  initProcesoAnimation();
  initAnalyzeForms();
  initCopyButtons();
});
