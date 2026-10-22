import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = [sys.executable, str(ROOT / "cli" / "mazu.py")]


def test_serve_moves_card(tmp_path):
    subprocess.run(CLI + ["init"], cwd=tmp_path, check=True)
    subprocess.run(CLI + ["add", "story", "Button", "--points", "2"], cwd=tmp_path, check=True)
    proc = subprocess.Popen(
        CLI + ["serve", "--port", "8766"],
        cwd=tmp_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        deadline = time.time() + 5
        page = ""
        while time.time() < deadline:
            try:
                with urllib.request.urlopen("http://127.0.0.1:8766/", timeout=0.5) as response:
                    page = response.read().decode("utf-8")
                    break
            except Exception:
                time.sleep(0.1)
        assert "MAZU-ADGILE" in page
        assert "var(--sage)" in page
        body = json.dumps({"id": "US-001", "status": "in-progress"}).encode()
        request = urllib.request.Request(
            "http://127.0.0.1:8766/api/move",
            data=body,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(request, timeout=2) as response:
            payload = json.loads(response.read().decode("utf-8"))
        assert payload["store"]["items"][0]["status"] == "in-progress"
    finally:
        proc.terminate()
        proc.wait(timeout=5)
