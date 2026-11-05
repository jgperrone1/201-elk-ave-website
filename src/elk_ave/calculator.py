"""Deterministic Clinical Footprint & Capital Preservation Calculator.

Provides pure business logic for evaluating how a prospective medical tenant's
room requirements, specialty type, and cosmetic finish tier map onto 207 Elk Ave S,
quantifying speed-to-market and Tenant Improvement (TI) capital preservation
compared to cold-shell medical construction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

VALID_SPECIALTIES = (
    "multi-specialty-outpatient",
    "urgent-care-diagnostics",
    "dental-oral-health",
    "dermatology-aesthetics",
    "rehab-physical-therapy",
    "behavioral-health",
    "academic-health-sciences",
)

VALID_FINISH_TIERS = (
    "turnkey-refresh",
    "modern-clinical",
    "bespoke-hospitality",
)


class CalculatorValidationError(ValueError):
    """Raised when clinical configurator inputs violate domain constraints."""


@dataclass(frozen=True)
class SpaceEstimateRequest:
    """Validated user input for clinical footprint and capital estimation."""

    specialty_id: str
    desired_clinical_rooms: int
    daily_patients: int
    finish_tier: str = "modern-clinical"
    needs_xray_or_lab: bool = True
    needs_conference_hall: bool = False


@dataclass(frozen=True)
class SpaceEstimateResult:
    """Calculated recommendation and capital preservation estimate."""

    recommended_floor_plan: str
    recommended_level_code: str
    plumbed_rooms_allocated: int
    procedure_rooms_included: int
    estimated_usable_sqft: int
    estimated_cold_shell_cost_usd: int
    estimated_turnkey_ti_cost_usd: int
    estimated_capital_saved_usd: int
    months_saved_vs_shell: int
    parking_spaces_available: int
    ibc_occupancy_note: str
    key_advantages: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize estimate result to a dictionary."""
        return asdict(self)


def validate_estimate_request(request: SpaceEstimateRequest) -> None:
    """Validate all fields of a SpaceEstimateRequest at the boundary."""
    if request.specialty_id not in VALID_SPECIALTIES:
        raise CalculatorValidationError(
            f"Unsupported specialty_id '{request.specialty_id}'. "
            f"Expected one of: {', '.join(VALID_SPECIALTIES)}."
        )
    if not isinstance(request.desired_clinical_rooms, int) or isinstance(request.desired_clinical_rooms, bool):
        raise CalculatorValidationError("desired_clinical_rooms must be an integer.")
    if request.desired_clinical_rooms < 1 or request.desired_clinical_rooms > 45:
        raise CalculatorValidationError(
            f"desired_clinical_rooms must be between 1 and 45 (received {request.desired_clinical_rooms})."
        )
    if not isinstance(request.daily_patients, int) or isinstance(request.daily_patients, bool):
        raise CalculatorValidationError("daily_patients must be an integer.")
    if request.daily_patients < 5 or request.daily_patients > 500:
        raise CalculatorValidationError(
            f"daily_patients must be between 5 and 500 (received {request.daily_patients})."
        )
    if request.finish_tier not in VALID_FINISH_TIERS:
        raise CalculatorValidationError(
            f"Unsupported finish_tier '{request.finish_tier}'. "
            f"Expected one of: {', '.join(VALID_FINISH_TIERS)}."
        )


def calculate_clinical_fit(request: SpaceEstimateRequest) -> SpaceEstimateResult:
    """Compute recommended floor selection, TI capital savings, and speed to market."""
    validate_estimate_request(request)

    rooms = request.desired_clinical_rooms

    # Determine optimal floor configuration based on room count & specialty profile
    if (
        rooms <= 11
        and (request.specialty_id in ("behavioral-health", "rehab-physical-therapy", "academic-health-sciences") or request.needs_conference_hall)
        and request.specialty_id != "urgent-care-diagnostics"
    ):
        level_code = "level-2"
        floor_plan = "Upper Level (2nd Floor — 11 Plumbed Rooms, Lab #235, 576 SF Hall & 16+ Offices)"
        allocated_rooms = 11
        proc_rooms = 1
        usable_sqft = 6800
        months_saved = 8
    elif rooms <= 14 and not request.needs_conference_hall:
        level_code = "level-1-wing"
        floor_plan = "Ground Floor Phased Clinical Pod (12–16 Plumbed Exam & Procedure Suites)"
        allocated_rooms = max(rooms, 12)
        proc_rooms = 4
        usable_sqft = 5800
        months_saved = 9
    elif rooms <= 24 and not request.needs_conference_hall:
        level_code = "level-1-full"
        floor_plan = "Full Ground Floor Clinical Wing (24+ Exam Rooms, 7 Procedure Suites, X-Ray & Dual Waiting)"
        allocated_rooms = 24
        proc_rooms = 7
        usable_sqft = 10500
        months_saved = 11
    else:
        level_code = "full-campus"
        floor_plan = "Full Two-Story Medical Campus (35+ Plumbed Rooms, 7 Procedure Suites, Labs & Executive Wing)"
        allocated_rooms = 35
        proc_rooms = 8
        usable_sqft = 17300
        months_saved = 14

    # Cold dark shell medical build-out in 2026 averages ~$215/SF due to wet-wall trenching,
    # MEP rough-ins, ADA restroom core construction, and solid-core partitioning.
    cold_shell_per_sqft = 215
    if request.specialty_id in ("dental-oral-health", "urgent-care-diagnostics", "dermatology-aesthetics"):
        cold_shell_per_sqft = 240

    # Existing turnkey infrastructure at 207 Elk Ave S preserves plumbing wet walls,
    # partitions, 12 ADA restrooms, elevator, and electrical panels.
    tier_cost_per_sqft = {
        "turnkey-refresh": 28,
        "modern-clinical": 52,
        "bespoke-hospitality": 82,
    }[request.finish_tier]

    cold_shell_cost = usable_sqft * cold_shell_per_sqft
    turnkey_ti_cost = usable_sqft * tier_cost_per_sqft
    capital_saved = max(0, cold_shell_cost - turnkey_ti_cost)

    # Dedicated 0.5-acre lot across Elk Ave S + on-site apron supports ~75+ spaces
    parking_spaces = 75

    advantages = [
        f"Avoids concrete slab trenching across {allocated_rooms} wet-wall plumbed clinical rooms.",
        "Retains protected IBC Group B (Business) medical classification with zero structural fire-code retrofits.",
    ]
    if request.needs_xray_or_lab:
        advantages.append(
            "Includes existing X-Ray suite, Reading Room, Phlebotomy Blood Draw, and built-in Laboratory cabinetry."
        )
    if request.needs_conference_hall or level_code in ("level-2", "full-campus"):
        advantages.append(
            "Includes 576 SF clear-span Conference/Didactic Hall (#222) and 2nd-floor Executive Lounge."
        )
    advantages.append(
        f"Accommodates {request.daily_patients} daily patient visits with dual waiting rooms and 0.5-acre dedicated parking."
    )

    return SpaceEstimateResult(
        recommended_floor_plan=floor_plan,
        recommended_level_code=level_code,
        plumbed_rooms_allocated=allocated_rooms,
        procedure_rooms_included=proc_rooms,
        estimated_usable_sqft=usable_sqft,
        estimated_cold_shell_cost_usd=cold_shell_cost,
        estimated_turnkey_ti_cost_usd=turnkey_ti_cost,
        estimated_capital_saved_usd=capital_saved,
        months_saved_vs_shell=months_saved,
        parking_spaces_available=parking_spaces,
        ibc_occupancy_note="Strict IBC Group B (Outpatient Medical / Clinical Training) — no Group E/I-1 retrofit triggers.",
        key_advantages=tuple(advantages),
    )
