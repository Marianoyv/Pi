import { fetchJsonFromSources, getIpcUrls, getIclUrls } from "/finance/shared/data-sources.js"

const q = (id) => document.getElementById(id)

const ipcLastEl = q("ipc-last")
const iclLastEl = q("icl-last")
const ipcRangeEl = q("ipc-range")
const iclRangeEl = q("icl-range")

const ipcStatusEl = q("ipc-status")
const iclStatusEl = q("icl-status")

const ipcAgoEl = q("ipc-ago")
const iclAgoEl = q("icl-ago")

const noteEl = q("updates-note")

const MONTHS_ES = [
  "Enero","Febrero","Marzo","Abril","Mayo","Junio",
  "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"
]

async function safeFetchJSON(urls) {
  try {
    const { data } = await fetchJsonFromSources(urls, { cache: "no-store" })
    return data
  } catch {
    return null
  }
}

function setNote(msg) {
  if (!noteEl) return
  if (!msg) {
    noteEl.hidden = true
    noteEl.textContent = ""
    return
  }
  noteEl.hidden = false
  noteEl.textContent = msg
}

function setStatus(el, type, text) {
  if (!el) return
  el.classList.remove("ok", "stale")
  if (type) el.classList.add(type)
  el.textContent = text || "—"
}

function setText(el, text) {
  if (!el) return
  el.textContent = text ?? "—"
}

function formatIPCMonth(ym) {
  if (!/^\d{4}-\d{2}$/.test(ym)) return null
  const y = Number(ym.slice(0, 4))
  const m = Number(ym.slice(5, 7))
  if (!Number.isFinite(y) || !Number.isFinite(m) || m < 1 || m > 12) return null
  return `${MONTHS_ES[m - 1]} ${y}`
}

function formatICLDate(iso) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(iso)) return null
  const y = iso.slice(0, 4)
  const m = iso.slice(5, 7)
  const d = iso.slice(8, 10)
  return `${d}/${m}/${y}`
}

function getIPCMinMax(ipcJson) {
  const monthly = ipcJson?.monthly
  if (!monthly || typeof monthly !== "object") return null
  const keys = Object.keys(monthly).filter(k => /^\d{4}-\d{2}$/.test(k)).sort()
  if (!keys.length) return null
  return { min: keys[0], max: keys[keys.length - 1] }
}

function getICLMinMax(iclJson) {
  const daily = iclJson?.daily
  if (!daily || typeof daily !== "object") return null
  const keys = Object.keys(daily).filter(k => /^\d{4}-\d{2}-\d{2}$/.test(k)).sort()
  if (!keys.length) return null
  return { min: keys[0], max: keys[keys.length - 1] }
}

function ymIndex(ym) {
  const y = Number(ym.slice(0, 4))
  const m = Number(ym.slice(5, 7))
  return y * 12 + (m - 1)
}

function todayISO() {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, "0")
  const day = String(d.getDate()).padStart(2, "0")
  return `${y}-${m}-${day}`
}

function todayYM() {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, "0")
  return `${y}-${m}`
}

function subtractDaysISO(iso, days) {
  const y = Number(iso.slice(0, 4))
  const m = Number(iso.slice(5, 7)) - 1
  const d = Number(iso.slice(8, 10))
  const dt = new Date(y, m, d)
  dt.setDate(dt.getDate() - days)
  const yy = dt.getFullYear()
  const mm = String(dt.getMonth() + 1).padStart(2, "0")
  const dd = String(dt.getDate()).padStart(2, "0")
  return `${yy}-${mm}-${dd}`
}

function daysBetweenISO(a, b) {
  const ay = Number(a.slice(0, 4))
  const am = Number(a.slice(5, 7)) - 1
  const ad = Number(a.slice(8, 10))
  const by = Number(b.slice(0, 4))
  const bm = Number(b.slice(5, 7)) - 1
  const bd = Number(b.slice(8, 10))
  const da = new Date(ay, am, ad)
  const db = new Date(by, bm, bd)
  const diff = db.getTime() - da.getTime()
  return Math.round(diff / 86400000)
}

function monthsAgoText(lastYM) {
  if (!/^\d{4}-\d{2}$/.test(lastYM)) return null
  const now = todayYM()
  const diff = ymIndex(now) - ymIndex(lastYM)
  if (diff <= 0) return "este mes"
  if (diff === 1) return "hace 1 mes"
  return `hace ${diff} meses`
}

function daysAgoText(lastISO) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(lastISO)) return null
  const t = todayISO()
  const diff = daysBetweenISO(lastISO, t)
  if (diff <= 0) return "hoy"
  if (diff === 1) return "ayer"
  return `hace ${diff} días`
}

function evaluateIPCStatus(lastUpdateYM) {
  if (!/^\d{4}-\d{2}$/.test(lastUpdateYM)) return null
  const nowIdx = ymIndex(todayYM())
  const lastIdx = ymIndex(lastUpdateYM)

  // El IPC suele publicarse el mes siguiente (típicamente a mitad de mes).
  // En la primera mitad del mes actual es esperable que el último dato sea el de hace 2 meses.
  const day = new Date().getDate()
  const allowedLag = day < 15 ? 2 : 1

  if (lastIdx >= (nowIdx - allowedLag)) return { type: "ok", text: "OK" }
  if (lastIdx < (nowIdx - allowedLag)) return { type: "stale", text: "Desactualizado" }
  return { type: "ok", text: "OK" }
}

function evaluateICLStatus(lastUpdateISO) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(lastUpdateISO)) return null
  const t = todayISO()
  const y = subtractDaysISO(t, 1)
  if (lastUpdateISO === t || lastUpdateISO === y) return { type: "ok", text: "OK" }
  return { type: "stale", text: "Desactualizado" }
}

async function init() {
  const [ipc, icl] = await Promise.all([
    safeFetchJSON(getIpcUrls()),
    safeFetchJSON(getIclUrls())
  ])

  const notes = []

  // IPC
  const ipcLastRaw = ipc?.lastUpdate
  const ipcLastFmt = ipcLastRaw ? formatIPCMonth(ipcLastRaw) : null
  setText(ipcLastEl, ipcLastFmt || "—")
  if (!ipcLastFmt) notes.push("No se pudo leer/formatear la última actualización de IPC.")

  const ipcAgo = ipcLastRaw ? monthsAgoText(ipcLastRaw) : null
  setText(ipcAgoEl, ipcAgo || "—")

  const ipcMM = getIPCMinMax(ipc)
  if (ipcMM) {
    const minFmt = formatIPCMonth(ipcMM.min)
    const maxFmt = formatIPCMonth(ipcMM.max)
    setText(ipcRangeEl, (minFmt && maxFmt) ? `${minFmt} → ${maxFmt}` : "—")
    if (!(minFmt && maxFmt)) notes.push("No se pudo formatear el rango de IPC.")
  } else {
    setText(ipcRangeEl, "—")
    notes.push("No se pudo leer el rango de IPC.")
  }

  const ipcStatus = ipcLastRaw ? evaluateIPCStatus(ipcLastRaw) : null
  if (ipcStatus) setStatus(ipcStatusEl, ipcStatus.type, ipcStatus.text)
  else setStatus(ipcStatusEl, "stale", "Sin datos")

  // ICL
  const iclLastRaw = icl?.lastUpdate
  const iclLastFmt = iclLastRaw ? formatICLDate(iclLastRaw) : null
  setText(iclLastEl, iclLastFmt || "—")
  if (!iclLastFmt) notes.push("No se pudo leer/formatear la última actualización de ICL.")

  const iclAgo = iclLastRaw ? daysAgoText(iclLastRaw) : null
  setText(iclAgoEl, iclAgo || "—")

  const iclMM = getICLMinMax(icl)
  if (iclMM) {
    const minFmt = formatICLDate(iclMM.min)
    const maxFmt = formatICLDate(iclMM.max)
    setText(iclRangeEl, (minFmt && maxFmt) ? `${minFmt} → ${maxFmt}` : "—")
    if (!(minFmt && maxFmt)) notes.push("No se pudo formatear el rango de ICL.")
  } else {
    setText(iclRangeEl, "—")
    notes.push("No se pudo leer el rango de ICL.")
  }

  const iclStatus = iclLastRaw ? evaluateICLStatus(iclLastRaw) : null
  if (iclStatus) setStatus(iclStatusEl, iclStatus.type, iclStatus.text)
  else setStatus(iclStatusEl, "stale", "Sin datos")

  setNote(notes.length ? notes.join(" ") : "")
}

init()
