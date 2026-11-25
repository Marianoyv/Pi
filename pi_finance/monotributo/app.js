import { monotributoCategory } from "/finance/calculadoras/assets/calculators.js"

const money = new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", maximumFractionDigits: 2 })
const percent = new Intl.NumberFormat("es-AR", { style: "percent", minimumFractionDigits: 1, maximumFractionDigits: 1 })
const form = document.querySelector("#calculator-form")
const errorPanel = document.querySelector("#calculator-error")
const resultPanel = document.querySelector("#calculator-result")
let data

function render() {
  try {
    const values = Object.fromEntries(new FormData(form))
    const result = monotributoCategory({ ...values, categories: data.categories })
    document.querySelector("#category").textContent = result.excluded ? "Fuera del tope" : `Categoría ${result.category}`
    document.querySelector("#category-limit").textContent = money.format(result.maximum)
    document.querySelector("#remaining").textContent = result.excluded ? "—" : money.format(result.remaining)
    document.querySelector("#monthly-fee").textContent = result.excluded ? "—" : money.format(result.monthlyFee)
    document.querySelector("#percent-used").textContent = result.excluded ? "Más del 100 %" : percent.format(result.percentUsed)
    document.querySelector("#next-category").textContent = result.excluded ? "Revisá el régimen general" : result.nextCategory ? `La siguiente es ${result.nextCategory}, hasta ${money.format(result.nextMaximum)}` : "Es la última categoría"
    document.querySelector("#effective-date").textContent = data.effectiveDate
    document.querySelector("#category-warning").textContent = result.excluded
      ? "La facturación supera el límite máximo informado por ARCA para el monotributo."
      : "Estimación por ingresos brutos: verificá también alquiler, superficie, energía y precio unitario cuando correspondan."
    resultPanel.hidden = false
    errorPanel.hidden = true
  } catch (error) {
    resultPanel.hidden = true
    errorPanel.hidden = false
    errorPanel.textContent = error instanceof Error ? error.message : "Revisá los datos ingresados."
  }
}

async function start() {
  data = await fetch("/finance/monotributo/data/categorias.json").then((response) => {
    if (!response.ok) throw new Error("No se pudieron cargar las categorías de ARCA.")
    return response.json()
  })
  form.addEventListener("input", render)
  form.addEventListener("change", render)
  form.addEventListener("submit", (event) => { event.preventDefault(); render() })
  render()
}
start().catch((error) => { errorPanel.hidden = false; errorPanel.textContent = error.message })
