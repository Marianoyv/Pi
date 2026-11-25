import { loadIPC } from "./data.js"
import { calculateIPC, monthIndex } from "./calculator.js"

const q = (id) => document.getElementById(id)

const form = q("ipc-form")
const amountEl = q("amount")
const fromEl = q("from")
const toEl = q("to")

const resultBox = q("result")
const resultEmptyEl = q("result-empty")
const errorEl = q("error")
const noticeEl = q("notice")

const updatedAmountEl = q("updated-amount")
const accumulatedEl = q("accumulated")
const periodEl = q("period")
const lastUpdateEl = q("last-update")
const calcBtn = q("calc-btn")

const scheduleBodyEl = q("schedule-body")

const fmtMoney = new Intl.NumberFormat("es-AR", { style: "currency", currency: "ARS", maximumFractionDigits: 2 })
const fmtPct = new Intl.NumberFormat("es-AR", { style: "percent", maximumFractionDigits: 2 })

let ipcData = null
let monthsAvailable = []
let minYM = ""
let maxYM = ""

function todayYM() {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, "0")
  return `${y}-${m}`
}

function parseMoney(raw) {
  const s = String(raw ?? "").trim()
  if (!s) return NaN
  const normalized = s.replace(/\./g, "").replace(",", ".").replace(/[^\d.-]/g, "")
  return Number(normalized)
}

function showError(msg) {
  errorEl.textContent = msg
  errorEl.hidden = false
  if (noticeEl) {
    noticeEl.hidden = true
    noticeEl.textContent = ""
  }
  resultBox.hidden = true
  if (resultEmptyEl) resultEmptyEl.hidden = false
}

function clearError() {
  errorEl.textContent = ""
  errorEl.hidden = true
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
  resultBox.hidden = false
  if (resultEmptyEl) resultEmptyEl.hidden = true
}

function clearTable() {
  if (!scheduleBodyEl) return
  scheduleBodyEl.innerHTML = ""
}

function addRow(cells) {
  if (!scheduleBodyEl) return
  const tr = document.createElement("tr")
  for (const c of cells) {
    const td = document.createElement("td")
    td.textContent = c
    tr.appendChild(td)
  }
  scheduleBodyEl.appendChild(tr)
}

function clampToAvailableMonths(from, to) {
  let effectiveFrom = from
  let effectiveTo = to
  const notes = []

  if (effectiveFrom < minYM) {
    effectiveFrom = minYM
    notes.push(`'Desde' ajustado a ${minYM} (mínimo disponible).`)
  }

  if (effectiveTo > maxYM) {
    effectiveTo = maxYM
    notes.push(`Último IPC disponible: ${maxYM}. Se calculó hasta ese mes.`)
  }

  if (effectiveFrom > effectiveTo) {
    effectiveFrom = effectiveTo
    notes.push(`Rango ajustado por disponibilidad: ${effectiveFrom} → ${effectiveTo}.`)
  }

  return { effectiveFrom, effectiveTo, notes }
}

function readInputs() {
  const amount = parseMoney(amountEl.value)
  const from = fromEl.value
  const to = toEl.value

  if (!Number.isFinite(amount) || amount <= 0) throw new Error("Ingresá un monto válido mayor a 0.")
  if (!from) throw new Error("Seleccioná el mes 'Desde'.")
  if (!to) throw new Error("Seleccioná el mes 'Hasta'.")
  if (from > to) throw new Error("'Desde' no puede ser mayor que 'Hasta'.")

  const { effectiveFrom, effectiveTo, notes } = clampToAvailableMonths(from, to)

  return { amount, from, to, effectiveFrom, effectiveTo, notes }
}

async function init() {
  try {
    if (calcBtn) calcBtn.disabled = true

    ipcData = await loadIPC()

    monthsAvailable = Object.keys(ipcData.monthly || {}).sort()
    if (!monthsAvailable.length) throw new Error("IPC vacío.")

    minYM = monthsAvailable[0]
    maxYM = monthsAvailable[monthsAvailable.length - 1]

    lastUpdateEl.textContent = ipcData.lastUpdate || maxYM

    fromEl.min = minYM
    fromEl.max = maxYM
    toEl.min = minYM
    toEl.max = maxYM

    const t = todayYM()
    if (!fromEl.value) fromEl.value = minYM
    if (!toEl.value) toEl.value = t <= maxYM ? t : maxYM

    if (calcBtn) calcBtn.disabled = false
  } catch (e) {
    showError("No se pudo cargar IPC. Verificá la fuente de datos (JSON) y la conexión.")
  }
}

fromEl.addEventListener("change", () => {
  const from = fromEl.value
  const to = toEl.value
  if (!from || !to) return
  if (monthIndex(from) > monthIndex(to)) toEl.value = from
})

toEl.addEventListener("change", () => {
  const from = fromEl.value
  const to = toEl.value
  if (!from || !to) return
  if (monthIndex(to) < monthIndex(from)) fromEl.value = to
})

form.addEventListener("submit", (ev) => {
  ev.preventDefault()
  clearError()
  showNotice("")
  if (calcBtn) calcBtn.disabled = true

  if (!ipcData) {
    showError("Todavía no se cargaron los datos de IPC.")
    if (calcBtn) calcBtn.disabled = false
    return
  }

  try {
    const { amount, effectiveFrom, effectiveTo, notes } = readInputs()

    const out = calculateIPC({ amount, from: effectiveFrom, to: effectiveTo, monthly: ipcData.monthly })

    updatedAmountEl.textContent = fmtMoney.format(out.updatedAmount)
    accumulatedEl.textContent = fmtPct.format(out.accumulatedRate)
    periodEl.textContent = `${out.period.from} → ${out.period.to} (${out.period.months} meses)`

    clearTable()
    let idx = 1
    for (const r of out.rows) {
      addRow([
        String(idx),
        r.ym,
        `${r.ipc.toFixed(2)}%`,
        r.factor.toFixed(6),
        fmtMoney.format(r.prevAmount),
        fmtMoney.format(r.newAmount)
      ])
      idx += 1
    }

    showNotice(notes.join(" • "))
    showResult()
  } catch (e) {
    showError(e?.message || "Error al calcular.")
  } finally {
    if (calcBtn) calcBtn.disabled = false
  }
})

init()
