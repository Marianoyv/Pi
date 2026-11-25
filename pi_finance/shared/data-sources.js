const DEFAULT_TIMEOUT_MS = 8000

export function getIclUrls() {
  return ["/finance/icl/data/icl.json"]
}

export function getIpcUrls() {
  return ["/finance/ipc/data/ipc.json"]
}

export async function fetchJsonFromSources(urls, opts = {}) {
  const { cache = "no-store", timeoutMs = DEFAULT_TIMEOUT_MS } = opts
  let lastErr = null

  for (const url of urls) {
    const controller = new AbortController()
    const t = setTimeout(() => controller.abort(), timeoutMs)

    try {
      const res = await fetch(url, { cache, signal: controller.signal })
      if (!res.ok) throw new Error(`fetch_failed_${res.status}`)
      const data = await res.json()
      return { data, url }
    } catch (e) {
      lastErr = e
    } finally {
      clearTimeout(t)
    }
  }

  throw lastErr || new Error("fetch_failed")
}
