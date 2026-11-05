"""Automated unit and integration tests for the 207 Elk Ave S leasing platform."""

from __future__ import annotations

import json
import tempfile
import threading
import unittest
from http import HTTPStatus
from pathlib import Path

import main as cli_main
from src.elk_ave.calculator import (
    CalculatorValidationError,
    SpaceEstimateRequest,
    calculate_clinical_fit,
)
from src.elk_ave.catalog import build_property_listing
from src.elk_ave.renderer import (
    AssetVerificationError,
    build_json_ld,
    build_static_site,
    render_index_html,
    verify_static_assets,
)
from src.elk_ave.server import dispatch_api_request


class CatalogAndGeneralizationTests(unittest.TestCase):
    """Verify catalog completeness, provenance, and tenant generalization."""

    def setUp(self) -> None:
        self.listing = build_property_listing()

    def test_core_property_attributes(self) -> None:
        self.assertEqual(self.listing.property_id, "207-elk-ave-s")
        self.assertEqual(self.listing.street_address, "207 Elk Ave S")
        self.assertEqual(self.listing.city, "Fayetteville")
        self.assertEqual(self.listing.state, "TN")
        self.assertAlmostEqual(
            self.listing.building_lot_acres + self.listing.parking_lot_acres,
            self.listing.total_campus_acres,
            places=2,
        )
        self.assertEqual(self.listing.contact.name, "Shaz Perrone")
        self.assertEqual(self.listing.contact.email, "Shaz.Perrone@gmail.com")

    def test_floors_and_zones_specifications(self) -> None:
        self.assertEqual(len(self.listing.floors), 2)
        ground, upper = self.listing.floors
        self.assertEqual(ground.level, 1)
        self.assertEqual(ground.exam_and_clinical_rooms, 24)
        self.assertEqual(ground.procedure_rooms, 7)
        self.assertEqual(ground.restrooms, 8)
        self.assertEqual(ground.exterior_egress_doors, 7)
        self.assertTrue(ground.elevator_served)

        self.assertEqual(upper.level, 2)
        self.assertEqual(upper.exam_and_clinical_rooms, 11)
        self.assertEqual(upper.restrooms, 4)
        self.assertTrue(upper.elevator_served)

    def test_content_is_generalized_beyond_single_tenant_pitch(self) -> None:
        """Ensure single-tenant target names from the reference PDF are generalized out."""
        html_output = render_index_html(self.listing)
        forbidden_tokens = ("TWU", "Tennessee Wesleyan", "Wilhelm")
        for token in forbidden_tokens:
            self.assertNotIn(
                token,
                html_output,
                f"Found ungeneralized single-tenant token '{token}' in rendered HTML.",
            )

    def test_provenance_preserved_across_all_entities(self) -> None:
        for metric in self.listing.metrics:
            self.assertTrue(metric.provenance.source_pages)
        for tr in self.listing.transformations:
            self.assertTrue(tr.provenance.source_pages)
        for arch in self.listing.archetypes:
            self.assertTrue(arch.provenance.source_pages)
        for pillar in self.listing.pillars:
            self.assertGreater(len(pillar.points), 0)
            for pt in pillar.points:
                self.assertTrue(pt.provenance.source_pages)


class CalculatorTests(unittest.TestCase):
    """Verify deterministic clinical footprint and TI capital calculator."""

    def test_boundary_minimum_values(self) -> None:
        req = SpaceEstimateRequest(
            specialty_id="behavioral-health",
            desired_clinical_rooms=1,
            daily_patients=5,
            finish_tier="turnkey-refresh",
            needs_xray_or_lab=False,
            needs_conference_hall=True,
        )
        res = calculate_clinical_fit(req)
        self.assertEqual(res.recommended_level_code, "level-2")
        self.assertEqual(res.plumbed_rooms_allocated, 11)
        self.assertGreater(res.estimated_capital_saved_usd, 0)

    def test_ground_floor_wing_and_full_ground_boundaries(self) -> None:
        pod_req = SpaceEstimateRequest(
            specialty_id="dermatology-aesthetics",
            desired_clinical_rooms=12,
            daily_patients=60,
            finish_tier="bespoke-hospitality",
            needs_conference_hall=False,
        )
        pod_res = calculate_clinical_fit(pod_req)
        self.assertEqual(pod_res.recommended_level_code, "level-1-wing")

        full_l1_req = SpaceEstimateRequest(
            specialty_id="multi-specialty-outpatient",
            desired_clinical_rooms=24,
            daily_patients=140,
            finish_tier="modern-clinical",
            needs_conference_hall=False,
        )
        full_l1_res = calculate_clinical_fit(full_l1_req)
        self.assertEqual(full_l1_res.recommended_level_code, "level-1-full")
        self.assertEqual(full_l1_res.plumbed_rooms_allocated, 24)

    def test_maximum_campus_boundary(self) -> None:
        max_req = SpaceEstimateRequest(
            specialty_id="academic-health-sciences",
            desired_clinical_rooms=45,
            daily_patients=500,
            finish_tier="modern-clinical",
            needs_xray_or_lab=True,
            needs_conference_hall=True,
        )
        max_res = calculate_clinical_fit(max_req)
        self.assertEqual(max_res.recommended_level_code, "full-campus")
        self.assertEqual(max_res.plumbed_rooms_allocated, 35)
        self.assertEqual(max_res.months_saved_vs_shell, 14)

    def test_invalid_inputs_raise_validation_error(self) -> None:
        invalid_cases = [
            SpaceEstimateRequest("unknown-specialty", 10, 50),
            SpaceEstimateRequest("dental-oral-health", 0, 50),
            SpaceEstimateRequest("dental-oral-health", 46, 50),
            SpaceEstimateRequest("dental-oral-health", True, 50),  # type: ignore[arg-type]
            SpaceEstimateRequest("dental-oral-health", 10, 4),
            SpaceEstimateRequest("dental-oral-health", 10, 501),
            SpaceEstimateRequest("dental-oral-health", 10, 50, finish_tier="luxury-gold"),
        ]
        for bad_req in invalid_cases:
            with self.subTest(bad_req=bad_req):
                with self.assertRaises(CalculatorValidationError):
                    calculate_clinical_fit(bad_req)


class RendererAndServerTests(unittest.TestCase):
    """Verify static site generation, asset verification, and HTTP server endpoints."""

    def test_missing_asset_raises_verification_error(self) -> None:
        listing = build_property_listing()
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(AssetVerificationError):
                verify_static_assets(listing, Path(tmp))

    def test_build_static_site_and_json_ld(self) -> None:
        listing = build_property_listing()
        ld = build_json_ld(listing)
        self.assertEqual(ld["@type"], "RealEstateListing")
        self.assertEqual(ld["address"]["streetAddress"], "207 Elk Ave S")

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "dist"
            manifest = build_static_site(out_dir)
            self.assertGreaterEqual(manifest["verified_asset_count"], 25)
            self.assertTrue((out_dir / "index.html").is_file())
            self.assertTrue((out_dir / "styles.css").is_file())
            self.assertTrue((out_dir / "app.js").is_file())
            self.assertTrue((out_dir / "property-data.json").is_file())

    def test_cli_check_and_build_commands(self) -> None:
        self.assertEqual(cli_main.main(["check"]), 0)
        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp) / "site"
            self.assertEqual(cli_main.main(["build", "--output", str(out_dir)]), 0)
            self.assertTrue((out_dir / "index.html").is_file())

    def test_http_server_routes(self) -> None:
        # 1. Health check
        health = dispatch_api_request("/api/health")
        self.assertIsNotNone(health)
        assert health is not None
        self.assertEqual(health[0], HTTPStatus.OK)
        self.assertEqual(health[1]["status"], "ok")

        # 2. Property listing endpoint
        prop = dispatch_api_request("/api/property")
        self.assertIsNotNone(prop)
        assert prop is not None
        self.assertEqual(prop[0], HTTPStatus.OK)
        self.assertEqual(prop[1]["property_id"], "207-elk-ave-s")

        # 3. Valid estimate request
        est = dispatch_api_request(
            "/api/estimate?specialty_id=dental-oral-health&rooms=18&patients=110&tier=modern-clinical"
        )
        self.assertIsNotNone(est)
        assert est is not None
        self.assertEqual(est[0], HTTPStatus.OK)
        self.assertEqual(est[1]["recommended_level_code"], "level-1-full")

        # 4. Invalid estimate request returns 400 Bad Request
        bad = dispatch_api_request("/api/estimate?rooms=999")
        self.assertIsNotNone(bad)
        assert bad is not None
        self.assertEqual(bad[0], HTTPStatus.BAD_REQUEST)
        self.assertEqual(bad[1]["error"], "invalid_estimate_request")

        # 5. Static paths return None so SimpleHTTPRequestHandler serves files
        self.assertIsNone(dispatch_api_request("/index.html"))

    def test_top_header_and_button_alignment_contract(self) -> None:
        listing = build_property_listing()
        html_output = render_index_html(listing)
        self.assertIn('<nav class="header-nav" aria-label="Primary Navigation">', html_output)
        self.assertIn('>Schedule Tour</a>', html_output)

        css_path = Path(__file__).resolve().parent.parent / "src" / "elk_ave" / "static" / "styles.css"
        css_text = css_path.read_text(encoding="utf-8")
        self.assertIn(".header-nav {", css_text)
        self.assertIn("white-space: nowrap;", css_text)
        self.assertIn("scrollbar-width: none;", css_text)


if __name__ == "__main__":
    unittest.main()
