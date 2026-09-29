# Northstar Workspace — Render Ready

A responsive glassmorphism project/task dashboard built with Flask. All project files are in the repository root; there are no subfolders.

## Files
- `app.py` — complete app, embedded HTML/CSS/JavaScript and Flask routes
- `requirements.txt` — Python dependencies
- `Procfile` — Gunicorn start command
- `render.yaml` — Render Blueprint
- `.gitignore` — excludes local Python files

## Deploy from a phone
1. Download and extract this ZIP.
2. Create a new GitHub repository.
3. Upload the files directly to the repository root. Do not upload the ZIP as a single file.
4. On Render, choose **New + → Blueprint**, then connect the repository.
5. Wait for deployment and open the `onrender.com` URL.

## Local run
`pip install -r requirements.txt` then `python app.py`

## Storage note
Demo data is stored in `/tmp/northstar_data.json`, which may reset on Render restarts. Add a managed PostgreSQL database for persistent production data. This starter does not include user login; add authentication before using private data.
