/* Best Nepal Tour Package · interactions
   Free libraries (cdnjs): GSAP + ScrollTrigger. Maps and elevation profiles are drawn on the server.
   Everything degrades: without JS the site stays readable, navigable and every form submits. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var track = function (name, data) { window.dataLayer = window.dataLayer || []; window.dataLayer.push(Object.assign({ event: name }, data || {})); };
  var store = {
    get: function (k, s) { try { return (s ? sessionStorage : localStorage).getItem(k); } catch (e) { return null; } },
    set: function (k, v, s) { try { (s ? sessionStorage : localStorage).setItem(k, v); } catch (e) {} }
  };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;" }[c]; }); };

  /* analytics hooks */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("[data-cta]");
    if (a) track("cta_click", { cta: a.dataset.cta, href: a.getAttribute("href") || "" });
  });
  $$("form[data-cta-form]").forEach(function (f) { f.addEventListener("submit", function () { track("form_submit", { form: f.dataset.ctaForm }); }); });

  /* currency: INR or USD, remembered per browser */
  function setCur(cur) {
    $$("[data-inr]").forEach(function (el) {
      var v = cur === "usd" ? el.dataset.usd : el.dataset.inr;
      if (v) el.textContent = v;
    });
    $$("[data-cur]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.cur === cur)); });
    doc.dataset.cur = cur;
  }
  $$("[data-cur]").forEach(function (b) { b.addEventListener("click", function () { store.set("cur", b.dataset.cur); setCur(b.dataset.cur); track("currency", { cur: b.dataset.cur }); }); });
  if (store.get("cur") === "usd") setCur("usd");

  /* masthead shadow, floating CTA, buy bar */
  var mast = $(".mast"), fab = $("[data-fab]"), buybar = $(".buybar"), buyAfter = $("[data-buybar-after]"), foot = $(".foot");
  function onScroll() {
    var y = window.scrollY;
    if (mast) mast.classList.toggle("is-scrolled", y > 10);
    /* the footer carries its own quote cards, so the floating button steps aside once it comes into view */
    if (fab) fab.classList.toggle("is-on", y > 520 && !(foot && foot.getBoundingClientRect().top < window.innerHeight * 0.6));
    if (buybar && buyAfter) {
      var on = buyAfter.getBoundingClientRect().bottom < 0;
      buybar.classList.toggle("is-on", on);
      document.body.classList.toggle("has-buybar", on);
    }
    if (altRail) altRail();
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  /* mega menus: hover intent on desktop, click anywhere, Esc closes */
  var drops = $$(".nav__drop");
  function closeAll(except) { drops.forEach(function (d) { if (d !== except) { d.classList.remove("is-open"); $("button", d).setAttribute("aria-expanded", "false"); } }); }
  drops.forEach(function (drop) {
    var btn = $("button", drop), timer;
    var open = function () { clearTimeout(timer); closeAll(drop); drop.classList.add("is-open"); btn.setAttribute("aria-expanded", "true"); };
    var close = function () { drop.classList.remove("is-open"); btn.setAttribute("aria-expanded", "false"); };
    btn.addEventListener("click", function (e) { e.stopPropagation(); drop.classList.contains("is-open") ? close() : open(); });
    if (window.matchMedia("(hover: hover)").matches) {
      drop.addEventListener("mouseenter", function () { clearTimeout(timer); timer = setTimeout(open, 90); });
      drop.addEventListener("mouseleave", function () { clearTimeout(timer); timer = setTimeout(close, 180); });
    }
  });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav__drop")) closeAll(); });

  /* mobile sheet */
  var sheet = $(".sheet");
  function closeSheet() { if (sheet) { sheet.classList.remove("is-open"); sheet.setAttribute("aria-hidden", "true"); document.body.style.overflow = ""; } }
  $$("[data-sheet-open]").forEach(function (b) { b.addEventListener("click", function () { sheet.classList.add("is-open"); sheet.setAttribute("aria-hidden", "false"); document.body.style.overflow = "hidden"; $(".sheet__close", sheet).focus(); }); });
  $$("[data-sheet-close]").forEach(function (b) { b.addEventListener("click", closeSheet); });

  /* search overlay: loads a small JSON index on first open */
  var search = $(".search"), input = $("#q"), results = $(".search__results"), index = null, active = -1;
  var norm = function (s) { return String(s).toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, ""); };
  function openSearch() {
    if (!search) return;
    closeSheet();
    search.hidden = false; document.body.style.overflow = "hidden"; input.focus();
    track("search_open");
    if (!index) fetch(input.dataset.searchUrl).then(function (r) { return r.json(); }).then(function (d) {
      index = d.map(function (row) { return { t: row[0], u: row[1], k: row[2], c: row[3], n: norm(row[0] + " " + row[3] + " " + row[2]) }; });
      run();
    });
  }
  function closeSearch() { if (search && !search.hidden) { search.hidden = true; document.body.style.overflow = ""; } }
  function run() {
    if (!index) return;
    var q = norm(input.value.trim());
    active = -1;
    if (!q) { results.innerHTML = ""; return; }
    var words = q.split(/\s+/);
    var hits = index.filter(function (r) { return words.every(function (w) { return r.n.indexOf(w) > -1; }); })
      .sort(function (a, b) { return (norm(a.t).indexOf(q) === 0 ? -1 : 0) - (norm(b.t).indexOf(q) === 0 ? -1 : 0); }).slice(0, 14);
    results.innerHTML = hits.length ? hits.map(function (r) {
      return '<li><a href="' + esc(r.u) + '"><b>' + esc(r.t) + "</b><em>" + esc(r.k.split(" · ")[0]) + "</em><small>" + esc(r.c || r.k) + "</small></a></li>";
    }).join("") : '<li class="search__empty">Nothing found for that. <a href="/plan/?from=search">Ask us instead</a> and we will reply with options.</li>';
    track("search", { q: q, hits: hits.length });
  }
  if (search) {
    input.addEventListener("input", run);
    input.addEventListener("keydown", function (e) {
      var links = $$("a", results);
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        active = Math.max(0, Math.min(links.length - 1, active + (e.key === "ArrowDown" ? 1 : -1)));
        links.forEach(function (l, i) { l.classList.toggle("is-active", i === active); });
        if (links[active]) links[active].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter" && links[active]) { window.location = links[active].href; }
    });
    search.addEventListener("click", function (e) { if (e.target === search) closeSearch(); });
    $$("[data-search-open]").forEach(function (b) { b.addEventListener("click", openSearch); });
    $$("[data-search-close]").forEach(function (b) { b.addEventListener("click", closeSearch); });
  }

  /* floating CTA menu */
  var fabToggle = fab && $(".fab__toggle", fab), fabMenu = fab && $(".fab__menu", fab);
  function closeFab() { if (fabMenu && !fabMenu.hidden) { fabMenu.hidden = true; fabToggle.setAttribute("aria-expanded", "false"); } }
  if (fabToggle) {
    fabToggle.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = fabMenu.hidden;
      fabMenu.hidden = !open; fabToggle.setAttribute("aria-expanded", String(open));
      if (open) track("fab_open");
    });
    document.addEventListener("click", function (e) { if (!e.target.closest(".fab")) closeFab(); });
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { closeAll(); closeSearch(); closeFab(); closeSheet(); }
    if (e.key === "/" && !/input|textarea|select/i.test((document.activeElement || {}).tagName || "")) { e.preventDefault(); openSearch(); }
  });

  /* hero altitude ladder: each stop swaps the photo and the card */
  var ladder = $("[data-ladder]");
  if (ladder) {
    var stops = $$(".ladder__stop", ladder), slides = $$(".hero__slide"), card = $(".ladder__card", ladder), auto, i0 = 0;
    var pick = function (i, user) {
      stops.forEach(function (s, j) { s.classList.toggle("is-on", j === i); s.setAttribute("aria-pressed", String(j === i)); });
      slides.forEach(function (s, j) { s.classList.toggle("is-on", j === i); });
      var s = stops[i];
      if (card && s) {
        card.href = s.dataset.url;
        card.innerHTML = "<small>" + esc(s.dataset.region) + "</small><b>" + esc(s.dataset.name) + " · " + esc(s.dataset.alt) + " m</b><span>" + esc(s.dataset.line) + " &rarr;</span>";
      }
      i0 = i;
      if (user) { clearInterval(auto); track("ladder", { stop: s.dataset.name }); }
    };
    stops.forEach(function (s, i) {
      s.addEventListener("click", function () { pick(i, true); });
      s.addEventListener("mouseenter", function () { pick(i, true); });
      s.addEventListener("focus", function () { pick(i, true); });
    });
    if (!reduce && stops.length > 1) auto = setInterval(function () { pick((i0 + 1) % stops.length); }, 5200);
  }

  /* finder tabs keep the type param */
  $$("[data-finder]").forEach(function (f) {
    f.addEventListener("submit", function () { $$("select, input", f).forEach(function (el) { if (!el.value && el.name !== "type") el.disabled = true; }); track("finder_submit"); });
  });

  /* package filters submit on change */
  $$("[data-autosubmit]").forEach(function (f) {
    $$("select", f).forEach(function (s) { s.addEventListener("change", function () { $$("select, input", f).forEach(function (el) { if (!el.value) el.disabled = true; }); f.submit(); }); });
  });

  /* trek chart: days (x) against highest point (y) */
  $$("[data-tchart]").forEach(function (box) {
    var pts = JSON.parse(box.dataset.points || "[]");
    if (!pts.length) return;
    var svgNS = "http://www.w3.org/2000/svg", W = 1000, H = 420, L = 64, R = 20, T = 16, B = 46;
    var maxD = Math.max.apply(null, pts.map(function (p) { return p.d; })) + 2;
    maxD = Math.ceil(maxD / 5) * 5;
    var minA = 2000, maxA = Math.ceil((Math.max.apply(null, pts.map(function (p) { return p.a; })) + 400) / 1000) * 1000;
    var X = function (d) { return L + (W - L - R) * d / maxD; };
    var Y = function (a) { return T + (H - T - B) * (1 - (a - minA) / (maxA - minA)); };
    var svg = document.createElementNS(svgNS, "svg");
    svg.setAttribute("viewBox", "0 0 " + W + " " + H); svg.setAttribute("class", "tchart__svg"); svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "Treks by number of days and highest point");
    var html = '<rect class="tchart__zone" x="' + L + '" y="' + T + '" width="' + (W - L - R) + '" height="' + (Y(5000) - T) + '"></rect>';
    for (var a = minA; a <= maxA; a += 1000) html += '<line class="tchart__grid" x1="' + L + '" x2="' + (W - R) + '" y1="' + Y(a) + '" y2="' + Y(a) + '"></line><text class="tchart__axis" x="' + (L - 10) + '" y="' + (Y(a) + 4) + '" text-anchor="end">' + a.toLocaleString("en-IN") + " m</text>";
    for (var d = 0; d <= maxD; d += 5) html += '<text class="tchart__axis" x="' + X(d) + '" y="' + (H - B + 22) + '" text-anchor="middle">' + d + "</text>";
    html += '<text class="tchart__axis" x="' + (W - R) + '" y="' + (H - 6) + '" text-anchor="end">days</text>';
    html += '<text class="tchart__axis" x="' + (L + 6) + '" y="' + (Y(5000) - 6) + '">above 5,000 m</text>';
    pts.forEach(function (p, i) {
      var jitter = ((i * 37) % 9) - 4;
      html += '<a href="' + esc(p.u) + '" class="tchart__pt" data-i="' + i + '" data-g="' + esc(p.g) + '"><circle class="tchart__dot" cx="' + (X(p.d) + jitter) + '" cy="' + Y(p.a) + '" r="8" fill="' + esc(p.c) + '" tabindex="0"></circle></a>';
    });
    svg.innerHTML = html;
    var wrap = $(".tchart__wrap", box);
    wrap.appendChild(svg);
    var tip = document.createElement("div"); tip.className = "tchart__tip"; wrap.appendChild(tip);
    var cur = doc.dataset.cur;
    $$(".tchart__pt", svg).forEach(function (a) {
      var p = pts[+a.dataset.i];
      var show = function () {
        var c = $("circle", a), rb = wrap.getBoundingClientRect(), cb = c.getBoundingClientRect();
        tip.innerHTML = "<b>" + esc(p.t) + "</b>" + esc(p.r) + " · " + p.d + " days · " + p.a.toLocaleString("en-IN") + " m · " + esc(p.g) + (p.p ? "<br>from US$" + p.p.toLocaleString("en-US") : "");
        var x = cb.left - rb.left + 14, y = cb.top - rb.top - 10;
        tip.style.left = Math.min(x, rb.width - 250) + "px"; tip.style.top = Math.max(0, y - 70) + "px"; tip.classList.add("is-on");
      };
      a.addEventListener("mouseenter", show); a.addEventListener("focusin", show);
      a.addEventListener("mouseleave", function () { tip.classList.remove("is-on"); }); a.addEventListener("focusout", function () { tip.classList.remove("is-on"); });
    });
    $$("[data-grade]", box).forEach(function (b) {
      b.addEventListener("click", function () {
        var g = b.dataset.grade;
        $$("[data-grade]", box).forEach(function (x) { x.classList.toggle("is-on", x === b); });
        $$(".tchart__pt", svg).forEach(function (a) { $("circle", a).classList.toggle("is-off", g !== "all" && a.dataset.g !== g); });
      });
    });
  });

  /* altimeter rail: reading follows scroll through the itinerary */
  var rail = $("[data-altrail]"), altRail = null;
  if (rail) {
    var max = +rail.dataset.max || 0, read = $(".altrail__read", rail), fill = $(".altrail__fill", rail), daysBox = $(".days");
    altRail = function () {
      if (!daysBox) return;
      var r = daysBox.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh * .5 - r.top) / r.height));
      var items = $$(".day", daysBox), idx = Math.min(items.length - 1, Math.floor(p * items.length));
      var alt = items[idx] ? +items[idx].dataset.alt : 0;
      if (read) read.textContent = alt.toLocaleString("en-IN") + " m";
      if (fill) fill.style.height = (max ? alt / max * 100 : 0) + "%";
      rail.classList.toggle("is-on", r.top < vh * .6 && r.bottom > vh * .3);
    };
  }

  /* expand / collapse all days */
  $$("[data-days-toggle]").forEach(function (b) {
    b.addEventListener("click", function () {
      var ds = $$(".days details"), open = ds.some(function (d) { return !d.open; });
      ds.forEach(function (d) { d.open = open; });
      b.textContent = open ? "Collapse all days" : "Expand all days";
    });
  });

  /* three-step quote wizard */
  var wiz = $("[data-wizard]");
  if (wiz) {
    var steps = $$(".step", wiz), bar = $(".wizard__bar span", wiz), labels = $$(".wizard__steps span", wiz), at = 0;
    var show = function (i) {
      steps.forEach(function (s, j) { s.hidden = j !== i; });
      labels.forEach(function (s, j) { s.classList.toggle("is-on", j <= i); });
      if (bar) bar.style.width = ((i + 1) / steps.length * 100) + "%";
      at = i; track("wizard_step", { step: i + 1 });
      var f = $("input, select, textarea", steps[i]); if (f && i) f.focus({ preventScroll: true });
    };
    $$("[data-next]", wiz).forEach(function (b) {
      b.addEventListener("click", function () {
        var bad = $$("[required]", steps[at]).filter(function (el) { return !el.checkValidity(); });
        if (bad.length) { bad[0].reportValidity(); return; }
        show(Math.min(steps.length - 1, at + 1));
      });
    });
    $$("[data-prev]", wiz).forEach(function (b) { b.addEventListener("click", function () { show(Math.max(0, at - 1)); }); });
    wiz.addEventListener("submit", function (e) {
      var phone = $("[name=phone]", wiz), email = $("[name=email]", wiz);
      if (phone && email && !phone.value.trim() && !email.value.trim()) { e.preventDefault(); phone.setCustomValidity("Leave a phone number or an email"); phone.reportValidity(); phone.setCustomValidity(""); }
    });
    show(0);
  }

  /* budget calculator */
  var calc = $("[data-calc]");
  if (calc) {
    var rate = +calc.dataset.rate || 84;
    var fmt = function (n) { return "₹" + Math.round(n).toLocaleString("en-IN"); };
    var go = function () {
      var v = function (n) { var el = $("[name=" + n + "]", calc); return el ? (el.type === "checkbox" ? (el.checked ? +el.value : 0) : +el.value) : 0; };
      var days = Math.max(1, v("days")), adults = Math.max(1, v("adults")), kids = v("kids");
      var hotel = v("hotel"), transport = v("transport"), guide = v("guide"), extras = v("heli") + v("flight") + v("permits") + v("safari") + v("rafting");
      var nights = days - 1;
      var rooms = Math.ceil(adults / 2);
      var hotelT = hotel * nights * rooms, carT = transport * days, guideT = guide * days, mealsT = 1400 * days * (adults + kids * .6), extrasT = extras * (adults + kids);
      var total = hotelT + carT + guideT + mealsT + extrasT;
      var pp = total / (adults + kids * .6);
      $("[data-out=total]", calc).textContent = fmt(total);
      $("[data-out=pp]", calc).textContent = fmt(pp) + " per person";
      $("[data-out=usd]", calc).textContent = "≈ US$" + Math.round(total / rate).toLocaleString("en-US");
      $("[data-out=rows]", calc).innerHTML = [["Hotels", hotelT], ["Car and driver", carT], ["Guide", guideT], ["Meals", mealsT], ["Flights, heli, permits, activities", extrasT]]
        .map(function (r) { return "<tr><td>" + r[0] + "</td><td>" + fmt(r[1]) + "</td></tr>"; }).join("");
      var link = $("[data-out=link]", calc);
      if (link) link.href = "/plan/?days=" + days + "&from=budget-calculator";
    };
    calc.addEventListener("input", go); calc.addEventListener("change", go); go();
  }

  /* season finder */
  var sf = $("[data-season]");
  if (sf) {
    var data = JSON.parse(sf.dataset.places || "[]"), out = $(".sf__out", sf), mSel = $("[name=m]", sf), rSel = $("[name=r]", sf);
    var draw = function () {
      var m = +mSel.value, r = rSel.value;
      var rows = data.filter(function (p) { return p.b[m] >= 1 && (!r || p.rs === r); }).sort(function (a, b) { return b.b[m] - a.b[m]; });
      out.innerHTML = rows.length ? rows.map(function (p) {
        return '<a class="sf__item" href="' + esc(p.u) + '">' + (p.i ? '<img src="' + esc(p.i) + '" alt="" loading="lazy">' : "<span></span>") + "<b>" + esc(p.n) + "</b><small>" + esc(p.r) + (p.a ? " · " + p.a.toLocaleString("en-IN") + " m" : "") + "</small><em>" + (p.b[m] === 2 ? "Best" : "Good") + "</em></a>";
      }).join("") : '<p class="empty">Few places are at their best then. Try the next month, or ask us.</p>';
    };
    mSel.addEventListener("change", draw); rSel.addEventListener("change", draw); draw();
  }

  /* altitude checker */
  var ac = $("[data-altcheck]");
  if (ac) {
    var D = JSON.parse(ac.dataset.pkgs || "{}"), sel = $("select", ac), table = $(".ac__rows", ac), summary = $(".ac__summary", ac);
    var check = function () {
      var p = D[sel.value]; if (!p) return;
      var prev = null, flags = 0;
      table.innerHTML = p.days.map(function (d) {
        var gain = prev == null ? 0 : d[2] - prev, warn = prev != null && d[2] > 3000 && gain > 500;
        if (warn) flags++;
        prev = d[2];
        return "<tr" + (warn ? ' class="is-warn"' : "") + "><td>" + d[0] + "</td><td>" + esc(d[1]) + "</td><td>" + d[2].toLocaleString("en-IN") + " m</td><td>" + (gain ? (gain > 0 ? "+" : "") + gain.toLocaleString("en-IN") + " m" : "–") + "</td><td>" + (d[3] > d[2] ? d[3].toLocaleString("en-IN") + " m" : "") + "</td><td>" + (warn ? "Gain above 500 m over 3,000 m" : (d[2] > 2500 ? "OK" : "")) + "</td></tr>";
      }).join("");
      summary.innerHTML = flags ? "<b>" + flags + " day" + (flags > 1 ? "s" : "") + "</b> sleep more than 500 m higher than the night before, above 3,000 m. That is common on fast itineraries; ask us about an extra acclimatisation day." : "<b>No big jumps.</b> Sleeping altitude never rises more than 500 m a night above 3,000 m on this itinerary.";
      $("[data-ac-link]", ac).href = p.u;
    };
    sel.addEventListener("change", check); check();
  }

  /* reveal on scroll (GSAP if present) */
  window.addEventListener("load", function () {
    onScroll();
    if (reduce || !window.gsap || !window.ScrollTrigger) { $$(".reveal").forEach(function (el) { el.style.opacity = 1; el.style.transform = "none"; }); return; }
    gsap.registerPlugin(ScrollTrigger);
    $$(".reveal").forEach(function (el) {
      gsap.to(el, { opacity: 1, y: 0, duration: .8, ease: "power3.out", scrollTrigger: { trigger: el, start: "top 88%", once: true } });
    });
    $$("[data-stagger]").forEach(function (g) {
      gsap.from(g.children, { opacity: 0, y: 28, duration: .7, ease: "power3.out", stagger: .07, scrollTrigger: { trigger: g, start: "top 85%", once: true } });
    });
    var hero = $(".hero h1");
    if (hero) gsap.from(hero, { y: 30, opacity: 0, duration: 1, ease: "power3.out" });
  });
  onScroll();
})();
