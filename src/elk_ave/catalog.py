"""Canonical property catalog for 207 Elk Ave S, Fayetteville, TN.

All facts, spatial counts, and strategic advantages derive from
`references/207 Elk Ave for TWU.pdf` (Pages 1-30) and are generalized for
prospective medical, dental, specialty clinical, behavioral health, outpatient
procedure, and healthcare training tenants.
"""

from __future__ import annotations

from src.elk_ave.models import (
    AdvantagePillar,
    AdvantagePoint,
    ContactProfile,
    FloorSpec,
    GalleryAsset,
    MetricHighlight,
    PropertyListing,
    Provenance,
    SpaceZone,
    TenantArchetype,
    TransformationPair,
)

SOURCE_PDF = "207-elk-ave-s-property-briefing-deck"


def build_property_listing() -> PropertyListing:
    """Return the canonical, generalized property dataset for 207 Elk Ave S."""
    contact = ContactProfile(
        name="Shaz Perrone",
        title="Commercial Real Estate Development",
        role="Principal / Owner",
        entity="207 Elk LLC (207 Elk Ave S)",
        phone_display="(973) 271-5324",
        phone_uri="tel:+19732715324",
        email="Shaz.Perrone@gmail.com",
        portrait_image="assets/images/owner-shaz-perrone.jpg",
        credentials_summary=(
            "Commercial real estate principal with a Master of Science in Finance, "
            "backed by a multidisciplinary ownership team rooted in clinical medicine, "
            "healthcare administration, academia, and engineering."
        ),
        provenance=Provenance(
            source_document=SOURCE_PDF,
            source_pages=(2, 18, 29, 30),
            derivation_note="Extracted directly from Owner contact slides and executive summary.",
        ),
    )

    metrics = (
        MetricHighlight(
            id="clinical-rooms",
            value="35+",
            unit_or_label="Plumbed Clinical & Exam Rooms",
            detail="24+ ground-floor private exam suites plus 11 upper-level sink-equipped clinical rooms.",
            category="Clinical Capacity",
            provenance=Provenance(SOURCE_PDF, (16, 20), "Sum of 24+ ground exam rooms and 11 upper clinical rooms."),
        ),
        MetricHighlight(
            id="procedure-suites",
            value="7",
            unit_or_label="Dedicated Procedure Rooms",
            detail="Specialized ground-floor procedure suites plus X-Ray, EKG, Blood Draw, and clinical labs.",
            category="Specialty Care",
            provenance=Provenance(SOURCE_PDF, (16, 20), "Page 20 Point 2 & Page 16 1st Floor Plan."),
        ),
        MetricHighlight(
            id="restrooms-ada",
            value="12",
            unit_or_label="Restrooms & Central Elevator",
            detail="8 ground-floor and 4 second-floor restrooms with full ADA commercial elevator access.",
            category="Accessibility",
            provenance=Provenance(SOURCE_PDF, (14, 16, 22), "Page 22 Point 8 & Page 14 Elevator photo."),
        ),
        MetricHighlight(
            id="dedicated-parking",
            value="0.5",
            unit_or_label="Acre Dedicated Parking Parcel",
            detail="Private off-street lot directly across Elk Ave S (Tract 2: 0.45 AC) plus on-site ADA parking.",
            category="Parking & Access",
            provenance=Provenance(SOURCE_PDF, (11, 15, 24), "Page 15 Survey Tract 1 (0.39 AC) & Tract 2 (0.45 AC); Page 24 Point 14."),
        ),
        MetricHighlight(
            id="egress-doors",
            value="7",
            unit_or_label="Ground-Floor Entry & Egress Doors",
            detail="Seamless separation of main patient arrival, pediatric/sub-waiting, staff access, and emergency egress.",
            category="Patient Flow",
            provenance=Provenance(SOURCE_PDF, (16, 22), "Page 22 Point 9."),
        ),
        MetricHighlight(
            id="campus-scale",
            value="17,300 SF",
            unit_or_label="Total Two-Story Clinical Footprint",
            detail="Elevator-connected two-story medical facility on a 0.84-acre total downtown campus.",
            category="Campus Scale",
            provenance=Provenance(SOURCE_PDF, (3, 11, 15), "Two-story building and campus acreage."),
        ),
    )

    floors = (
        FloorSpec(
            level=1,
            name="Ground Level (1st Floor)",
            tagline="High-Density Outpatient Clinical, Diagnostic & Procedure Wing",
            summary=(
                "Engineered for high-throughput outpatient care with dual waiting rooms, "
                "dedicated check-in/check-out reception, 24+ plumbed exam rooms, 7 procedure suites, "
                "4 nurse workstations, X-ray & reading rooms, phlebotomy/lab suites, and 7 exterior doors."
            ),
            floorplan_image="assets/images/floorplan-level-1.png",
            exam_and_clinical_rooms=24,
            procedure_rooms=7,
            restrooms=8,
            exterior_egress_doors=7,
            elevator_served=True,
            key_features=(
                "24+ private exam rooms with functional wet walls and sinks",
                "7 dedicated procedure rooms (including Med/Peds procedure suite)",
                "Dual waiting lounges: Main Waiting Room + Dedicated Pediatric / Specialty Sub-Waiting",
                "Dedicated Reception, 2 private Intake Offices, and high-density Medical File Room",
                "On-site X-Ray suite with adjacent Reading Room and Dressing Room",
                "Dedicated Blood Draw station, Clinical Laboratory, and EKG suite",
                "4 centralized Nurse Workstations distributed across clinical corridors",
                "8 ADA-compliant patient and staff restrooms + central stainless commercial elevator",
            ),
            zones=(
                SpaceZone(
                    id="l1-front-of-house",
                    name="Patient Arrival, Dual Waiting & Intake Suite",
                    floor_level=1,
                    category="Front of House",
                    room_count_label="Lobby + 2 Waiting Rooms + 3 Intake/Admin Rooms",
                    plumbing_equipped=False,
                    highlights=(
                        "Covered main entry vestibule off Elk Ave S with adjacent ADA parking",
                        "Main Waiting Room & separate Pediatric/Sub-Waiting Lounge to isolate patient cohorts",
                        "Dedicated Check-In / Check-Out Reception window, 2 Intake Offices, and secure File Room",
                    ),
                    ideal_uses=(
                        "High-volume multi-provider check-in",
                        "Well-child vs. sick-visit waiting separation",
                        "Spacious patient arrival lobby and intake reception counter",
                    ),
                ),
                SpaceZone(
                    id="l1-clinical-exam",
                    name="Primary & Specialty Exam Pod Corridors",
                    floor_level=1,
                    category="Clinical Exam",
                    room_count_label="24+ Private Exam Suites",
                    plumbing_equipped=True,
                    highlights=(
                        "24+ private exam rooms arranged in efficient double-loaded clinical pods",
                        "Existing cabinetry, sinks, wet-wall plumbing, and medical-grade electrical layouts",
                        "Direct subfloor utility access for rapid dental chair, laser, or vacuum line connections",
                    ),
                    ideal_uses=(
                        "Primary Care & Family Medicine",
                        "Multi-specialty outpatient clinics",
                        "Dental operatories & oral hygiene suites",
                    ),
                ),
                SpaceZone(
                    id="l1-procedure-diagnostics",
                    name="Procedure, Imaging & Diagnostic Wing",
                    floor_level=1,
                    category="Procedures & Diagnostics",
                    room_count_label="7 Procedure Suites + X-Ray + Lab + EKG",
                    plumbing_equipped=True,
                    highlights=(
                        "7 specialized procedure rooms along the southern and central clinical wings",
                        "Dedicated X-Ray suite with private Dressing Room and diagnostic Reading Room",
                        "Dedicated Blood Draw station, Clinical Lab, EKG room, and Med/Supply closets",
                    ),
                    ideal_uses=(
                        "Outpatient dermatology, Mohs & aesthetic procedures",
                        "Urgent care & orthopedic walk-in diagnostics",
                        "On-site phlebotomy and point-of-care testing",
                    ),
                ),
                SpaceZone(
                    id="l1-nurse-support",
                    name="Nurse Stations & Clinical Operations Core",
                    floor_level=1,
                    category="Clinical Support",
                    room_count_label="4 Nurse Stations + 6 Private Physician Offices + 8 Restrooms",
                    plumbing_equipped=True,
                    highlights=(
                        "4 strategically positioned Nurse Workstations and Work Alcoves with sightlines down exam corridors",
                        "6 private physician/provider consultation offices distributed across clinical pods",
                        "Central passenger elevator, 3 interior stairwells, and 7 exterior egress doors",
                    ),
                    ideal_uses=(
                        "Care team charting & triage",
                        "Provider dictation & telemedicine consults",
                        "Seamless staff circulation & compliant emergency egress",
                    ),
                ),
            ),
            provenance=Provenance(
                source_document=SOURCE_PDF,
                source_pages=(16, 20, 21, 22),
                derivation_note="Derived from 1st Floor architectural plan (p. 16) and clinical infrastructure points 1-9 (pp. 20-22).",
            ),
        ),
        FloorSpec(
            level=2,
            name="Upper Level (2nd Floor)",
            tagline="Specialty Clinic, Laboratory, Executive Offices & Training Wing",
            summary=(
                "Flexible second-story layout accessible via central elevator and three stairwells, "
                "featuring 11 sink-equipped clinical rooms, a built-in laboratory (#235), a 576 sq ft "
                "clear-span conference/training hall (#222), a secondary conference/break lounge, "
                "16+ executive/administrative offices, and 4 restrooms."
            ),
            floorplan_image="assets/images/floorplan-level-2.png",
            exam_and_clinical_rooms=11,
            procedure_rooms=1,
            restrooms=4,
            exterior_egress_doors=2,
            elevator_served=True,
            key_features=(
                "11 sink-equipped upper-level clinical exam and treatment rooms",
                "Built-in laboratory suite (#235) with existing clinical cabinetry and wet walls",
                "576 sq ft (24 x 24 ft) clear-span Conference / Training Room (#222) plus secondary Conference Lounge",
                "Dedicated upper-floor Waiting Lounge and Reception desk right off the elevator lobby",
                "16+ private executive, behavioral health, or administrative offices along the perimeter",
                "2 staff kitchens/breakrooms, abundant archive storage, and 4 dedicated restrooms",
            ),
            zones=(
                SpaceZone(
                    id="l2-clinical-lab",
                    name="Upper Clinical & Built-In Laboratory Suite",
                    floor_level=2,
                    category="Clinical & Lab",
                    room_count_label="11 Sink-Equipped Rooms + Lab Suite (#235)",
                    plumbing_equipped=True,
                    highlights=(
                        "11 plumbed exam/clinical rooms ideal for specialty practice or simulation suites",
                        "Turnkey Laboratory (#235) with built-in cabinetry and plumbing",
                        "Dedicated upper Waiting Room and Reception station adjacent to elevator shaft",
                    ),
                    ideal_uses=(
                        "Specialty clinic or independently leased 2nd-floor practice",
                        "Physical/occupational therapy & rehabilitation gym",
                        "Clinical simulation & skills laboratory",
                    ),
                ),
                SpaceZone(
                    id="l2-conference-training",
                    name="Clear-Span Conference, Didactic & Staff Lounge Core",
                    floor_level=2,
                    category="Conference & Education",
                    room_count_label="576 SF Hall (#222) + Lounge + 2 Kitchens",
                    plumbing_equipped=True,
                    highlights=(
                        "Suite #222 offers a 24 x 24 ft (576 sq ft) clear-span lecture, boardroom, or group therapy hall",
                        "Expansive 2nd-floor Breakroom / Staff Lounge with natural window light and kitchen cabinetry",
                        "Supports CME seminars, multi-provider case conferences, and cohort instruction",
                    ),
                    ideal_uses=(
                        "Continuing medical education (CME) & training cohorts",
                        "Group behavioral therapy or cardiac/pulmonary rehab",
                        "Physician lounge & staff wellness suite",
                    ),
                ),
                SpaceZone(
                    id="l2-executive-behavioral",
                    name="Executive, Behavioral Health & Administrative Wing",
                    floor_level=2,
                    category="Executive & Counseling",
                    room_count_label="16+ Private Perimeter Offices",
                    plumbing_equipped=False,
                    highlights=(
                        "Quiet perimeter wing with 16+ private windowed offices and central storage",
                        "Acoustically separated from ground-floor acute clinical traffic",
                        "Direct stairwell and central elevator connectivity",
                    ),
                    ideal_uses=(
                        "Outpatient behavioral health, psychiatry & counseling suites",
                        "Healthcare administration, billing & telehealth hub",
                        "Multi-disciplinary medical group headquarters",
                    ),
                ),
            ),
            provenance=Provenance(
                source_document=SOURCE_PDF,
                source_pages=(10, 16, 20, 21, 22),
                derivation_note="Derived from 2nd Floor architectural plan (p. 16), Breakroom slide (p. 10), and points 1, 3, 4, 8 (pp. 20-22).",
            ),
        ),
    )

    transformations = (
        TransformationPair(
            id="exterior-facade",
            title="Architectural Exterior & Street Presence",
            subtitle="207 Elk Ave S — Historic Brick Character Meets Modern Medical Identity",
            category="Exterior",
            before_label="Current Clinical Exterior",
            before_image="assets/images/exterior-original.jpg",
            after_label="Renovated Architectural Concept",
            after_image="assets/images/exterior-renovated.jpg",
            alt_image="assets/images/aerial-front-facade.jpg",
            alt_label="Aerial Campus Perspective",
            description=(
                "Positioned one block off Fayetteville's historic Town Square, the building combines "
                "classic two-story masonry architecture with a single-story clinical wing, storefront glass, "
                "and immediate curbside and off-street patient parking."
            ),
            clinical_value=(
                "High-visibility corner presence at Elk Ave S & Campbell St E with custom tenant signage "
                "opportunities and zero structural demolition required."
            ),
            provenance=Provenance(SOURCE_PDF, (4, 5, 11, 17), "Pages 4 & 5 Original vs Renovated exterior."),
        ),
        TransformationPair(
            id="waiting-lounge",
            title="Primary Patient Waiting Lounge",
            subtitle="High-Capacity Patient Seating with Warm Acoustic Finishes",
            category="Waiting Lounge",
            before_label="Existing Waiting Room",
            before_image="assets/images/waiting-room-original.jpg",
            after_label="Modernized Lounge Concept",
            after_image="assets/images/waiting-room-renovated.jpg",
            alt_image="assets/images/practice-intake-business-office.jpg",
            alt_label="Secondary / Pediatric Waiting Room",
            description=(
                "Supported by decorative architectural columns and generous ceiling heights, the primary "
                "waiting room accommodates large patient volumes while a separate secondary waiting room "
                "allows dedicated pediatric, urgent care, or specialty cohort separation."
            ),
            clinical_value=(
                "Dual waiting areas (Waiting 1 & Waiting 2) prevent cross-traffic between sick visits, "
                "elective procedures, and specialty consultations."
            ),
            provenance=Provenance(SOURCE_PDF, (7, 13, 14, 21), "Page 7 Waiting Room Original vs Renovated & Page 21 Point 5."),
        ),
        TransformationPair(
            id="exam-procedure-suite",
            title="Private Exam & Specialty Procedure Suites",
            subtitle="35+ Plumbed Clinical Rooms Ready for Immediate Finish Customization",
            category="Exam & Procedure",
            before_label="Existing Plumbed Exam Room",
            before_image="assets/images/exam-room-original.jpg",
            after_label="Renovated Clinical Suite",
            after_image="assets/images/exam-room-renovated.jpg",
            alt_image="assets/images/exam-room-procedure-derm.jpg",
            alt_label="Specialty Derm / Procedure Setup",
            description=(
                "Every exam and procedure room features intact partition walls, solid-core doors, "
                "wet-wall plumbing with sinks, and medical-grade electrical distribution—upgradable "
                "with luxury vinyl plank flooring and custom millwork in days rather than months."
            ),
            clinical_value=(
                "Subfloor plumbing access and vertical wet walls allow rapid connection of dental chairs, "
                "surgical lighting, lasers, and vacuum drainage with zero concrete slab trenching."
            ),
            provenance=Provenance(SOURCE_PDF, (8, 20, 21, 22), "Page 8 Exam Room Original, Renovated & Derm Exam Room."),
        ),
        TransformationPair(
            id="nurses-station",
            title="Centralized Nurse Workstations & Triage Hubs",
            subtitle="4 Ground-Floor Stations Engineered for Care Team Efficiency",
            category="Clinical Core",
            before_label="Existing Nurse Station",
            before_image="assets/images/nurses-station-original.jpg",
            after_label="Renovated Triage & Charting Hub",
            after_image="assets/images/nurses-station-renovated.jpg",
            alt_image="assets/images/practice-clinical-corridor-station.jpg",
            alt_label="Corridor Care Team Station",
            description=(
                "Wrap-around counters, overhead cabinetry, natural daylight windows, and multi-terminal "
                "data/power drops position clinical support staff at the heart of each exam pod."
            ),
            clinical_value=(
                "Minimizes clinician footsteps per patient encounter and supports team-based care coordination."
            ),
            provenance=Provenance(SOURCE_PDF, (9, 13, 20), "Page 9 Nurses Station Original vs Renovated."),
        ),
        TransformationPair(
            id="upper-breakroom-conference",
            title="2nd Floor Conference, Lounge & Didactic Suite",
            subtitle="Clear-Span Collaboration Space for Providers, Staff & Training Cohorts",
            category="Executive & Education",
            before_label="Existing 2nd Floor Space",
            before_image="assets/images/breakroom-2nd-floor-original.jpg",
            after_label="Renovated Conference & Lounge",
            after_image="assets/images/breakroom-2nd-floor-renovated.jpg",
            alt_image="assets/images/practice-multipurpose-room.jpg",
            alt_label="Additional Multi-Purpose Training Room",
            description=(
                "Generous clear-span dimensions and perimeter windows on the second floor create "
                "an inviting setting for staff dining, provider board meetings, telehealth operations, "
                "or 20+ person clinical instruction cohorts."
            ),
            clinical_value=(
                "Supports staff retention, multi-disciplinary case reviews, and academic/clinical training "
                "programs under the same roof."
            ),
            provenance=Provenance(SOURCE_PDF, (10, 12, 21), "Page 10 2nd Floor Breakroom Original vs Renovated & Page 21 Point 4."),
        ),
    )

    archetypes = (
        TenantArchetype(
            id="multi-specialty-outpatient",
            specialty="Primary Care & Multi-Specialty Medical Group",
            icon_name="stethoscope",
            headline="Turnkey High-Volume Outpatient Clinic with Proven Community Heritage",
            recommended_configuration="Ground Floor (Full Wing) or Full 2-Story Campus",
            target_rooms=24,
            why_it_fits=(
                "Known throughout Lincoln County as a trusted primary care destination (formerly HH Lincoln Health Primary Care), offering immediate patient recognition.",
                "24+ ground-floor exam rooms, 7 procedure rooms, and 4 nurse stations allow 6 to 10+ providers to run concurrent schedules without bottlenecks.",
                "Minutes from Lincoln Medical Center for seamless hospitalist, imaging, and specialist referrals.",
            ),
            infrastructure_match=(
                "Dual waiting rooms (Main + Pediatric/Sub-Waiting)",
                "On-site X-Ray suite, Reading Room, EKG, Blood Draw & Lab",
                "Dedicated 0.5-acre parking lot across the street + curbside ADA spaces",
            ),
            provenance=Provenance(SOURCE_PDF, (4, 16, 20, 25, 26), "Generalized from clinical density and healthcare heritage points."),
        ),
        TenantArchetype(
            id="urgent-care-diagnostics",
            specialty="Urgent Care, Orthopedic Walk-In & Occupational Medicine",
            icon_name="activity",
            headline="Rapid Patient Triage with On-Site X-Ray, Procedure Suites & 7 Exterior Doors",
            recommended_configuration="Ground Floor (Full or Phased Wing)",
            target_rooms=16,
            why_it_fits=(
                "Built-in X-Ray room with adjacent Reading Room and Dressing Room eliminates expensive radiology vault construction.",
                "7 dedicated procedure rooms support laceration repair, splinting/casting, IV hydration, and occupational drug testing.",
                "7 ground-floor entry/exit doors allow dedicated ambulance/stretcher transfer or contagious-symptom isolation pathways.",
            ),
            infrastructure_match=(
                "Dedicated X-Ray, Phlebotomy Blood Draw & Clinical Lab",
                "7 procedure suites + 4 centralized nurse triage stations",
                "Direct access off Elk Ave S in downtown Fayetteville",
            ),
            provenance=Provenance(SOURCE_PDF, (16, 20, 21, 22), "Derived from 1st floor plan diagnostics & egress specs."),
        ),
        TenantArchetype(
            id="dental-oral-health",
            specialty="Dental Group, Oral Surgery & Hygiene Clinic",
            icon_name="smile",
            headline="Subfloor Plumbing Access for Zero-Trenching Operatory Installation",
            recommended_configuration="Ground Floor, Upper Floor, or Multi-Level Clinic",
            target_rooms=18,
            why_it_fits=(
                "Direct subfloor access and stacked vertical wet walls allow dental chair water lines, treated utilities, and vacuum drainage to connect rapidly without concrete slab trenching.",
                "Dual waiting rooms and separate intake/check-out windows keep high-turnover hygiene patients separated from surgical consultations.",
                "Built-in sterilization/lab suites on both floors (#235 on Level 2 plus Ground Floor Lab) streamline instrument processing.",
            ),
            infrastructure_match=(
                "Subfloor utility access + 35+ plumbed rooms across both levels",
                "Sterilization & laboratory cabinetry already installed",
                "High-capacity 0.5-acre parking lot for patient and staff vehicles",
            ),
            provenance=Provenance(SOURCE_PDF, (19, 20, 21, 26), "Generalized from dental hygiene & subfloor plumbing points 2, 3, 5, 6."),
        ),
        TenantArchetype(
            id="dermatology-aesthetics",
            specialty="Dermatology, Mohs Surgery, Aesthetics & MedSpa",
            icon_name="sparkles",
            headline="Elevated Hospitality Arrival Paired with Dedicated Procedure & Laser Suites",
            recommended_configuration="Ground Floor or Custom Phased Suite",
            target_rooms=14,
            why_it_fits=(
                "7 specialized ground-floor procedure rooms accommodate surgical excisions, Mohs micrographic labs, and energy/laser devices.",
                "Front lobby and waiting lounge easily accommodate an upscale patient arrival desk and dedicated clinical consultation suites.",
                "Walkable historic downtown square location attracts affluent regional patients across the Huntsville–Fayetteville corridor.",
            ),
            infrastructure_match=(
                "Procedure suites with medical-grade electrical & wet walls",
                "Dedicated patient arrival reception with separate private check-out",
                "24+ exam rooms for simultaneous medical and cosmetic tracks",
            ),
            provenance=Provenance(SOURCE_PDF, (5, 6, 7, 8, 20, 24, 25), "Derived from Derm Exam Room rendering (p. 8) and Wellness Cafe concepts (pp. 5-7)."),
        ),
        TenantArchetype(
            id="rehab-physical-therapy",
            specialty="Physical, Occupational & Pediatric Rehabilitation",
            icon_name="heart-pulse",
            headline="Accessible Multi-Suite Layout for Adult Mobility & Pediatric Developmental Therapy",
            recommended_configuration="Ground Floor Wing or Upper Level Clinical Suite",
            target_rooms=12,
            why_it_fits=(
                "Complete ADA compliance with 12 restrooms, zero-step ground entries, wide clinical corridors, and a central commercial passenger elevator.",
                "576 sq ft clear-span room (#222) plus multi-purpose rooms support open therapeutic exercise, balance training, and ADL simulation.",
                "Private plumbed exam rooms accommodate 1-on-1 manual therapy, speech/swallow therapy, and pediatric sensory fieldwork.",
            ),
            infrastructure_match=(
                "Central stainless elevator + 7 ground-level access doors",
                "576 sq ft clear-span suite + private treatment rooms",
                "Dedicated Pediatric Waiting Room with built-in aquarium window",
            ),
            provenance=Provenance(SOURCE_PDF, (13, 14, 16, 21, 22, 27), "Generalized from ADA, clear-span, and occupational therapy points 4, 8, 9, 22."),
        ),
        TenantArchetype(
            id="behavioral-health",
            specialty="Behavioral Health, Psychiatry & Counseling Center",
            icon_name="brain",
            headline="Private Consultation Offices, Group Therapy Halls & Discreet Patient Flow",
            recommended_configuration="Upper Level (2nd Floor) or Integrated Multi-Floor Suite",
            target_rooms=16,
            why_it_fits=(
                "Second floor provides 16+ private windowed consultation offices plus 11 clinical rooms for medication management and psychiatric evaluations.",
                "Two large conference/group rooms on Level 2 support intensive outpatient programs (IOP), family counseling, and clinical supervision.",
                "Multiple exterior doors and dual waiting areas enable discreet patient arrival and departure.",
            ),
            infrastructure_match=(
                "16+ private perimeter offices + 11 upper clinical rooms",
                "2 group therapy / conference halls + 2 staff kitchens",
                "Dedicated exterior egress doors for private patient circulation",
            ),
            provenance=Provenance(SOURCE_PDF, (16, 20, 21, 23, 27), "Generalized from 2nd floor plan and behavioral health vision point 23."),
        ),
        TenantArchetype(
            id="academic-health-sciences",
            specialty="Healthcare Workforce Training, Nursing & Allied Health Campus",
            icon_name="graduation-cap",
            headline="Turnkey Didactic Classroom, Skills Labs & Public Student Clinic Infrastructure",
            recommended_configuration="Upper Level, Ground Level, or Phased Multi-Floor Campus",
            target_rooms=35,
            why_it_fits=(
                "Upper suite #222 offers a 24 x 24 ft (576 sq ft) clear-span lecture hall alongside built-in lab #235 and 11 sink-equipped simulation rooms.",
                "Ground-floor reception, dual waiting rooms, and 24+ exam rooms enable public-facing community clinics without mixing patient traffic with instructional zones.",
                "Post-secondary instruction and outpatient clinical training utilize existing multi-room clinical pods and clear-span didactic halls without major structural reconfigurations.",
            ),
            infrastructure_match=(
                "576 sq ft clear-span classroom + built-in laboratory (#235)",
                "Turnkey clinical infrastructure for post-secondary medical & nursing training",
                "0.5-acre dedicated parking lot for commuter cohorts, faculty & patients",
            ),
            provenance=Provenance(SOURCE_PDF, (18, 19, 20, 21, 22, 23, 24, 26), "Derived from points 1-12 and 19-23."),
        ),
    )

    pillars = (
        AdvantagePillar(
            id="turnkey-clinical",
            title="Turnkey Clinical Infrastructure & Speed to Market",
            subtitle="Bypass Protracted Redesign Cycles & Open on Schedule",
            summary=(
                "Intact clinical partition walls, solid-core doors, medical-grade electrical layouts, "
                "wet-wall plumbing in 35+ rooms, and dual waiting suites eliminate 12 to 18 months of "
                "architectural reconstruction."
            ),
            points=(
                AdvantagePoint(
                    number=1,
                    title="Multi-Level Selection Flexibility",
                    description="Total footprint flexibility to lease the ground floor, upper level, or a phased multi-floor campus tailored to exact square footage and clinical program needs.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (20,), "Point 1 generalized for all medical tenants."),
                ),
                AdvantagePoint(
                    number=2,
                    title="Turnkey Ground-Floor Clinical Density",
                    description="24+ private ground-floor exam rooms, 7 specialized procedure rooms, X-ray & diagnostic suites, multiple labs, and 4 central nurse stations—all with functional wet walls and sinks.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (16, 20), "Point 2 & 1st Floor Plan."),
                ),
                AdvantagePoint(
                    number=3,
                    title="Turnkey Upper-Floor Clinical, Lab & Executive Layout",
                    description="11 sink-equipped second-floor clinical rooms, a built-in laboratory with cabinetry (#235), 16+ private perimeter offices, and 4 dedicated restrooms.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (16, 20), "Point 3 & 2nd Floor Plan."),
                ),
                AdvantagePoint(
                    number=4,
                    title="Dedicated Clear-Span Conference & Training Space",
                    description="Upper suite #222 provides a 24 x 24 ft (576 sq ft) clear-span hall—plus a secondary conference/break lounge—ideal for provider meetings, patient education, rehab, or 20+ person training cohorts.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (10, 16, 21), "Point 4 generalized."),
                ),
                AdvantagePoint(
                    number=5,
                    title="Turnkey Patient Reception & Dual Waiting Suites",
                    description="Fully built-out front-of-house featuring a main lobby, dual waiting rooms (Main Waiting & Pediatric/Specialty Sub-Waiting), dedicated check-in/out reception, two intake offices, and a high-density file room.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (16, 21), "Point 5 generalized."),
                ),
                AdvantagePoint(
                    number=6,
                    title="Subfloor Plumbing & Utility Efficiency",
                    description="Direct subfloor access and stacked vertical wet walls allow dental chairs, surgical sinks, treated water lines, and vacuum drainage to be connected rapidly with zero concrete slab trenching.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (21,), "Point 6."),
                ),
                AdvantagePoint(
                    number=7,
                    title="Accelerated Speed to Market",
                    description="Intact clinical partitions, solid-core doors, drop ceilings, medical electrical distribution, and extensive plumbing allow tenants to bypass protracted construction cycles and launch on schedule.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (22,), "Point 7 generalized."),
                ),
                AdvantagePoint(
                    number=8,
                    title="Comprehensive Restroom & ADA Elevator Infrastructure",
                    description="12 total restrooms across both floors (8 on Ground, 4 on Upper Level) paired with central passenger elevator access ensure full ADA compliance and fixture capacity for patients and staff.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (14, 22), "Point 8."),
                ),
                AdvantagePoint(
                    number=9,
                    title="Seamless 7-Door Egress & Circulation",
                    description="The ground floor features 7 exterior entry/exit doors alongside 3 interior stairwells, enabling dedicated staff entries, contagious-patient isolation, and compliant emergency egress.",
                    pillar_id="turnkey-clinical",
                    provenance=Provenance(SOURCE_PDF, (16, 22), "Point 9."),
                ),
            ),
        ),
        AdvantagePillar(
            id="parking-location",
            title="Unmatched Parking, Downtown Walkability & Regional Reach",
            subtitle="Dedicated 0.5-Acre Parking Lot + Huntsville Growth Corridor Position",
            summary=(
                "Rare downtown medical campus combining immediate walkability to Fayetteville's historic "
                "Town Square with a dedicated half-acre private parking parcel directly across Elk Ave S."
            ),
            points=(
                AdvantagePoint(
                    number=10,
                    title="Immediate Proximity to Historic Downtown Square",
                    description="Situated as the premier commercial medical building directly behind Fayetteville's historic downtown square, offering providers, staff, and patients walkable access to dining, pharmacies, and civic amenities.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (3, 11, 24), "Point 13."),
                ),
                AdvantagePoint(
                    number=11,
                    title="Dedicated 0.5-Acre Private Parking Lot Across the Street",
                    description="In addition to curbside and on-site ADA building parking (Tract 1: 0.39 AC), ownership provides a dedicated 0.45-acre (~0.5 AC) paved parking parcel directly across Elk Ave S (Tract 2), eliminating parking constraints.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (11, 15, 24), "Point 14 & Page 15 Survey."),
                ),
                AdvantagePoint(
                    number=12,
                    title="Geographic Core for the 3-County Catchment Area",
                    description="Centrally situated in Lincoln County along the US-64 / US-231 / US-431 crossroads to draw patients and clinical staff seamlessly across Lincoln, Moore, Giles, Franklin, Coffee, and Bedford counties.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (24,), "Point 15 generalized."),
                ),
                AdvantagePoint(
                    number=13,
                    title="Proximity to HH Lincoln Medical Center",
                    description="Located minutes from Lincoln Medical Center (Huntsville Hospital Health System), facilitating seamless physician hospital privileges, diagnostic coordination, and regional referral networks.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (25,), "Point 17 generalized."),
                ),
                AdvantagePoint(
                    number=14,
                    title="Positioned in the High-Growth Huntsville / Rocket City Corridor",
                    description="Located directly north of the booming Huntsville, AL metro corridor, capturing rapid cross-border residential growth and accelerating demand for accessible outpatient specialty care.",
                    pillar_id="parking-location",
                    provenance=Provenance(SOURCE_PDF, (18, 25), "Point 18 & Executive Summary."),
                ),
            ),
        ),
        AdvantagePillar(
            id="partnership-vision",
            title="Healthcare Heritage, Incentives & Long-Term Ownership Partnership",
            subtitle="Flexible Lease Structures Backed by a Healthcare-Aligned Ownership Team",
            summary=(
                "Formerly home to HH Lincoln Health Primary Care, 207 Elk Ave S carries decades of "
                "patient trust and is backed by an ownership team committed to long-term tenant success."
            ),
            points=(
                AdvantagePoint(
                    number=15,
                    title="Proven Community Healthcare Heritage",
                    description="Recognized throughout Southern Middle Tennessee as a trusted multi-provider medical facility, providing new tenants with immediate local awareness, patient comfort, and organic clinic volume.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (4, 12, 13, 14, 26), "Point 19 generalized."),
                ),
                AdvantagePoint(
                    number=16,
                    title="Multi-Specialty & Interprofessional Campus Synergy",
                    description="Substantial clinical capacity across two floors allows a single anchor health system or complementary co-tenants (primary care, dental, rehab, behavioral health, diagnostics) to cross-refer on site.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (26, 27), "Points 20-23 generalized."),
                ),
                AdvantagePoint(
                    number=17,
                    title="Incentive & Grant Navigation Support",
                    description="Ownership provides hands-on financial and development expertise to help tenants navigate downtown revitalization programs, Main Street incentives, and rural healthcare infrastructure grants.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (28,), "Point 24 generalized."),
                ),
                AdvantagePoint(
                    number=18,
                    title="Flexible Expansion Horizon & Custom Lease Frameworks",
                    description="Cooperative long-term institutional and private practice lease structures with expansion rights across two floors and adjacent parcels—supported by an ownership team rooted in finance, medicine, and engineering.",
                    pillar_id="partnership-vision",
                    provenance=Provenance(SOURCE_PDF, (18, 28, 29), "Points 25-28 generalized."),
                ),
            ),
        ),
    )

    gallery = (
        GalleryAsset(
            id="gal-ext-renovated",
            title="Renovated Exterior Architectural Rendering",
            caption="Modernized brick & dark architectural bronze facade concept along Elk Ave S.",
            category="Exterior & Aerial",
            image_path="assets/images/exterior-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (5, 17), "Page 5 Renovated Exterior."),
        ),
        GalleryAsset(
            id="gal-ext-original",
            title="Current Street-Level Exterior (207 Elk Ave S)",
            caption="Existing two-story brick & clinical wing facade with curbside and side-lot ADA parking.",
            category="Exterior & Aerial",
            image_path="assets/images/exterior-original.jpg",
            provenance=Provenance(SOURCE_PDF, (4,), "Page 4 Original Exterior."),
        ),
        GalleryAsset(
            id="gal-aerial-front",
            title="Drone View — Elk Ave S Frontage & ADA Parking",
            caption="Oblique aerial showing main entrance, side ADA parking lot, and covered drive-under bay.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-front-facade.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 1."),
        ),
        GalleryAsset(
            id="gal-aerial-campus",
            title="Drone View — Full Medical Building Footprint",
            caption="Overview of the two-story brick core and single-story clinical exam wing.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-campus-oblique.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 2."),
        ),
        GalleryAsset(
            id="gal-aerial-parking-pin",
            title="Dedicated 0.5-Acre Parking Parcel Across Elk Ave S",
            caption="Private off-street parking lot (Tract 2: 0.45 AC) directly across the street for patients and staff.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-parking-parcel-pin.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 3."),
        ),
        GalleryAsset(
            id="gal-aerial-building-boundary",
            title="Tract 1 Building Parcel Boundary (0.39 Acres)",
            caption="Overhead boundary view of the medical building and on-site parking apron.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-building-boundary.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 5."),
        ),
        GalleryAsset(
            id="gal-aerial-parking-boundary",
            title="Tract 2 Dedicated Parking Lot Boundary (0.45 Acres)",
            caption="Overhead boundary view of the dedicated parking parcel directly across Elk Ave S.",
            category="Exterior & Aerial",
            image_path="assets/images/aerial-parking-lot-boundary.jpg",
            provenance=Provenance(SOURCE_PDF, (11,), "Page 11 Aerial View 6."),
        ),
        GalleryAsset(
            id="gal-exam-renovated",
            title="Renovated Private Exam Suite Concept",
            caption="Plumbed clinical exam room with wood-tone flooring, custom cabinetry, and wet-wall sink.",
            category="Clinical Interiors",
            image_path="assets/images/exam-room-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (8,), "Page 8 Exam Room Renovated."),
        ),
        GalleryAsset(
            id="gal-exam-derm",
            title="Specialty Procedure & Dermatology Suite (Renovation Concept)",
            caption="Conceptual renovation rendering showing procedure room configuration with surgical lighting, power exam chair, and laser/device cart (not actual existing condition).",
            category="Clinical Interiors",
            image_path="assets/images/exam-room-procedure-derm.jpg",
            provenance=Provenance(SOURCE_PDF, (8,), "Page 8 Derm Exam Room."),
        ),
        GalleryAsset(
            id="gal-nurses-renovated",
            title="Renovated Central Nurse Workstation",
            caption="Modernized care-team triage and charting station with natural window daylight.",
            category="Clinical Interiors",
            image_path="assets/images/nurses-station-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (9,), "Page 9 Nurses Station Renovated."),
        ),
        GalleryAsset(
            id="gal-elevator",
            title="Central Commercial Stainless Elevator Lobby",
            caption="Full ADA passenger elevator connecting Ground Level and 2nd Floor clinical wings.",
            category="Clinical Interiors",
            image_path="assets/images/practice-central-elevator.jpg",
            provenance=Provenance(SOURCE_PDF, (14,), "Page 14 Elevator Lobby."),
        ),
        GalleryAsset(
            id="gal-waiting-renovated",
            title="Hospitality-Inspired Patient Waiting Lounge",
            caption="Warm biophilic waiting room concept with wood flooring and comfortable seating.",
            category="Lobby & Waiting",
            image_path="assets/images/waiting-room-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (7,), "Page 7 Waiting Room Renovated."),
        ),
        GalleryAsset(
            id="gal-main-waiting",
            title="Existing Primary Waiting Room & Brick Archway",
            caption="Spacious ground-floor waiting lounge with direct sightlines to reception and sub-waiting.",
            category="Lobby & Waiting",
            image_path="assets/images/practice-main-waiting-archway.jpg",
            provenance=Provenance(SOURCE_PDF, (14,), "Page 14 Main Waiting Room."),
        ),
        GalleryAsset(
            id="gal-peds-waiting",
            title="Dedicated Pediatric / Specialty Sub-Waiting Room",
            caption="Secondary waiting lounge with built-in aquarium window for cohort separation.",
            category="Lobby & Waiting",
            image_path="assets/images/practice-intake-business-office.jpg",
            provenance=Provenance(SOURCE_PDF, (13,), "Page 13 Pediatric Waiting Room."),
        ),
        GalleryAsset(
            id="gal-breakroom-renovated",
            title="2nd Floor Executive Conference & Staff Lounge Concept",
            caption="Clear-span 2nd floor lounge with full cabinetry, conference table, and presentation screen.",
            category="Executive & Education",
            image_path="assets/images/breakroom-2nd-floor-renovated.jpg",
            provenance=Provenance(SOURCE_PDF, (10,), "Page 10 2nd Floor Breakroom Renovated."),
        ),
        GalleryAsset(
            id="gal-admin-office",
            title="Business & Intake Office Suite",
            caption="Multi-workstation administrative and patient billing office with pass-through window.",
            category="Executive & Education",
            image_path="assets/images/practice-pediatric-waiting.jpg",
            provenance=Provenance(SOURCE_PDF, (13,), "Page 13 Intake/Business Office."),
        ),
        GalleryAsset(
            id="gal-town-square",
            title="Historic Downtown Fayetteville Town Square (1 Block Away)",
            caption="Walkable historic courthouse square immediately adjacent to 207 Elk Ave S.",
            category="Downtown & Community",
            image_path="assets/images/downtown-town-square-aerial.jpg",
            provenance=Provenance(SOURCE_PDF, (3,), "Page 3 Town Square."),
        ),
        GalleryAsset(
            id="gal-main-ave",
            title="Downtown Fayetteville Main Avenue Streetscape",
            caption="Vibrant local dining, retail, and historic architecture steps from the medical campus.",
            category="Downtown & Community",
            image_path="assets/images/downtown-main-ave.jpg",
            provenance=Provenance(SOURCE_PDF, (3,), "Page 3 Main Ave."),
        ),
        GalleryAsset(
            id="gal-survey-tracts",
            title="Boundary Survey — Tract 1 (0.39 AC) & Tract 2 (0.45 AC)",
            caption="Certified boundary survey showing the building parcel and dedicated parking lot across Elk Ave S.",
            category="Floorplans & Surveys",
            image_path="assets/images/survey-two-tracts.png",
            provenance=Provenance(SOURCE_PDF, (15,), "Page 15 2-Tract Survey."),
        ),
    )

    return PropertyListing(
        property_id="207-elk-ave-s",
        headline="Turnkey Medical & Executive Office Campus in Historic Downtown Fayetteville",
        subheadline=(
            "35+ plumbed clinical & exam suites, 7 procedure rooms, on-site X-ray & lab infrastructure, "
            "and a dedicated 0.5-acre parking lot—engineered for immediate outpatient, specialty, "
            "dental, and healthcare clinical operations."
        ),
        street_address="207 Elk Ave S",
        campus_alias="201–207 Elk Ave S Medical Campus",
        city="Fayetteville",
        state="TN",
        postal_code="37334",
        county="Lincoln County",
        occupancy_classification="Outpatient Medical & Executive Office",
        building_lot_acres=0.39,
        parking_lot_acres=0.45,
        total_campus_acres=0.84,
        executive_summary=(
            "Securing turnkey clinical space in Southern Middle Tennessee and the North Huntsville growth "
            "corridor—without incurring $150 to $250+ per square foot in speculative shell build-out costs "
            "or 18-month architectural delays—is one of the greatest challenges facing expanding medical groups.",
            "207 Elk Ave S (formerly HH Lincoln Health Primary Care) delivers an immediate, capital-efficient, "
            "and spatially versatile home for primary care, multi-specialty outpatient clinics, urgent care, "
            "dental & oral surgery, dermatology, physical/occupational rehabilitation, behavioral health, and "
            "health sciences training cohorts.",
            "Backed by 35+ sink-equipped clinical rooms across two elevator-served floors, 7 procedure suites, "
            "on-site X-ray and laboratory rooms, 12 ADA restrooms, and a dedicated half-acre private parking lot "
            "directly across the street, 207 Elk Ave S provides unmatched speed to market and long-term operational stability.",
        ),
        metrics=metrics,
        floors=floors,
        transformations=transformations,
        archetypes=archetypes,
        pillars=pillars,
        gallery=gallery,
        contact=contact,
        metadata={
            "corridor": "Huntsville / Rocket City North Growth Corridor (US-231 / US-64 / US-431)",
            "nearby_hospital": "HH Lincoln Medical Center (Minutes Away)",
            "catchment_counties": ["Lincoln", "Moore", "Giles", "Franklin", "Coffee", "Bedford", "Madison (AL)"],
            "lease_structures": [
                "Ground Floor Clinical Wing",
                "Upper Level Specialty / Executive / Didactic Wing",
                "Phased Multi-Floor Custom Suite",
                "Full-Building Single-Tenant Medical Campus",
            ],
        },
    )
