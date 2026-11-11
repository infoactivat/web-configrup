import json, html, os
OUT = "/mnt/project-files/web-configrup"
E = html.escape

I = {
 "car": '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
 "bike": '<circle cx="5.5" cy="17.5" r="3.5"/><circle cx="18.5" cy="17.5" r="3.5"/><path d="M15 6a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm-3 11.5V14l-3-3 4-3 2 3h2"/>',
 "moto": '<circle cx="5" cy="16" r="3"/><circle cx="19" cy="16" r="3"/><path d="M5 16h4l3-6h4l3 6M12 10l-1-3H8M16 10l-1-3h2"/>',
 "caravan": '<path d="M2 17V8a3 3 0 0 1 3-3h11a5 5 0 0 1 5 5v7h-3"/><circle cx="7" cy="17" r="2"/><path d="M9 17h7M5 9h5v4H5zM14 9h3v8"/>',
 "mountain": '<path d="m8 3 4 8 5-5 5 15H2L8 3z"/>',
 "home": '<path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
 "heart": '<path d="M19 14c1.5-1.5 3-3.2 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.8 0-3 .5-4.5 2-1.5-1.5-2.7-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4 3 5.5l7 7z"/><path d="M3.2 12h4.3l1.5-3 3 6 1.5-3h7.3"/>',
 "bandage": '<path d="M10 10.01h.01M10 14.01h.01M14 10.01h.01M14 14.01h.01M18 6v12M6 6v12"/><rect x="2" y="6" width="20" height="12" rx="2"/>',
 "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4M8 6h.01M16 6h.01M12 6h.01M12 10h.01M12 14h.01M16 10h.01M16 14h.01M8 10h.01M8 14h.01"/>',
 "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
 "flower": '<path d="M12 7.5a4.5 4.5 0 1 1 4.5 4.5M12 7.5A4.5 4.5 0 1 0 7.5 12M12 7.5V9m-4.5 3a4.5 4.5 0 1 0 4.5 4.5M7.5 12H9m7.5 0a4.5 4.5 0 1 1-4.5 4.5m4.5-4.5H15m-3 4.5V15"/><circle cx="12" cy="12" r="3"/>',
 "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
 "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
 "paw": '<circle cx="11" cy="4" r="2"/><circle cx="18" cy="8" r="2"/><circle cx="20" cy="16" r="2"/><path d="M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z"/>',
 "boat": '<path d="M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M19.38 20A11.6 11.6 0 0 0 21 14l-9-4-9 4c0 2.9.94 5.34 2.81 7.76M19 13V7a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v6M12 10v4M12 2v3"/>',
 "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M15 22v-4a2 2 0 0 0-2-2h-2a2 2 0 0 0-2 2v4M2 7h20M22 7v3a2 2 0 0 1-2 2 2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 16 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 12 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 8 12a2.7 2.7 0 0 1-1.59-.63.7.7 0 0 0-.82 0A2.7 2.7 0 0 1 4 12a2 2 0 0 1-2-2V7"/>',
 "factory": '<path d="M2 20a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V8l-7 5V8l-7 5V4a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2Z"/><path d="M17 18h1M12 18h1M7 18h1"/>',
 "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1ZM2 16l3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1ZM7 21h10M12 3v18M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
 "brief": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
 "cyber": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
 "clipboard": '<rect x="8" y="2" width="8" height="4" rx="1"/><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2M9 14l2 2 4-4"/>',
 "hardhat": '<path d="M2 18a1 1 0 0 0 1 1h18a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1H3a1 1 0 0 0-1 1v2zM10 10V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v5M4 15v-3a6 6 0 0 1 6-6M14 6a6 6 0 0 1 6 6v3"/>',
 "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
 "truck": '<path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2M15 18H9M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.62l-3.48-4.35A1 1 0 0 0 17.52 8H14"/><circle cx="17" cy="18" r="2"/><circle cx="7" cy="18" r="2"/>',
 "medal": '<path d="M7.21 15 2.66 7.14a2 2 0 0 1 .13-2.2L4.4 2.8A2 2 0 0 1 6 2h12a2 2 0 0 1 1.6.8l1.6 2.14a2 2 0 0 1 .14 2.2L16.79 15M11 12 5.12 2.2M13 12l5.88-9.8M8 7h8"/><circle cx="12" cy="17" r="5"/>',
 "handshake": '<path d="m11 17 2 2a1 1 0 1 0 3-3"/><path d="m14 14 2.5 2.5a1 1 0 1 0 3-3l-3.88-3.88a3 3 0 0 0-4.24 0l-.88.88a1 1 0 1 1-3-3l2.81-2.81a5.79 5.79 0 0 1 7.06-.87l.47.28a2 2 0 0 0 1.42.25L21 4"/><path d="m21 3 1 11h-2M3 3 2 14l6.5 6.5a1 1 0 1 0 3-3M3 4h8"/>',
 "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
 "star": '<path d="M11.5 2.3a.5.5 0 0 1 .9 0l2.3 4.7a2 2 0 0 0 1.6 1.1l5.2.8a.5.5 0 0 1 .3.8l-3.8 3.7a2 2 0 0 0-.6 1.9l.9 5.2a.5.5 0 0 1-.8.5l-4.6-2.4a2 2 0 0 0-2 0l-4.6 2.4a.5.5 0 0 1-.8-.5l.9-5.2a2 2 0 0 0-.6-1.9L2.2 9.8a.5.5 0 0 1 .3-.9l5.2-.8a2 2 0 0 0 1.6-1.1z"/>',
 "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path d="M8 12h.01M12 12h.01M16 12h.01"/>',
 "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/>',
 "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
 "pin": '<path d="M20 10c0 4.99-5.54 10.19-7.4 11.8a1 1 0 0 1-1.2 0C9.54 20.19 4 14.99 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
 "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
 "arrow": '<path d="M5 12h14M12 5l7 7-7 7"/>',
 "x": '<path d="M18 6 6 18M6 6l12 12"/>',
 "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
 "plus": '<path d="M5 12h14M12 5v14"/>',
}
def ic(n): return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

SOC = {
 "linkedin": ("https://www.linkedin.com/company/confisergur-corredoria-d-assegurances", '<path d="M20.45 20.45h-3.55v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.12 2.06 2.06 0 0 1 0 4.12zM7.12 20.45H3.56V9h3.56v11.45z"/>'),
 "instagram": ("https://instagram.com/confisergur", '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 3.25.15 4.77 1.69 4.92 4.92.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.15 3.23-1.66 4.77-4.92 4.92-1.27.06-1.64.07-4.85.07s-3.58-.01-4.85-.07c-3.26-.15-4.77-1.7-4.92-4.92C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85C2.38 3.92 3.9 2.38 7.15 2.23 8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 2.7.27.27 2.69.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.2 4.36 2.62 6.78 6.98 6.98C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c4.35-.2 6.78-2.62 6.98-6.98.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.2-4.35-2.62-6.78-6.98-6.98C15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/>'),
 "facebook": ("https://www.facebook.com/Confisergur/", '<path d="M24 12.07C24 5.41 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.04V9.41c0-3.02 1.8-4.7 4.54-4.7 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.5 0-1.96.93-1.96 1.89v2.26h3.32l-.53 3.5h-2.8V24C19.62 23.1 24 18.1 24 12.07"/>'),
 "x": ("https://twitter.com/confisergur", '<path d="M18.9 1.15h3.68l-8.04 9.19L24 22.85h-7.4l-5.8-7.58-6.64 7.58H.48l8.6-9.83L0 1.15h7.59l5.24 6.93 6.07-6.93zm-1.29 19.5h2.04L6.48 3.24H4.3l13.31 17.41z"/>'),
}
WA = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.07-.3-.15-1.26-.46-2.4-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.62-.92-2.21-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.07.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.18-1.41-.07-.12-.27-.2-.57-.35zM12.05 21.8h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.51-5.26c0-5.45 4.44-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.88 9.88zm8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.31-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.9 0-3.18-1.24-6.16-3.49-8.41z"/></svg>'

TEL = "938 892 969"; TEL_H = "tel:+34938892969"
MAIL = "info@confisergur.com"
WA_URL = "https://api.whatsapp.com/send?phone=34620957920&text=Hola%2C%20voldria%20fer%20una%20consulta."
MAPS = "https://goo.gl/maps/mGQ9cpg4AagAHEQAA"

def head(title, desc, actiu):
    nav = [("index.html","Inici"),("assegurances.html","Assegurances"),("nosaltres.html","Nosaltres")]
    links = "".join(f'<a href="{h}"{" class=\"actiu\" aria-current=\"page\"" if h==actiu else ""}>{t}</a>' for h,t in nav)
    return f'''<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0f28ff">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="img/configrup-logo.png">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/estil.css">
</head>
<body>
<div class="topbar"><div class="wrap">
  <span class="esquerra">Corredoria d'assegurances a Vic · Independència, objectivitat i transparència</span>
  <span class="dreta"><a href="{TEL_H}">{ic("phone")}Truca'ns {TEL}</a><a href="mailto:{MAIL}" class="esquerra">{ic("mail")}{MAIL}</a></span>
</div></div>
<header class="cap"><div class="wrap">
  <a class="logo" href="index.html" aria-label="Configrup, inici"><img src="img/configrup-logo.png" alt="ConfiGrup Corredoria d'assegurances" width="832" height="257"></a>
  <nav class="menu" id="menu">{links}<a href="contacte.html" class="btn btn-blau{" actiu" if actiu=="contacte.html" else ""}">Contacte {ic("arrow")}</a></nav>
  <button class="hamburguesa" aria-label="Obrir el menú" aria-expanded="false" aria-controls="menu"><span></span></button>
</div></header>
<main>
'''

def foot():
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n.capitalize()}"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg></a>' for n,(u,p) in SOC.items())
    return f'''</main>
<footer class="peu"><div class="wrap">
  <div class="peu-grid">
    <div>
      <img class="logo-peu" src="img/configrup-logo-negatiu.png" alt="ConfiGrup" width="832" height="257">
      <p>Som corredors d'assegurances. Treballem amb total independència per oferir-te sempre la millor solució.</p>
      <div class="xarxes">{soc}</div>
    </div>
    <div><h4>Enllaços</h4><ul>
      <li><a href="index.html">Inici</a></li><li><a href="assegurances.html">Assegurances</a></li>
      <li><a href="nosaltres.html">Nosaltres</a></li><li><a href="contacte.html">Contacte</a></li>
    </ul></div>
    <div><h4>Legal</h4><ul>
      <li><a href="legal.html#avis-legal">Avís legal</a></li><li><a href="legal.html#privacitat">Privacitat</a></li>
      <li><a href="legal.html#cookies">Cookies</a></li><li><a href="legal.html#transparencia">Transparència</a></li>
      <li><a href="legal.html#canal-denuncies">Canal de denúncies</a></li>
    </ul></div>
    <div><h4>Contacte</h4><ul>
      <li>Carrer Camí de la Tolosa, 9 desp. 6<br>08500 Vic (Edifici Tolosa)</li>
      <li><a href="mailto:{MAIL}">{MAIL}</a></li>
      <li><a href="{TEL_H}">{TEL}</a></li>
      <li><a href="{MAPS}" target="_blank" rel="noopener">Obrir a Google Maps →</a></li>
    </ul></div>
  </div>
  <div class="peu-baix"><span>© <span class="any">2026</span> Configrup. Tots els drets reservats.</span><span>Corredoria d'assegurances · Vic</span></div>
</div></footer>
<a class="whatsapp" href="{WA_URL}" target="_blank" rel="noopener" aria-label="Escriu-nos per WhatsApp">{WA}</a>
<div class="galetes" role="dialog" aria-label="Avís de galetes">
  <strong>Fem servir galetes</strong>
  <p>Fem servir galetes i altres tecnologies de seguiment per millorar la teva experiència de navegació al nostre lloc web, per mostrar-te contingut personalitzat i anuncis interessants per a tu, per analitzar el nostre trànsit i entendre d'on venen els nostres visitants. <a href="legal.html#cookies" class="blau">Més informació</a></p>
  <div class="bts"><button class="btn btn-blau" data-galetes="si">Estic d'acord</button><button class="btn btn-linia" data-galetes="no">Declino</button></div>
</div>
<script src="js/principal.js"></script>
</body>
</html>
'''

FORM_CHECK = '<label class="check"><input type="checkbox" required> <span>He llegit i accepto la <a href="legal.html#privacitat">Política de privacitat</a>.</span></label>'
def form(missatge=True, assumpte=False, boto="Enviar"):
    return f'''<form class="form" data-form>
  <div class="camps form">
    <div><label>Nom i cognoms</label><input name="nom" required autocomplete="name"></div>
    <div class="doble"><div><label>Email</label><input type="email" name="email" required autocomplete="email"></div>
    <div><label>Telèfon</label><input type="tel" name="telefon" required autocomplete="tel"></div></div>
    {'<div><label>Assumpte</label><input name="assumpte"></div>' if assumpte else ''}
    {'<div><label>Missatge</label><textarea name="missatge"></textarea></div>' if missatge else ''}
    {FORM_CHECK}
    <button class="btn btn-blau" type="submit">{boto} {ic("arrow")}</button>
  </div>
  <div class="gracies" role="status"><strong>Moltes gràcies per contactar amb nosaltres</strong>Ens posarem en contacte amb tu el més aviat possible.</div>
</form>'''

# ---------- Productes ----------
PART = [
 ("cotxe","car","Assegurança de cotxe","Necessites una assegurança pel teu cotxe nou? Has de renovar la teva assegurança de cotxe?",["A Configrup t'assessorem sobre les cobertures que més et convenen, comparem amb les millors companyies per oferir-te la millor assegurança de cotxe per a tu, amb les millors cobertures i al millor preu. A més, estem al teu costat davant qualsevol imprevist, realitzant totes les gestions amb la companyia per tu."]),
 ("moto","moto","Assegurança de moto","Necessites una assegurança de moto que s'adapti a les teves necessitats?",["A Configrup treballem amb les companyies líders en el sector. Negociem amb elles per oferir-te les millors cobertures, sempre al millor preu, perquè gaudeixis dels teus viatges en moto amb total seguretat."]),
 ("autocaravana","caravan","Assegurança de Camper / Autocaravana","Si el que busques és una assegurança per la teva casa rodant, tenim LA TEVA ASSEGURANÇA!",["Som especialistes en assegurances per campers i autocaravanes. La nostra experiència ens ha permès crear la millor assegurança d'autocaravana i camper, amb cobertures exclusives perquè tu només t'hagis de preocupar de gaudir-la al màxim."]),
 ("caravana","caravan","Assegurança de Caravana","",["Les nostres assegurances per a caravanes t'ofereixen les millors cobertures per la teva casa rodant, perquè tu només hagis d'escollir el destí.","La nostra experiència en el sector ens ha permès conèixer les necessitats que poden sorgir quan viatges amb la teva caravana, i així poder-te oferir les millors cobertures per viatjar segur."]),
 ("offroad","mountain","Assegurança d'Off Road","A Configrup tenim la millor assegurança pel teu vehicle Off Road.",["Som conscients que es tracta d'un vehicle especial, amb el que busques aventures i bons moments. Nosaltres t'oferim l'assegurança ideal perquè el puguis gaudir al màxim."]),
 ("llar","home","Assegurança de Llar","Necessites una assegurança per casa teva? Necessites una assegurança pel teu pis de lloguer?",["A Configrup analitzem el teu cas i t'assessorem sobre les cobertures que necessites per estar ben protegit. T'oferim la millor assegurança per la teva llar, aquella que s'adapta a les teves necessitats i al millor preu. A més, revisem periòdicament la pòlissa perquè sempre estiguis ben cobert davant qualsevol imprevist."]),
 ("salut","heart","Assegurança de Salut","",["A Configrup t'oferim només les millors assegurances de salut, les que tenen les millors cobertures als millors preus, perquè sabem que la salut és el més important.","Protegeix la teva salut i la de la teva família amb una assegurança mèdica que et respongui de manera eficient i ràpida sempre que ho necessitis, i amb un quadre mèdic a prop teu."]),
 ("accidents","bandage","Assegurança d'Accidents","Estàs buscant una assegurança d'accidents?",["A Configrup sabem l'important que és estar ben protegit davant qualsevol accident.","Els nostres professionals compten amb l'experiència necessària per assessorar-te sobre quina és la millor assegurança d'accidents per a tu. Treballem amb les millors companyies per oferir-te les assegurances d'accidents més completes, amb les millors cobertures i sempre al millor preu."]),
 ("comunitat","building","Assegurança de Comunitat de Propietaris","Ets administrador o administradora d'una comunitat de veïns? Necessites una assegurança per a la vostra comunitat?",["Les comunitats de propietaris necessiten una assegurança que els cobreixi davant qualsevol eventualitat.","A Configrup sabem que cada comunitat és diferent, per això analitzem el vostre cas i us proporcionem l'assegurança que millor s'adapti a les vostres necessitats."]),
 ("vida","users","Assegurança de Vida","Estàs buscant una assegurança de vida?",["A Configrup treballem amb les millors companyies, comparem i negociem amb elles per proporcionar-te l'assegurança de vida que millor s'adapta a les teves necessitats.","Perquè no totes les assegurances de vida són iguals, l'equip de professionals de Configrup t'assessorem sobre quina és l'assegurança de vida ideal per a tu."]),
 ("decessos","flower","Assegurança de Decessos","",["L'assegurança de decessos protegeix els teus familiars davant la delicada situació emocional que suposa gestionar tots els tràmits legals de la defunció d'un ésser estimat. Aquesta assegurança cobreix les despeses del servei fúnebre i es responsabilitza dels tràmits administratius, i així allibera els familiars de totes aquestes gestions en aquests moments tan delicats.","A Configrup t'ajudem a trobar la pòlissa de decessos que millor s'adapti a les teves circumstàncies i garanteixi la tranquil·litat dels teus familiars."]),
 ("viatge","plane","Assegurança de Viatge","Estàs planificant un viatge? Busques una assegurança de viatge per poder viatjar amb total tranquil·litat?",["Cada viatge és diferent i cada viatger també. Per això a Configrup t'assessorem sobre quina és l'assegurança de viatge que necessites. Treballem amb les millors companyies especialitzades per oferir-te l'assegurança de viatge que millor s'adapti a tu i al millor preu."]),
 ("lloguer","key","Assegurança d'Impagament de Lloguer","Si ets propietari d'un immoble i tens pensat llogar-lo, a Configrup tenim la solució ideal per a tu.",["L'assegurança d'impagament de lloguer és el millor aliat per protegir la teva propietat contra danys i per assegurar l'impagament dels lloguers. Lloga amb la màxima seguretat!"]),
 ("mascotes","paw","Assegurança de Mascotes","Si estimes la teva mascota com un membre més de la teva família, protegeix-la amb la millor assegurança de mascotes.",["T'oferim diferents opcions de cobertura i t'ajudem a escollir quina és l'assegurança de mascotes que millor s'adapta al teu estimat amic."]),
 ("bicicletes","bike","Assegurança de Bicicletes i Patinets","La vida canvia. La manera de desplaçar-nos també.",["Una mobilitat més respectuosa amb el medi ambient és responsabilitat de tots.","A Configrup som conscients d'això i per aquest motiu t'oferim una àmplia varietat d'assegurances per a bicicletes i patinets, siguin elèctrics o no, amb les millors cobertures i al millor preu."]),
 ("embarcacions","boat","Assegurança d'Embarcacions Recreatives","Tens alguna embarcació amb la qual gaudeixes de la teva passió pel mar?",["A Configrup t'oferim l'assegurança a mida perquè tu decideixis el nivell de cobertura que li vulguis donar. Màxima seguretat i tranquil·litat perquè gaudeixis al màxim de la navegació."]),
]
EMP = [
 ("comerc","store","Assegurança de Comerç","Sabem que el teu negoci és el projecte dels teus somnis. En ell hi destines molts esforços i il·lusions.",["A Configrup t'oferim les assegurances que millor s'adapten al teu negoci. Màxima protecció i cobertures perquè tu només pensis en assolir l'èxit empresarial."]),
 ("pime","factory","Assegurança de PIME","",["Estar al capdavant d'una empresa requereix focalitzar-se en el bon funcionament, adoptant els ajustos necessaris, prenent decisions i adaptant-se als canvis constants del mercat.","La nostra experiència en assegurances per a empreses ens converteix en el millor aliat per a la seva protecció, continuïtat i èxit."]),
 ("responsabilitat","scale","Assegurança de Responsabilitat Civil","",["L'activitat de les empreses s'exposa a certs riscos necessaris per assolir l'èxit, però que poden ocasionar danys a tercers, tant materials com personals.","Les nostres assegurances de responsabilitat civil ofereixen la tranquil·litat de no comprometre la viabilitat i futur de les empreses que confien en nosaltres."]),
 ("do","brief","Assegurança de D&O","",["Les decisions preses des dels equips directius poden arribar a generar responsabilitats que afectin el patrimoni dels seus integrants.","L'assegurança D&O protegeix davant els riscos que poden comportar determinats càrrecs directius i dona protecció davant les conseqüències de les seves decisions.","A Configrup us assessorem sobre quina és l'assegurança de D&O que millor s'adapta a la vostra organització, oferint-vos totes les gestions de contractació i seguiment."]),
 ("ciber","cyber","Assegurança Ciber","",["La tecnologia ha proporcionat agilitat, eficiència i connectivitat en l'activitat de les empreses, però també ha generat nous riscos als quals estan exposades.","La demanda d'assegurances contra ciberriscos creix de manera exponencial en els últims anys. La nostra experiència ens ha ensenyat que l'assegurança ciber és una de les imprescindibles per a qualsevol organització d'avui en dia, independentment de la seva mida o activitat."]),
 ("baixa","clipboard","Assegurança de Baixa Laboral","",["No hi ha dubte que les assegurances de baixa laboral són un imprescindible per als treballadors autònoms.","Ajuden a mantenir el nivell d'ingressos i fer front a les despeses fixes recurrents del teu negoci, assegurant així la seva continuïtat."]),
 ("conveni","bandage","Assegurança d'Accidents Conveni","",["L'assegurança d'accidents conveni dona compliment a la normativa de determinats convenis col·lectius.","A Configrup t'oferim la millor opció d'assegurança d'accidents de conveni perquè no t'hagis de preocupar. Realitzem els tràmits de contractació i gestió perquè els teus treballadors estiguin sempre ben protegits i la teva empresa compleixi amb el conveni establert."]),
 ("salut-empresa","heart","Assegurança de Salut","",["Cada vegada hi ha més empreses que aposten per millors beneficis socials, econòmics i emocionals per als seus treballadors.","Les assegurances de salut col·lectives afavoreixen un bon clima laboral, incrementen la satisfacció i productivitat dels treballadors i reforcen el compromís amb l'empresa.","Els nostres professionals assessoren la vostra empresa a trobar aquella assegurança de salut col·lectiva que millor s'adapti a les vostres singularitats i necessitats."]),
 ("mediambiental","leaf","Assegurança de Responsabilitat Mediambiental","",["Tota activitat empresarial té major o menor impacte mediambiental. La Llei de Responsabilitat Mediambiental pretén assegurar que qualsevol operador econòmic pugui disposar dels recursos econòmics suficients per poder fer front a les despeses derivades dels danys que pogués provocar la seva activitat en el medi ambient.","Els nostres experts us assessoraran sobre quina pòlissa de responsabilitat mediambiental requereix la vostra empresa, per així complir amb la legislació vigent."]),
 ("construccio","hardhat","Assegurança de Tot Risc Construcció","",["L'objectiu fonamental de l'assegurança de tot risc construcció és protegir contra els danys i pèrdues accidentals que l'obra pugui ocasionar, així com contra reclamacions de tercers per danys personals o materials.","A Configrup no volem que cap contratemps impedeixi acabar la teva obra. Per això treballem amb companyies especialitzades en assegurances de la construcció, que protegeixen de la millor manera els riscos que puguin esdevenir."]),
 ("decennal","home","Assegurança Decennal","",["L'assegurança decennal és una garantia per a qualsevol comprador d'un nou habitatge i d'obligada contractació per part del promotor.","Ofereix tranquil·litat i seguretat en la promoció d'habitatges per als futurs compradors, és sinònim de prestigi i reconeixement de bona praxi.","A Configrup treballem amb companyies líders en el sector per oferir-te les millors opcions d'assegurança decennal del mercat, proporcionant-te assessorament i realitzant tots els tràmits i gestions amb la companyia."]),
 ("transports","truck","Assegurança de Transports","",["Protegir les mercaderies de tercers davant l'ocurrència de diversos riscos que puguin esdevenir durant tot el procés de transport, ja sigui per via fluvial, ferroviària, aèria o marítima, és l'essència de l'assegurança de transports.","A Configrup analitzem de manera personalitzada les teves necessitats i busquem la millor solució perquè les mercaderies arribin sempre a bon port amb la millor assegurança de transport, la qual et respongui de manera eficient davant qualsevol imprevist."]),
]
COMP = ['allianz','arag','asefa','axa','calife','catalana','cosalud','crouco','dkv','fiatc','generali','liberty','markel','mmt','mussap','mutuacat','plus','prevision','reale','vital','zurich']

def w(name, s):
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)

# ---------- INICI ----------
slides = [
 ("car","Condueix tranquil. Nosaltres ens cuidem de tot.","La teva assegurança de cotxe o moto amb les millors cobertures i al millor preu.","assegurances.html#cotxe","Saber-ne més"),
 ("heart","El més important, la salut.","Cuida dels teus amb les millors assegurances de salut.","assegurances.html#salut","Consulta'ns"),
 ("home","La teva llar sempre ben protegida.","Sabem que casa teva és el teu refugi, per això t'ajudem a protegir-la.","assegurances.html#llar","Saber-ne més"),
 ("users","Assegura la teva vida per protegir el seu futur.","T'ajudem a protegir-los quan més ho necessitin.","assegurances.html#vida","Consulta'ns"),
]
hero_cards = "".join(f'''<div class="targeta-hero{" activa" if i==0 else ""}" aria-hidden="{"false" if i==0 else "true"}"><div class="icona-gran">{ic(a)}</div><h3>{E(b)}</h3><p>{E(c)}</p><a class="btn btn-blanc" href="{d}" tabindex="{0 if i==0 else -1}">{e} {ic("arrow")}</a></div>''' for i,(a,b,c,d,e) in enumerate(slides))
punts = "".join(f'<button aria-label="Diapositiva {i+1}"{" class=\"activa\"" if i==0 else ""}></button>' for i in range(len(slides)))

def links(items):
    return "".join(f'<a href="{h}"{" target=\"_blank\" rel=\"noopener\"" if h.startswith("http") else ""}>{ic(i)}{t}</a>' for i,t,h in items)

motius = ["Estem al teu costat. T'escoltem i realitzem, per tu, totes les gestions amb la companyia, defensant sempre els teus interessos.",
 "Només treballem amb les millors companyies, aquelles que ens ofereixen la confiança i seguretat necessàries per als nostres clients.",
 "Busquem la millor assegurança segons els teus interessos. Perquè la millor assegurança és la que millor s'adapta a les teves necessitats.",
 "Treballem amb independència, objectivitat i transparència, això ens permet oferir-te la millor opció d'assegurança.",
 "Posem tota la nostra experiència al teu servei perquè sempre estiguis ben atès davant qualsevol consulta."]
logos = "".join(f'<img src="img/companyies/{c}.jpg" alt="{c.capitalize()}" width="150" height="75">' for c in COMP)

index = head("Configrup · Corredoria d'assegurances a Vic", "Configrup és una corredoria d'assegurances a Vic. Assegurances per a particulars i empreses amb les millors companyies, amb independència, objectivitat i transparència.", "index.html") + f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="etiqueta">Corredoria d'assegurances</span>
    <h1>Som especialistes en <span class="blau">confiança i seguretat</span></h1>
    <p class="intro">A Configrup t'oferim l'assegurança que millor s'adapta a tu, amb les cobertures necessàries per a cada moment. I el més important: estem al teu costat quan ho necessites.</p>
    <div class="accions"><a class="btn btn-blau" href="assegurances.html">Descobreix les assegurances {ic("arrow")}</a><a class="btn btn-linia" href="#parlem">Et truquem</a></div>
  </div>
  <div>
    <div class="hero-rotatiu" aria-live="polite">{hero_cards}</div>
    <div class="punts">{punts}</div>
  </div>
</div></section>

<section class="seccio alt"><div class="wrap">
  <div class="cap-seccio apareix">
    <div><span class="etiqueta">La nostra essència</span><h2>Confiança, seguretat i servei</h2></div>
    <p>Tres valors que defineixen la manera com treballem amb cadascun dels nostres clients, cada dia.</p>
  </div>
  <div class="valors">
    <div class="valor apareix"><div class="ic">{ic("handshake")}</div><small>CONFIANÇA</small><h3>Parlem amb confiança</h3><p>La nostra relació amb els clients es fonamenta en el respecte, la responsabilitat i la confidencialitat.</p></div>
    <div class="valor apareix"><div class="ic">{ic("shield")}</div><small>SEGURETAT</small><h3>Oferim seguretat</h3><p>Treballem des de la professionalitat per proporcionar tranquil·litat a tots els nostres clients.</p></div>
    <div class="valor apareix"><div class="ic">{ic("star")}</div><small>SERVEI</small><h3>Vocació de servei</h3><p>Tots els nostres esforços estan orientats a aconseguir l'excel·lència en una gestió solvent.</p></div>
  </div>
</div></section>

<section class="seccio"><div class="wrap bloc">
  <div class="bloc-img apareix"><img src="img/img_particulares.jpg" alt="Família sota un sostre simbòlic a casa" width="600" height="382" loading="lazy"><div class="xip"><span class="ic">{ic("user")}</span>Per a tu i els teus</div></div>
  <div class="apareix">
    <span class="etiqueta">Particulars</span>
    <h2>Assegurances per a particulars</h2>
    <p><strong>Totes les persones som diferents, les assegurances també.</strong></p>
    <p>Busques una assegurança per al teu cotxe, moto, salut, vida o llar? T'oferim la millor solució asseguradora per cobrir totes les teves necessitats.</p>
    <div class="llista-prod">{links([("car","Assegurança Auto","assegurances.html#cotxe"),("home","Assegurança Llar","assegurances.html#llar"),("users","Assegurança Vida","assegurances.html#vida"),("caravan","Assegurança Autocaravana","https://conficaravan.com/")])}</div>
    <a class="btn btn-linia" href="assegurances.html?tipus=particulars">Descobreix-les totes {ic("arrow")}</a>
  </div>
</div></section>

<section class="wrap" id="parlem">
  <div class="cta apareix">
    <div><h2>Parlem?</h2><p>Contactem amb tu i t'ajudem a trobar la teva assegurança.</p></div>
    <a class="btn btn-blanc" href="contacte.html">Et truquem {ic("phone")}</a>
  </div>
</section>

<section class="seccio"><div class="wrap bloc invers">
  <div class="bloc-img apareix"><img src="img/img_empresas.jpg" alt="Reunió d'assessorament amb una clienta" width="600" height="382" loading="lazy"><div class="xip"><span class="ic">{ic("brief")}</span>Pla 100% personalitzat</div></div>
  <div class="apareix">
    <span class="etiqueta">Empreses i autònoms</span>
    <h2>Assegurances per a empreses</h2>
    <p><strong>Les empreses evolucionen i s'enfronten a nous reptes. Nosaltres estem al teu costat per cobrir els riscos.</strong></p>
    <p>Assessorem empreses i autònoms sobre les millors cobertures i creem un pla 100% personalitzat.</p>
    <div class="llista-prod">{links([("store","Assegurança Comerç","assegurances.html#comerc"),("factory","Assegurança PIME","assegurances.html#pime"),("clipboard","Assegurança Baixa laboral","assegurances.html#baixa"),("scale","Responsabilitat civil","assegurances.html#responsabilitat")])}</div>
    <a class="btn btn-linia" href="assegurances.html?tipus=empreses">Descobreix-les totes {ic("arrow")}</a>
  </div>
</div></section>

<section class="seccio alt"><div class="wrap">
  <div class="cap-seccio apareix">
    <div><span class="etiqueta">Per què nosaltres</span><h2>Per què confiar en Configrup?</h2></div>
    <div><p>La nostra experiència i professionalitat al teu servei.</p><p style="margin-top:14px"><a class="blau" href="nosaltres.html"><strong>Sobre nosaltres →</strong></a></p></div>
  </div>
  <div class="motius">{"".join(f'<div class="motiu apareix"><p>{E(m)}</p></div>' for m in motius)}</div>
</div></section>

<section class="seccio"><div class="wrap companyies">
  <div class="apareix">
    <span class="etiqueta">Les millors companyies al teu servei</span>
    <h2>Som corredors d'assegurances</h2>
    <p class="intro">Això ens permet treballar amb total independència per oferir-te sempre la millor solució, realitzant totes les gestions de les teves assegurances.</p>
  </div>
  <div class="carrusel apareix" aria-label="Companyies amb què treballem"><div class="pista">{logos}{logos.replace('alt="', 'aria-hidden="true" alt="')}</div></div>
</div></section>
''' + foot()
w("index.html", index)

# ---------- ASSEGURANCES ----------
def cards(lst):
    return "".join(f'<button class="prod" data-prod="{k}"><span class="ic">{ic(i)}</span><h3>{E(t)}</h3><span class="mes">Més informació {ic("arrow")}</span></button>' for k,i,t,q,p in lst)
altre = f'<a class="prod altre" href="contacte.html"><span class="ic">{ic("plus")}</span><h3>Busques algun altre tipus d\'assegurança?</h3><p>Explica\'ns què necessites i et proporcionarem una solució a mida.</p><span class="mes">T\'ajudem {ic("arrow")}</span></a>'
dades = {k:{"t":t,"q":q,"p":p,"i":i} for k,i,t,q,p in PART+EMP}
ass = head("Assegurances per a particulars i empreses · Configrup", "Assegurances de cotxe, moto, autocaravana, llar, salut, vida, comerç, PIME, responsabilitat civil, ciber i moltes més. Com a corredors treballem amb les millors companyies.", "assegurances.html") + f'''
<section class="cap-pagina"><div class="wrap">
  <span class="etiqueta">Assegurances</span>
  <h1>Quina assegurança necessites?</h1>
  <div class="pestanyes" role="tablist">
    <button role="tab" id="t-part" aria-controls="p-part" aria-selected="true">Sóc particular</button>
    <button role="tab" id="t-emp" aria-controls="p-emp" aria-selected="false">Sóc empresa</button>
  </div>
</div></section>
<section class="seccio" style="padding-top:40px"><div class="wrap">
  <div class="panell" id="p-part" role="tabpanel" aria-labelledby="t-part">
    <div class="intro-panell"><h2>Assegurances per a particulars</h2><p class="intro">T'oferim les millors assegurances perquè tu i els teus estigueu sempre ben protegits. Com a corredors treballem amb les millors companyies per proporcionar-te la millor solució asseguradora en cada moment.</p></div>
    <div class="graella">{cards(PART)}{altre}</div>
  </div>
  <div class="panell" id="p-emp" role="tabpanel" aria-labelledby="t-emp" hidden>
    <div class="intro-panell"><h2>Assegurances per a empreses</h2><p class="intro">Els negocis s'enfronten a multitud de riscos amb la seva activitat empresarial. Els nostres professionals especialitzats en assegurances per a empreses analitzen els vostres riscos per oferir-vos la millor solució asseguradora per al vostre negoci.</p></div>
    <div class="graella">{cards(EMP)}{altre}</div>
  </div>
</div></section>
<section class="wrap" style="padding-bottom:100px">
  <div class="cta"><div><h2>Necessites assessorament?</h2><p>El nostre equip de professionals és aquí per ajudar-te.</p></div><a class="btn btn-blanc" href="contacte.html">Consulta'ns {ic("arrow")}</a></div>
</section>
<dialog id="dlg" aria-labelledby="dlg-t">
  <div class="dlg">
    <div class="dlg-text"><h2 id="dlg-t"></h2><p class="preg"></p><div class="cos"></div></div>
    <div class="dlg-form"><button class="tancar" aria-label="Tancar">{ic("x")}</button>
      <h3>Ens posarem en contacte amb tu</h3><p>Emplena el formulari i ens posarem en contacte amb tu.</p>
      {form(missatge=False, boto="Contacta'ns")}
    </div>
  </div>
</dialog>
<script>window.PRODUCTES={json.dumps(dades, ensure_ascii=False)};</script>
''' + foot()
w("assegurances.html", ass)

# ---------- NOSALTRES ----------
nos = head("Sobre nosaltres · Configrup", "Configrup és la corredoria d'assegurances que treballa per oferir-te la millor solució asseguradora, amb un tracte personalitzat.", "nosaltres.html") + f'''
<section class="cap-pagina"><div class="wrap">
  <span class="etiqueta">Sobre nosaltres</span>
  <h1>Creixem junts</h1>
  <p class="intro">La nostra professionalitat, solvència i ètica ens defineixen.</p>
</div></section>
<section class="seccio" style="padding-top:40px"><div class="wrap text-llarg">
  <p class="xifra-cita apareix">Confiança, seguretat i servei: <span class="blau">treballem cada dia per oferir-te el millor servei.</span></p>
  <div class="cos apareix">
    <p>Configrup som la corredoria d'assegurances que treballa per oferir-te la millor solució asseguradora, atenent les teves necessitats específiques amb un tracte personalitzat.</p>
    <p>Et proporcionem una gestió integral de totes les teves assegurances, amb un servei de qualitat gràcies al nostre equip d'alt nivell professional. Protegint i vetllant el teu patrimoni personal i professional.</p>
  </div>
</div></section>
<section class="seccio alt"><div class="wrap">
  <div class="valors" style="margin-top:0">
    <div class="valor apareix"><div class="ic">{ic("handshake")}</div><small>CONFIANÇA</small><h3>Confiança</h3><p>La nostra relació amb els clients es fonamenta en el respecte, la responsabilitat i la confidencialitat.</p></div>
    <div class="valor apareix"><div class="ic">{ic("shield")}</div><small>SEGURETAT</small><h3>Seguretat</h3><p>Treballem des de la professionalitat per proporcionar tranquil·litat a tots els nostres clients.</p></div>
    <div class="valor apareix"><div class="ic">{ic("star")}</div><small>SERVEI</small><h3>Servei</h3><p>Tots els nostres esforços estan orientats a aconseguir l'excel·lència en una gestió solvent.</p></div>
  </div>
</div></section>
<section class="seccio"><div class="wrap">
  <div class="valor-afegit apareix">
    <div><span class="etiqueta" style="color:#8f9cff">El nostre valor afegit</span><h2>Independència i experiència al teu costat</h2></div>
    <div>
      <p>Pertànyer a Configrup és formar part d'una empresa amb una dilatada experiència en el sector assegurador, sense perdre mai la nostra independència. És disposar d'un assessorament professional per a la teva seguretat.</p>
      <p>Significa gaudir de tots els recursos i coneixement per a l'estudi dels riscos, tramitació de pòlisses, gestió de sinistres, així com la resolució de conflictes que puguin sorgir amb les companyies.</p>
      <p>L'equip de professionals de Configrup ens esforcem cada dia al màxim per protegir els interessos dels nostres clients, amb voluntat de fer-los sentir part d'una gran empresa, en constant expansió i evolució, i en qui confiar.</p>
    </div>
  </div>
</div></section>
<section class="seccio alt"><div class="wrap companyies">
  <div><span class="etiqueta">Les millors companyies al teu servei</span><h2>Som corredors d'assegurances</h2><p class="intro">Això ens permet treballar amb total independència per oferir-te sempre la millor solució.</p></div>
  <div class="carrusel"><div class="pista">{logos}{logos.replace('alt="', 'aria-hidden="true" alt="')}</div></div>
</div></section>
''' + foot()
w("nosaltres.html", nos)

# ---------- CONTACTE ----------
con = head("Contacte · Configrup", "Truca'ns, escriu-nos o vine a les nostres oficines a Vic. Estarem encantats d'atendre't.", "contacte.html") + f'''
<section class="cap-pagina"><div class="wrap">
  <span class="etiqueta">Contacte</span>
  <h1>Parlem?</h1>
  <p class="intro">Pots trucar-nos, contactar per correu electrònic o, si tens temps, venir-nos a veure a les nostres oficines. Sigui com sigui, estarem encantats d'atendre't.</p>
</div></section>
<section class="seccio" style="padding-top:40px"><div class="wrap">
  <div class="contacte-grid">
    <div class="caixa"><h2 style="font-size:1.8rem;margin-bottom:24px">Formulari de contacte</h2>{form(missatge=True, assumpte=True)}</div>
    <div class="info-c">
      <div class="item"><span class="ic">{ic("pin")}</span><div><h4>Oficines</h4><p>Carrer Camí de la Tolosa, 9 desp. 6<br>08500 Vic (Edifici Tolosa)</p><a href="{MAPS}" target="_blank" rel="noopener" class="blau">Obrir a Google Maps →</a></div></div>
      <div class="item"><span class="ic">{ic("phone")}</span><div><h4>Telèfon</h4><a href="{TEL_H}">{TEL}</a><br><a href="{WA_URL}" target="_blank" rel="noopener">620 957 920 (WhatsApp)</a></div></div>
      <div class="item"><span class="ic">{ic("mail")}</span><div><h4>Correu electrònic</h4><a href="mailto:{MAIL}">{MAIL}</a></div></div>
      <div class="item"><span class="ic">{ic("clock")}</span><div><h4>Horari</h4><div class="horari"><span>De dilluns a divendres</span><span></span><b>Matins</b><span>9:00 - 14:00</span><b>Tardes</b><span>16:00 - 18:00</span><b>Intensiu</b><span>9:00 - 14:00</span></div></div></div>
    </div>
  </div>
  <div class="mapa"><iframe title="Mapa de les oficines de Configrup a Vic" loading="lazy" src="https://www.google.com/maps?q=Cam%C3%AD+de+la+Tolosa+9,+08500+Vic&output=embed"></iframe></div>
</div></section>
''' + foot()
w("contacte.html", con)

# ---------- LEGAL (pendent) ----------
leg = head("Informació legal · Configrup", "Avís legal, política de privacitat, cookies i transparència de Configrup.", "") + '''
<section class="cap-pagina"><div class="wrap"><span class="etiqueta">Informació legal</span><h1>Informació legal</h1>
<p class="intro">Textos pendents d'actualitzar amb les dades legals de la nova societat (raó social, NIF, registre de mediadors de la DGSFP, etc.).</p></div></section>
<section class="seccio" style="padding-top:40px"><div class="wrap" style="max-width:820px;display:grid;gap:48px">
  <div id="avis-legal"><h2>Avís legal</h2><p class="intro">Pendent.</p></div>
  <div id="privacitat"><h2>Política de privacitat</h2><p class="intro">Pendent.</p></div>
  <div id="cookies"><h2>Política de galetes</h2><p class="intro">Pendent.</p></div>
  <div id="transparencia"><h2>Transparència</h2><p class="intro">Pendent.</p></div>
  <div id="canal-denuncies"><h2>Canal de denúncies</h2><p class="intro">Pendent. A la web actual enllaça amb el canal extern de mediadors.</p></div>
</div></section>
''' + foot()
w("legal.html", leg)
print("ok")
