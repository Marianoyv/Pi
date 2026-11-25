async function loadComponent(name, selector) {
  const el = document.querySelector(selector)
  if (!el) return
  const res = await fetch(`/finance/shared/components/${name}.html`)
  el.innerHTML = await res.text()

  if (name === "header") {
    const financeHome = "/finance/"
    const currentPath = window.location.pathname.replace(/index\.html$/, "") || financeHome
    const links = el.querySelectorAll(".nav__links a")

    links.forEach((link) => {
      const target = new URL(link.href, window.location.origin)
      const targetPath = target.pathname.replace(/index\.html$/, "") || financeHome
      const isHomeCatalog = currentPath === financeHome && targetPath === financeHome && target.hash === "#calculadoras"

      if (isHomeCatalog || (currentPath !== financeHome && currentPath === targetPath)) {
        link.setAttribute("aria-current", "page")
      }
    })
  }
}

loadComponent("header", "[data-component='header']")
loadComponent("footer", "[data-component='footer']")
