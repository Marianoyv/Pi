(function () {
  const site = document.querySelector(".pi-site");
  const header = document.querySelector("[data-pi-header]");
  const toggle = document.querySelector("[data-pi-menu-toggle]");
  const navigation = document.querySelector("[data-pi-navigation]");

  if (!site) {
    return;
  }

  site.classList.add("pi-site-js");

  function setHeaderState() {
    if (!header) {
      return;
    }
    header.classList.toggle("pi-site-header-scrolled", window.scrollY > 8);
  }

  function closeMenu() {
    if (!toggle || !navigation) {
      return;
    }
    site.classList.remove("pi-site-menu-open");
    toggle.setAttribute("aria-expanded", "false");
    document.documentElement.style.overflow = "";
  }

  function openMenu() {
    if (!toggle || !navigation) {
      return;
    }
    site.classList.add("pi-site-menu-open");
    toggle.setAttribute("aria-expanded", "true");
    document.documentElement.style.overflow = "hidden";
  }

  if (toggle && navigation) {
    toggle.addEventListener("click", function () {
      if (site.classList.contains("pi-site-menu-open")) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    navigation.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        closeMenu();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeMenu();
      }
    });
  }

  window.addEventListener("scroll", setHeaderState, { passive: true });
  setHeaderState();
})();
