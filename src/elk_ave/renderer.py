"""Static site renderer and asset verifier for 207 Elk Ave S."""

from __future__ import annotations

import html
import json
import shutil
from pathlib import Path
from typing import Any

from src.elk_ave.catalog import build_property_listing
from src.elk_ave.models import PropertyListing

STATIC_SOURCE_DIR = Path(__file__).resolve().parent / "static"


class AssetVerificationError(FileNotFoundError):
    """Raised when a required image or static asset is missing on disk."""


def _esc(val: Any) -> str:
    """HTML-escape any value safely."""
    return html.escape(str(val), quote=True)


def build_json_ld(listing: PropertyListing) -> dict[str, Any]:
    """Build Schema.org JSON-LD metadata for medical commercial real estate."""
    return {
        "@context": "https://schema.org",
        "@type": "RealEstateListing",
        "name": f"{listing.street_address} — {listing.headline}",
        "description": listing.subheadline,
        "address": {
            "@type": "PostalAddress",
            "streetAddress": listing.street_address,
            "addressLocality": listing.city,
            "addressRegion": listing.state,
            "postalCode": listing.postal_code,
            "addressCountry": "US",
        },
        "additionalProperty": [
            {"@type": "PropertyValue", "name": "Plumbed Clinical & Exam Rooms", "value": "35+"},
            {"@type": "PropertyValue", "name": "Dedicated Procedure Suites", "value": "7"},
            {"@type": "PropertyValue", "name": "Restrooms", "value": "12"},
            {"@type": "PropertyValue", "name": "IBC Occupancy", "value": listing.occupancy_classification},
            {"@type": "PropertyValue", "name": "Dedicated Parking Lot Acres", "value": str(listing.parking_lot_acres)},
        ],
        "seller": {
            "@type": "Person",
            "name": listing.contact.name,
            "jobTitle": f"{listing.contact.role}, {listing.contact.entity}",
            "telephone": listing.contact.phone_display,
            "email": listing.contact.email,
        },
    }


def render_index_html(listing: PropertyListing) -> str:
    """Render the complete semantic HTML5 document for 207 Elk Ave S."""
    json_ld_str = json.dumps(build_json_ld(listing), indent=2)
    embedded_data_str = json.dumps(listing.to_dict())

    # Metric Bento Cards
    metrics_html = "\n".join(
        f"""
        <article class="metric-card">
          <div>
            <div class="metric-category">{_esc(m.category)}</div>
            <div class="metric-value">{_esc(m.value)}</div>
            <h3 class="metric-label">{_esc(m.unit_or_label)}</h3>
          </div>
          <p class="metric-detail">{_esc(m.detail)}</p>
        </article>
        """
        for m in listing.metrics
    )

    # Archetype Pills & Default Active Stage
    first_arch = listing.archetypes[0]
    archetype_pills_html = "\n".join(
        f"""<button type="button" class="archetype-pill{' active' if idx == 0 else ''}" data-archetype-id="{_esc(a.id)}">{_esc(a.specialty)}</button>"""
        for idx, a in enumerate(listing.archetypes)
    )
    first_arch_why = "\n".join(
        f"<li><span>{_esc(pt)}</span></li>" for pt in first_arch.why_it_fits
    )
    first_arch_infra = "\n".join(
        f'<span class="infra-tag">{_esc(tag)}</span>'
        for tag in first_arch.infrastructure_match
    )

    # Transformation Studio Tabs & Default Active Pair
    first_tr = listing.transformations[0]
    studio_tabs_html = "\n".join(
        f"""<button type="button" class="studio-tab{' active' if idx == 0 else ''}" data-transform-id="{_esc(t.id)}">{_esc(t.category)}: {_esc(t.title.split('&')[0].strip())}</button>"""
        for idx, t in enumerate(listing.transformations)
    )

    # Floor Explorer Default Level 1
    first_floor = listing.floors[0]
    floor_tabs_html = "\n".join(
        f"""<button type="button" class="floor-tab-btn{' active' if idx == 0 else ''}" data-floor-level="{f.level}">{_esc(f.name)}</button>"""
        for idx, f in enumerate(listing.floors)
    )
    first_floor_zones_html = "\n".join(
        f"""
        <article class="zone-card">
          <div class="zone-card-header">
            <h4 class="zone-title">{_esc(z.name)}</h4>
            <span class="zone-badge">{_esc(z.room_count_label)}</span>
          </div>
          <ul class="zone-highlights">
            {"".join(f"<li>{_esc(h)}</li>" for h in z.highlights)}
          </ul>
          <div class="infra-tags">
            {"".join(f'<span class="infra-tag">{_esc(u)}</span>' for u in z.ideal_uses)}
          </div>
        </article>
        """
        for z in first_floor.zones
    )

    # Calculator Specialty Options
    calc_options_html = "\n".join(
        f'<option value="{_esc(a.id)}">{_esc(a.specialty)}</option>'
        for a in listing.archetypes
    )

    # Strategic Pillars (21 Generalized Points)
    pillars_html = "\n".join(
        f"""
        <article class="pillar-card">
          <div class="pillar-subtitle">{_esc(p.subtitle)}</div>
          <h3 class="pillar-title">{_esc(p.title)}</h3>
          <p style="font-size: 0.92rem; color: var(--text-secondary);">{_esc(p.summary)}</p>
          <ul class="pillar-points">
            {"".join(
                f'''
                <li class="pillar-point">
                  <span class="point-num">{pt.number:02d}</span>
                  <div class="point-body">
                    <strong>{_esc(pt.title)}</strong>
                    <p>{_esc(pt.description)}</p>
                  </div>
                </li>
                '''
                for pt in p.points
            )}
          </ul>
        </article>
        """
        for p in listing.pillars
    )

    # Gallery Categories & Items
    gallery_categories = ["All"] + sorted({g.category for g in listing.gallery})
    gallery_filters_html = "\n".join(
        f"""<button type="button" class="archetype-pill{' active' if cat == 'All' else ''}" data-gallery-cat="{_esc(cat)}">{_esc(cat)}</button>"""
        for cat in gallery_categories
    )
    gallery_items_html = "\n".join(
        f"""
        <article class="gallery-item" data-gallery-item="{_esc(g.id)}" data-item-category="{_esc(g.category)}">
          <div class="gallery-thumb">
            <img src="{_esc(g.image_path)}" alt="{_esc(g.title)}" loading="lazy" />
          </div>
          <div class="gallery-meta">
            <div class="gallery-cat">{_esc(g.category)}</div>
            <h3 class="gallery-title">{_esc(g.title)}</h3>
            <p class="gallery-caption">{_esc(g.caption)}</p>
          </div>
        </article>
        """
        for g in listing.gallery
    )

    return f"""<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{_esc(listing.street_address)} ({_esc(listing.campus_alias)}) | Turnkey Medical &amp; Executive Space for Lease — Fayetteville, TN</title>
  <meta name="description" content="{_esc(listing.subheadline)}" />
  <meta property="og:title" content="{_esc(listing.street_address)} — Turnkey Medical &amp; Executive Campus for Lease" />
  <meta property="og:description" content="{_esc(listing.subheadline)}" />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="assets/images/exterior-renovated.jpg" />
  <link rel="stylesheet" href="styles.css" />
  <script type="application/ld+json">{json_ld_str}</script>
</head>
<body>
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- Sticky Glassmorphic Navigation -->
  <header class="site-header" role="banner">
    <div class="container header-inner">
      <a href="#top" class="brand" aria-label="207 Elk Ave S Home">
        <span class="brand-mark">207</span>
        <span class="brand-text">
          <span class="brand-name">207 Elk Ave S</span>
          <span class="brand-location">Fayetteville, TN · Medical Campus</span>
        </span>
      </a>

      <nav class="header-nav" aria-label="Primary Navigation">
        <ul class="nav-links">
          <li><a href="#overview">Overview</a></li>
          <li><a href="#specialties">Specialties</a></li>
          <li><a href="#transformations">Renovations</a></li>
          <li><a href="#floorplans">Floorplans</a></li>
          <li><a href="#calculator">TI Calculator</a></li>
          <li><a href="#advantages">Advantages</a></li>
          <li><a href="#location">Parking</a></li>
          <li><a href="#gallery">Gallery</a></li>
        </ul>
      </nav>

      <div class="header-actions">
        <button type="button" id="theme-toggle-btn" class="icon-btn" aria-label="Toggle color theme">🌙</button>
        <a href="#contact" class="btn btn--primary btn--sm">Schedule Tour</a>
      </div>
    </div>
  </header>

  <main id="main-content">
    <!-- Hero Section -->
    <section id="top" class="hero">
      <div class="container hero-grid">
        <div class="hero-copy">
          <div class="hero-badges">
            <span class="badge badge--dot">Available for Lease · Single-Floor or Full-Campus</span>
            <span class="badge">IBC Group B Medical</span>
            <span class="badge">Huntsville North Growth Corridor</span>
          </div>

          <h1 class="hero-title">
            Turnkey Clinical Scale at <span>207 Elk Ave S</span>.
          </h1>

          <p class="hero-lead">
            {_esc(listing.subheadline)} Formerly home to <strong>HH Lincoln Health Primary Care</strong>
            at the 201–207 Elk Ave S corner campus, one block off Fayetteville’s historic Town Square.
          </p>

          <div class="hero-cta-row">
            <a href="#floorplans" class="btn btn--primary">Explore Interactive Floorplans</a>
            <a href="#calculator" class="btn btn--secondary">Calculate TI Capital Savings</a>
          </div>

          <div class="hero-quick-facts">
            <div>
              <div class="quick-fact-val">35+ Rooms</div>
              <div class="quick-fact-lbl">Sink-equipped exam &amp; clinical suites across 2 levels</div>
            </div>
            <div>
              <div class="quick-fact-val">0.5 Acre</div>
              <div class="quick-fact-lbl">Dedicated private parking lot directly across Elk Ave S</div>
            </div>
            <div>
              <div class="quick-fact-val">$0 Trenching</div>
              <div class="quick-fact-lbl">Intact wet walls, subfloor access, X-ray &amp; lab rooms</div>
            </div>
          </div>
        </div>

        <div class="hero-showcase">
          <div class="hero-image-frame">
            <img
              id="hero-main-image"
              src="assets/images/exterior-renovated.jpg"
              alt="207 Elk Ave S Renovated Medical &amp; Executive Exterior Concept"
            />
          </div>
          <div class="hero-view-switcher">
            <div class="hero-view-caption">
              <strong id="hero-view-label">Renovated Architectural Concept</strong>
              <span id="hero-view-sub">Modernized brick &amp; dark architectural bronze facade along Elk Ave S</span>
            </div>
            <div class="segmented-control" role="group" aria-label="Exterior View Selector">
              <button type="button" class="segmented-btn active" data-hero-view="renovated">Renovated</button>
              <button type="button" class="segmented-btn" data-hero-view="original">Current</button>
              <button type="button" class="segmented-btn" data-hero-view="aerial">Aerial</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Executive Overview & Bento Metrics -->
    <section id="overview" class="section section--alt">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Executive Briefing · 201–207 Elk Ave S Campus</span>
          <h2 class="section-title">Immediate Clinical Readiness Without Cold-Shell Capital Outlay</h2>
          <p class="section-subtitle">
            {_esc(listing.executive_summary[0])} {_esc(listing.executive_summary[1])}
          </p>
        </div>

        <div class="bento-metrics">
          {metrics_html}
        </div>
      </div>
    </section>

    <!-- Interactive Specialty Fit Explorer -->
    <section id="specialties" class="section">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Multi-Discipline Adaptability</span>
          <h2 class="section-title">Engineered for Every Healthcare &amp; Clinical Specialty</h2>
          <p class="section-subtitle">
            Select your clinical discipline below to inspect how 207 Elk Ave S’s existing wet walls,
            procedure rooms, dual waiting lounges, and upper didactic/executive suites align with your practice.
          </p>
        </div>

        <div class="archetype-pills" role="tablist" aria-label="Medical Specialty Profiles">
          {archetype_pills_html}
        </div>

        <div class="archetype-stage" role="tabpanel">
          <div>
            <span class="eyebrow" id="arch-specialty">{_esc(first_arch.specialty)}</span>
            <h3 class="archetype-headline" id="arch-headline">{_esc(first_arch.headline)}</h3>
            <ul class="archetype-list" id="arch-why-list">
              {first_arch_why}
            </ul>
            <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 1.5rem;">
              <button type="button" id="arch-load-calc-btn" class="btn btn--primary">
                Load Profile into TI Capital Estimator →
              </button>
              <a href="#contact" class="btn btn--secondary">Request Custom Space Plan</a>
            </div>
          </div>

          <div class="archetype-meta-box">
            <div class="archetype-meta-row">
              <div class="archetype-meta-label">Recommended Footprint Selection</div>
              <div class="archetype-meta-val" id="arch-config">{_esc(first_arch.recommended_configuration)}</div>
            </div>
            <div class="archetype-meta-row">
              <div class="archetype-meta-label">Typical Clinical Suite Allocation</div>
              <div class="archetype-meta-val" id="arch-rooms">{first_arch.target_rooms} Plumbed Clinical / Exam Rooms</div>
            </div>
            <div>
              <div class="archetype-meta-label">Turnkey Infrastructure Match</div>
              <div class="infra-tags" id="arch-infra-tags">
                {first_arch_infra}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Before / After Transformation Studio -->
    <section id="transformations" class="section section--dark">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Architectural Transformation Studio</span>
          <h2 class="section-title">Compare Existing Clinical Infrastructure with Renovated Finish Concepts</h2>
          <p class="section-subtitle">
            Drag the interactive split-screen slider across all six property zones to see how cosmetic
            millwork, lighting, and flooring upgrades transform the intact clinical footprint.
          </p>
        </div>

        <div class="studio-tabs" role="tablist" aria-label="Transformation Spaces">
          {studio_tabs_html}
        </div>

        <div class="studio-layout">
          <div class="comparison-viewer">
            <span class="comparison-badge comparison-badge--before" id="studio-before-badge">
              {_esc(first_tr.before_label)}
            </span>
            <span class="comparison-badge comparison-badge--after" id="studio-after-badge">
              {_esc(first_tr.after_label)}
            </span>

            <div class="comparison-layer comparison-after">
              <img id="studio-after-img" src="{_esc(first_tr.after_image)}" alt="{_esc(first_tr.after_label)}" />
            </div>
            <div class="comparison-layer comparison-before" id="studio-before-layer">
              <img id="studio-before-img" src="{_esc(first_tr.before_image)}" alt="{_esc(first_tr.before_label)}" />
            </div>

            <div class="comparison-handle" id="studio-handle">
              <div class="comparison-knob">↔</div>
            </div>

            <input
              type="range"
              id="studio-range"
              class="comparison-range"
              min="0"
              max="100"
              value="50"
              aria-label="Before and after image comparison slider"
            />
          </div>

          <div class="studio-details">
            <div class="studio-subtitle" id="studio-subtitle">{_esc(first_tr.subtitle)}</div>
            <h3 class="studio-title" id="studio-title">{_esc(first_tr.title)}</h3>
            <p class="studio-desc" id="studio-desc">{_esc(first_tr.description)}</p>
            <div class="studio-clinical-box" id="studio-clinical">
              {_esc(first_tr.clinical_value)}
            </div>
            <div class="studio-preset-row">
              <button type="button" class="studio-tab" data-slider-pos="100">Show Existing (100%)</button>
              <button type="button" class="studio-tab" data-slider-pos="50">50/50 Split</button>
              <button type="button" class="studio-tab" data-slider-pos="0">Show Renovated (100%)</button>
              <button type="button" class="studio-tab" id="studio-alt-btn">View {_esc(first_tr.alt_label or 'Alternate')}</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Interactive Dual-Level Architectural Floorplan Explorer -->
    <section id="floorplans" class="section">
      <div class="container">
        <div class="floor-switcher-bar">
          <div>
            <span class="eyebrow">Architectural Schematics &amp; Suite Breakdown</span>
            <h2 class="section-title" style="margin-bottom: 0.25rem;">Interactive Dual-Level Floorplan Explorer</h2>
            <p class="section-subtitle">
              Lease the Ground Floor, the Upper Level, or combine both elevator-connected levels into a custom medical campus.
            </p>
          </div>
          <div class="floor-tabs" role="tablist" aria-label="Building Floor Selector">
            {floor_tabs_html}
          </div>
        </div>

        <div class="floor-explorer-grid">
          <div class="floorplan-card">
            <div class="floorplan-toolbar">
              <div>
                <strong id="floorplan-name" style="font-size: 1.1rem;">{_esc(first_floor.name)}</strong>
                <div id="floorplan-tagline" style="font-size: 0.82rem; color: #4b5c63;">{_esc(first_floor.tagline)}</div>
              </div>
              <button type="button" id="floorplan-zoom-btn" class="btn btn--secondary btn--sm" style="color:#11191c; background:#f3f7f6;">
                🔍 Fullscreen Schematic
              </button>
            </div>

            <div class="floorplan-canvas" id="floorplan-canvas-wrap" title="Click to enlarge architectural schematic">
              <img id="floorplan-img" src="{_esc(first_floor.floorplan_image)}" alt="{_esc(first_floor.name)} Floorplan" />
            </div>

            <p id="floorplan-summary" style="font-size: 0.88rem; color: #3f4f56; margin-top: 1rem;">
              {_esc(first_floor.summary)}
            </p>

            <div class="floor-stats-strip">
              <div>
                <div class="floor-stat-num" id="floor-stat-exam">{first_floor.exam_and_clinical_rooms}+</div>
                <div class="floor-stat-lbl">Plumbed Exam Rooms</div>
              </div>
              <div>
                <div class="floor-stat-num" id="floor-stat-proc">{first_floor.procedure_rooms}</div>
                <div class="floor-stat-lbl">Procedure Suites</div>
              </div>
              <div>
                <div class="floor-stat-num" id="floor-stat-rest">{first_floor.restrooms}</div>
                <div class="floor-stat-lbl">ADA Restrooms</div>
              </div>
              <div>
                <div class="floor-stat-num" id="floor-stat-doors">{first_floor.exterior_egress_doors}</div>
                <div class="floor-stat-lbl">Egress Doors</div>
              </div>
            </div>
          </div>

          <div class="zone-cards-stack" id="floor-zones-container">
            {first_floor_zones_html}
          </div>
        </div>
      </div>
    </section>

    <!-- Clinical Footprint & TI Capital Preservation Calculator -->
    <section id="calculator" class="section section--alt">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Capital Stewardship &amp; Speed-to-Market Model</span>
          <h2 class="section-title">Clinical Footprint &amp; TI Capital Preservation Estimator</h2>
          <p class="section-subtitle">
            Cold-shell medical construction in 2026 averages $215–$240+/SF due to concrete trenching,
            wet-wall plumbing, and ADA restroom cores. Configure your practice parameters to quantify your savings at 207 Elk Ave S.
          </p>
        </div>

        <div class="calculator-shell">
          <form id="clinical-calc-form" onsubmit="return false;">
            <div class="calc-form-group">
              <label class="calc-label" for="calc-specialty">1. Clinical Specialty Profile</label>
              <select id="calc-specialty" class="calc-select">
                {calc_options_html}
              </select>
            </div>

            <div class="calc-form-group">
              <label class="calc-label" for="calc-rooms">
                <span>2. Desired Plumbed Exam / Clinical Suites</span>
                <span class="calc-label-val" id="calc-rooms-val">20 Rooms</span>
              </label>
              <input type="range" id="calc-rooms" class="calc-range" min="4" max="35" value="20" />
              <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted);">
                <span>4 Rooms (Boutique Pod)</span>
                <span>18 Rooms (Single Wing)</span>
                <span>35 Rooms (Full Campus)</span>
              </div>
            </div>

            <div class="calc-form-group">
              <label class="calc-label" for="calc-patients">
                <span>3. Projected Daily Patient / Client Visits</span>
                <span class="calc-label-val" id="calc-patients-val">95 Visits / Day</span>
              </label>
              <input type="range" id="calc-patients" class="calc-range" min="15" max="300" step="5" value="95" />
            </div>

            <div class="calc-form-group">
              <label class="calc-label" for="calc-tier">4. Interior Finish Customization Tier</label>
              <select id="calc-tier" class="calc-select">
                <option value="turnkey-refresh">Turnkey Clinical Refresh (Paint, LED &amp; Flooring Polish)</option>
                <option value="modern-clinical" selected>Modern Clinical Upgrade (LVP Wood Flooring &amp; Custom Millwork)</option>
                <option value="bespoke-hospitality">Bespoke Hospitality &amp; MedSpa (Wellness Cafe Lobby &amp; Designer Finishes)</option>
              </select>
            </div>

            <div class="calc-checkbox-row">
              <label class="calc-checkbox-label">
                <input type="checkbox" id="calc-xray" checked />
                <span>Utilize existing on-site X-Ray suite, Phlebotomy Blood Draw &amp; Lab rooms</span>
              </label>
              <label class="calc-checkbox-label">
                <input type="checkbox" id="calc-conf" />
                <span>Include 576 SF clear-span Conference / Didactic Training Hall (#222)</span>
              </label>
            </div>
          </form>

          <div class="calc-results-panel" aria-live="polite">
            <div>
              <div class="calc-savings-banner">
                <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; color:#a9babf; font-weight:700;">
                  Estimated TI Capital Preserved vs. Cold Shell Build-Out
                </div>
                <div class="calc-savings-val" id="res-capital-saved">$1,711,500</div>
                <div style="font-size:0.88rem; color:#e2f1ef; margin-top:0.35rem;">
                  Recommended: <strong id="res-floor-plan">Full Ground Floor Clinical Wing</strong>
                </div>
              </div>

              <div class="calc-kpi-grid">
                <div class="calc-kpi-box">
                  <div class="calc-kpi-num" id="res-kpi-rooms">24 Plumbed + 7 Proc</div>
                  <div class="calc-kpi-lbl">Clinical Suite Capacity</div>
                </div>
                <div class="calc-kpi-box">
                  <div class="calc-kpi-num" id="res-kpi-months">11 Months Faster</div>
                  <div class="calc-kpi-lbl">Speed to Market Advantage</div>
                </div>
                <div class="calc-kpi-box">
                  <div class="calc-kpi-num" id="res-kpi-parking">75+ Spaces</div>
                  <div class="calc-kpi-lbl">0.5-Acre Lot + On-Site ADA</div>
                </div>
              </div>

              <div class="cost-bars">
                <div class="cost-bar-row">
                  <div class="cost-bar-meta">
                    <span>Typical Cold-Shell Medical Build-Out</span>
                    <strong id="res-shell-cost">$2,257,500</strong>
                  </div>
                  <div class="cost-bar-track">
                    <div class="cost-bar-fill cost-bar-fill--shell"></div>
                  </div>
                </div>
                <div class="cost-bar-row">
                  <div class="cost-bar-meta">
                    <span>207 Elk Ave S Turnkey Adaptive Reuse Estimate</span>
                    <strong id="res-ti-cost" style="color:#5eead4;">$546,000</strong>
                  </div>
                  <div class="cost-bar-track">
                    <div class="cost-bar-fill cost-bar-fill--turnkey" id="res-ti-bar" style="width: 24%;"></div>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; color:#5eead4; font-weight:700; margin-bottom:0.5rem;">
                Included Infrastructure Highlights
              </div>
              <ul id="res-advantages-list" style="padding-left:1.1rem; font-size:0.86rem; color:#d1e0dd; display:grid; gap:0.35rem;"></ul>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 21 Strategic Advantages Across 4 Pillars -->
    <section id="advantages" class="section">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Comprehensive Due Diligence Briefing</span>
          <h2 class="section-title">21 Reasons 207 Elk Ave S Anchors Healthcare in Southern Middle Tennessee</h2>
          <p class="section-subtitle">
            Distilled from ownership’s institutional property briefing—covering turnkey wet-wall density,
            IBC Group B code protection, unmatched downtown parking, and flexible lease structures.
          </p>
        </div>

        <div class="pillars-grid">
          {pillars_html}
        </div>
      </div>
    </section>

    <!-- Location, Dedicated 0.5-Acre Parking & Certified Surveys -->
    <section id="location" class="section section--alt">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Two-Tract Campus · Downtown Fayetteville &amp; Huntsville Corridor</span>
          <h2 class="section-title">Unmatched Off-Street Parking Steps from Historic Town Square</h2>
          <p class="section-subtitle">
            Unlike typical downtown buildings with constrained street parking, 207 Elk Ave S includes both
            on-site ADA parking on <strong>Tract 1 (0.39 AC)</strong> and a dedicated <strong>0.45-acre (~0.5 AC) paved parking lot (Tract 2)</strong>
            directly across Elk Ave S.
          </p>
        </div>

        <div class="campus-location-grid">
          <div>
            <div class="floorplan-card">
              <div class="floorplan-toolbar">
                <strong>Certified Two-Tract Boundary Survey (Tract 1 &amp; Tract 2)</strong>
                <span class="zone-badge">0.84 Total Campus Acres</span>
              </div>
              <img src="assets/images/survey-two-tracts.png" alt="Certified Two-Tract Survey for 207 Elk Ave S" />
              <p style="font-size:0.84rem; color:#4b5c63; margin-top:0.75rem;">
                Survey by Michael R. Gooding PE, RLS — showing Tract 1 (0.39 AC Medical Building at Elk Ave S &amp; Campbell St E)
                and Tract 2 (0.45 AC Dedicated Parking Lot directly across Elk Ave S).
              </p>
            </div>
          </div>

          <div style="display:flex; flex-direction:column; justify-content:space-between;">
            <div>
              <h3 style="font-family:var(--font-serif); font-size:2rem; margin-bottom:0.75rem;">
                Strategic Regional Healthcare Hub
              </h3>
              <p style="color:var(--text-secondary); margin-bottom:1rem;">
                Positioned one block behind Fayetteville’s historic Courthouse Square and minutes from
                <strong>HH Lincoln Medical Center</strong>, 207 Elk Ave S sits at the geographic center of a
                multi-county catchment area directly north of the booming <strong>Huntsville / Rocket City</strong> corridor.
              </p>
              <ul class="archetype-list">
                <li><span><strong>Walkable Downtown Amenities:</strong> Immediate access to Main Avenue dining, pharmacies, banking, and municipal services for providers and patients.</span></li>
                <li><span><strong>Dedicated 0.5-Acre Parking Parcel:</strong> Eliminates parking bottlenecks for high-volume outpatient clinics, staff shifts, and training cohorts.</span></li>
                <li><span><strong>Hospital &amp; Referral Synergy:</strong> Minutes from Lincoln Medical Center (Huntsville Hospital Health System) for imaging, lab, and inpatient coordination.</span></li>
              </ul>
            </div>

            <div class="parcel-cards">
              <div class="parcel-card">
                <img src="assets/images/aerial-building-boundary.jpg" alt="Tract 1 Building Boundary Aerial" loading="lazy" />
                <div class="parcel-card-body">
                  <strong style="font-size:0.92rem;">Tract 1: Medical Building (0.39 AC)</strong>
                  <p style="font-size:0.8rem; color:var(--text-secondary);">2-story brick core + 1-story clinical wing + curbside &amp; side ADA parking.</p>
                </div>
              </div>
              <div class="parcel-card">
                <img src="assets/images/aerial-parking-lot-boundary.jpg" alt="Tract 2 Dedicated Parking Lot Boundary Aerial" loading="lazy" />
                <div class="parcel-card-body">
                  <strong style="font-size:0.92rem;">Tract 2: Dedicated Parking (0.45 AC)</strong>
                  <p style="font-size:0.8rem; color:var(--text-secondary);">Expansive paved private lot directly across Elk Ave S.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filterable High-Resolution Property Gallery -->
    <section id="gallery" class="section">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Visual Due Diligence Library</span>
          <h2 class="section-title">Exterior, Clinical Interior, Aerial &amp; Community Gallery</h2>
          <p class="section-subtitle">
            Filter all 20 high-resolution property photographs, architectural renovation concepts, drone aerials,
            and surveys. Click any card to inspect in fullscreen.
          </p>
        </div>

        <div class="gallery-filters" role="group" aria-label="Gallery Category Filter">
          {gallery_filters_html}
        </div>

        <div class="gallery-grid">
          {gallery_items_html}
        </div>
      </div>
    </section>

    <!-- Direct Principal / Owner Contact & Tour Request Builder -->
    <section id="contact" class="section section--dark">
      <div class="container">
        <div class="section-header">
          <span class="eyebrow">Direct Ownership Leasing &amp; Partnership</span>
          <h2 class="section-title">Partner Directly with Principal Ownership</h2>
          <p class="section-subtitle">
            Work directly with ownership—without broker friction—to structure a single-floor, phased,
            or full-building medical lease tailored to your clinical timeline and capital goals.
          </p>
        </div>

        <div class="contact-grid">
          <div class="owner-card">
            <div class="owner-header">
              <img
                src="{_esc(listing.contact.portrait_image)}"
                alt="{_esc(listing.contact.name)}"
                class="owner-avatar"
              />
              <div>
                <div style="font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; color:#5eead4; font-weight:700;">
                  {_esc(listing.contact.role)} · {_esc(listing.contact.entity)}
                </div>
                <h3 style="font-family:var(--font-serif); font-size:2rem; line-height:1.15;">
                  {_esc(listing.contact.name)}
                </h3>
                <div style="font-size:0.9rem; color:var(--text-on-dark-muted);">
                  {_esc(listing.contact.title)}
                </div>
              </div>
            </div>

            <p style="font-size:0.95rem; color:#d5e3e0; line-height:1.65;">
              {_esc(listing.contact.credentials_summary)}
            </p>

            <div class="owner-contact-links">
              <a href="{_esc(listing.contact.phone_uri)}" class="owner-contact-link">
                <span>📞</span>
                <div>
                  <div style="font-size:0.75rem; color:var(--text-on-dark-muted);">Direct Telephone</div>
                  <div>{_esc(listing.contact.phone_display)}</div>
                </div>
              </a>
              <a href="mailto:{_esc(listing.contact.email)}" class="owner-contact-link">
                <span>✉️</span>
                <div>
                  <div style="font-size:0.75rem; color:var(--text-on-dark-muted);">Direct Email</div>
                  <div>{_esc(listing.contact.email)}</div>
                </div>
              </a>
              <div class="owner-contact-link">
                <span>📍</span>
                <div>
                  <div style="font-size:0.75rem; color:var(--text-on-dark-muted);">Property Location</div>
                  <div>207 Elk Ave S (201–207 Elk Ave Campus), Fayetteville, TN 37334</div>
                </div>
              </div>
            </div>

            <div style="font-size:0.82rem; color:var(--text-on-dark-muted); border-top:1px solid var(--border-on-dark); padding-top:1rem;">
              Ownership provides hands-on guidance for Main Street district incentives, downtown revitalization
              programs, and rural healthcare grant navigation.
            </div>
          </div>

          <div class="inquiry-card">
            <h3 style="font-family:var(--font-serif); font-size:1.85rem; margin-bottom:0.35rem;">
              Generate Custom Tour &amp; Leasing Briefing
            </h3>
            <p style="font-size:0.9rem; color:var(--text-secondary); margin-bottom:1.25rem;">
              Your selections from the TI Capital Estimator are automatically synchronized below. Customize your
              practice details and send directly to ownership or copy to your clipboard.
            </p>

            <div class="form-row-2" style="margin-bottom:1rem;">
              <div>
                <label class="calc-label" for="inq-name">Your Name &amp; Title</label>
                <input type="text" id="inq-name" class="calc-input" placeholder="e.g., Dr. Sarah Jenkins, MD / VP Operations" />
              </div>
              <div>
                <label class="calc-label" for="inq-org">Medical Practice or Organization</label>
                <input type="text" id="inq-org" class="calc-input" placeholder="e.g., Southern Middle TN Specialty Group" />
              </div>
            </div>

            <div class="form-row-2" style="margin-bottom:1rem;">
              <div>
                <label class="calc-label" for="inq-timeline">Target Occupancy Horizon</label>
                <input type="text" id="inq-timeline" class="calc-input" value="Q1 / Q2 Next Year (Turnkey Launch)" />
              </div>
              <div>
                <label class="calc-label" for="inq-notes">Specific Clinical or Lease Notes</label>
                <input type="text" id="inq-notes" class="calc-input" placeholder="e.g., Ground floor wing + X-ray room" />
              </div>
            </div>

            <div style="margin-bottom:1.25rem;">
              <label class="calc-label" for="inquiry-preview-box">Auto-Generated Leasing Briefing Preview</label>
              <textarea
                id="inquiry-preview-box"
                class="calc-input"
                rows="8"
                readonly
                style="font-family:var(--font-mono); font-size:0.8rem; line-height:1.45;"
              ></textarea>
            </div>

            <div style="display:flex; flex-wrap:wrap; gap:0.75rem;">
              <button type="button" id="inq-mailto-btn" class="btn btn--primary">
                ✉️ Open in Email Client to Shaz Perrone
              </button>
              <button type="button" id="inq-copy-btn" class="btn btn--secondary">
                📋 Copy Briefing to Clipboard
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>

  <!-- Lightbox Modal -->
  <div id="lightbox-modal" class="lightbox" role="dialog" aria-modal="true" aria-hidden="true" aria-label="Image Lightbox">
    <div class="lightbox-content">
      <div class="lightbox-img-wrap">
        <img id="lightbox-image" src="assets/images/exterior-renovated.jpg" alt="Enlarged Property View" />
      </div>
      <div class="lightbox-bar">
        <div>
          <strong id="lightbox-title" style="display:block; font-size:1.05rem;">Property Image</strong>
          <span id="lightbox-caption" style="font-size:0.85rem; color:#a9babf;"></span>
        </div>
        <div style="display:flex; gap:0.5rem;">
          <button type="button" id="lightbox-prev" class="btn btn--secondary btn--sm" style="background:#1b272c; color:#fff;">← Prev</button>
          <button type="button" id="lightbox-next" class="btn btn--secondary btn--sm" style="background:#1b272c; color:#fff;">Next →</button>
          <button type="button" id="lightbox-close" class="btn btn--primary btn--sm">Close ✕</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container" style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:1rem;">
      <div>
        <strong style="color:#ffffff;">207 Elk Ave S (201–207 Elk Ave S Medical Campus)</strong> · Fayetteville, TN 37334
        <p style="margin-top:0.25rem;">Owned &amp; Managed by 207 Elk LLC · Principal/Owner: Shaz Perrone · (973) 271-5324 · Shaz.Perrone@gmail.com</p>
      </div>
      <div style="text-align:right;">
        <span>IBC Group B Medical &amp; Executive Office</span> · <span>0.84 Total Acres (Building + Dedicated Parking)</span>
      </div>
    </div>
  </footer>

  <!-- Embedded Canonical Property Data -->
  <script id="property-data-json" type="application/json">{embedded_data_str}</script>
  <script src="app.js"></script>
</body>
</html>
"""


def verify_static_assets(listing: PropertyListing, root_dir: Path = STATIC_SOURCE_DIR) -> list[Path]:
    """Verify that all image assets referenced in the listing exist on disk."""
    referenced_paths: set[str] = {listing.contact.portrait_image}
    for floor in listing.floors:
        referenced_paths.add(floor.floorplan_image)
    for tr in listing.transformations:
        referenced_paths.add(tr.before_image)
        referenced_paths.add(tr.after_image)
        if tr.alt_image:
            referenced_paths.add(tr.alt_image)
    for gal in listing.gallery:
        referenced_paths.add(gal.image_path)

    verified: list[Path] = []
    for rel_path in sorted(referenced_paths):
        full_path = root_dir / rel_path
        if not full_path.is_file() or full_path.stat().st_size == 0:
            raise AssetVerificationError(
                f"Missing or empty required property asset: '{rel_path}' (expected at {full_path})."
            )
        verified.append(full_path)
    return verified


def build_static_site(output_dir: Path) -> dict[str, Any]:
    """Build the complete static site into output_dir and return build manifest."""
    listing = build_property_listing()
    verified_assets = verify_static_assets(listing, STATIC_SOURCE_DIR)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Copy CSS, JS, and image assets
    shutil.copy2(STATIC_SOURCE_DIR / "styles.css", output_dir / "styles.css")
    shutil.copy2(STATIC_SOURCE_DIR / "app.js", output_dir / "app.js")

    assets_dst = output_dir / "assets" / "images"
    assets_dst.mkdir(parents=True, exist_ok=True)
    for src_img in (STATIC_SOURCE_DIR / "assets" / "images").glob("*"):
        if src_img.is_file():
            shutil.copy2(src_img, assets_dst / src_img.name)

    # Write index.html and property-data.json to output_dir
    index_html = render_index_html(listing)
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")
    (output_dir / "property-data.json").write_text(
        json.dumps(listing.to_dict(), indent=2), encoding="utf-8"
    )

    return {
        "property_id": listing.property_id,
        "output_dir": str(output_dir.resolve()),
        "verified_asset_count": len(verified_assets),
        "html_bytes": len(index_html.encode("utf-8")),
    }
