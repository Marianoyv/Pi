(() => {
  const stage = document.querySelector('[data-product-stage]');
  if (!stage) return;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const clamp = value => Math.min(1, Math.max(0, value));
  const ramp = (p, a, b) => clamp((p - a) / (b - a));
  const smooth = value => value * value * (3 - 2 * value);
  const softer = value => value ** 3 * (value * (value * 6 - 15) + 10);
  const mix = (a, b, p) => a + (b - a) * p;
  const viewport = stage.querySelector('.pi-product__sticky');
  const intro = stage.querySelector('.pi-product__intro');
  const panels = {
    desktop: stage.querySelector('.pi-product__details--desktop'),
    mobile: stage.querySelector('.pi-product__details--mobile'),
    backendLeft: stage.querySelector('.pi-product__details--backend-left'),
    backendRight: stage.querySelector('.pi-product__details--backend-right'),
  };
  const desktopArticles = [...panels.desktop.querySelectorAll('article')];
  const phoneCards = [...panels.mobile.querySelectorAll('article')];
  let energyAnimations = [], energyEnabled = null, energyScanned = false;
  let pending = false, active = true, progress = null, entrance = null, titleReveal = null, previousTime = 0;
  let layout = null;
  function measure() {
    const vh = viewport.offsetHeight;
    return {
      vh,
      top: window.scrollY + stage.getBoundingClientRect().top,
      distance: Math.max(1, stage.offsetHeight - vh - window.innerHeight * .6),
      navHeight: parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-height')) || 92,
      viewportWidth: viewport.clientWidth,
      introWidth: intro.offsetWidth,
      introHeight: intro.offsetHeight,
      introTop: intro.offsetTop,
      introLeft: intro.offsetLeft,
      backendLeftHeight: panels.backendLeft.offsetHeight,
      backendRightHeight: panels.backendRight.offsetHeight,
      mobileCenter: panels.mobile.offsetTop + panels.mobile.offsetHeight / 2,
      phoneTopHeight: phoneCards[0].offsetHeight,
      phoneBottomHeight: phoneCards[2].offsetHeight,
      bodyHeights: desktopArticles.map(article => article.querySelector('p').scrollHeight),
    };
  }
  function invalidate() { layout = null; schedule(); }
  function render(time = performance.now()) {
    pending = false;
    const enabled = document.documentElement.classList.contains('pi-motion-enabled');
    stage.classList.toggle('is-scrollable', enabled);
    stage.classList.toggle('is-still', !enabled);
    layout ||= measure();
    const compact = window.matchMedia('(max-width: 900px)').matches;
    const { vh, distance } = layout;
    const top = layout.top - window.scrollY;
    const target = enabled ? clamp(-top / distance) : 0.24;
    const targetEntrance = enabled ? (compact ? ramp(vh*.45-top,0,vh*.95) : ramp(-top,vh*.55,vh*1.3)) : 1;
    const targetTitleReveal = enabled ? ramp(vh - top, 0, vh) : 1;
    const dt = previousTime ? Math.min(64, time - previousTime) : 16;
    previousTime = time;
    const follow = enabled ? 1 - Math.exp(-dt / 160) : 1;
    const titleFollow = enabled ? 1 - Math.exp(-dt / 260) : 1;
    progress = progress === null ? target : mix(progress, target, follow);
    entrance = entrance === null ? targetEntrance : mix(entrance, targetEntrance, follow);
    titleReveal = titleReveal === null ? targetTitleReveal : mix(titleReveal, targetTitleReveal, titleFollow);
    if (Math.abs(progress - target) < .00001) progress = target;
    if (Math.abs(entrance - targetEntrance) < .00001) entrance = targetEntrance;
    if (Math.abs(titleReveal - targetTitleReveal) < .00001) titleReveal = targetTitleReveal;
    const p = progress;
    const park = smooth(entrance);
    // One full turn, with a readable back-facing chapter at its midpoint.
    const toBack = smooth(ramp(p, .34, .43));
    const toPhone = smooth(ramp(p, .59, .70));
    const exit = smooth(ramp(p, .90, .97));
    const navHeight = layout.navHeight;
    const safeTop = navHeight + 24;
    const titlePlace = enabled ? smooth(compact ? ramp(p*distance,0,vh*.55) : ramp(p*distance,vh*.65,vh*1.3)) : 1;
    const titleScale = Math.max(1, Math.min(1.15, (layout.viewportWidth - 64) / layout.introWidth));
    const centeredX = (layout.viewportWidth - layout.introWidth) / 2 - layout.introLeft;
    const centeredY = (safeTop + vh - layout.introHeight) / 2 - layout.introTop;
    const titleBottom = layout.introTop + layout.introHeight;
    const widthLimit = compact ? Math.min(window.innerWidth*.94, Math.max(220,(vh-safeTop-300)*1.6/.88)) : Math.min(window.innerWidth*.50,780);
    const availableHeight = Math.max(160, vh - titleBottom - 48 - 40);
    const desktopWidth = Math.min(widthLimit, (availableHeight / .88 - 24) * 1.6);
    const desktopHeight = desktopWidth / 1.6;
    const desktopCenter = titleBottom + (compact ? 28 : 48) + (desktopHeight + 24) * .88 / 2;
    let tabletWidth = Math.min(window.innerWidth * (compact ? .47 : .30), 420, vh * .48);
    if (compact) {
      const cardSpace = layout.backendLeftHeight + layout.backendRightHeight;
      const maxTabletHeight = Math.max(120,(vh-safeTop-cardSpace-64)/.88-24);
      tabletWidth = Math.min(tabletWidth,maxTabletHeight*.75);
    }
    const tabletHeight = tabletWidth * 4 / 3;
    let phoneHeight = Math.min(vh * (compact ? .47 : .61), 580);
    if (compact) phoneHeight = Math.min(phoneHeight,Math.max(vh < 620 ? 160 : 180,(vh-safeTop-layout.phoneTopHeight-layout.phoneBottomHeight-72)/.88-24));
    const phoneGridGap = compact ? 12 : 16;
    const phoneGridLimit = Math.min(layout.viewportWidth-56,400);
    const phoneWidth = compact ? Math.min((phoneGridLimit-phoneGridGap)/2/.88,phoneHeight*.62) : phoneHeight*.48;
    const phoneHalf = (phoneHeight + 24) * .88 / 2;
    // Center the phone against its existing information column, within safe edges.
    const panelCenter = layout.mobileCenter;
    const phoneStackGap = compact ? (vh < 520 ? 4 : vh < 620 ? 10 : 20) : 20;
    const phoneStackHeight = layout.phoneTopHeight+layout.phoneBottomHeight+phoneHalf*2+phoneStackGap*2;
    const phoneStackTop = safeTop+Math.max(8,(vh-safeTop-phoneStackHeight)/2);
    const phoneCenter = compact ? phoneStackTop+layout.phoneTopHeight+phoneStackGap+phoneHalf : Math.max(safeTop+phoneHalf,Math.min(vh-phoneHalf-32,panelCenter));
    const phoneVisualWidth = phoneWidth*.88;
    const phoneCardWidth = compact
      ? Math.min(230, Math.max(190, window.innerWidth * .36))
      : phoneVisualWidth;
    const phoneGridWidth = phoneCardWidth + phoneVisualWidth + phoneGridGap;
    const phoneRowLeft = (layout.viewportWidth-phoneGridWidth)/2;
    const phoneLeft = compact ? (phoneRowLeft+phoneCardWidth+phoneGridGap+phoneVisualWidth/2)/layout.viewportWidth*100 : 73;
    const backHalf = (tabletHeight+24)*.88/2;
    const backendStackHeight = layout.backendLeftHeight + layout.backendRightHeight + backHalf*2 + 48;
    const backendStackTop = safeTop + Math.max(12,(vh-safeTop-backendStackHeight)/2);
    const backCenter = compact ? backendStackTop+layout.backendLeftHeight+24+backHalf : (safeTop+vh)/2;
    const desktopOpacity = compact && enabled ? ramp(p,.10,.12)*(1-ramp(p,.325,.34)) : ramp(p * distance, vh * 1.3, vh * 1.65) * (1 - ramp(p, .30, .34));
    const backendOpacity = ramp(p, .43, .46) * (1 - ramp(p, .56, .59));
    const mobileOpacity = ramp(p, .70, .74) * (1 - ramp(p, .88, .92));
    const phase = p < .14 ? 'entrance' : p < .34 ? 'desktop' : p < .43 ? 'turn-to-back' : p < .59 ? 'backend' : p < .70 ? 'turn-to-phone' : p < .90 ? 'mobile' : 'finale';
    stage.dataset.phase = phase;
    // Retiming preserves the current frame: energy slows down but never freezes.
    if (energyEnabled !== enabled) { energyAnimations = []; energyEnabled = enabled; energyScanned = false; }
    if (enabled) {
      if (!energyScanned) {
        energyAnimations = stage.getAnimations({subtree:true}).filter(animation => ['pi-energy-route','pi-energy-return','pi-package-pulse','pi-core-glow'].includes(animation.animationName));
        energyScanned = true;
      }
      const presence = smooth(ramp(p,.30,.43)) * (1-smooth(ramp(p,.59,.74)));
      const energyRate = .18 + .82 * presence;
      energyAnimations.forEach(animation => {
        if (Math.abs(animation.playbackRate-energyRate)>.005) animation.updatePlaybackRate(energyRate);
      });
    }
    const values = {
      '--progress':p, '--composition-y':'0px',
      '--intro-opacity':(enabled ? ramp(titleReveal,0,.3) : 1) * (1-ramp(p,.30,.34)),
      '--intro-scale':mix(titleScale,1,titlePlace),
      '--intro-x':`${centeredX*(1-titlePlace)}px`,
      '--intro-y':`${mix(safeTop-layout.introTop+layout.introHeight*(titleScale-1)/2,centeredY,softer(titleReveal))*(1-titlePlace)}px`,
      '--device-width':`${mix(mix(desktopWidth,tabletWidth,toBack),phoneWidth,toPhone)}px`,
      '--device-height':`${mix(mix(desktopHeight,tabletHeight,toBack),phoneHeight,toPhone)}px`,
      '--device-left':`${mix(mix(mix(50,compact?50:32,park),50,toBack),phoneLeft,toPhone)}%`,
      '--device-top':`${mix(mix(desktopCenter,backCenter,toBack),phoneCenter,toPhone)/vh*100}%`,
      '--screen-anchor':'-50%', '--device-opacity':enabled?ramp(entrance,0,.28):1,
      '--device-blur':`${enabled?14*(1-ramp(entrance,0,.65)):0}px`,
      '--rear-camera':`${20*toPhone}px`,
      '--laptop-y':`${-65*(1-park)-exit*(vh+phoneHeight)}px`,
      '--rx':`${12*(1-park)}deg`,
      '--ry':`${(p<.34?-165*(1-park):0)+180*toBack+180*toPhone}deg`,
      '--rz':`${-6*(1-park)}deg`,
      '--device-depth':`${mix(mix(18,14,toBack),16,toPhone)}px`,
      '--device-radius':`${mix(mix(18,26,toBack),38,toPhone)}px`,
      '--glass-radius':`${mix(mix(5,16,toBack),28,toPhone)}px`,
      '--desktop-opacity':desktopOpacity,'--backend-opacity':backendOpacity,'--mobile-opacity':mobileOpacity,
      '--outro-opacity':enabled?ramp(p,.94,.97):1,
      '--outro-button-fill':enabled?smooth(ramp(p,.97,.995)):1,
    };
    if (enabled) {
      const chipZoom = smooth(ramp(p,.44,.49))*(1-smooth(ramp(p,.52,.585)));
      values['--chip-zoom'] = 1+1.15*chipZoom;
      values['--chip-shine-x'] = `${mix(-110,110,softer(ramp(p,.465,.555)))}%`;
      values['--chip-shine-opacity'] = ramp(p,.46,.48)*(1-ramp(p,.54,.56));
    }
    if (compact && enabled) {
      values['--chip-window-top'] = `${backendStackTop+layout.backendLeftHeight+10}px`;
      values['--chip-window-bottom'] = `${Math.max(0,vh-(backCenter+backHalf+14))}px`;
      const phoneCardEntry = smooth(ramp(p,.70,.76));
      values['--phone-card-entry'] = phoneCardEntry;
      values['--phone-card-top-y'] = `${-90*(1-phoneCardEntry)}px`;
      values['--phone-card-middle-x'] = `${-(layout.viewportWidth*.65)*(1-phoneCardEntry)}px`;
      values['--phone-card-bottom-y'] = `${90*(1-phoneCardEntry)}px`;
      values['--phone-top-card'] = `${phoneStackTop}px`;
      values['--phone-middle-card'] = `${phoneCenter-phoneHalf}px`;
      values['--phone-bottom-card'] = `${phoneCenter+phoneHalf+phoneStackGap}px`;
      values['--phone-grid-width'] = `${phoneGridWidth}px`;
      values['--phone-grid-left'] = `${phoneRowLeft}px`;
      values['--phone-card-width'] = `${phoneCardWidth}px`;
      values['--phone-row-left'] = `${phoneRowLeft}px`;
      values['--phone-row-height'] = `${phoneHalf*2}px`;
      values['--backend-top-card'] = `${backendStackTop}px`;
      values['--backend-bottom-card'] = `${backCenter+backHalf+24}px`;
      const lift = smooth(ramp(p,.035,.10));
      const pinnedCenter = safeTop + 8 + (desktopHeight+24)*.88/2;
      values['--intro-x'] = `${centeredX*(1-titlePlace)}px`;
      values['--intro-y'] = `${parseFloat(values['--intro-y'])-(vh*.65+layout.introHeight)*lift}px`;
      values['--intro-opacity'] = ramp(titleReveal,0,.3)*(1-ramp(p,.065,.10));
      values['--device-top'] = `${mix(mix(mix(desktopCenter,pinnedCenter,lift),backCenter,toBack),phoneCenter,toPhone)/vh*100}%`;
      values['--front-cards-top'] = `${pinnedCenter+(desktopHeight+24)*.88/2+20}px`;
    }
    const firstFold = smooth(ramp(p,compact?.17:.217,compact?.19:.237));
    const secondFold = smooth(ramp(p,compact?.235:.272,compact?.255:.292));
    const folds = [1-firstFold,firstFold*(1-secondFold),secondFold];
    desktopArticles.forEach((article,index)=>{
      const open = compact&&enabled ? folds[index] : 1;
      const body = article.querySelector('p');
      article.style.setProperty('--card-open',open);
      article.style.setProperty('--card-body-height',`${layout.bodyHeights[index]*open}px`);
      article.style.setProperty('--card-opacity',1);
      article.style.setProperty('--card-y','0px');
      article.removeAttribute('aria-hidden');
      body.setAttribute('aria-hidden',String(compact&&enabled&&open<.05));
    });
    Object.entries(values).forEach(([key,value])=>stage.style.setProperty(key,value));
    // Reflow the front while it is hidden behind the opaque back face.
    stage.classList.toggle('is-phone',toPhone>0);
    stage.classList.toggle('is-desktop-chapter',!enabled||desktopOpacity>0);
    stage.classList.toggle('is-backend-chapter',!enabled||backendOpacity>0);
    stage.classList.toggle('is-mobile-chapter',!enabled||mobileOpacity>0);
    stage.classList.toggle('is-complete',!enabled||p>.94);
    stage.querySelector('.pi-product__outro').inert=enabled&&p<=.96;
    for(const [key,panel] of Object.entries(panels)){
      const opacity=key==='desktop'?desktopOpacity:key==='mobile'?mobileOpacity:backendOpacity;
      panel.setAttribute('aria-hidden',String(enabled&&opacity===0));
    }
    if(active&&enabled&&(progress!==target||entrance!==targetEntrance||titleReveal!==targetTitleReveal))schedule();
  }
  function schedule(){if(!pending){pending=true;window.requestAnimationFrame(render);}}
  new IntersectionObserver(([entry])=>{
    active=entry.isIntersecting;
    stage.classList.toggle('is-dormant', !active);
    if(active) schedule();
  },{rootMargin:'100px'}).observe(stage);
  window.addEventListener('scroll',()=>{if(active)schedule();},{passive:true});
  window.addEventListener('resize',invalidate);
  document.addEventListener('pi:motionchange',invalidate);
  reduced.addEventListener('change',invalidate);
  document.fonts?.ready.then(invalidate);
  if ('ResizeObserver' in window) {
    const geometryObserver = new ResizeObserver(invalidate);
    geometryObserver.observe(stage);
    geometryObserver.observe(viewport);
    geometryObserver.observe(phoneCards[0]);
    geometryObserver.observe(phoneCards[2]);
    const hero = document.querySelector('.pi-home-hero');
    if (hero) geometryObserver.observe(hero);
  }
  render();
})();
