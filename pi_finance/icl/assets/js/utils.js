export function parseMoney(input) {
  const s = String(input ?? "").trim()
  const normalized = s.replace(/\./g, "").replace(",", ".")
  const n = Number(normalized)
  return Number.isFinite(n) ? n : NaN
}

export function formatARS(n) {
  return new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", maximumFractionDigits: 2 }).format(n)
}

export function formatPct(n) {
  return new Intl.NumberFormat("es-AR", { style: "percent", maximumFractionDigits: 2 }).format(n)
}

export function addMonthsISO(isoDate, months) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(String(isoDate))
  if (!match || !Number.isInteger(months)) throw new Error("Fecha inválida.")

  const year = Number(match[1])
  const monthIndex = Number(match[2]) - 1
  const day = Number(match[3])
  const sourceDate = new Date(Date.UTC(year, monthIndex, day))

  if (
    sourceDate.getUTCFullYear() !== year ||
    sourceDate.getUTCMonth() !== monthIndex ||
    sourceDate.getUTCDate() !== day
  ) {
    throw new Error("Fecha inválida.")
  }

  const targetIndex = year * 12 + monthIndex + months
  const targetYear = Math.floor(targetIndex / 12)
  const targetMonthIndex = ((targetIndex % 12) + 12) % 12
  const lastDayOfTargetMonth = new Date(Date.UTC(targetYear, targetMonthIndex + 1, 0)).getUTCDate()
  const targetDay = Math.min(day, lastDayOfTargetMonth)

  const yyyy = String(targetYear).padStart(4, "0")
  const mm = String(targetMonthIndex + 1).padStart(2, "0")
  const dd = String(targetDay).padStart(2, "0")
  return `${yyyy}-${mm}-${dd}`
}
