import hashlib
import os
import platform
import time
import uuid
from typing import Any, Dict, Optional, Tuple

import requests


def get_device_fingerprint() -> str:
    raw = f"{platform.node()}|{platform.system()}|{platform.release()}|{uuid.getnode()}"
    return hashlib.sha256(raw.encode("utf-8", errors="ignore")).hexdigest()


def verify_license(license_server_url: Optional[str], license_key: Optional[str]) -> Tuple[bool, str, Dict[str, Any]]:
    license_server_url = (license_server_url or os.environ.get("LICENSE_SERVER_URL") or "").strip()
    license_key = (license_key or os.environ.get("LICENSE_KEY") or "").strip()
    if not license_server_url or not license_key:
        return True, "Licencia no configurada (modo libre)", {"mode": "unlicensed"}

    payload = {
        "license_key": license_key,
        "device_id": get_device_fingerprint(),
        "ts": int(time.time()),
    }
    try:
        resp = requests.post(license_server_url, json=payload, timeout=15)
    except Exception as e:
        return False, f"No se pudo validar licencia (sin conexión): {e}", {"mode": "offline"}

    if resp.status_code != 200:
        return False, f"Licencia inválida (HTTP {resp.status_code})", {"mode": "error", "status": resp.status_code}

    try:
        data = resp.json()
    except Exception:
        return False, "Respuesta de licencia no es JSON", {"mode": "error"}

    if data.get("maintenance") is True:
        return False, "Sistema en mantenimiento. Intenta más tarde.", data

    if data.get("status") != "ok":
        return False, data.get("message") or "Licencia inválida", data

    expires_at = data.get("expires_at")
    if isinstance(expires_at, (int, float)):
        if time.time() > float(expires_at):
            return False, "Licencia vencida", data

    return True, "Licencia válida", data

