document.addEventListener("DOMContentLoaded", () => {
  const setMenuOpen = (open) => {
    const nav = document.querySelector(".nav__links")
    const toggle = document.querySelector(".nav__toggle")
    if (!nav || !toggle) return

    nav.classList.toggle("is-open", open)
    toggle.setAttribute("aria-expanded", String(open))
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú")
  }

  document.addEventListener("click", (e) => {
    const btn = e.target.closest(".nav__toggle")
    const link = e.target.closest(".nav__links a")

    if (btn) {
      const expanded = btn.getAttribute("aria-expanded") === "true"
      setMenuOpen(!expanded)
      return
    }

    if (link) {
      setMenuOpen(false)
      return
    }

    if (!e.target.closest(".nav") && document.querySelector(".nav__links.is-open")) {
      setMenuOpen(false)
    }
  })

  document.addEventListener("keydown", (e) => {
    if (e.key !== "Escape" || !document.querySelector(".nav__links.is-open")) return
    setMenuOpen(false)
    document.querySelector(".nav__toggle")?.focus()
  })

  window.addEventListener("resize", () => {
    if (window.innerWidth > 820) setMenuOpen(false)
  })
})
