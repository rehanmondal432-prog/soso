"""soso - Simple HTTP requests helper."""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional, Union

__version__ = "0.1.0"
__all__ = ["get", "post", "request", "Response", "__version__"]


class Response:
    """Minimal response object similar to requests.Response."""

    def __init__(self, status_code: int, headers: Dict[str, str], content: bytes, url: str):
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self.url = url
        self.ok = 200 <= status_code < 300

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", errors="replace")

    def json(self) -> Any:
        return json.loads(self.text)

    def __repr__(self) -> str:
        return f"<Response [{self.status_code}]>"


def request(
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Union[Dict[str, Any], bytes, str]] = None,
    json_data: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 30.0,
) -> Response:
    """
    Send an HTTP request.

    Parameters
    ----------
    method : str
        HTTP method (GET, POST, PUT, DELETE, etc.)
    url : str
        Target URL
    params : dict, optional
        Query string parameters
    data : dict | bytes | str, optional
        Request body (form-encoded if dict)
    json_data : any, optional
        JSON body (sets Content-Type to application/json)
    headers : dict, optional
        Extra headers
    timeout : float
        Timeout in seconds

    Returns
    -------
    Response
    """
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}?{query}" if "?" not in url else f"{url}&{query}"

    body: Optional[bytes] = None
    req_headers = dict(headers or {})

    if json_data is not None:
        body = json.dumps(json_data).encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")
    elif data is not None:
        if isinstance(data, dict):
            body = urllib.parse.urlencode(data).encode("utf-8")
            req_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        elif isinstance(data, str):
            body = data.encode("utf-8")
        else:
            body = data

    req = urllib.request.Request(url, data=body, headers=req_headers, method=method.upper())

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            content = resp.read()
            status = resp.getcode() or 0
            resp_headers = {k: v for k, v in resp.headers.items()}
            return Response(status, resp_headers, content, resp.geturl())
    except urllib.error.HTTPError as e:
        content = e.read() if e.fp else b""
        resp_headers = {k: v for k, v in (e.headers.items() if e.headers else [])}
        return Response(e.code, resp_headers, content, url)


def get(url: str, **kwargs: Any) -> Response:
    """Send a GET request."""
    return request("GET", url, **kwargs)


def post(url: str, **kwargs: Any) -> Response:
    """Send a POST request."""
    return request("POST", url, **kwargs)
