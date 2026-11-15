/* Exact Fibonacci proportions, with slow, overlapping drafting passes. */
(() => {
  const field = document.querySelector('.pi-genesis');
  if (!field) return;
  const sources = [...field.querySelectorAll('defs > g')];
  const compactLayout = window.matchMedia('(max-width: 600px)').matches;
  const random = (min, max) => min + Math.random() * (max - min);
  // The tiny seed resolves first; visible squares each get a full 4.6-second pass.
  const startAt = index => index < 5 ? index * (.65 / 3) : (3.25 / 3) + (index - 5) * 4.6;

  function draw(generation, leadIn = 0, opening = false) {
    const fragment = document.createDocumentFragment();
    sources.forEach((source, index) => {
      const stage = source.cloneNode(true);
      stage.removeAttribute('id');
      // A short opening draws a useful silhouette immediately; later cycles stay slow.
      const openingSeed = opening && index < 10;
      const start = opening ? (index < 10 ? index * .14 : 1.4 + (index - 10) * 4.6) : startAt(index);
      stage.querySelectorAll('path').forEach(path => {
        const depth = Number(path.dataset.depth || 0);
        const isArc = path.classList.contains('pi-genesis__arc');
        const isEdge = path.classList.contains('pi-genesis__tile');
        let delay, duration;
        if (isArc) {
          // Adjacent arcs touch in space AND time: the pen moves from the center out.
          delay = start + (opening ? .06 : .3);
          duration = openingSeed ? .14 : (opening ? 4.6 : (index < 5 ? .65 / 3 : 4.6));
        } else if (isEdge) {
          const birthSpeed = openingSeed ? 7 : (index < 5 ? 3 : 1);
          delay = start + (Number(path.dataset.edge) * .38 + random(-.15, .45)) / birthSpeed;
          duration = openingSeed ? random(.22, .55) : (index < 5 ? .8 / 3 : random(2.3, 3.8));
        } else {
          // Secondary construction is locally staggered, never a synchronized reveal.
          delay = opening ? start + .5 + depth * .25 + random(0, .8) : start + 2.2 + depth * 2.6 + random(0, 5.2);
          duration = opening ? random(1.2, 3.4) : random(4.6, 8.5);
        }
        path.classList.add('pi-genesis__stroke');
        path.style.setProperty('--trace-delay', `${Math.max(0, delay) + leadIn}s`);
        path.style.setProperty('--trace-time', `${duration}s`);
      });
      stage.querySelectorAll('circle').forEach(detail => {
        detail.classList.add('pi-genesis__detail');
        const delay = opening ? start + .06 + (openingSeed ? .14 : 4.6) : start + .3 + (index < 5 ? .65 / 3 : 4.6);
        detail.style.setProperty('--trace-delay', `${delay + leadIn}s`);
      });
      fragment.append(stage);
    });
    generation.replaceChildren(fragment);
  }

  const introDelay = parseFloat(getComputedStyle(field).getPropertyValue('--intro-delay'));
  field.querySelectorAll('.pi-genesis__generation').forEach(generation => {
    if (compactLayout && generation.dataset.mobilePhase) {
      generation.style.setProperty('--phase', `${generation.dataset.mobilePhase}s`);
    }
    const phase = parseFloat(generation.style.getPropertyValue('--phase')) || 0;
    // The first plane starts at a visible scale, but its strokes still draw from zero.
    draw(generation, introDelay + Math.max(0, phase), phase < 0);
    generation.addEventListener('animationiteration', event => {
      if (event.target === generation && event.animationName === 'pi-genesis-growth') draw(generation);
    });
  });
  field.classList.add('pi-genesis--ready');
  const visibility = new IntersectionObserver(([entry]) => {
    field.classList.toggle('pi-genesis--paused', !entry.isIntersecting || document.hidden);
  }, { rootMargin: '150px' });
  visibility.observe(field);
  document.addEventListener('visibilitychange', () => {
    field.classList.toggle('pi-genesis--paused', document.hidden || field.getBoundingClientRect().bottom < -150 || field.getBoundingClientRect().top > innerHeight + 150);
  });
})();
