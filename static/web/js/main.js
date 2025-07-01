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
