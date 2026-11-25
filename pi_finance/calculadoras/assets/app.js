import {
  compoundInterest,
  convertRates,
  fixedTerm,
  frenchLoan,
  investmentReturn,
  cashOrInstallments,
  debtPayoff,
  percentageDiscount,
  percentageIncrease,
  percentageVariation,
  simpleInterest,
  vat
} from "./calculators.js"

const money = new Intl.NumberFormat("es-AR", {
  style: "currency",
  currency: "ARS",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
})

const percent = new Intl.NumberFormat("es-AR", {
  style: "percent",
  minimumFractionDigits: 2,
  maximumFractionDigits: 2
})

const number = new Intl.NumberFormat("es-AR", {
  minimumFractionDigits: 0,
  maximumFractionDigits: 2
})

const calculators = {
  "cuotas-o-contado": (values) => cashOrInstallments(values),
  "cancelar-deudas": (values) => debtPayoff(values),
  "interes-simple": (values) => simpleInterest(values),
  "interes-compuesto": (values) => compoundInterest(values),
  "plazo-fijo": (values) => fixedTerm(values),
  "prestamo-frances": (values) => frenchLoan(values),
  "tna-tea": (values) => convertRates(values),
  "porcentaje-aumento": (values) => percentageIncrease(values),
  "porcentaje-descuento": (values) => percentageDiscount(values),
  "variacion-porcentual": (values) => percentageVariation(values),
  iva: (values) => vat(values),
  rentabilidad: (values) => investmentReturn(values)
}

function valuesFrom(form) {
  return Object.fromEntries([...new FormData(form)].map(([key, value]) => {
    if (value !== "" && !Number.isNaN(Number(value))) return [key, Number(value)]
    return [key, value]
  }))
}

function formatValue(value, format) {
  if (value === null || value === undefined || !Number.isFinite(value)) return "No aplica"
  if (format === "percent") return percent.format(value)
  if (format === "number") return number.format(value)
  return money.format(value)
}

function renderSchedule(schedule) {
  const body = document.querySelector("#amortization-body")
  if (!body) return
  body.replaceChildren(...schedule.map((row) => {
    const tr = document.createElement("tr")
    const values = [row.installment, row.payment, row.interest, row.amortization, row.balance]
    values.forEach((value, index) => {
      const cell = document.createElement("td")
      cell.textContent = index === 0 ? String(value) : money.format(value)
      if (index === 0) cell.dataset.label = "Cuota"
      tr.append(cell)
    })
    return tr
  }))
}

function render(result) {
  document.querySelectorAll("[data-result]").forEach((element) => {
    const value = result[element.dataset.result]
    element.textContent = formatValue(value, element.dataset.format)
  })
  document.querySelectorAll("[data-result-text]").forEach((element) => {
    element.textContent = result[element.dataset.resultText] ?? ""
  })
  if (result.schedule) renderSchedule(result.schedule)
}

function setupConditionalFields(form) {
  const update = () => {
    const mode = form.elements.mode?.value
    document.querySelectorAll("[data-show-when]").forEach((element) => {
      element.hidden = element.dataset.showWhen !== mode
    })
  }
  form.elements.mode?.addEventListener("change", update)
  update()
}

const form = document.querySelector("#calculator-form")
const calculatorName = document.body.dataset.calculator
const calculate = calculators[calculatorName]

if (form && calculate) {
  const resultPanel = document.querySelector("#calculator-result")
  const errorPanel = document.querySelector("#calculator-error")

  const run = () => {
    try {
      const result = calculate(valuesFrom(form))
      render(result)
      resultPanel.hidden = false
      errorPanel.hidden = true
      errorPanel.textContent = ""
    } catch (error) {
      resultPanel.hidden = true
      errorPanel.hidden = false
      errorPanel.textContent = error instanceof Error ? error.message : "Revisá los datos ingresados."
    }
  }

  form.addEventListener("submit", (event) => {
    event.preventDefault()
    run()
  })
  form.addEventListener("input", run)
  form.addEventListener("change", run)
  setupConditionalFields(form)
  run()
}
