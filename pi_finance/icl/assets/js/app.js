import { parseMoney, formatARS, formatPct, addMonthsISO } from "./utils.js"
import { loadICL, resolveDateAvailable, resolveAvailableInfo, calcICL } from "./icl.js"

const q = (id) => document.getElementById(id)

const form = q("icl-form")
const amountEl = q("amount")
const fromEl = q("from")
const todayEl = q("today")
const durationEl = q("duration")
const frequencyEl = q("frequency")
const btn = q("calc-btn")

const errorEl = q("error")
const noticeEl = q("notice")
const resultEl = q("result")
const resultEmptyEl = q("result-empty")

const currentAmountEl = q("current-amount")
const updatedEl = q("updated-amount")
const accumulatedEl = q("accumulated")
const rangeEl = q("range")
const scheduleBodyEl = q("schedule-body")

const nextAdjustDateEl = q("next-adjust-date")
const nextAdjustAmountEl = q("next-adjust-amount")

let ICL_CACHE = null

function todayISO() {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, "0")
  const day = String(d.getDate()).padStart(2, "0")
  return `${y}-${m}-${day}`
}

function showError(msg) {
  errorEl.textContent = msg
  errorEl.hidden = false
  if (noticeEl) {
    noticeEl.hidden = true
    noticeEl.textContent = ""
  }
  resultEl.hidden = true
  if (resultEmptyEl) resultEmptyEl.hidden = false
}

function clearError() {
  errorEl.hidden = true
  errorEl.textContent = ""
}

function showNotice(msg) {
  if (!noticeEl) return
  if (!msg) {
    noticeEl.hidden = true
    noticeEl.textContent = ""
    return
  }
  noticeEl.hidden = false
  noticeEl.textContent = msg
}

function showResult() {
  resultEl.hidden = false
  if (resultEmptyEl) resultEmptyEl.hidden = true
}

async function getICL() {
  if (ICL_CACHE) return ICL_CACHE
  ICL_CACHE = await loadICL()
  return ICL_CACHE
}

async function setDefaultsFromICL() {
  const icl = await getICL()

  rangeEl.textContent = `${icl.min} → ${icl.max}`

  fromEl.min = icl.min
  fromEl.max = icl.max

  todayEl.min = icl.min
  todayEl.max = icl.max

  if (!todayEl.value) {
    const t = todayISO()
    todayEl.value = t <= icl.max ? t : icl.max
  }
}

function buildScheduleDates(startISO, durationMonths, frequencyMonths) {
  const endISO = addMonthsISO(startISO, durationMonths)
  const dates = []
  let k = frequencyMonths
  while (k <= durationMonths) {
    dates.push(addMonthsISO(startISO, k))
    k += frequencyMonths
  }
  return { endISO, adjustDates: dates }
}

function clearTable() {
  scheduleBodyEl.innerHTML = ""
}

function addRow(cells) {
  const tr = document.createElement("tr")
  for (const c of cells) {
    const td = document.createElement("td")
    td.textContent = c
    tr.appendChild(td)
  }
  scheduleBodyEl.appendChild(tr)
}

async function init() {
  await setDefaultsFromICL()
}

form.addEventListener("submit", async (e) => {
  e.preventDefault()
  clearError()
  showNotice("")
  btn.disabled = true

  try {
    const amount = parseMoney(amountEl.value)
    const from = fromEl.value
    const today = todayEl.value
    const durationMonths = Number(durationEl.value)
    const frequencyMonths = Number(frequencyEl.value)

    if (!Number.isFinite(amount) || amount <= 0) throw new Error("Monto inválido.")
    if (!from || !today) throw new Error("Completá fecha inicio y fecha hoy.")
    if (today < from) throw new Error("La fecha hoy no puede ser anterior al inicio.")
    if (![12, 24, 36].includes(durationMonths)) throw new Error("Duración inválida.")
    if (![3, 4, 6, 12].includes(frequencyMonths)) throw new Error("Frecuencia inválida.")

    const icl = await getICL()

    if (from < icl.min) throw new Error(`ICL disponible desde ${icl.min}.`)

    const { endISO, adjustDates } = buildScheduleDates(from, durationMonths, frequencyMonths)

    let warningMsg = ""
    let effectiveToday = today
    let effectiveEnd = endISO

    if (today > icl.max) {
      effectiveToday = icl.max
      warningMsg = `Último ICL disponible: ${icl.max}. Se calculó con ese valor.`
    }

    if (endISO > icl.max) {
      effectiveEnd = icl.max
      warningMsg = warningMsg || `ICL llega hasta ${icl.max}. La tabla se calcula hasta esa fecha.`
    }

    const usedFromInfo = resolveAvailableInfo(icl, from)
    const usedTodayInfo = resolveAvailableInfo(icl, effectiveToday)

    const iclFrom = Number(icl.map[usedFromInfo.used])
    const iclToday = Number(icl.map[usedTodayInfo.used])

    if (!Number.isFinite(iclFrom) || !Number.isFinite(iclToday)) {
      throw new Error("Datos ICL inválidos.")
    }

    const cont = calcICL(amount, iclFrom, iclToday)
    updatedEl.textContent = formatARS(cont.updated)
    accumulatedEl.textContent = formatPct(cont.accumulated)

    clearTable()

    let currentPayable = amount
    let periodStart = from
    let periodAmount = amount
    let rowIndex = 1

    let nextAdjustDate = null
    let nextAdjustAmount = null

    for (const d of adjustDates) {
      const periodEnd = d
      if (periodEnd > effectiveEnd) break

      const uStart = resolveDateAvailable(icl, periodStart)
      const uEnd = resolveDateAvailable(icl, periodEnd)

      const vStart = Number(icl.map[uStart])
      const vEnd = Number(icl.map[uEnd])

      if (!Number.isFinite(vStart) || !Number.isFinite(vEnd)) {
        throw new Error("Datos ICL inválidos.")
      }

      const r = calcICL(periodAmount, vStart, vEnd)
      const prevAmount = periodAmount
      periodAmount = r.updated

      addRow([
        String(rowIndex),
        periodStart,
        periodEnd,
        uStart,
        uEnd,
        formatPct(r.accumulated),
        formatARS(prevAmount),
        formatARS(periodAmount)
      ])

      if (!nextAdjustDate && effectiveToday < periodEnd) {
        nextAdjustDate = periodEnd
        nextAdjustAmount = periodAmount
      }

      if (effectiveToday >= periodEnd) {
        currentPayable = periodAmount
      }

      periodStart = periodEnd
      rowIndex += 1
    }

    currentAmountEl.textContent = formatARS(currentPayable)

    if (nextAdjustDate) {
      nextAdjustDateEl.textContent = nextAdjustDate
      nextAdjustAmountEl.textContent = formatARS(nextAdjustAmount)
    } else {
      nextAdjustDateEl.textContent = "No quedan ajustes dentro del contrato."
      nextAdjustAmountEl.textContent = "—"
    }

    const usedBits = []
    if (usedFromInfo.adjusted) usedBits.push(`Inicio ICL usado: ${usedFromInfo.used}`)
    if (usedTodayInfo.adjusted) usedBits.push(`Hoy ICL usado: ${usedTodayInfo.used}`)
    if (warningMsg) usedBits.push(warningMsg)

    showNotice(usedBits.join(" • "))

    rangeEl.textContent = `${icl.min} → ${icl.max}`

    showResult()
  } catch (err) {
    showError(err?.message || "Error inesperado.")
  } finally {
    btn.disabled = false
  }
})

fromEl.addEventListener("change", async () => {
  const from = fromEl.value
  if (!from) return

  const icl = await getICL()

  todayEl.min = from
  todayEl.max = icl.max

  if (!todayEl.value || todayEl.value < from) {
    todayEl.value = from
  }
})

init().catch(() => showError("No se pudo inicializar la calculadora (ICL)."))
