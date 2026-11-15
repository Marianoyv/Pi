import { animate } from 'https://cdn.jsdelivr.net/npm/motion@13.1.1/mini/+esm';

const activeAnimations = new Set();
const observedElements = new WeakSet();

function motionIsEnabled() {
  return document.documentElement.classList.contains('pi-motion-enabled');
}

function remember(animation) {
  activeAnimations.add(animation);
  Promise.resolve(animation.finished)
    .then(() => animation.cancel?.())
    .catch(() => {})
    .finally(() => activeAnimations.delete(animation));
  return animation;
}

function reveal(elements, options = {}) {
  if (!motionIsEnabled()) return;
  const list = [...elements];
  const distance = options.distance ?? 24;
  const duration = options.duration ?? 0.82;
  const stagger = options.stagger ?? 0.075;
  const delay = options.delay ?? 0;

  list.forEach((element, index) => {
    remember(animate(
      element,
      {
        opacity: [0, 1],
        transform: [`translate3d(0, ${distance}px, 0)`, 'translate3d(0, 0, 0)'],
      },
      {
        duration,
        delay: delay + index * stagger,
        ease: [0.22, 0.75, 0.25, 1],
      },
    ));
  });
}

function revealOnce(element) {
  if (element.dataset.motionRevealed === 'true' || !motionIsEnabled()) return;
  element.dataset.motionRevealed = 'true';

  if (element.matches('.pi-service-row')) {
    reveal(element.children, { stagger: 0.095, distance: 20 });
    return;
  }

  if (element.matches('.pi-home-case, .portfolio-overview__card--case')) {
    reveal(element.children, { stagger: 0.11, distance: 34, duration: 0.95 });
    return;
  }

  reveal([element], { distance: 28 });
}

function observePageReveals() {
  const targets = document.querySelectorAll([
    '.pi-section-head',
    '.pi-human-signal',
    '.pi-service-row',
    '.pi-home-case',
    '.portfolio-overview__card--case',
    '.pi-method__steps > li',
    '.pi-tool-tile',
  ].join(','));

  if (!('IntersectionObserver' in window)) {
    targets.forEach(revealOnce);
    return;
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      if (!motionIsEnabled()) return;
      revealOnce(entry.target);
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -7% 0px' });

  targets.forEach((target) => {
    if (observedElements.has(target)) return;
    observedElements.add(target);
    observer.observe(target);
  });
}

function runOpeningSequence() {
  if (!motionIsEnabled() || document.body.dataset.motionOpening === 'true') return;
  document.body.dataset.motionOpening = 'true';

  reveal(document.querySelectorAll('.pi-home-hero__copy > *'), {
    distance: 30,
    stagger: 0.095,
    duration: 0.9,
  });

  const core = document.querySelector('[data-pi-core]');
  if (core) {
    remember(animate(core, { opacity: [0, 1] }, { duration: 1.05, delay: 0.18, easing: 'ease-out' }));
    reveal(core.querySelectorAll('.pi-core__node'), {
      distance: 18,
      stagger: 0.12,
      duration: 0.72,
      delay: 0.42,
    });
  }
}

function startMotionExperience() {
  if (!motionIsEnabled()) return;
  runOpeningSequence();
  observePageReveals();
}

function stopMotionExperience() {
  activeAnimations.forEach((animation) => animation.stop?.());
  activeAnimations.clear();
}

document.addEventListener('pi:motionchange', (event) => {
  if (event.detail?.enabled) {
    startMotionExperience();
  } else {
    stopMotionExperience();
  }
});

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', startMotionExperience, { once: true });
} else {
  startMotionExperience();
}
