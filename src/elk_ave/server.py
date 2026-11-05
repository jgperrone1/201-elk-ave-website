"""Local preview HTTP server and JSON API for the 207 Elk Ave S leasing platform."""

from __future__ import annotations

import json
import logging
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from src.elk_ave.calculator import (
    CalculatorValidationError,
    SpaceEstimateRequest,
    calculate_clinical_fit,
)
from src.elk_ave.catalog import build_property_listing
from src.elk_ave.renderer import STATIC_SOURCE_DIR, build_static_site

logger = logging.getLogger("elk_ave.server")


def dispatch_api_request(raw_path: str) -> tuple[HTTPStatus, dict[str, Any]] | None:
    """Route `/api/*` requests deterministically and return (status, payload) or None."""
    parsed = urlparse(raw_path)
    if parsed.path == "/api/health":
        return HTTPStatus.OK, {"status": "ok", "property_id": "207-elk-ave-s"}

    if parsed.path == "/api/property":
        listing = build_property_listing()
        return HTTPStatus.OK, listing.to_dict()

    if parsed.path == "/api/estimate":
        qs = parse_qs(parsed.query)
        try:
            req = SpaceEstimateRequest(
                specialty_id=qs.get("specialty_id", ["multi-specialty-outpatient"])[0],
                desired_clinical_rooms=int(qs.get("rooms", ["20"])[0]),
                daily_patients=int(qs.get("patients", ["95"])[0]),
                finish_tier=qs.get("tier", ["modern-clinical"])[0],
                needs_xray_or_lab=qs.get("xray", ["true"])[0].lower() in ("true", "1", "yes"),
                needs_conference_hall=qs.get("conf", ["false"])[0].lower() in ("true", "1", "yes"),
            )
            result = calculate_clinical_fit(req)
            return HTTPStatus.OK, result.to_dict()
        except (ValueError, CalculatorValidationError) as exc:
            return (
                HTTPStatus.BAD_REQUEST,
                {"error": "invalid_estimate_request", "message": str(exc)},
            )

    return None


class ElkAveRequestHandler(SimpleHTTPRequestHandler):
    """HTTP handler serving static property assets and JSON API routes."""

    def __init__(self, *args: Any, directory: str | None = None, **kwargs: Any) -> None:
        target_dir = directory or str(STATIC_SOURCE_DIR)
        super().__init__(*args, directory=target_dir, **kwargs)

    def log_message(self, format: str, *args: Any) -> None:
        logger.info("%s - %s", self.address_string(), format % args)

    def _send_json(self, payload: dict[str, Any], status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        api_result = dispatch_api_request(self.path)
        if api_result is not None:
            status, payload = api_result
            self._send_json(payload, status=status)
            return

        super().do_GET()


def create_server(host: str = "127.0.0.1", port: int = 8000, build_dir: Path | None = None) -> ThreadingHTTPServer:
    """Build static assets and return a configured ThreadingHTTPServer instance."""
    target_dir = build_dir or (Path.cwd() / "dist")
    build_static_site(target_dir)
    handler_cls = partial(ElkAveRequestHandler, directory=str(target_dir))
    return ThreadingHTTPServer((host, port), handler_cls)
