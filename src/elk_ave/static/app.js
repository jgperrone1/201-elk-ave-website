/**
 * 207 Elk Ave S — Interactive Medical & Executive Office Leasing Application
 */
(function () {
  "use strict";

  const state = {
    theme: localStorage.getItem("elk_theme") || "light",
    activeArchetypeId: "multi-specialty-outpatient",
    activeTransformId: "exterior-facade",
    activeFloorLevel: 1,
    activeGalleryCategory: "All",
    lightboxIndex: 0,
    filteredGallery: [],
    lastEstimate: null,
  };

  function getPropertyData() {
    const el = document.getElementById("property-data-json");
    if (!el) return null;
    try {
      return JSON.parse(el.textContent);
    } catch (err) {
      console.error("Failed to parse embedded property data:", err);
      return null;
    }
  }

  function formatUSD(amount) {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency: "USD",
      maximumFractionDigits: 0,
    }).format(amount);
  }

  /* --------------------------------------------------------------------------
     1. Theme Toggle
     -------------------------------------------------------------------------- */
  function initTheme() {
    document.documentElement.setAttribute("data-theme", state.theme);
    const btn = document.getElementById("theme-toggle-btn");
    if (!btn) return;
    const updateIcon = () => {
      btn.textContent = state.theme === "dark" ? "☀️" : "🌙";
      btn.setAttribute(
        "aria-label",
        state.theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
      );
    };
    updateIcon();
    btn.addEventListener("click", () => {
      state.theme = state.theme === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", state.theme);
      localStorage.setItem("elk_theme", state.theme);
      updateIcon();
    });
  }

  /* --------------------------------------------------------------------------
     2. Hero View Switcher
     -------------------------------------------------------------------------- */
  function initHeroSwitcher() {
    const heroImg = document.getElementById("hero-main-image");
    const heroLabel = document.getElementById("hero-view-label");
    const heroSub = document.getElementById("hero-view-sub");
    const buttons = document.querySelectorAll("[data-hero-view]");
    if (!heroImg || !buttons.length) return;

    const views = {
      renovated: {
        src: "assets/images/exterior-renovated.jpg",
        label: "Renovated Architectural Concept",
        sub: "Modernized brick & dark architectural bronze facade along Elk Ave S",
      },
      original: {
        src: "assets/images/exterior-original.jpg",
        label: "Current Clinical Exterior",
        sub: "Turnkey two-story brick & clinical wing (formerly HH Lincoln Health Primary Care)",
      },
      aerial: {
        src: "assets/images/aerial-front-facade.jpg",
        label: "Aerial Campus & ADA Parking View",
        sub: "Direct street frontage, side ADA spaces, plus 0.5-acre lot across Elk Ave S",
      },
    };

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const key = btn.getAttribute("data-hero-view");
        const view = views[key];
        if (!view) return;
        buttons.forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        heroImg.src = view.src;
        if (heroLabel) heroLabel.textContent = view.label;
        if (heroSub) heroSub.textContent = view.sub;
      });
    });
  }

  /* --------------------------------------------------------------------------
     3. Interactive Specialty Fit Explorer
     -------------------------------------------------------------------------- */
  function initArchetypeExplorer(data) {
    if (!data || !data.archetypes) return;
    const pills = document.querySelectorAll("[data-archetype-id]");
    const titleEl = document.getElementById("arch-specialty");
    const headlineEl = document.getElementById("arch-headline");
    const whyListEl = document.getElementById("arch-why-list");
    const configEl = document.getElementById("arch-config");
    const roomsEl = document.getElementById("arch-rooms");
    const infraEl = document.getElementById("arch-infra-tags");
    const loadCalcBtn = document.getElementById("arch-load-calc-btn");

    function renderArchetype(id) {
      const item = data.archetypes.find((a) => a.id === id);
      if (!item) return;
      state.activeArchetypeId = item.id;

      pills.forEach((p) => {
        p.classList.toggle("active", p.getAttribute("data-archetype-id") === id);
      });

      if (titleEl) titleEl.textContent = item.specialty;
      if (headlineEl) headlineEl.textContent = item.headline;
      if (configEl) configEl.textContent = item.recommended_configuration;
      if (roomsEl)
        roomsEl.textContent = `${item.target_rooms} Plumbed Clinical / Exam Rooms`;

      if (whyListEl) {
        whyListEl.innerHTML = item.why_it_fits
          .map((pt) => `<li><span>${pt}</span></li>`)
          .join("");
      }
      if (infraEl) {
        infraEl.innerHTML = item.infrastructure_match
          .map((tag) => `<span class="infra-tag">${tag}</span>`)
          .join("");
      }
    }

    pills.forEach((pill) => {
      pill.addEventListener("click", () => {
        renderArchetype(pill.getAttribute("data-archetype-id"));
      });
    });

    if (loadCalcBtn) {
      loadCalcBtn.addEventListener("click", () => {
        const item = data.archetypes.find((a) => a.id === state.activeArchetypeId);
        if (!item) return;
        const specSelect = document.getElementById("calc-specialty");
        const roomsRange = document.getElementById("calc-rooms");
        if (specSelect) specSelect.value = item.id;
        if (roomsRange) {
          roomsRange.value = String(item.target_rooms);
          roomsRange.dispatchEvent(new Event("input"));
        }
        const calcSection = document.getElementById("calculator");
        if (calcSection) calcSection.scrollIntoView({ behavior: "smooth" });
      });
    }
  }

  /* --------------------------------------------------------------------------
     4. Before / After Transformation Studio
     -------------------------------------------------------------------------- */
  function initTransformationStudio(data) {
    if (!data || !data.transformations) return;
    const tabs = document.querySelectorAll("[data-transform-id]");
    const beforeImg = document.getElementById("studio-before-img");
    const afterImg = document.getElementById("studio-after-img");
    const beforeBadge = document.getElementById("studio-before-badge");
    const afterBadge = document.getElementById("studio-after-badge");
    const beforeLayer = document.getElementById("studio-before-layer");
    const handle = document.getElementById("studio-handle");
    const rangeInput = document.getElementById("studio-range");
    const titleEl = document.getElementById("studio-title");
    const subEl = document.getElementById("studio-subtitle");
    const descEl = document.getElementById("studio-desc");
    const clinicalEl = document.getElementById("studio-clinical");
    const altBtn = document.getElementById("studio-alt-btn");
    const presetBtns = document.querySelectorAll("[data-slider-pos]");

    function setSliderPos(percent) {
      const clamped = Math.max(0, Math.min(100, Number(percent)));
      if (beforeLayer) {
        beforeLayer.style.clipPath = `inset(0 ${100 - clamped}% 0 0)`;
      }
      if (handle) {
        handle.style.left = `${clamped}%`;
      }
      if (rangeInput) {
        rangeInput.value = String(clamped);
      }
    }

    function renderTransformation(id) {
      const item = data.transformations.find((t) => t.id === id);
      if (!item) return;
      state.activeTransformId = item.id;

      tabs.forEach((t) => {
        t.classList.toggle("active", t.getAttribute("data-transform-id") === id);
      });

      if (beforeImg) {
        beforeImg.src = item.before_image;
        beforeImg.alt = `${item.title} - ${item.before_label}`;
      }
      if (afterImg) {
        afterImg.src = item.after_image;
        afterImg.alt = `${item.title} - ${item.after_label}`;
      }
      if (beforeBadge) beforeBadge.textContent = item.before_label;
      if (afterBadge) afterBadge.textContent = item.after_label;
      if (titleEl) titleEl.textContent = item.title;
      if (subEl) subEl.textContent = item.subtitle;
      if (descEl) descEl.textContent = item.description;
      if (clinicalEl) clinicalEl.textContent = item.clinical_value;

      if (altBtn) {
        if (item.alt_image && item.alt_label) {
          altBtn.style.display = "inline-flex";
          altBtn.textContent = `View ${item.alt_label}`;
          altBtn.onclick = () => {
            if (afterImg) afterImg.src = item.alt_image;
            if (afterBadge) afterBadge.textContent = item.alt_label;
            setSliderPos(12);
          };
        } else {
          altBtn.style.display = "none";
        }
      }
      setSliderPos(50);
    }

    if (rangeInput) {
      rangeInput.addEventListener("input", (e) => {
        setSliderPos(e.target.value);
      });
    }

    presetBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const pos = btn.getAttribute("data-slider-pos");
        const item = data.transformations.find(
          (t) => t.id === state.activeTransformId
        );
        if (item && afterImg && afterBadge) {
          afterImg.src = item.after_image;
          afterBadge.textContent = item.after_label;
        }
        setSliderPos(pos);
      });
    });

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        renderTransformation(tab.getAttribute("data-transform-id"));
      });
    });
  }

  /* --------------------------------------------------------------------------
     5. Interactive Dual-Level Floorplan Explorer
     -------------------------------------------------------------------------- */
  function initFloorExplorer(data) {
    if (!data || !data.floors) return;
    const tabBtns = document.querySelectorAll("[data-floor-level]");
    const imgEl = document.getElementById("floorplan-img");
    const nameEl = document.getElementById("floorplan-name");
    const taglineEl = document.getElementById("floorplan-tagline");
    const summaryEl = document.getElementById("floorplan-summary");
    const statExam = document.getElementById("floor-stat-exam");
    const statProc = document.getElementById("floor-stat-proc");
    const statRest = document.getElementById("floor-stat-rest");
    const statDoors = document.getElementById("floor-stat-doors");
    const zonesContainer = document.getElementById("floor-zones-container");
    const zoomBtn = document.getElementById("floorplan-zoom-btn");
    const canvasWrap = document.getElementById("floorplan-canvas-wrap");

    function renderFloor(levelNum) {
      const floor = data.floors.find((f) => f.level === Number(levelNum));
      if (!floor) return;
      state.activeFloorLevel = floor.level;

      tabBtns.forEach((b) => {
        b.classList.toggle(
          "active",
          Number(b.getAttribute("data-floor-level")) === floor.level
        );
      });

      if (imgEl) {
        imgEl.src = floor.floorplan_image;
        imgEl.alt = `${floor.name} Architectural Floorplan`;
      }
      if (nameEl) nameEl.textContent = floor.name;
      if (taglineEl) taglineEl.textContent = floor.tagline;
      if (summaryEl) summaryEl.textContent = floor.summary;
      if (statExam) statExam.textContent = `${floor.exam_and_clinical_rooms}+`;
      if (statProc) statProc.textContent = String(floor.procedure_rooms);
      if (statRest) statRest.textContent = String(floor.restrooms);
      if (statDoors) statDoors.textContent = String(floor.exterior_egress_doors);

      if (zonesContainer) {
        zonesContainer.innerHTML = floor.zones
          .map(
            (z) => `
          <article class="zone-card">
            <div class="zone-card-header">
              <h4 class="zone-title">${z.name}</h4>
              <span class="zone-badge">${z.room_count_label}</span>
            </div>
            <ul class="zone-highlights">
              ${z.highlights.map((h) => `<li>${h}</li>`).join("")}
            </ul>
            <div class="infra-tags">
              ${z.ideal_uses.map((u) => `<span class="infra-tag">${u}</span>`).join("")}
            </div>
          </article>
        `
          )
          .join("");
      }
    }

    tabBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        renderFloor(btn.getAttribute("data-floor-level"));
      });
    });

    const openFloorplanModal = () => {
      const floor = data.floors.find((f) => f.level === state.activeFloorLevel);
      if (!floor) return;
      openStandaloneLightbox(
        floor.floorplan_image,
        `${floor.name} — Architectural Floorplan`,
        floor.summary
      );
    };

    if (zoomBtn) zoomBtn.addEventListener("click", openFloorplanModal);
    if (canvasWrap) canvasWrap.addEventListener("click", openFloorplanModal);
  }

  /* --------------------------------------------------------------------------
     6. Deterministic Clinical Footprint & TI Capital Calculator
     -------------------------------------------------------------------------- */
  function computeLocalEstimate(req) {
    const rooms = Number(req.desired_clinical_rooms);
    let floorPlan = "";
    let allocatedRooms = 24;
    let procRooms = 7;
    let usableSqft = 10500;
    let monthsSaved = 11;

    if (
      rooms <= 11 &&
      (["behavioral-health", "rehab-physical-therapy", "academic-health-sciences"].includes(
        req.specialty_id
      ) ||
        req.needs_conference_hall) &&
      req.specialty_id !== "urgent-care-diagnostics"
    ) {
      floorPlan =
        "Upper Level (2nd Floor — 11 Plumbed Rooms, Lab #235, 576 SF Hall & 16+ Offices)";
      allocatedRooms = 11;
      procRooms = 1;
      usableSqft = 6800;
      monthsSaved = 8;
    } else if (rooms <= 14 && !req.needs_conference_hall) {
      floorPlan =
        "Ground Floor Phased Clinical Pod (12–16 Plumbed Exam & Procedure Suites)";
      allocatedRooms = Math.max(rooms, 12);
      procRooms = 4;
      usableSqft = 5800;
      monthsSaved = 9;
    } else if (rooms <= 24 && !req.needs_conference_hall) {
      floorPlan =
        "Full Ground Floor Clinical Wing (24+ Exam Rooms, 7 Procedure Suites, X-Ray & Dual Waiting)";
      allocatedRooms = 24;
      procRooms = 7;
      usableSqft = 10500;
      monthsSaved = 11;
    } else {
      floorPlan =
        "Full Two-Story Medical Campus (35+ Plumbed Rooms, 7 Procedure Suites, Labs & Executive Wing)";
      allocatedRooms = 35;
      procRooms = 8;
      usableSqft = 17300;
      monthsSaved = 14;
    }

    const coldShellPerSqft = [
      "dental-oral-health",
      "urgent-care-diagnostics",
      "dermatology-aesthetics",
    ].includes(req.specialty_id)
      ? 240
      : 215;

    const tierMap = {
      "turnkey-refresh": 28,
      "modern-clinical": 52,
      "bespoke-hospitality": 82,
    };
    const tiPerSqft = tierMap[req.finish_tier] || 52;

    const coldShellCost = usableSqft * coldShellPerSqft;
    const turnkeyCost = usableSqft * tiPerSqft;
    const saved = Math.max(0, coldShellCost - turnkeyCost);

    const advantages = [
      `Avoids concrete slab trenching across ${allocatedRooms} wet-wall plumbed clinical rooms.`,
      "Retains protected IBC Group B (Business) medical classification with zero structural fire-code retrofits.",
    ];
    if (req.needs_xray_or_lab) {
      advantages.push(
        "Includes existing X-Ray suite, Reading Room, Phlebotomy Blood Draw, and built-in Laboratory cabinetry."
      );
    }
    if (req.needs_conference_hall || usableSqft !== 5800) {
      advantages.push(
        "Access to 576 SF clear-span Conference/Didactic Hall (#222) and 2nd-floor Executive Lounge."
      );
    }
    advantages.push(
      `Accommodates ${req.daily_patients} daily patient visits with dual waiting rooms and 0.5-acre dedicated parking.`
    );

    return {
      recommended_floor_plan: floorPlan,
      plumbed_rooms_allocated: allocatedRooms,
      procedure_rooms_included: procRooms,
      estimated_usable_sqft: usableSqft,
      estimated_cold_shell_cost_usd: coldShellCost,
      estimated_turnkey_ti_cost_usd: turnkeyCost,
      estimated_capital_saved_usd: saved,
      months_saved_vs_shell: monthsSaved,
      parking_spaces_available: 75,
      key_advantages: advantages,
    };
  }

  function initCalculator() {
    const specEl = document.getElementById("calc-specialty");
    const roomsEl = document.getElementById("calc-rooms");
    const patientsEl = document.getElementById("calc-patients");
    const tierEl = document.getElementById("calc-tier");
    const xrayEl = document.getElementById("calc-xray");
    const confEl = document.getElementById("calc-conf");

    const roomsValEl = document.getElementById("calc-rooms-val");
    const patientsValEl = document.getElementById("calc-patients-val");
    const savedEl = document.getElementById("res-capital-saved");
    const recPlanEl = document.getElementById("res-floor-plan");
    const kpiRoomsEl = document.getElementById("res-kpi-rooms");
    const kpiMonthsEl = document.getElementById("res-kpi-months");
    const kpiParkingEl = document.getElementById("res-kpi-parking");
    const shellCostEl = document.getElementById("res-shell-cost");
    const tiCostEl = document.getElementById("res-ti-cost");
    const tiBarEl = document.getElementById("res-ti-bar");
    const advListEl = document.getElementById("res-advantages-list");

    if (!specEl || !roomsEl || !patientsEl || !tierEl) return;

    function updateCalculator() {
      const req = {
        specialty_id: specEl.value,
        desired_clinical_rooms: Number(roomsEl.value),
        daily_patients: Number(patientsEl.value),
        finish_tier: tierEl.value,
        needs_xray_or_lab: xrayEl ? xrayEl.checked : true,
        needs_conference_hall: confEl ? confEl.checked : false,
      };

      if (roomsValEl) roomsValEl.textContent = `${req.desired_clinical_rooms} Rooms`;
      if (patientsValEl)
        patientsValEl.textContent = `${req.daily_patients} Visits / Day`;

      const res = computeLocalEstimate(req);
      state.lastEstimate = { req, res };

      if (savedEl) savedEl.textContent = formatUSD(res.estimated_capital_saved_usd);
      if (recPlanEl) recPlanEl.textContent = res.recommended_floor_plan;
      if (kpiRoomsEl)
        kpiRoomsEl.textContent = `${res.plumbed_rooms_allocated} Plumbed + ${res.procedure_rooms_included} Proc`;
      if (kpiMonthsEl)
        kpiMonthsEl.textContent = `${res.months_saved_vs_shell} Months Faster`;
      if (kpiParkingEl)
        kpiParkingEl.textContent = `${res.parking_spaces_available}+ Spaces (0.5 AC Lot)`;
      if (shellCostEl)
        shellCostEl.textContent = formatUSD(res.estimated_cold_shell_cost_usd);
      if (tiCostEl)
        tiCostEl.textContent = formatUSD(res.estimated_turnkey_ti_cost_usd);

      if (tiBarEl && res.estimated_cold_shell_cost_usd > 0) {
        const pct = Math.round(
          (res.estimated_turnkey_ti_cost_usd / res.estimated_cold_shell_cost_usd) *
            100
        );
        tiBarEl.style.width = `${Math.max(10, Math.min(100, pct))}%`;
      }

      if (advListEl) {
        advListEl.innerHTML = res.key_advantages
          .map((a) => `<li>${a}</li>`)
          .join("");
      }

      syncInquirySummary();
    }

    [specEl, roomsEl, patientsEl, tierEl, xrayEl, confEl].forEach((input) => {
      if (input) {
        input.addEventListener("input", updateCalculator);
        input.addEventListener("change", updateCalculator);
      }
    });

    updateCalculator();
  }

  /* --------------------------------------------------------------------------
     7. Filterable Gallery & Lightbox
     -------------------------------------------------------------------------- */
  function openStandaloneLightbox(src, title, caption) {
    const modal = document.getElementById("lightbox-modal");
    const img = document.getElementById("lightbox-image");
    const titleEl = document.getElementById("lightbox-title");
    const capEl = document.getElementById("lightbox-caption");
    if (!modal || !img) return;
    img.src = src;
    img.alt = title;
    if (titleEl) titleEl.textContent = title;
    if (capEl) capEl.textContent = caption || "";
    modal.classList.add("open");
    modal.setAttribute("aria-hidden", "false");
  }

  function initGallery(data) {
    if (!data || !data.gallery) return;
    const filterBtns = document.querySelectorAll("[data-gallery-cat]");
    const items = document.querySelectorAll("[data-gallery-item]");
    const modal = document.getElementById("lightbox-modal");
    const closeBtn = document.getElementById("lightbox-close");
    const prevBtn = document.getElementById("lightbox-prev");
    const nextBtn = document.getElementById("lightbox-next");

    state.filteredGallery = data.gallery.slice();

    function showLightboxByIndex(idx) {
      if (!state.filteredGallery.length) return;
      state.lightboxIndex =
        (idx + state.filteredGallery.length) % state.filteredGallery.length;
      const asset = state.filteredGallery[state.lightboxIndex];
      openStandaloneLightbox(asset.image_path, asset.title, asset.caption);
    }

    filterBtns.forEach((btn) => {
      btn.addEventListener("click", () => {
        const cat = btn.getAttribute("data-gallery-cat");
        state.activeGalleryCategory = cat;
        filterBtns.forEach((b) => b.classList.toggle("active", b === btn));

        state.filteredGallery =
          cat === "All"
            ? data.gallery.slice()
            : data.gallery.filter((g) => g.category === cat);

        items.forEach((card) => {
          const itemCat = card.getAttribute("data-item-category");
          const match = cat === "All" || itemCat === cat;
          card.style.display = match ? "block" : "none";
        });
      });
    });

    items.forEach((card) => {
      card.addEventListener("click", () => {
        const id = card.getAttribute("data-gallery-item");
        const idx = state.filteredGallery.findIndex((g) => g.id === id);
        showLightboxByIndex(idx >= 0 ? idx : 0);
      });
    });

    if (closeBtn && modal) {
      closeBtn.addEventListener("click", () => {
        modal.classList.remove("open");
        modal.setAttribute("aria-hidden", "true");
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener("click", () =>
        showLightboxByIndex(state.lightboxIndex - 1)
      );
    }
    if (nextBtn) {
      nextBtn.addEventListener("click", () =>
        showLightboxByIndex(state.lightboxIndex + 1)
      );
    }
    if (modal) {
      modal.addEventListener("click", (e) => {
        if (e.target === modal) {
          modal.classList.remove("open");
          modal.setAttribute("aria-hidden", "true");
        }
      });
    }

    document.addEventListener("keydown", (e) => {
      if (!modal || !modal.classList.contains("open")) return;
      if (e.key === "Escape") {
        modal.classList.remove("open");
        modal.setAttribute("aria-hidden", "true");
      } else if (e.key === "ArrowLeft") {
        showLightboxByIndex(state.lightboxIndex - 1);
      } else if (e.key === "ArrowRight") {
        showLightboxByIndex(state.lightboxIndex + 1);
      }
    });
  }

  /* --------------------------------------------------------------------------
     8. Direct Owner Tour & Leasing Proposal Generator
     -------------------------------------------------------------------------- */
  function syncInquirySummary() {
    const previewEl = document.getElementById("inquiry-preview-box");
    if (!previewEl || !state.lastEstimate) return;
    const name =
      (document.getElementById("inq-name") || {}).value || "Prospective Medical Tenant";
    const org =
      (document.getElementById("inq-org") || {}).value || "Healthcare Practice / Group";
    const timeline =
      (document.getElementById("inq-timeline") || {}).value || "Q3/Q4 Target Launch";
    const notes = (document.getElementById("inq-notes") || {}).value || "";

    const { req, res } = state.lastEstimate;
    const lines = [
      `Subject: 207 Elk Ave S Medical Leasing Inquiry — ${org}`,
      "",
      "Dear Shaz Perrone (207 Elk LLC),",
      "",
      `We are evaluating medical/clinical space at 207 Elk Ave S in Fayetteville, TN for ${org} (Contact: ${name}).`,
      "",
      "Configuration Summary:",
      `• Target Specialty Profile: ${req.specialty_id}`,
      `• Desired Plumbed Clinical / Exam Rooms: ${req.desired_clinical_rooms} rooms`,
      `• Recommended Footprint: ${res.recommended_floor_plan}`,
      `• Estimated Daily Patient Volume: ~${req.daily_patients} visits/day`,
      `• Estimated TI Capital Preserved vs. Cold Shell: ${formatUSD(res.estimated_capital_saved_usd)}`,
      `• Target Occupancy Horizon: ${timeline}`,
    ];
    if (notes.trim()) {
      lines.push(`• Additional Requirements: ${notes.trim()}`);
    }
    lines.push(
      "",
      "Please let us know available times for a private on-site tour and floorplan review.",
      "",
      `Best regards,\n${name}\n${org}`
    );
    previewEl.value = lines.join("\n");
  }

  function initInquiryForm() {
    const inputs = ["inq-name", "inq-org", "inq-timeline", "inq-notes"];
    inputs.forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.addEventListener("input", syncInquirySummary);
    });

    const copyBtn = document.getElementById("inq-copy-btn");
    const mailtoBtn = document.getElementById("inq-mailto-btn");
    const previewEl = document.getElementById("inquiry-preview-box");

    if (copyBtn && previewEl) {
      copyBtn.addEventListener("click", () => {
        navigator.clipboard.writeText(previewEl.value).then(() => {
          const orig = copyBtn.textContent;
          copyBtn.textContent = "✓ Copied Briefing to Clipboard";
          setTimeout(() => {
            copyBtn.textContent = orig;
          }, 2200);
        });
      });
    }

    if (mailtoBtn && previewEl) {
      mailtoBtn.addEventListener("click", () => {
        const org =
          (document.getElementById("inq-org") || {}).value ||
          "Medical Practice Inquiry";
        const subject = encodeURIComponent(
          `207 Elk Ave S Medical Leasing Inquiry — ${org}`
        );
        const body = encodeURIComponent(previewEl.value);
        window.location.href = `mailto:Shaz.Perrone@gmail.com?subject=${subject}&body=${body}`;
      });
    }

    syncInquirySummary();
  }

  document.addEventListener("DOMContentLoaded", () => {
    const data = getPropertyData();
    initTheme();
    initHeroSwitcher();
    initArchetypeExplorer(data);
    initTransformationStudio(data);
    initFloorExplorer(data);
    initCalculator();
    initGallery(data);
    initInquiryForm();
  });
})();
