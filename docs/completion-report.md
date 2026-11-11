# Completion Report: 207 Elk Ave S Medical & Executive Leasing Platform

**Branches:** `dev`, `main`  
**Date:** 2026-11-11  
**Status:** Completed & Validated

---

## 1. Scope & Key Changes

- **Exterior & Waiting Room Photo Replacements (No Cafe) (`src/elk_ave/catalog.py`, `src/elk_ave/renderer.py`, `src/elk_ave/static/app.js`)**:
  - Replaced exterior renovation rendering across the Hero image switcher, OpenGraph metadata, Transformation Studio, and Gallery with `assets/images/exterior_wellness_no_cafe.png`, removing "CAFE" signage from the building facade.
  - Replaced renovated waiting lounge concept across the Transformation Studio and Gallery with `assets/images/Gemini_No_Cafe.jpeg`, removing "CAFE" branding from the wood feature wall.
- **Disclosures & Disclaimers Section & Navigation Tab (`src/elk_ave/renderer.py`, `src/elk_ave/static/styles.css`)**:
  - Added a prominent, styled "Disclosures" tab in primary navigation and footer linking to `#disclosures`.
  - Added dedicated disclosures card grid featuring verbatim legal text:
    1. **Real Estate Licensing & Ownership Disclosure**: 207 Elk Ave S ownership by 207 ELK, LLC; Shazia (Shaz) Perrone direct leasing/management under Tennessee statutory owner-exemption laws (T.C.A. § 62-13-104); active commercial real estate sales associate license in Florida with RealtyMark Solutions, LLC; no TN brokerage/agency relationship created; recommendation of independent advisory counsel.
    2. **Renderings & Information Disclaimer**: Architectural visualizations and conceptual renderings are for illustrative purposes only and do not constitute warranties of final finishes; building conditions subject to final plans/permits; square footage, specs, and operational expenses compiled in good faith and subject to change without notice.
- **Scrubbing of Code, Capital & IBC Group B References (`src/elk_ave/catalog.py`, `src/elk_ave/renderer.py`, `src/elk_ave/calculator.py`, `src/elk_ave/static/app.js`)**:
  - Removed all references to: `Code, Permitting & Capital Efficiency`, `CODE & CAPITAL`, `Group B`, and `Protected IBC Medical Occupancy`.
  - Removed from footer: `IBC Group B Medical & Executive Office · 0.84 Total Acres (Building + Dedicated Parking)`.
  - Re-structured strategic pillars from 4 to 3 clean pillars (18 points total: Turnkey Infrastructure, Parking & Downtown Location, Healthcare Heritage & Partnership).
  - Cleaned tenant archetype descriptions to focus on clinical operational suitability without code classification claims.
- **Cafe References & Image Removals (`src/elk_ave/catalog.py`, `src/elk_ave/renderer.py`)**:
  - Removed cafe concepts from ground floor zoning and tenant archetypes.
  - Removed front lobby / cafe transformation pair.
- **TI Capital Preservation Estimator Transition (`src/elk_ave/calculator.py`, `main.py`, `src/elk_ave/renderer.py`, `src/elk_ave/static/app.js`)**:
  - Removed public-facing TI Estimator calculator section and client-side calculator code from website.
  - Preserved full deterministic calculator business logic in `src/elk_ave/calculator.py` for ownership's private use.
  - Added `main.py estimate` CLI subcommand allowing ownership to calculate clinical footprint and TI capital preservation offline with customizable parameters (`--rooms`, `--specialty`, `--patients`, `--tier`, `--no-xray`, `--conference`).
- **Gallery Corrections (`src/elk_ave/catalog.py`)**:
  - Clinical Interiors: `Specialty Procedure & Dermatology Suite (Renovation Concept)` now explicitly states conceptual renovation rendering (not actual existing condition).
  - Removed `Fayetteville Public Utilities Easement Survey`.
  - Swapped images: `Business & Intake Office Suite` now points to `practice-pediatric-waiting.jpg` (pass-through window) and `Dedicated Pediatric / Specialty Sub-Waiting Room` points to `practice-intake-business-office.jpg` (built-in aquarium window).
- **Mobile Responsive & Header Containment Optimization (`src/elk_ave/static/styles.css`)**:
  - Resolved mobile horizontal overflow where the title bar previously forced layout width to ~484px on small viewports.
  - Hid secondary location badge on screens <= 640px, scaled mobile header action buttons and badges, added `html`/`body` horizontal overflow containment, and converted inquiry call-to-actions to responsive full-width mobile controls.

---

## 2. Validation Commands & Results

| Gate | Command | Status / Result |
| :--- | :--- | :--- |
| **Unit & Integration Tests** | `uv run python3 -m unittest discover -s tests -v` | **PASS** (15 tests in `0.05s`, 0 failures, 0 errors) |
| **Catalog & Asset Verification** | `uv run python3 main.py check` | **PASS** (`floors=2`, `archetypes=7`, `pillars=3`, `verified_assets=28`) |
| **Static Site Build** | `uv run python3 main.py build` | **PASS** (`dist/index.html`, root `index.html` + `.nojekyll` for GitHub Pages, 28 verified images) |
| **Ownership CLI Estimator** | `uv run python3 main.py estimate --rooms 16 --specialty dermatology-aesthetics` | **PASS** (deterministic capital estimate and speed-to-market calculations) |
| **Bytecode & Syntax Check** | `uv run python3 -m compileall -q src tests main.py` | **PASS** (0 syntax/compilation errors) |
| **Formatter / Linter (`ruff`)** | *Not configured* | Explicitly unconfigured in offline local environment |
| **Type Checker (`pyright`)** | *Not configured* | Explicitly unconfigured in offline local environment |

---

## 3. Known Limitations & Follow-Up Work

- **Offline / Local First Draft**: Per user instructions, this initial draft is strictly local (`dist/` static bundle + `uv run python3 main.py serve` local preview server). No external form backend or cloud deployment is connected; the Tour & Leasing Briefing Generator formats inquiries for 1-click clipboard copy and `mailto:` email client launch directly to ownership.
- **Future Enhancements**:
  - Optional deployment pipeline (e.g., Cloudflare Pages, Vercel, or Netlify static hosting) once approved for public release.
  - Optional interactive SVG polygon overlays on the 1st and 2nd floor raster schematics if CAD/vector source files become available.
