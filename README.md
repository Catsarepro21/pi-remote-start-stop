# pi-remote-start-stop

A minimalist PWA remote control for a Raspberry Pi 5 — start/stop Docker-based book-server containers and toggle Minecraft Mode to free RAM.

---

## Architecture

| Layer | Detail |
|---|---|
| Frontend | `index.html` hosted on GitHub Pages |
| Backend | Flask API (`app.py`) on the Pi, port 5000 |
| Networking | Tailscale (static IP `100.84.248.6`) |

---

## Pi Setup

### 1. Clone the repo

```bash
git clone https://github.com/Catsarepro21/pi-remote-start-stop.git /home/pi/pi-remote-start-stop
```

### 2. Install dependencies

```bash
pip3 install flask gunicorn
```

### 3. Install and enable the systemd service

```bash
sudo cp /home/pi/pi-remote-start-stop/books-server.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable books-server
sudo systemctl start books-server
```

Check status:
```bash
sudo systemctl status books-server
```

---

## API Endpoints

| Method | Path | Action |
|---|---|---|
| `POST` | `/start-books` | `docker start` for all book containers |
| `POST` | `/stop-books` | `docker stop` for all book containers |

**Containers managed:** `transmission`, `lazylibrarian`, `prowlarr`, `flaresolverr`

> **Security:** The API has no authentication layer by design — Tailscale provides network-level access control so only devices on your Tailnet can reach port 5000. Do not expose this port to the public internet.

---

## Frontend (GitHub Pages)

The `index.html` is served directly from the `main` branch via GitHub Pages.

- **📚 OPEN LIBRARY** — starts all book containers  
- **📦 STOP LIBRARY** — stops all book containers  
- **🎮 Minecraft Mode toggle** — flips the same stop/start logic; designed as a persistent state indicator so you always know which mode the Pi is in

> **Why `no-cors`?** Requests go from an HTTPS GitHub Pages origin to a plain HTTP Tailscale address. The browser would block this as a mixed-content request unless `mode: 'no-cors'` is used. With `no-cors` the request is sent as an *opaque* fetch — the command still reaches the Pi, but the response body is not readable by the page (which is fine here).

---

## PWA / Add to Home Screen

`manifest.json` is linked in the `<head>`. On iOS: tap **Share → Add to Home Screen**. On Android: tap the browser menu **→ Install app**.
