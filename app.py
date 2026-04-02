from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

CONTAINERS = ["transmission", "lazylibrarian", "prowlarr", "flaresolverr"]


def run(action: str) -> tuple[dict, int]:
    results = {}
    for c in CONTAINERS:
        try:
            subprocess.run(
                ["docker", action, c],
                check=True,
                capture_output=True,
                timeout=30,
            )
            results[c] = "ok"
        except subprocess.CalledProcessError as e:
            results[c] = f"error: {e.stderr.decode().strip()}"
        except subprocess.TimeoutExpired:
            results[c] = "error: timeout"

    failed = [k for k, v in results.items() if v != "ok"]
    status = 500 if failed else 200
    return jsonify({"action": action, "results": results}), status


@app.post("/start-books")
def start_books():
    return run("start")


@app.post("/stop-books")
def stop_books():
    return run("stop")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
