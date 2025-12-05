export async function postAuth(username) {
  const res = await fetch('/api/auth', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username })
  })
  return res.json()
}

export async function registerUser(payload) {
  const res = await fetch('/api/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
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

export async function createDealership(payload) {
  const res = await fetch('/api/dealerships', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function createCar(payload) {
  const res = await fetch('/api/cars', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function sellCar(carId, payload) {
  const res = await fetch(`/api/cars/${carId}/sell`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return res.json()
}
