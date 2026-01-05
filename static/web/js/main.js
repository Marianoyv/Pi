function initRellax() {
  if (typeof Rellax !== 'function') return;
  if (!document.querySelector('.rellax')) return;
  new Rellax('.rellax', { center: true });
}

function initVanta() {
  if (!window.VANTA || typeof window.VANTA.GLOBE !== 'function') return;
  const el = document.getElementById('vanta-hero');
  if (!el) return;

  if (el.__vanta) {
    el.__vanta.destroy();
    el.__vanta = null;
  }

  el.__vanta = window.VANTA.GLOBE({
    el,
    mouseControls: true,
    touchControls: true,
    gyroControls: true,
    minHeight: 200.0,
    minWidth: 200.0,
    scale: 1.0,
    scaleMobile: 1.0,
    color: 0xffb703,
    backgroundColor: 0x000000
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initRellax();
  initVanta();
});

document.addEventListener('DOMContentLoaded', () => {
  // ========== Toggle menú responsive ==========
  const nav = document.getElementById("Topnav");
  const menuBtn = document.querySelector(".menu-icon");

  function toggleMenu() {
    if (nav && nav.className === "topnav") {
      nav.className += " responsive";
    } else if (nav) {
      nav.className = "topnav";
    }
  }

  if (menuBtn) {
    menuBtn.addEventListener("click", toggleMenu);
  }

  // ========== Navbar oscuro al hacer scroll ==========
  window.addEventListener("scroll", () => {
    if (nav) {
      nav.classList.toggle("dark", window.scrollY > 100);
    }

    // ========== Fade del texto con scroll ==========
    const fadeText = document.getElementById("fade-text");
    const viewportHeight = window.innerHeight;
    if (fadeText) {
      fadeText.style.opacity = window.scrollY > viewportHeight * 0.3 ? "0" : "1";
    }

    // ========== Barra de progreso  ==========
    const progressBar = document.getElementById("progress-bar");
    const scrollTop = window.scrollY;
    const docHeight = document.body.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    if (progressBar) {
      progressBar.style.width = `${progress}%`;
    }
  });
});
// ========== Animación de pasos del proceso ==========
// Selecciona todos los pasos del proceso
  const procesoSteps = document.querySelectorAll('.proceso-step');

function revealSteps() {
  const trigger = window.innerHeight * 0.85;

  procesoSteps.forEach((step, i) => {
    const top = step.getBoundingClientRect().top;
    if (top < trigger) {
      setTimeout(() => {
        step.classList.add('visible');
      }, i * 200); // delay progresivo
    }
  });
}

window.addEventListener('scroll', revealSteps);
window.addEventListener('load', revealSteps);

window.handleContact = function (e) {
  e.preventDefault();

  const nombre = document.getElementById('nombre')?.value?.trim();
  const email = document.getElementById('correo_electronico')?.value?.trim();

  if (!nombre || !email) {
    alert('Completa nombre y correo.');
    return;
  }

  const phone = '5491170619703'; // tu número con código país
  const message = `Hola! Soy ${nombre}. Mi correo es ${email}. Vengo desde pidevelopment.web.app`;

  const url = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;

  window.open(url, '_blank');

  if (typeof gtag === 'function') {
    gtag('event', 'contact_submit', {
      method: 'whatsapp'
    });
  }
};

