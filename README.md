# Web de Configrup

Web estàtica de **Configrup Brokers** (abans Confisergur), corredoria d'assegurances amb oficines a Vic, Granollers, Vilassar de Mar, Barberà del Vallès i Roda de Ter. Bilingüe: català (per defecte) i castellà.

Versió actual: **G**.

## Estructura

```
web/          La web publicable: és el que s'ha de pujar al servidor (arrel del domini configrup.com)
  index.html  Redirigeix sempre a ca/index.html
  ca/  es/    Pàgines en català i castellà
  css/        estil.css
  js/         principal.js (slider, diàlegs, formularis, mapa, galetes, avís d'incidència)
  img/        Imatges i logos
  vendor/     Leaflet 1.9.4 (mapa d'oficines)
generador/    Scripts que generen les pàgines HTML de web/
```

## Com es modifica

Els textos, les oficines i l'estructura de les pàgines són a `generador/generar.py`; els textos de les fitxes d'assegurança a `prods.json`, els textos legals a `legal.json` i la pàgina de la incidència de seguretat a `incidencia.json`. Després de canviar-los:

```
python3 generador/generar.py
```

Això torna a escriure els HTML de `web/ca/`, `web/es/`, `web/index.html`, `sitemap.xml` i `robots.txt`. Els estils (`web/css/estil.css`) i el JavaScript (`web/js/principal.js`) s'editen directament.

## Per publicar

- **Formularis:** envien per POST als scripts de la web actual (`/code/contact_email.php`, `/code/home_contact_email.php` i `/code/seguros_contact_email.php`). Cal copiar la carpeta `/code/` del servidor actual al nou. Els correus arriben a info@confisergur.com.
- **Google Analytics:** `GA_ID` és buit a `web/js/principal.js`. Només es carrega si el visitant accepta les galetes.
- **Mapa:** fons de l'Institut Cartogràfic i Geològic de Catalunya (CC BY 4.0). Funciona tant publicat com obrint els fitxers en local.

## Pendent

- Xarxes socials (encara apunten a confisergur).
- Decidir la propietat de Google Analytics.
- Allotjament del domini configrup.com.
