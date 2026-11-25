function parseYM(ym) {
  const [y, m] = ym.split("-").map(Number)
  if (!y || !m || m < 1 || m > 12) throw new Error("Fecha inválida.")
  return { y, m }
}

function toIndex({ y, m }) {
  return y * 12 + (m - 1)
}

function fromIndex(i) {
  const y = Math.floor(i / 12)
  const m = (i % 12) + 1
  return `${String(y).padStart(4, "0")}-${String(m).padStart(2, "0")}`
}

function buildMonthList(fromYM, toYM) {
  const a = toIndex(parseYM(fromYM))
  const b = toIndex(parseYM(toYM))
  if (a > b) throw new Error("'Desde' no puede ser mayor que 'Hasta'.")
  const out = []
  for (let i = a; i <= b; i++) out.push(fromIndex(i))
  return out
}

export function calculateIPC({ amount, from, to, monthly }) {
  // monthly[YYYY-MM] representa la variación % de ese mes vs el mes anterior.
  // Para actualizar un monto desde "from" hacia "to", se aplican las variaciones
  // desde el mes siguiente a "from" hasta "to" (inclusive).
  const months = buildMonthList(from, to).slice(1)

  let factor = 1
  let current = amount
  const rows = []

  for (const ym of months) {
    const v = monthly[ym]
    if (v === undefined || v === null) throw new Error(`Falta IPC para ${ym}.`)
    const r = Number(v)
    if (!Number.isFinite(r)) throw new Error(`IPC inválido para ${ym}.`)

    const periodFactor = 1 + (r / 100)
    const prev = current
    current = current * periodFactor
    factor = factor * periodFactor

    rows.push({
      ym,
      ipc: r,
      factor: periodFactor,
      prevAmount: prev,
      newAmount: current
    })
  }

  const updatedAmount = amount * factor
  const accumulatedRate = factor - 1

  return {
    updatedAmount,
    accumulatedRate,
    period: { from, to, months: months.length },
    rows
  }
}

export function monthIndex(ym) {
  return toIndex(parseYM(ym))
}
