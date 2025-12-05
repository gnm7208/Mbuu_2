export async function postAuth(username) {
  const res = await fetch('/api/auth', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username })
  })
  return res.json()
}

export async function fetchCars(params = {}) {
  const qs = new URLSearchParams(params).toString()
  const res = await fetch('/api/cars' + (qs ? `?${qs}` : ''))
  return res.json()
}

export async function fetchDealerships() {
  const res = await fetch('/api/dealerships')
  return res.json()
}
