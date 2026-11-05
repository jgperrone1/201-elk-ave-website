"""CLI entrypoint for building, validating, and serving the 207 Elk Ave S website."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.elk_ave.catalog import build_property_listing
from src.elk_ave.renderer import STATIC_SOURCE_DIR, build_static_site, verify_static_assets
from src.elk_ave.server import create_server

logger = logging.getLogger("elk_ave.cli")


def configure_logging() -> None:
    """Configure structured console logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="elk-ave-web",
        description="Build, verify, or serve the 207 Elk Ave S medical leasing website.",
    )
    subparsers = parser.add_subparsers(dest="command")

    build_cmd = subparsers.add_parser("build", help="Generate static website into dist/")
    build_cmd.add_argument(
        "--output",
        type=Path,
        default=Path("dist"),
        help="Target output directory (default: dist)",
    )

    subparsers.add_parser("check", help="Validate property catalog, provenance, and static assets")

    serve_cmd = subparsers.add_parser("serve", help="Build and run local preview server")
    serve_cmd.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    serve_cmd.add_argument("--port", type=int, default=8000, help="Bind port (default: 8000)")
    serve_cmd.add_argument(
        "--output",
        type=Path,
        default=Path("dist"),
        help="Target build directory to serve (default: dist)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Execute the requested CLI operation."""
    configure_logging()
    parser = build_parser()
    args = parser.parse_args(argv)
    command = args.command or "build"

    if command == "check":
        listing = build_property_listing()
        verified = verify_static_assets(listing, STATIC_SOURCE_DIR)
        logger.info(
            "Validation passed: property_id=%s floors=%d archetypes=%d pillars=%d verified_assets=%d",
            listing.property_id,
            len(listing.floors),
            len(listing.archetypes),
            len(listing.pillars),
            len(verified),
        )
        return 0

    if command == "build":
        output_dir = getattr(args, "output", Path("dist"))
        manifest = build_static_site(output_dir)
        logger.info(
            "Static site built: output_dir=%s verified_assets=%d html_bytes=%d",
            manifest["output_dir"],
            manifest["verified_asset_count"],
            manifest["html_bytes"],
        )
        return 0

    if command == "serve":
        server = create_server(host=args.host, port=args.port, build_dir=args.output)
        logger.info("Serving 207 Elk Ave S website at http://%s:%d", args.host, args.port)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down local preview server.")
        finally:
            server.server_close()
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
