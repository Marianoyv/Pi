import { calculateIPC } from "/finance/ipc/assets/js/calculator.js"
import { salaryPurchasingPower } from "/finance/calculadoras/assets/calculators.js"

const money = new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", maximumFractionDigits: 0 })
const percent = new Intl.NumberFormat("es-AR", { style: "percent", minimumFractionDigits: 1, maximumFractionDigits: 1 })
const monthName = new Intl.DateTimeFormat("es-AR", { month: "long", year: "numeric", timeZone: "UTC" })
const form = document.querySelector("#calculator-form")
const errorPanel = document.querySelector("#calculator-error")
const resultPanel = document.querySelector("#calculator-result")
let data

function labelMonth(ym) {
  return monthName.format(new Date(`${ym}-01T00:00:00Z`))
}

function render() {
  try {
    const values = Object.fromEntries(new FormData(form))
    const ipc = calculateIPC({ amount: 1, from: values.from, to: values.to, monthly: data.monthly })
    const result = salaryPurchasingPower({ initialSalary: values.initialSalary, currentSalary: values.currentSalary, inflationFactor: ipc.updatedAmount })
    document.querySelector("#inflation").textContent = percent.format(ipc.accumulatedRate)
    document.querySelector("#needed-salary").textContent = money.format(result.inflationAdjustedSalary)
    document.querySelector("#nominal-increase").textContent = percent.format(result.nominalIncrease)
    document.querySelector("#real-variation").textContent = percent.format(result.realVariation)
    document.querySelector("#purchasing-difference").textContent = money.format(result.purchasingPowerDifference)
    document.querySelector("#salary-verdict").textContent = result.realVariation >= 0 ? "Tu sueldo le ganó a la inflación" : "Tu sueldo perdió poder de compra"
    document.querySelector("#source-date").textContent = labelMonth(data.lastUpdate)
    resultPanel.hidden = false
    errorPanel.hidden = true
  } catch (error) {
    resultPanel.hidden = true
    errorPanel.hidden = false
    errorPanel.textContent = error instanceof Error ? error.message : "Revisá los datos ingresados."
  }
}

async function start() {
  data = await fetch("/finance/ipc/data/ipc.json").then((response) => {
    if (!response.ok) throw new Error("No se pudieron cargar los datos de IPC.")
    return response.json()
  })
  const months = Object.keys(data.monthly).sort()
  for (const id of ["from", "to"]) {
    const select = document.querySelector(`#${id}`)
    select.replaceChildren(...months.map((ym) => new Option(labelMonth(ym), ym)))
  }
  document.querySelector("#from").value = months.at(-13) || months[0]
  document.querySelector("#to").value = months.at(-1)
  form.addEventListener("input", render)
  form.addEventListener("change", render)
  form.addEventListener("submit", (event) => { event.preventDefault(); render() })
  render()
}

start().catch((error) => { errorPanel.hidden = false; errorPanel.textContent = error.message })
