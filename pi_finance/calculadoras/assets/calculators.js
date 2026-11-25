const assertFinite = (value, label) => {
  const number = Number(value)
  if (!Number.isFinite(number)) throw new RangeError(`${label} debe ser un número válido.`)
  return number
}

const assertPositive = (value, label) => {
  const number = assertFinite(value, label)
  if (number <= 0) throw new RangeError(`${label} debe ser mayor que cero.`)
  return number
}

const assertNonNegative = (value, label) => {
  const number = assertFinite(value, label)
  if (number < 0) throw new RangeError(`${label} no puede ser negativo.`)
  return number
}

export function simpleInterest({ capital, annualRate, term, unit = "months" }) {
  const principal = assertPositive(capital, "El capital")
  const rate = assertNonNegative(annualRate, "La tasa anual") / 100
  const duration = assertPositive(term, "El plazo")
  const years = unit === "days" ? duration / 365 : unit === "years" ? duration : duration / 12
  const interest = principal * rate * years

  return { principal, interest, total: principal + interest, effectiveRate: rate * years }
}

export function compoundInterest({ capital, annualRate, months, compoundsPerYear = 12 }) {
  const principal = assertPositive(capital, "El capital")
  const rate = assertNonNegative(annualRate, "La tasa anual") / 100
  const duration = assertPositive(months, "El plazo")
  const frequency = assertPositive(compoundsPerYear, "La frecuencia")
  const periods = frequency * duration / 12
  const total = principal * Math.pow(1 + rate / frequency, periods)

  return {
    principal,
    interest: total - principal,
    total,
    periods,
    effectiveRate: total / principal - 1
  }
}

export function fixedTerm({ capital, tna, days }) {
  const principal = assertPositive(capital, "El capital")
  const annualRate = assertNonNegative(tna, "La TNA") / 100
  const duration = assertPositive(days, "El plazo")
  const effectiveRate = annualRate * duration / 365
  const interest = principal * effectiveRate

  return { principal, interest, total: principal + interest, effectiveRate }
}

export function frenchLoan({ principal, tna, months }) {
  const amount = assertPositive(principal, "El monto del préstamo")
  const annualRate = assertNonNegative(tna, "La TNA") / 100
  const installments = Math.trunc(assertPositive(months, "La cantidad de cuotas"))
  if (installments > 600) throw new RangeError("La cantidad de cuotas no puede superar 600.")
  const monthlyRate = annualRate / 12
  const payment = monthlyRate === 0
    ? amount / installments
    : amount * monthlyRate / (1 - Math.pow(1 + monthlyRate, -installments))

  let balance = amount
  const schedule = []
  for (let installment = 1; installment <= installments; installment += 1) {
    const interest = balance * monthlyRate
    const amortization = installment === installments ? balance : payment - interest
    const installmentPayment = installment === installments ? amortization + interest : payment
    balance = Math.max(0, balance - amortization)
    schedule.push({ installment, payment: installmentPayment, interest, amortization, balance })
  }

  const total = schedule.reduce((sum, row) => sum + row.payment, 0)
  return { payment, total, interest: total - amount, monthlyRate, schedule }
}

export function convertRates({ mode = "tna", annualRate, periodsPerYear = 12 }) {
  const inputRate = assertNonNegative(annualRate, "La tasa") / 100
  const periods = assertPositive(periodsPerYear, "La cantidad de capitalizaciones")
  let tna
  let tea
  let periodicRate

  if (mode === "tea") {
    tea = inputRate
    periodicRate = Math.pow(1 + tea, 1 / periods) - 1
    tna = periodicRate * periods
  } else {
    tna = inputRate
    periodicRate = tna / periods
    tea = Math.pow(1 + periodicRate, periods) - 1
  }

  const tem = Math.pow(1 + tea, 1 / 12) - 1
  return { inputRate, tna, tea, tem, periodicRate }
}

export function percentageIncrease({ amount, percentage }) {
  const base = assertNonNegative(amount, "El valor inicial")
  const rate = assertNonNegative(percentage, "El porcentaje") / 100
  const change = base * rate
  return { base, change, total: base + change, rate }
}

export function percentageDiscount({ amount, percentage }) {
  const base = assertNonNegative(amount, "El precio original")
  const percent = assertNonNegative(percentage, "El descuento")
  if (percent > 100) throw new RangeError("El descuento no puede superar el 100 %.")
  const rate = percent / 100
  const change = base * rate
  return { base, change, total: base - change, rate }
}

export function percentageVariation({ initial, final }) {
  const start = assertPositive(initial, "El valor inicial")
  const end = assertFinite(final, "El valor final")
  const difference = end - start
  return { initial: start, final: end, difference, variation: difference / start }
}

export function vat({ amount, rate = 21, mode = "add" }) {
  const enteredAmount = assertNonNegative(amount, "El importe")
  const taxRate = assertNonNegative(rate, "La alícuota") / 100

  if (mode === "extract") {
    const base = enteredAmount / (1 + taxRate)
    return { base, tax: enteredAmount - base, total: enteredAmount, taxRate }
  }

  const tax = enteredAmount * taxRate
  return { base: enteredAmount, tax, total: enteredAmount + tax, taxRate }
}

export function investmentReturn({ initialInvestment, finalValue, income = 0, months = 12 }) {
  const investment = assertPositive(initialInvestment, "La inversión inicial")
  const endingValue = assertNonNegative(finalValue, "El valor final")
  const additionalIncome = assertFinite(income, "Los ingresos adicionales")
  const duration = assertPositive(months, "El plazo")
  const profit = endingValue + additionalIncome - investment
  const roi = profit / investment
  const annualized = 1 + roi >= 0 ? Math.pow(1 + roi, 12 / duration) - 1 : null

  return { investment, profit, roi, annualized, multiplier: (endingValue + additionalIncome) / investment }
}

function installmentPresentValue(payment, installments, monthlyRate) {
  if (Math.abs(monthlyRate) < 1e-12) return payment * installments
  return payment * (1 - Math.pow(1 + monthlyRate, -installments)) / monthlyRate
}

export function cashOrInstallments({ cashPrice, installmentCount, installmentAmount, monthlyOpportunityRate = 0 }) {
  const cash = assertPositive(cashPrice, "El precio de contado")
  const installments = Math.trunc(assertPositive(installmentCount, "La cantidad de cuotas"))
  if (installments > 120) throw new RangeError("La cantidad de cuotas no puede superar 120.")
  const payment = assertPositive(installmentAmount, "El valor de cada cuota")
  const opportunityRate = assertNonNegative(monthlyOpportunityRate, "La tasa mensual de referencia") / 100
  const financedTotal = payment * installments
  const surcharge = financedTotal - cash

  let low = -0.99
  let high = 10
  for (let iteration = 0; iteration < 180; iteration += 1) {
    const middle = (low + high) / 2
    if (installmentPresentValue(payment, installments, middle) > cash) low = middle
    else high = middle
  }

  const implicitMonthlyRate = (low + high) / 2
  const implicitAnnualRate = Math.pow(1 + implicitMonthlyRate, 12) - 1
  const presentValue = installmentPresentValue(payment, installments, opportunityRate)
  const presentValueDifference = presentValue - cash

  return {
    cash,
    payment,
    installments,
    financedTotal,
    surcharge,
    surchargeRate: surcharge / cash,
    implicitMonthlyRate,
    implicitAnnualRate,
    presentValue,
    presentValueDifference,
    recommendation: presentValue < cash ? "Convienen las cuotas" : presentValue > cash ? "Conviene pagar de contado" : "Las opciones son equivalentes"
  }
}

function simulateDebt(balance, monthlyRate, monthlyPayment, maximumMonths = 1_200) {
  let outstanding = balance
  let totalInterest = 0
  let totalPaid = 0
  const schedule = []

  if (monthlyPayment <= outstanding * monthlyRate && monthlyRate > 0) {
    throw new RangeError("El pago mensual no alcanza para cubrir los intereses del primer mes.")
  }

  for (let month = 1; month <= maximumMonths && outstanding > 0.005; month += 1) {
    const interest = outstanding * monthlyRate
    const payment = Math.min(monthlyPayment, outstanding + interest)
    const amortization = payment - interest
    outstanding = Math.max(0, outstanding - amortization)
    totalInterest += interest
    totalPaid += payment
    schedule.push({ installment: month, payment, interest, amortization, balance: outstanding })
  }

  if (outstanding > 0.005) throw new RangeError("Con estos datos la deuda tarda más de 100 años en cancelarse.")
  return { months: schedule.length, totalInterest, totalPaid, schedule }
}

export function debtPayoff({ balance, tna, monthlyPayment, extraPayment = 0 }) {
  const debt = assertPositive(balance, "La deuda")
  const annualRate = assertNonNegative(tna, "La TNA") / 100
  const payment = assertPositive(monthlyPayment, "El pago mensual")
  const extra = assertNonNegative(extraPayment, "El pago extra")
  const monthlyRate = annualRate / 12
  const base = simulateDebt(debt, monthlyRate, payment)
  const accelerated = extra > 0 ? simulateDebt(debt, monthlyRate, payment + extra) : base

  return {
    monthlyRate,
    months: accelerated.months,
    totalInterest: accelerated.totalInterest,
    totalPaid: accelerated.totalPaid,
    paymentWithExtra: payment + extra,
    monthsSaved: base.months - accelerated.months,
    interestSaved: base.totalInterest - accelerated.totalInterest,
    baseMonths: base.months,
    baseInterest: base.totalInterest,
    schedule: accelerated.schedule
  }
}

export function salaryPurchasingPower({ initialSalary, currentSalary, inflationFactor }) {
  const initial = assertPositive(initialSalary, "El sueldo inicial")
  const current = assertPositive(currentSalary, "El sueldo actual")
  const factor = assertPositive(inflationFactor, "El factor de inflación")
  const inflationAdjustedSalary = initial * factor
  const nominalIncrease = current / initial - 1
  const realVariation = current / inflationAdjustedSalary - 1

  return {
    initial,
    current,
    inflationAdjustedSalary,
    nominalIncrease,
    realVariation,
    purchasingPowerDifference: current - inflationAdjustedSalary
  }
}

export function fixedTermFromTea({ capital, tea, days, expectedAnnualInflation = 0 }) {
  const principal = assertPositive(capital, "El capital")
  const annualEffectiveRate = assertNonNegative(tea, "La TEA") / 100
  const duration = assertPositive(days, "El plazo")
  const inflation = assertNonNegative(expectedAnnualInflation, "La inflación anual esperada") / 100
  const periodRate = Math.pow(1 + annualEffectiveRate, duration / 365) - 1
  const inflationRate = Math.pow(1 + inflation, duration / 365) - 1
  const total = principal * (1 + periodRate)
  const realTotal = total / (1 + inflationRate)

  return { principal, total, interest: total - principal, periodRate, inflationRate, realTotal, realGain: realTotal - principal }
}

export function uvaLoanScenario({ principal, currentUva, annualRate, months, annualInflation, monthlyIncome, annualIncomeGrowth = 0 }) {
  const amount = assertPositive(principal, "El monto del crédito")
  const uva = assertPositive(currentUva, "El valor UVA")
  const realAnnualRate = assertNonNegative(annualRate, "La tasa fija anual") / 100
  const installments = Math.trunc(assertPositive(months, "La cantidad de cuotas"))
  if (installments > 480) throw new RangeError("El plazo no puede superar 480 meses.")
  const inflation = assertNonNegative(annualInflation, "La inflación anual") / 100
  const income = assertPositive(monthlyIncome, "El ingreso mensual")
  const incomeGrowth = assertNonNegative(annualIncomeGrowth, "El aumento anual del ingreso") / 100
  const monthlyRealRate = realAnnualRate / 12
  const monthlyInflation = Math.pow(1 + inflation, 1 / 12) - 1
  const monthlyIncomeGrowth = Math.pow(1 + incomeGrowth, 1 / 12) - 1
  const principalUva = amount / uva
  const paymentUva = monthlyRealRate === 0
    ? principalUva / installments
    : principalUva * monthlyRealRate / (1 - Math.pow(1 + monthlyRealRate, -installments))

  let balanceUva = principalUva
  let uvaValue = uva
  let projectedIncome = income
  let totalNominal = 0
  const schedule = []

  for (let month = 1; month <= installments; month += 1) {
    uvaValue *= 1 + monthlyInflation
    projectedIncome *= 1 + monthlyIncomeGrowth
    const interestUva = balanceUva * monthlyRealRate
    const amortizationUva = month === installments ? balanceUva : paymentUva - interestUva
    const installmentUva = month === installments ? amortizationUva + interestUva : paymentUva
    balanceUva = Math.max(0, balanceUva - amortizationUva)
    const payment = installmentUva * uvaValue
    const balance = balanceUva * uvaValue
    totalNominal += payment
    schedule.push({ installment: month, payment, balance, uvaValue, income: projectedIncome, incomeRatio: payment / projectedIncome })
  }

  const rowAt = (month) => schedule[Math.min(month, installments) - 1]
  return {
    principalUva,
    paymentUva,
    initialPayment: schedule[0].payment,
    payment12: rowAt(12).payment,
    payment24: rowAt(24).payment,
    finalPayment: schedule.at(-1).payment,
    balance12: rowAt(12).balance,
    totalNominal,
    initialIncomeRatio: schedule[0].incomeRatio,
    maximumIncomeRatio: Math.max(...schedule.map((row) => row.incomeRatio)),
    schedule
  }
}

export function monotributoCategory({ annualRevenue, activity = "services", categories }) {
  const revenue = assertNonNegative(annualRevenue, "La facturación anual")
  if (!Array.isArray(categories) || categories.length === 0) throw new RangeError("No se pudieron cargar las categorías vigentes.")
  const eligibleCategories = activity === "services"
    ? categories.filter((item) => !/venta de/i.test(String(item.activity || "")))
    : categories
  const category = eligibleCategories.find((item) => revenue <= Number(item.maxAnnualRevenue))
  if (!category) return { excluded: true, revenue, maximum: Number(eligibleCategories.at(-1).maxAnnualRevenue) }
  const monthlyFee = Number(activity === "goods" ? category.totalGoods : category.totalServices)
  const remaining = Number(category.maxAnnualRevenue) - revenue
  const index = eligibleCategories.indexOf(category)

  return {
    excluded: false,
    revenue,
    category: category.category,
    maximum: Number(category.maxAnnualRevenue),
    remaining,
    percentUsed: revenue / Number(category.maxAnnualRevenue),
    monthlyFee,
    nextCategory: eligibleCategories[index + 1]?.category || null,
    nextMaximum: Number(eligibleCategories[index + 1]?.maxAnnualRevenue || 0)
  }
}
