from __future__ import annotations

import json
from typing import Any, Optional
from urllib import error, request


class BackendRequestError(RuntimeError):
    def __init__(self, status_code: Optional[int], message: str, body: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.body = body


def post_json(url: str, payload: dict[str, Any], timeout: int = 10) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, method="POST", headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
    except error.HTTPError as exc:
        body_text = exc.read().decode("utf-8")
        try:
            body = json.loads(body_text) if body_text else None
        except json.JSONDecodeError:
            body = body_text
        raise BackendRequestError(exc.code, f"Backend returned HTTP {exc.code}", body) from exc
    except error.URLError as exc:
        raise BackendRequestError(None, f"Could not reach backend: {exc.reason}") from exc
