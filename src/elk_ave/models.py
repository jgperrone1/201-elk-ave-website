"""Domain models for the 207 Elk Ave S medical & executive leasing platform."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class Provenance:
    """Tracks source document derivation for every piece of repository data."""

    source_document: str
    source_pages: tuple[int, ...]
    derivation_note: str


@dataclass(frozen=True)
class ContactProfile:
    """Ownership and leasing contact details."""

    name: str
    title: str
    role: str
    entity: str
    phone_display: str
    phone_uri: str
    email: str
    portrait_image: str
    credentials_summary: str
    provenance: Provenance


@dataclass(frozen=True)
class MetricHighlight:
    """Key quantitative property metric displayed in executive summaries."""

    id: str
    value: str
    unit_or_label: str
    detail: str
    category: str
    provenance: Provenance


@dataclass(frozen=True)
class SpaceZone:
    """A functional clinical or operational zone on a specific floor."""

    id: str
    name: str
    floor_level: int
    category: str
    room_count_label: str
    plumbing_equipped: bool
    highlights: tuple[str, ...]
    ideal_uses: tuple[str, ...]


@dataclass(frozen=True)
class FloorSpec:
    """Detailed architectural and clinical specification for a building floor."""

    level: int
    name: str
    tagline: str
    summary: str
    floorplan_image: str
    exam_and_clinical_rooms: int
    procedure_rooms: int
    restrooms: int
    exterior_egress_doors: int
    elevator_served: bool
    key_features: tuple[str, ...]
    zones: tuple[SpaceZone, ...]
    provenance: Provenance


@dataclass(frozen=True)
class TransformationPair:
    """Before-and-after architectural visualization pair."""

    id: str
    title: str
    subtitle: str
    category: str
    before_label: str
    before_image: str
    after_label: str
    after_image: str
    alt_image: str | None
    alt_label: str | None
    description: str
    clinical_value: str
    provenance: Provenance


@dataclass(frozen=True)
class TenantArchetype:
    """Medical or healthcare specialty profile showing property fit."""

    id: str
    specialty: str
    icon_name: str
    headline: str
    recommended_configuration: str
    target_rooms: int
    why_it_fits: tuple[str, ...]
    infrastructure_match: tuple[str, ...]
    provenance: Provenance


@dataclass(frozen=True)
class AdvantagePoint:
    """A generalized strategic advantage derived from the 28-point briefing."""

    number: int
    title: str
    description: str
    pillar_id: str
    provenance: Provenance


@dataclass(frozen=True)
class AdvantagePillar:
    """High-level strategic pillar grouping multiple property advantages."""

    id: str
    title: str
    subtitle: str
    summary: str
    points: tuple[AdvantagePoint, ...]


@dataclass(frozen=True)
class GalleryAsset:
    """Categorized visual asset for the property media gallery."""

    id: str
    title: str
    caption: str
    category: str
    image_path: str
    provenance: Provenance


@dataclass(frozen=True)
class PropertyListing:
    """Complete canonical dataset for 207 Elk Ave S medical & executive campus."""

    property_id: str
    headline: str
    subheadline: str
    street_address: str
    campus_alias: str
    city: str
    state: str
    postal_code: str
    county: str
    occupancy_classification: str
    building_lot_acres: float
    parking_lot_acres: float
    total_campus_acres: float
    executive_summary: tuple[str, ...]
    metrics: tuple[MetricHighlight, ...]
    floors: tuple[FloorSpec, ...]
    transformations: tuple[TransformationPair, ...]
    archetypes: tuple[TenantArchetype, ...]
    pillars: tuple[AdvantagePillar, ...]
    gallery: tuple[GalleryAsset, ...]
    contact: ContactProfile
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the complete property listing to a JSON-compatible dictionary."""
        return asdict(self)

