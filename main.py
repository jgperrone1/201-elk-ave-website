"""CLI entrypoint for building, validating, and serving the 207 Elk Ave S website."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from src.elk_ave.calculator import (
    VALID_FINISH_TIERS,
    VALID_SPECIALTIES,
    SpaceEstimateRequest,
    calculate_clinical_fit,
)
from src.elk_ave.catalog import build_property_listing
from src.elk_ave.renderer import (
    STATIC_SOURCE_DIR,
    build_root_pages_entry,
    build_static_site,
    verify_static_assets,
)
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

    est_cmd = subparsers.add_parser(
        "estimate", help="Calculate clinical footprint and TI capital preservation (internal/ownership tool)"
    )
    est_cmd.add_argument(
        "--specialty",
        choices=VALID_SPECIALTIES,
        default="multi-specialty-outpatient",
        help="Medical specialty profile",
    )
    est_cmd.add_argument(
        "--rooms",
        type=int,
        default=14,
        help="Desired clinical / exam rooms (1-45)",
    )
    est_cmd.add_argument(
        "--patients",
        type=int,
        default=60,
        help="Estimated daily patient visits (5-500)",
    )
    est_cmd.add_argument(
        "--tier",
        choices=VALID_FINISH_TIERS,
        default="modern-clinical",
        help="Cosmetic finish tier",
    )
    est_cmd.add_argument(
        "--no-xray",
        action="store_true",
        help="Exclude X-Ray and laboratory requirement",
    )
    est_cmd.add_argument(
        "--conference",
        action="store_true",
        help="Require didactic / conference hall (#222)",
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

    if command == "estimate":
        req = SpaceEstimateRequest(
            specialty_id=args.specialty,
            desired_clinical_rooms=args.rooms,
            daily_patients=args.patients,
            finish_tier=args.tier,
            needs_xray_or_lab=not args.no_xray,
            needs_conference_hall=args.conference,
        )
        res = calculate_clinical_fit(req)
        sys.stdout.write(
            "\n"
            "====================================================================\n"
            "  207 ELK AVE S — CLINICAL FIT & CAPITAL ESTIMATE (INTERNAL USE)\n"
            "====================================================================\n"
            f"Specialty Profile         : {req.specialty_id}\n"
            f"Recommended Floor Plan    : {res.recommended_floor_plan}\n"
            f"Level Allocation          : Level {res.recommended_level_code}\n"
            f"Plumbed Clinical Rooms    : {res.plumbed_rooms_allocated} rooms\n"
            f"Procedure Suites Included : {res.procedure_rooms_included} suites\n"
            f"Usable Footprint          : {res.estimated_usable_sqft:,} SF\n"
            "--------------------------------------------------------------------\n"
            f"Estimated Cold-Shell Cost : ${res.estimated_cold_shell_cost_usd:,.2f}\n"
            f"Estimated Turnkey TI Cost : ${res.estimated_turnkey_ti_cost_usd:,.2f}\n"
            f"Estimated Capital Saved   : ${res.estimated_capital_saved_usd:,.2f}\n"
            f"Speed-to-Market Advantage : {res.months_saved_vs_shell} months faster\n"
            f"Dedicated Parking Spaces  : {res.parking_spaces_available}+ spaces (0.5-acre lot)\n"
            "--------------------------------------------------------------------\n"
            "Key Advantages:\n"
            + "".join(f"  • {adv}\n" for adv in res.key_advantages)
            + "====================================================================\n\n"
        )
        return 0

    if command == "build":
        output_dir = getattr(args, "output", Path("dist"))
        manifest = build_static_site(output_dir)
        if output_dir == Path("dist"):
            root_index = build_root_pages_entry()
            logger.info("Synchronized GitHub Pages root entrypoint: %s", root_index)
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
