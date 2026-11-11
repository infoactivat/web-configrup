(function () {
  "use strict";

  // Google Analytics: la web actual fa servir G-6BH2K47E1S.
  // Deixa-ho buit fins a decidir si la nova web continua amb aquesta propietat o en crea una de nova.
  // Només es carrega si el visitant accepta les galetes.
  var GA_ID = "";

  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var redueix = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  $$(".any").forEach(function (e) { e.textContent = new Date().getFullYear(); });

  // Capçalera i menú mòbil
  var cap = $("header.cap");
  var onScroll = function () { if (cap) cap.classList.toggle("scrolled", window.scrollY > 8); };
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  var ham = $(".hamburguesa");
  if (ham) ham.addEventListener("click", function () {
    var obert = cap.classList.toggle("obert");
    ham.setAttribute("aria-expanded", obert);
  });

  // Enllaços pendents (p. ex. Accés clients)
  $$("[data-pendent]").forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); }); });

  // Slider principal (7 s, com a l'original)
  var slides = $$(".slide"), dots = $$(".slider-punts button"), cur = 0, timer;
  function show(i) {
    slides.forEach(function (s, j) {
      var on = j === i;
      s.classList.toggle("activa", on);
      s.setAttribute("aria-hidden", on ? "false" : "true");
      $$("a,button", s).forEach(function (b) { b.tabIndex = on ? 0 : -1; });
    });
    dots.forEach(function (d, j) { d.classList.toggle("activa", j === i); });
    cur = i;
  }
  function start() { if (!redueix && slides.length > 1) timer = setInterval(function () { show((cur + 1) % slides.length); }, 7000); }
  dots.forEach(function (d, i) { d.addEventListener("click", function () { clearInterval(timer); show(i); start(); }); });
  var slider = $(".slider");
  if (slider) {
    slider.addEventListener("mouseenter", function () { clearInterval(timer); });
    slider.addEventListener("mouseleave", function () { clearInterval(timer); start(); });
    var x0 = null;
    slider.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    slider.addEventListener("touchend", function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 40) { clearInterval(timer); show((cur + (dx < 0 ? 1 : slides.length - 1)) % slides.length); start(); }
    });
  }
  start();

  // Hero: les fotos es van canviant (5,5 s)
  $$("[data-rotar]").forEach(function (box) {
    var imgs = $$("img", box), pts = $$(".foto-punts button", box), i = 0, t;
    function ves(n) {
      imgs[i].classList.remove("activa"); if (pts[i]) pts[i].classList.remove("activa");
      i = n; imgs[i].classList.add("activa"); if (pts[i]) pts[i].classList.add("activa");
    }
    function go() { if (!redueix && imgs.length > 1) t = setInterval(function () { ves((i + 1) % imgs.length); }, 5500); }
    pts.forEach(function (b, n) { b.addEventListener("click", function () { clearInterval(t); ves(n); go(); }); });
    go();
  });

  // "Per què confiar": ressalta un motiu cada 3 s (com a l'original)
  var motius = $$("[data-llum] .motiu"), m = 0;
  if (motius.length && !redueix) setInterval(function () {
    motius[m].classList.remove("llum"); m = (m + 1) % motius.length; motius[m].classList.add("llum");
  }, 3000);

  // Aparició en fer scroll
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("vist"); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    $$(".apareix").forEach(function (e) { io.observe(e); });
  } else { $$(".apareix").forEach(function (e) { e.classList.add("vist"); }); }

  // Formularis: envien als mateixos scripts PHP que la web actual (/code/*.php al servidor).
  //  - fitxa d'assegurança -> seguros_contact_email.php (name, email, tel, seguro)
  //  - pàgina de contacte  -> contact_email.php (name, email, tel, subject, message)
  //  - la resta            -> home_contact_email.php (name, email, tel, message)
  // En obrir els fitxers en local (file://) no hi ha servidor: només es mostra l'agraïment.
  $$("form[data-form]").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var v = function (n) { var e = f.elements[n]; return e ? e.value.trim() : ""; };
      var dades = { name: v("nom"), email: v("email"), tel: v("telefon") }, url;
      if (f.elements.producte) { url = "/code/seguros_contact_email.php"; dades.seguro = v("producte"); }
      else if (f.elements.assumpte) { url = "/code/contact_email.php"; dades.subject = v("assumpte"); dades.message = v("missatge"); }
      else { url = "/code/home_contact_email.php"; dades.message = v("missatge"); }
      if (location.protocol === "file:") { f.classList.add("enviat"); return; }
      var boto = $("button[type=submit]", f); if (boto) boto.disabled = true;
      fetch(url, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: new URLSearchParams(dades).toString() })
        .then(function (r) { if (!r.ok) throw new Error(r.status); f.classList.add("enviat"); })
        .catch(function () {
          alert(document.documentElement.lang === "es"
            ? "No hemos podido enviar el formulario. Llámanos al 938 892 969 o escríbenos a info@confisergur.com."
            : "No hem pogut enviar el formulari. Truca'ns al 938 892 969 o escriu-nos a info@confisergur.com.");
        })
        .then(function () { if (boto) boto.disabled = false; });
    });
  });

  // Diàlegs
  function obreDlg(d) {
    var f = $("form", d); if (f) { f.classList.remove("enviat"); f.reset(); }
    if (typeof d.showModal === "function") d.showModal(); else d.setAttribute("open", "");
  }
  $$("dialog").forEach(function (d) {
    $$(".tancar", d).forEach(function (b) { b.addEventListener("click", function () { d.close(); }); });
    d.addEventListener("click", function (e) { if (e.target === d) d.close(); });
  });
  // Avís d'incidència de seguretat: s'obre en entrar a la web (un cop per sessió)
  var avis = $("#dlg-avis");
  if (avis) {
    $$(".tancar-avis", avis).forEach(function (b) { b.addEventListener("click", function () { avis.close(); }); });
    var vist = null; try { vist = sessionStorage.getItem("avis-inc"); } catch (e) {}
    if (!vist) setTimeout(function () {
      if ($("dialog[open]")) return;
      obreDlg(avis); try { sessionStorage.setItem("avis-inc", "1"); } catch (e) {}
    }, 0);
  }
  var simple = $("#dlg-simple");
  $$('[data-obrir="simple"]').forEach(function (b) { b.addEventListener("click", function () { obreDlg(simple); }); });

  // Fitxes d'assegurança (#coche o ?tag=coche, com a la web actual)
  var dlg = $("#dlg"), P = window.PRODUCTES || {}, IC = window.ICONES || {};
  function obrir(k) {
    var d = P[k]; if (!d || !dlg) return false;
    $("#dlg-t", dlg).textContent = d.t;
    $(".dlg-ic", dlg).innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (IC[k] || "") + "</svg>";
    var cos = $(".cos", dlg); cos.innerHTML = "";
    d.p.forEach(function (t) { var p = document.createElement("p"); p.textContent = t; cos.appendChild(p); });
    var f = $("form", dlg), hid = $('input[name="producte"]', f);
    if (!hid) { hid = document.createElement("input"); hid.type = "hidden"; hid.name = "producte"; f.appendChild(hid); }
    obreDlg(dlg);
    hid.value = d.t;
    history.replaceState(null, "", location.pathname + "#" + k);
    return true;
  }
  $$("[data-prod]").forEach(function (b) { b.addEventListener("click", function () { obrir(b.getAttribute("data-prod")); }); });
  if (dlg) {
    dlg.addEventListener("close", function () { history.replaceState(null, "", location.pathname); });
    var tag = new URLSearchParams(location.search).get("tag");
    var k = tag || location.hash.slice(1);
    if (k && P[k]) obrir(k);
  }

  // Mapa d'oficines (Leaflet + mapa base de l'ICGC, llicència CC BY 4.0).
  // L'ICGC no exigeix l'adreça de la web que demana el mapa, així que també es veu obrint els fitxers en local.
  function initMapa() {
    var el = $("#mapa"); if (!el || !window.L || !window.OFICINES || el._fet) return;
    el._fet = true;
    var map = L.map(el, { scrollWheelZoom: false });
    L.tileLayer("https://geoserveis.icgc.cat/servei/catalunya/mapa-base/wmts/estandard/MON3857NW/{z}/{x}/{y}.png", {
      minZoom: 7, maxZoom: 18, attribution: '&copy; <a href="https://www.icgc.cat" target="_blank" rel="noopener">Institut Cartogràfic i Geològic de Catalunya</a>'
    }).addTo(map);
    var marks = {}, bounds = [];
    window.OFICINES.forEach(function (o) {
      var mk = L.circleMarker([o.lat, o.lng], {
        radius: 11, weight: 3, color: "#fff", fillColor: o.pendent ? "#8e98b3" : "#0f28ff", fillOpacity: 1
      }).addTo(map);
      mk.bindPopup("<b>Configrup " + o.nom + "</b><br>" + o.adr + "<br>" + o.cp + '<br><a href="' + o.maps + '" target="_blank" rel="noopener">' + (window.TXT_MAPS || "Google Maps") + "</a>");
      marks[o.id] = mk; bounds.push([o.lat, o.lng]);
    });
    map.fitBounds(bounds, { padding: [40, 40] });
    $$(".oficina[data-of]").forEach(function (c) {
      function sel() {
        $$(".oficina").forEach(function (x) { x.classList.remove("sel"); });
        c.classList.add("sel");
        var mk = marks[c.getAttribute("data-of")];
        map.flyTo(mk.getLatLng(), 15, { duration: redueix ? 0 : 0.8 }); mk.openPopup();
        if (window.innerWidth < 980) document.getElementById("mapa").scrollIntoView({ behavior: "smooth", block: "center" });
      }
      c.addEventListener("click", function (e) { if (e.target.tagName !== "A") sel(); });
      c.addEventListener("keydown", function (e) { if (e.key === "Enter") sel(); });
    });
  }
  if ($("#mapa")) {
    if (window.L) initMapa(); else window.addEventListener("load", initMapa);
  }

  // Galetes + Google Analytics (només amb consentiment)
  function carregaGA() {
    if (!GA_ID || window.gtag) return;
    var s = document.createElement("script"); s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID; document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date()); window.gtag("config", GA_ID, { anonymize_ip: true });
  }
  var g = $(".galetes"), ok = null;
  try { ok = localStorage.getItem("galetes"); } catch (e) {}
  if (ok === "si") carregaGA();
  if (g && !ok) g.classList.add("visible");
  $$("[data-galetes]").forEach(function (b) {
    b.addEventListener("click", function () {
      var v = b.getAttribute("data-galetes");
      try { localStorage.setItem("galetes", v); } catch (e) {}
      g.classList.remove("visible");
      if (v === "si") carregaGA();
    });
  });
})();
