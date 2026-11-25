import { uvaLoanScenario } from "/finance/calculadoras/assets/calculators.js"

const money = new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", maximumFractionDigits: 0 })
const number = new Intl.NumberFormat("es-AR", { maximumFractionDigits: 2 })
const percent = new Intl.NumberFormat("es-AR", { style: "percent", minimumFractionDigits: 1, maximumFractionDigits: 1 })
const date = new Intl.DateTimeFormat("es-AR", { dateStyle: "long", timeZone: "UTC" })
const form = document.querySelector("#calculator-form")
const errorPanel = document.querySelector("#calculator-error")
const resultPanel = document.querySelector("#calculator-result")
let data

function render() {
  try {
    const lastDate = Object.keys(data.daily).sort().at(-1)
    const currentUva = data.daily[lastDate]
    const values = Object.fromEntries(new FormData(form))
    const result = uvaLoanScenario({ ...values, currentUva })
    document.querySelector("#uva-current").textContent = money.format(currentUva)
    document.querySelector("#uva-date").textContent = date.format(new Date(`${lastDate}T00:00:00Z`))
    document.querySelector("#principal-uva").textContent = `${number.format(result.principalUva)} UVA`
    document.querySelector("#payment-initial").textContent = money.format(result.initialPayment)
    document.querySelector("#payment-12").textContent = money.format(result.payment12)
    document.querySelector("#payment-24").textContent = money.format(result.payment24)
    document.querySelector("#balance-12").textContent = money.format(result.balance12)
    document.querySelector("#max-ratio").textContent = percent.format(result.maximumIncomeRatio)
    const wanted = new Set([1, 12, 24, 60, 120, result.schedule.length])
    document.querySelector("#uva-schedule-body").replaceChildren(...result.schedule.filter((row) => wanted.has(row.installment)).map((row) => {
      const tr = document.createElement("tr")
      for (const value of [row.installment, money.format(row.uvaValue), money.format(row.payment), money.format(row.balance), percent.format(row.incomeRatio)]) { const td = document.createElement("td"); td.textContent = String(value); tr.append(td) }
      return tr
    }))
    resultPanel.hidden = false
    errorPanel.hidden = true
  } catch (error) {
    resultPanel.hidden = true
    errorPanel.hidden = false
    errorPanel.textContent = error instanceof Error ? error.message : "Revisá los datos ingresados."
  }
}

async function start() {
  data = await fetch("/finance/credito-uva/data/uva.json").then((response) => {
    if (!response.ok) throw new Error("No se pudo cargar el valor UVA del BCRA.")
    return response.json()
  })
  form.addEventListener("input", render)
  form.addEventListener("change", render)
  form.addEventListener("submit", (event) => { event.preventDefault(); render() })
  render()
}
start().catch((error) => { errorPanel.hidden = false; errorPanel.textContent = error.message })
