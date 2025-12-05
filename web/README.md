# Mbuu Web (development)

Run the frontend dev server:

```bash
cd web
npm install
npm run dev
```

The frontend expects the backend API at `/api/*` — during development run the Flask API at port 5001:

```bash
pipenv install -r requirements.txt
pipenv run python lib/web_api.py
```
