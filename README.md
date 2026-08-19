# Interactive Learning Mat

An interactive learning application with a desktop interface and a browser-based 3D model viewer.

## Deploy with GitHub Pages

1. Push the `main` branch to GitHub.
2. Open **Settings > Pages** in the repository.
3. Under **Build and deployment**, select **GitHub Actions**.
4. Pushes to `main` will deploy the root site automatically.

The deployed viewer is available at:
`https://prathampimpalikar.github.io/Interactive-Learning-_Mat/`

GitHub Pages hosts the browser viewer and static 3D assets. The CustomTkinter desktop application still runs locally with Python and cannot run inside GitHub Pages.

## Run the desktop app

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python main.py
```

The Firebase service-account file is intentionally ignored. Keep `firebase_key.json` only on trusted local machines and never commit it.
