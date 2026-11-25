import { fixedTermFromTea } from "/finance/calculadoras/assets/calculators.js"

const money = new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", maximumFractionDigits: 0 })
const percentNumber = new Intl.NumberFormat("es-AR", { minimumFractionDigits: 2, maximumFractionDigits: 2 })
const date = new Intl.DateTimeFormat("es-AR", { dateStyle: "long", timeZone: "UTC" })
const form = document.querySelector("#calculator-form")
const errorPanel = document.querySelector("#calculator-error")
const resultPanel = document.querySelector("#calculator-result")
let data

function render() {
  try {
    const values = Object.fromEntries(new FormData(form))
    const capital = Number(values.capital)
    const days = Number(values.days)
    const expectedAnnualInflation = Number(values.expectedAnnualInflation)
    const results = data.banks
      .filter((bank) => capital >= bank.minimumAmount)
      .map((bank) => ({ bank, result: fixedTermFromTea({ capital, tea: bank.tea, days, expectedAnnualInflation }) }))
      .sort((a, b) => b.result.total - a.result.total)
    if (!results.length) throw new Error("El capital no alcanza el mínimo informado por las entidades disponibles.")
    const best = results[0]
    document.querySelector("#best-bank").textContent = best.bank.bank
    document.querySelector("#best-total").textContent = money.format(best.result.total)
    document.querySelector("#best-interest").textContent = money.format(best.result.interest)
    document.querySelector("#best-real-gain").textContent = money.format(best.result.realGain)
    document.querySelector("#best-tea").textContent = `${percentNumber.format(best.bank.tea)} %`
    document.querySelector("#rates-date").textContent = date.format(new Date(`${data.lastUpdate}T00:00:00Z`))
    const body = document.querySelector("#rates-body")
    body.replaceChildren(...results.slice(0, 20).map(({ bank, result }, index) => {
      const row = document.createElement("tr")
      const cells = [String(index + 1), bank.bank, `${percentNumber.format(bank.tea)} %`, money.format(result.interest), money.format(result.total), bank.channel]
      for (const value of cells) { const cell = document.createElement("td"); cell.textContent = value; row.append(cell) }
      return row
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
  data = await fetch("/finance/comparador-plazos-fijos/data/plazos-fijos.json").then((response) => {
    if (!response.ok) throw new Error("No se pudieron cargar las tasas bancarias.")
    return response.json()
  })
  form.addEventListener("input", render)
  form.addEventListener("change", render)
  form.addEventListener("submit", (event) => { event.preventDefault(); render() })
  render()
}
start().catch((error) => { errorPanel.hidden = false; errorPanel.textContent = error.message })
