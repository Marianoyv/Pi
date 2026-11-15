(() => {
  const WIDTH = 170;
  const HEIGHT = 102;
  const PADDLE_HEIGHT = 20;
  const PADDLE_INSET = 12;
  const PADDLE_SPEED = 50;
  const BALL_RADIUS = 2.2;
  const STARTING_SPEED = 55;

  const clamp = (value, minimum, maximum) => Math.max(minimum, Math.min(maximum, value));
  const randomBetween = (minimum, maximum) => minimum + Math.random() * (maximum - minimum);

  function initPong(root) {
    const canvas = root.querySelector('[data-pong-canvas]');
    const leftScore = root.querySelector('[data-pong-score-left]');
    const rightScore = root.querySelector('[data-pong-score-right]');
    const context = canvas?.getContext('2d');
    if (!canvas || !context || !leftScore || !rightScore) return;

    const styles = getComputedStyle(document.documentElement);
    const colors = {
      paddle: styles.getPropertyValue('--pi-cobalt').trim() || '#173fce',
      ball: '#39e0b7',
    };

    const state = {
      ball: { x: WIDTH / 2, y: HEIGHT / 2, vx: STARTING_SPEED, vy: 15 },
      leftY: (HEIGHT - PADDLE_HEIGHT) / 2,
      rightY: (HEIGHT - PADDLE_HEIGHT) / 2,
      leftPoints: 0,
      rightPoints: 0,
      playerControlled: false,
      serveDelay: 0.45,
      leftAimOffset: randomBetween(-12, 12),
      rightAimOffset: randomBetween(-12, 12),
      visible: true,
      lastFrame: performance.now(),
      activePointerId: null,
      suppressClick: false,
      clickTimer: null,
    };

    function resizeCanvas() {
      const density = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.round(WIDTH * density);
      canvas.height = Math.round(HEIGHT * density);
      context.setTransform(density, 0, 0, density, 0, 0);
    }

    function updateScore() {
      leftScore.textContent = String(state.leftPoints);
      rightScore.textContent = String(state.rightPoints);
    }

    function resetBall(direction) {
      const verticalDirection = Math.random() > 0.5 ? 1 : -1;
      state.ball.x = WIDTH / 2;
      state.ball.y = HEIGHT / 2;
      state.ball.vx = direction * STARTING_SPEED;
      state.ball.vy = verticalDirection * randomBetween(12, 22);
      state.serveDelay = 0.55;
      state.leftAimOffset = randomBetween(-13, 13);
      state.rightAimOffset = randomBetween(-13, 13);
    }

    function movePaddle(current, target, delta) {
      const movement = clamp(target - current, -PADDLE_SPEED * delta, PADDLE_SPEED * delta);
      return clamp(current + movement, 2, HEIGHT - PADDLE_HEIGHT - 2);
    }

    function updateAutomaticPaddles(delta) {
      const centerTarget = (HEIGHT - PADDLE_HEIGHT) / 2;

      if (!state.playerControlled) {
        const leftTarget = state.ball.vx < 0
          ? state.ball.y - PADDLE_HEIGHT / 2 + state.leftAimOffset
          : centerTarget;
        state.leftY = movePaddle(state.leftY, leftTarget, delta);
      }

      const rightTarget = state.ball.vx > 0
        ? state.ball.y - PADDLE_HEIGHT / 2 + state.rightAimOffset
        : centerTarget;
      state.rightY = movePaddle(state.rightY, rightTarget, delta);
    }

    function paddleHit(paddleY) {
      return state.ball.y + BALL_RADIUS >= paddleY
        && state.ball.y - BALL_RADIUS <= paddleY + PADDLE_HEIGHT;
    }

    function updateBall(delta) {
      if (state.serveDelay > 0) {
        state.serveDelay -= delta;
        return;
      }

      state.ball.x += state.ball.vx * delta;
      state.ball.y += state.ball.vy * delta;

      if (state.ball.y - BALL_RADIUS <= 1) {
        state.ball.y = 1 + BALL_RADIUS;
        state.ball.vy = Math.abs(state.ball.vy);
      } else if (state.ball.y + BALL_RADIUS >= HEIGHT - 1) {
        state.ball.y = HEIGHT - 1 - BALL_RADIUS;
        state.ball.vy = -Math.abs(state.ball.vy);
      }

      const leftEdge = PADDLE_INSET + 2;
      if (state.ball.vx < 0 && state.ball.x - BALL_RADIUS <= leftEdge && paddleHit(state.leftY)) {
        const impact = (state.ball.y - (state.leftY + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2);
        state.ball.x = leftEdge + BALL_RADIUS;
        state.ball.vx = Math.min(Math.abs(state.ball.vx) * 1.025, 58);
        state.ball.vy = clamp(state.ball.vy + impact * 13, -34, 34);
        state.leftAimOffset = randomBetween(-13, 13);
      }

      const rightEdge = WIDTH - PADDLE_INSET - 2;
      if (state.ball.vx > 0 && state.ball.x + BALL_RADIUS >= rightEdge && paddleHit(state.rightY)) {
        const impact = (state.ball.y - (state.rightY + PADDLE_HEIGHT / 2)) / (PADDLE_HEIGHT / 2);
        state.ball.x = rightEdge - BALL_RADIUS;
        state.ball.vx = -Math.min(Math.abs(state.ball.vx) * 1.025, 58);
        state.ball.vy = clamp(state.ball.vy + impact * 13, -34, 34);
        state.rightAimOffset = randomBetween(-13, 13);
      }

      if (state.ball.x < -BALL_RADIUS) {
        state.rightPoints += 1;
        updateScore();
        resetBall(1);
      } else if (state.ball.x > WIDTH + BALL_RADIUS) {
        state.leftPoints += 1;
        updateScore();
        resetBall(-1);
      }
    }

    function draw() {
      context.clearRect(0, 0, WIDTH, HEIGHT);
      context.strokeStyle = colors.paddle;
      context.lineWidth = 2;
      context.lineCap = 'round';

      context.beginPath();
      context.moveTo(PADDLE_INSET, state.leftY);
      context.lineTo(PADDLE_INSET, state.leftY + PADDLE_HEIGHT);
      context.moveTo(WIDTH - PADDLE_INSET, state.rightY);
      context.lineTo(WIDTH - PADDLE_INSET, state.rightY + PADDLE_HEIGHT);
      context.stroke();

      context.fillStyle = colors.ball;
      context.beginPath();
      context.arc(state.ball.x, state.ball.y, BALL_RADIUS, 0, Math.PI * 2);
      context.fill();
    }

    function frame(now) {
      const delta = Math.min((now - state.lastFrame) / 1000, 0.04);
      state.lastFrame = now;

      if (state.visible && !document.hidden) {
        updateAutomaticPaddles(delta);
        updateBall(delta);
        draw();
      }

      window.requestAnimationFrame(frame);
    }

    function activatePlayer() {
      state.playerControlled = true;
      root.dataset.pongMode = 'player';
    }

    function movePlayer(event) {
      activatePlayer();
      const bounds = root.getBoundingClientRect();
      const pointerY = ((event.clientY - bounds.top) / bounds.height) * HEIGHT;
      state.leftY = clamp(pointerY - PADDLE_HEIGHT / 2, 2, HEIGHT - PADDLE_HEIGHT - 2);
    }

    function activateAutomaticPlay() {
      state.playerControlled = false;
      root.dataset.pongMode = 'auto';
      state.leftAimOffset = randomBetween(-13, 13);
    }

    function isTouchPointer(event) {
      return event.pointerType === 'touch' || event.pointerType === 'pen';
    }

    function handlePointerDown(event) {
      if (!isTouchPointer(event)) return;
      state.activePointerId = event.pointerId;
      state.suppressClick = true;
      try {
        root.setPointerCapture?.(event.pointerId);
      } catch (error) {
        // Synthetic or older mobile browsers can omit native pointer capture.
      }
      movePlayer(event);
      event.preventDefault();
    }

    function handlePointerMove(event) {
      if (isTouchPointer(event) && state.activePointerId !== event.pointerId) return;
      movePlayer(event);
      if (isTouchPointer(event)) event.preventDefault();
    }

    function handlePointerLeave(event) {
      if (state.activePointerId === event.pointerId) return;
      activateAutomaticPlay();
    }

    function handlePointerEnd(event) {
      if (!isTouchPointer(event) || state.activePointerId !== event.pointerId) return;
      try {
        if (root.hasPointerCapture?.(event.pointerId)) root.releasePointerCapture(event.pointerId);
      } catch (error) {
        // The control still works when pointer capture is unavailable.
      }
      state.activePointerId = null;
      activateAutomaticPlay();
      event.preventDefault();

      window.clearTimeout(state.clickTimer);
      state.clickTimer = window.setTimeout(() => {
        state.suppressClick = false;
      }, 450);
    }

    root.addEventListener('pointerenter', activatePlayer);
    root.addEventListener('pointerdown', handlePointerDown);
    root.addEventListener('pointermove', handlePointerMove);
    root.addEventListener('pointerleave', handlePointerLeave);
    root.addEventListener('pointerup', handlePointerEnd);
    root.addEventListener('pointercancel', handlePointerEnd);
    root.addEventListener('mouseenter', activatePlayer);
    root.addEventListener('mousemove', movePlayer);
    root.addEventListener('mouseleave', activateAutomaticPlay);
    root.addEventListener('click', (event) => {
      if (!state.suppressClick) return;
      event.preventDefault();
      event.stopPropagation();
      state.suppressClick = false;
    });

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(([entry]) => {
        state.visible = entry.isIntersecting;
        state.lastFrame = performance.now();
      }, { threshold: 0.05 });
      observer.observe(root);
    }

    resizeCanvas();
    updateScore();
    draw();
    window.requestAnimationFrame(frame);
  }

  function initPongGames() {
    document.querySelectorAll('[data-pong-game]').forEach(initPong);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPongGames, { once: true });
  } else {
    initPongGames();
  }
})();
