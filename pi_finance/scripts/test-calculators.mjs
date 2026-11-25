import assert from "node:assert/strict"
import fs from "node:fs"

import { addMonthsISO } from "../icl/assets/js/utils.js"
import { calculateIPC } from "../ipc/assets/js/calculator.js"
import {
  compoundInterest,
  convertRates,
  cashOrInstallments,
  debtPayoff,
  fixedTerm,
  fixedTermFromTea,
  frenchLoan,
  investmentReturn,
  monotributoCategory,
  percentageDiscount,
  percentageIncrease,
  percentageVariation,
  simpleInterest,
  salaryPurchasingPower,
  uvaLoanScenario,
  vat
} from "../calculadoras/assets/calculators.js"

const closeTo = (actual, expected, tolerance = 0.000001) => {
  assert.ok(Math.abs(actual - expected) <= tolerance, `${actual} debería aproximarse a ${expected}`)
}

const dateCases = [
  ["2025-01-31", 3, "2025-04-30"],
  ["2023-11-30", 3, "2024-02-29"],
  ["2024-02-29", 12, "2025-02-28"],
  ["2026-01-15", 3, "2026-04-15"]
]

for (const [start, months, expected] of dateCases) {
  assert.equal(addMonthsISO(start, months), expected, `${start} + ${months} meses`)
}

const ipc = JSON.parse(fs.readFileSync(new URL("../ipc/data/ipc.json", import.meta.url), "utf8"))
const ipcResult = calculateIPC({
  amount: 100_000,
  from: "2026-01",
  to: "2026-07",
  monthly: ipc.monthly
})

assert.equal(ipcResult.rows.length, 6)
assert.ok(ipcResult.updatedAmount > 100_000)

const simple = simpleInterest({ capital: 100_000, annualRate: 36, term: 30, unit: "days" })
closeTo(simple.interest, 2_958.904109589041)

const compound = compoundInterest({ capital: 100_000, annualRate: 12, months: 12, compoundsPerYear: 12 })
closeTo(compound.total, 112_682.50301319698)

const deposit = fixedTerm({ capital: 500_000, tna: 35, days: 30 })
closeTo(deposit.interest, 14_383.561643835616)

const loan = frenchLoan({ principal: 1_000_000, tna: 60, months: 12 })
assert.equal(loan.schedule.length, 12)
closeTo(loan.schedule.at(-1).balance, 0)
closeTo(loan.total, loan.payment * 12, 0.01)

const rates = convertRates({ mode: "tna", annualRate: 60, periodsPerYear: 12 })
closeTo(rates.tea, Math.pow(1.05, 12) - 1)
const ratesBack = convertRates({ mode: "tea", annualRate: rates.tea * 100, periodsPerYear: 12 })
closeTo(ratesBack.tna, 0.6)

assert.deepEqual(percentageIncrease({ amount: 100_000, percentage: 15 }), {
  base: 100_000, change: 15_000, total: 115_000, rate: 0.15
})
assert.deepEqual(percentageDiscount({ amount: 50_000, percentage: 20 }), {
  base: 50_000, change: 10_000, total: 40_000, rate: 0.2
})
closeTo(percentageVariation({ initial: 80_000, final: 100_000 }).variation, 0.25)

const vatAdded = vat({ amount: 100_000, rate: 21, mode: "add" })
assert.equal(vatAdded.total, 121_000)
const vatExtracted = vat({ amount: 121_000, rate: 21, mode: "extract" })
closeTo(vatExtracted.base, 100_000)

const roi = investmentReturn({ initialInvestment: 500_000, finalValue: 620_000, income: 0, months: 12 })
closeTo(roi.roi, 0.24)
closeTo(roi.annualized, 0.24)

const purchase = cashOrInstallments({ cashPrice: 900_000, installmentCount: 12, installmentAmount: 100_000, monthlyOpportunityRate: 3 })
assert.equal(purchase.financedTotal, 1_200_000)
assert.ok(purchase.implicitMonthlyRate > 0)
assert.ok(purchase.presentValue < purchase.financedTotal)

const debt = debtPayoff({ balance: 1_500_000, tna: 90, monthlyPayment: 200_000, extraPayment: 50_000 })
assert.ok(debt.months < debt.baseMonths)
assert.ok(debt.interestSaved > 0)
closeTo(debt.schedule.at(-1).balance, 0)

const salary = salaryPurchasingPower({ initialSalary: 800_000, currentSalary: 1_000_000, inflationFactor: 1.5 })
closeTo(salary.realVariation, -1 / 6)

const bankDeposit = fixedTermFromTea({ capital: 1_000_000, tea: 25, days: 30, expectedAnnualInflation: 20 })
assert.ok(bankDeposit.total > 1_000_000)

const uva = uvaLoanScenario({ principal: 80_000_000, currentUva: 2_000, annualRate: 6, months: 240, annualInflation: 25, monthlyIncome: 4_500_000, annualIncomeGrowth: 22 })
assert.equal(uva.schedule.length, 240)
assert.ok(uva.payment12 > uva.initialPayment)

const categoriesData = JSON.parse(fs.readFileSync(new URL("../monotributo/data/categorias.json", import.meta.url), "utf8"))
const taxpayer = monotributoCategory({ annualRevenue: 18_000_000, activity: "services", categories: categoriesData.categories })
assert.equal(taxpayer.category, "C")
assert.ok(taxpayer.monthlyFee > 0)

const pageDirectories = [
  "interes-simple",
  "interes-compuesto",
  "plazo-fijo",
  "prestamo-sistema-frances",
  "tna-tea",
  "porcentaje-aumento",
  "porcentaje-descuento",
  "variacion-porcentual",
  "iva",
  "rentabilidad-inversion"
  ,"cuotas-o-contado"
  ,"cancelar-deudas"
  ,"sueldo-real"
  ,"comparador-plazos-fijos"
  ,"credito-uva"
  ,"monotributo"
]

const titles = new Set()
const root = new URL("../", import.meta.url)
for (const directory of pageDirectories) {
  const html = fs.readFileSync(new URL(`${directory}/index.html`, root), "utf8")
  const title = html.match(/<title>([^<]+)<\/title>/)?.[1]
  assert.ok(title, `${directory} necesita title`)
  assert.ok(!titles.has(title), `${directory} necesita un title único`)
  titles.add(title)
  assert.match(html, /<meta name="description" content="[^"]+">/)
  assert.match(html, new RegExp(`<link rel="canonical" href="https://pidevelopment\\.web\\.app/finance/${directory}/">`))
  assert.match(html, /<h1>[^<]+<\/h1>/)
  assert.match(html, /<script type="application\/ld\+json">/)
  assert.match(html, /<script type="module" src="\/finance\/(?:calculadoras\/assets|[^\"]+)\/app\.js"><\/script>/)

  for (const json of html.matchAll(/<script type="application\/ld\+json">\s*([\s\S]*?)\s*<\/script>/g)) {
    assert.doesNotThrow(() => JSON.parse(json[1]), `${directory} contiene JSON-LD inválido`)
  }
}

const sitemap = fs.readFileSync(new URL("sitemap.xml", root), "utf8")
for (const directory of pageDirectories) {
  assert.ok(sitemap.includes(`https://pidevelopment.web.app/finance/${directory}/`), `${directory} falta en sitemap.xml`)
}

const home = fs.readFileSync(new URL("index.html", root), "utf8")
assert.match(home, /id="calculadoras"/)
assert.equal((home.match(/class="card card-link calculator-card"/g) || []).length, 18)
assert.match(home, /"@type":"ItemList","numberOfItems":18/)
assert.match(home, /"@type":"Organization","@id":"https:\/\/pidevelopment\.web\.app\/finance\/#pi-development","name":"Pi Development"/)
assert.match(home, /<link rel="canonical" href="https:\/\/pidevelopment\.web\.app\/finance\/">/)
assert.match(home, /<link rel="icon" type="image\/png" href="\/finance\/icons\/favicon\.png">/)
assert.ok(fs.statSync(new URL("icons/favicon.png", root)).size > 0, "El favicon no puede estar vacío")
assert.ok(!fs.existsSync(new URL("calculadoras/index.html", root)), "El catálogo no debe duplicar la portada")
assert.ok(!sitemap.includes("https://pidevelopment.web.app/finance/calculadoras/"), "La URL consolidada no debe figurar en el sitemap")

for (const file of ["index.html", "shared/components/header.html", "shared/components/footer.html", ...pageDirectories.map((directory) => `${directory}/index.html`)]) {
  const html = fs.readFileSync(new URL(file, root), "utf8")
  assert.ok(!html.includes('href="/calculadoras/"'), `${file} todavía enlaza al catálogo anterior`)
  assert.ok(!html.includes("indices-argentinos.web.app"), `${file} todavía enlaza al dominio anterior`)
}

const footer = fs.readFileSync(new URL("shared/components/footer.html", root), "utf8")
assert.match(footer, /Un producto de <a href="\/">.*Pi Development.*<\/a>/s)

const uvaData = JSON.parse(fs.readFileSync(new URL("credito-uva/data/uva.json", root), "utf8"))
assert.ok(Object.keys(uvaData.daily).length > 3_000)
const ratesData = JSON.parse(fs.readFileSync(new URL("comparador-plazos-fijos/data/plazos-fijos.json", root), "utf8"))
assert.ok(ratesData.banks.length >= 20)
assert.equal(categoriesData.categories.length, 11)

console.log(`OK: 18 herramientas, fuentes oficiales, cálculos, SEO, autoría, redirección y sitemap verificados.`)
