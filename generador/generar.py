"""Generador de la versió G (F + correcció del text de la incidència) (CA + ES) de la web de Configrup."""
import json, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "web")
DOMINI = "configrup.com"
E = html.escape

# Icones i xarxes socials (reutilitzades de build.py)
_src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read().split("TEL = ")[0]
ns = {}; exec(_src, ns)
I, ic, SOC, WA = ns["I"], ns["ic"], ns["SOC"], ns["WA"]

PRODS = json.load(open(os.path.join(HERE, "prods.json"), encoding="utf-8"))
INCI = json.load(open(os.path.join(HERE, "incidencia.json"), encoding="utf-8"))
INCI["ca"]["body"] = INCI["ca"]["body"].replace("indicades al final d'aquest missatge", "indicades al final d'aquesta pàgina")
AVIS = {
 "ca": {"barra": "Informació important: incidència de seguretat en un proveïdor tecnològic (3 de novembre de 2026).", "barra_mes": "Més informació",
  "p1": "El 3 de novembre es va produir una incidència de seguretat en un dels nostres proveïdors tecnològics que podria haver exposat algunes dades personals, com ara el nom, el DNI, la data de naixement, les dades de contacte i la informació de la pòlissa. Ja hem notificat la incidència a l’Agència Espanyola de Protecció de Dades (AEPD).",
  "p2": "Desconfia de qualsevol comunicació que et demani contrasenyes, pagaments o canvis de compte bancari, ja que nosaltres mai no sol·licitarem aquesta informació per aquests mitjans.",
  "p3": "Més informació <a href=\"{inc}\">aquí</a> o al telèfon <a href=\"tel:+34938892969\">938 892 969</a>.", "boto": "Més informació", "tancar": "Tancar", "etiqueta": "Avís important"},
 "es": {"barra": "Información importante: incidencia de seguridad en un proveedor tecnológico (3 de noviembre de 2026).", "barra_mes": "Más información",
  "p1": "El 3 de noviembre se produjo una incidencia de seguridad en uno de nuestros proveedores tecnológicos que podría haber expuesto algunos datos personales, como el nombre, el DNI, la fecha de nacimiento, los datos de contacto y la información de la póliza. Ya hemos notificado la incidencia a la Agencia Española de Protección de Datos (AEPD).",
  "p2": "Desconfía de cualquier comunicación que te solicite contraseñas, pagos o cambios de cuenta bancaria, ya que nosotros nunca solicitaremos esta información por estos medios.",
  "p3": "Más información <a href=\"{inc}\">aquí</a> o en el teléfono <a href=\"tel:+34938892969\">938 892 969</a>.", "boto": "Más información", "tancar": "Cerrar", "etiqueta": "Aviso importante"},
}
LEGAL = json.load(open(os.path.join(HERE, "legal.json"), encoding="utf-8"))
def legal_f(h):
    h = re.sub(r"CONFISERGUR DE GESTIÓ ROVIRA I ASSOCIATS, S\.?L\.?\.?", "CONFIGRUP BROKERS, S.L.", h)
    h = h.replace("Confisergur de Gestió Rovira, S.L.", "CONFIGRUP BROKERS, S.L.")
    h = re.sub(r"(?<!@)(www\.)?confisergur\.com", lambda m: (m.group(1) or "") + "configrup.com", h)
    h = h.replace("Rambla del Carme, 31 Entresuelo 1, C.P. 08500 de Vic", "Carrer Camí de la Tolosa, 9 desp. 6 (Edifici Tolosa), C.P. 08500 de Vic")
    h = h.replace("Rambla del Carme, 31 Entresuelo 1, 08500 Vic (Barcelona)", "Carrer Camí de la Tolosa, 9 desp. 6 - 08500 Vic (Edifici Tolosa)")
    h = h.replace("“CONFISERGUR”", "“CONFIGRUP”").replace("CONFISERGUR", "CONFIGRUP")
    return h
for _L in LEGAL:
    for _k in LEGAL[_L]: LEGAL[_L][_k] = legal_f(LEGAL[_L][_k])

def marca(t):
    return t.replace("Confisergur", "Configrup").replace("CONFISERGUR", "CONFIGRUP")

TEL = "938 892 969"; TEL_H = "tel:+34938892969"
MAIL = "info@confisergur.com"
WA_TXT = {"ca": "Hola, voldria fer una consulta.", "es": "Hola, quiero haceros una consulta."}
def wa(L): return "https://api.whatsapp.com/send?phone=34620957920&text=" + E(WA_TXT[L].replace(" ", "%20").replace(",", "%2C"))
CANAL = "https://canaldenunciasmediadores.com/configrup/"
CONFICARAVAN = "https://conficaravan.com"
GMAPS = "https://www.google.com/maps/search/?api=1&query="

OFICINES = [
 {"id": "vic", "nom": "Vic", "adr": {"ca": "Carrer Camí de la Tolosa, 9 desp. 6", "es": "Calle Camí de la Tolosa, 9 desp. 6"}, "cp": {"ca": "08500 Vic (Edifici Tolosa)", "es": "08500 Vic (Edifici Tolosa)"}, "lat": 41.938632, "lng": 2.250796, "maps": "https://goo.gl/maps/mGQ9cpg4AagAHEQAA", "pendent": False},
 {"id": "granollers", "nom": "Granollers", "adr": {"ca": "Carrer de Josep Umbert, 72-74", "es": "Calle Josep Umbert, 72-74"}, "cp": {"ca": "08402 Granollers", "es": "08402 Granollers"}, "lat": 41.6026841, "lng": 2.2947768, "maps": GMAPS + "Carrer+Josep+Umbert+72+08402+Granollers", "pendent": False},
 {"id": "vilassar", "nom": "Vilassar de Mar", "adr": {"ca": "Plaça Josep Tarradellas, 1, local 3", "es": "Plaza Josep Tarradellas, 1, local 3"}, "cp": {"ca": "08340 Vilassar de Mar", "es": "08340 Vilassar de Mar"}, "lat": 41.5089596, "lng": 2.388849, "maps": GMAPS + "Pla%C3%A7a+Josep+Tarradellas+1+08340+Vilassar+de+Mar", "pendent": False},
 {"id": "barbera", "nom": "Barberà del Vallès", "adr": {"ca": "Carrer de Mogoda, 1", "es": "Calle de Mogoda, 1"}, "cp": {"ca": "08210 Barberà del Vallès", "es": "08210 Barberà del Vallès"}, "lat": 41.515318, "lng": 2.1581664, "maps": GMAPS + "Carrer+de+Mogoda+1+08210+Barber%C3%A0+del+Vall%C3%A8s", "pendent": False},
 {"id": "roda", "nom": "Roda de Ter", "adr": {"ca": "Carrer d'en Bac de Roda, 47", "es": "Calle d'en Bac de Roda, 47"}, "cp": {"ca": "08510 Les Masies de Roda", "es": "08510 Les Masies de Roda"}, "lat": 41.9830, "lng": 2.3096, "maps": GMAPS + "Carrer+Bac+de+Roda+47+08510+Roda+de+Ter", "pendent": False},
]

# Pàgines i slugs per idioma
PAG = {
 "ca": {"inici": "index.html", "ass": "assegurances.html", "nos": "nosaltres.html", "con": "contacte.html", "legal": "avis-legal.html", "priv": "privacitat.html", "cook": "cookies.html", "trans": "transparencia.html", "map": "mapa-web.html", "inc": "incidencia-seguretat.html"},
 "es": {"inici": "index.html", "ass": "seguros.html", "nos": "nosotros.html", "con": "contacto.html", "legal": "aviso-legal.html", "priv": "privacidad.html", "cook": "cookies.html", "trans": "transparencia.html", "map": "mapa-web.html", "inc": "incidencia-seguridad.html"},
}
T = {
 "ca": {
  "lang": "ca", "altre": "es", "altre_nom": "ES", "altre_titol": "Castellano",
  "topbar": "Corredoria d'assegurances · Vic · Granollers · Vilassar de Mar · Roda de Ter · Barberà del Vallès",
  "truca": "Truca'ns", "acces": "Accés clients",
  "nav": {"inici": "Inici", "ass": "Assegurances", "nos": "Nosaltres", "con": "Contacte"},
  "menu_obrir": "Obrir el menú",
  "enllacos": "Enllaços", "legal_t": "Informació legal", "contacte_t": "Contacte", "oficines_t": "Oficines",
  "legal_links": {"legal": "Avís legal", "priv": "Privacitat", "cook": "Cookies", "trans": "Transparència", "map": "Mapa web"},
  "canal": "Canal de denúncies", "maps": "Obrir a Google Maps", "com_arribar": "Com arribar-hi",
  "peu_text": "Som corredors d'assegurances. Treballem amb total independència per oferir-te sempre la millor solució.",
  "drets": "Tots els drets reservats.", "pendent": "Pendent de confirmar",
  "wa_aria": "Escriu-nos per WhatsApp",
  "cookie_t": "Fem servir galetes", "cookie_p": "Fem servir galetes i altres tecnologies de seguiment per millorar la teva experiència de navegació al nostre lloc web, per mostrar-te contingut personalitzat i anuncis interessants per a tu, per analitzar el nostre trànsit i entendre d'on venen els nostres visitants.",
  "cookie_si": "Estic d'acord", "cookie_no": "Declino", "cookie_mes": "Més informació",
  # formularis
  "f_nom": "Nom i cognoms", "f_email": "Email", "f_tel": "Telèfon", "f_assumpte": "Assumpte", "f_missatge": "Missatge",
  "f_check": "He llegit i accepto la", "f_priv": "Política de privacitat", "f_enviar": "Enviar",
  "f_gracies_t": "Moltes gràcies per contactar amb nosaltres", "f_gracies_p": "Ens posarem en contacte amb tu el més aviat possible.",
  "m_titol": "Ens posarem en contacte amb tu", "m_text": "Emplena el formulari i ens posarem en contacte amb tu.",
  "contactans": "Contacta'ns", "tancar": "Tancar",
  # inici
  "slides": [
   ("slider_coche.jpg", "Condueix tranquil.<br>Nosaltres ens cuidem de tot.", "La teva assegurança de cotxe o moto amb les millors cobertures i al millor preu.", "link", "Saber-ne més"),
   ("slider_salud.jpg", "El més important, la salut.", "Cuida d'ells amb les millors assegurances de salut.", "modal", "Consulta'ns"),
   ("slider_hogar.jpg", "La teva llar sempre ben protegida.", "Sabem que casa teva és el teu refugi, per això t'ajudem a protegir-la.", "link", "Saber-ne més"),
   ("slider_pensiones.jpg", "Assegura la teva vida per protegir el seu futur.", "T'ajudem a protegir-los quan més ho necessitin.", "modal", "Consulta'ns"),
  ],
  "dia": "Diapositiva",
  "esp_t": "Som especialistes en <span>confiança i seguretat</span>",
  "esp_p": ["A Configrup t'oferim l'assegurança que millor s'adapta a tu, amb les cobertures necessàries per a cada moment.", "I el més important, estem al teu costat quan ho necessites."],
  "valors": [("handshake", "Confiança", "Parlem amb confiança"), ("shield", "Seguretat", "Oferim seguretat"), ("star", "Servei", "Vocació de servei")],
  "part_et": "Particulars", "part_t": "Assegurances per a particulars", "part_b": "Totes les persones som diferents, les assegurances també.",
  "part_p": "Busques una assegurança pel teu cotxe, moto, salut, vida o llar? T'oferim la millor solució asseguradora per a cobrir totes les teves necessitats.",
  "part_links": [("car", "Assegurança Auto", "coche"), ("home", "Assegurança Llar", "hogar"), ("users", "Assegurança Vida", "vida"), ("caravan", "Assegurança Autocaravana", "@conficaravan")],
  "descobreix": "Descobreix-les totes", "part_xip": "Per a tu i els teus",
  "parlem_t": "Parlem?", "parlem_p": "Contactem amb tu i t'ajudem a trobar la teva assegurança.", "et_truquem": "Et truquem",
  "emp_et": "Empreses i autònoms", "emp_t": "Assegurances per a empreses", "emp_b": "Les empreses evolucionen i s'enfronten a nous reptes. Nosaltres estem al teu costat per a cobrir els riscos.",
  "emp_p": "Assessorem empreses i autònoms sobre les millors cobertures i creem un pla 100% personalitzat.",
  "emp_links": [("store", "Assegurança Comerç", "comercio"), ("factory", "Assegurança PIME", "pime"), ("clipboard", "Assegurança Baixa laboral", "baja"), ("scale", "Assegurança Responsabilitat civil", "responsabilidad")],
  "emp_xip": "Pla 100% personalitzat",
  "perque_et": "Per què nosaltres", "perque_t": "Per què confiar en Configrup?", "perque_p": "La nostra experiència i professionalitat al teu servei.", "sobre": "Sobre nosaltres",
  "motius": ["Estem al teu costat. T'escoltem i realitzem, per tu, totes les gestions amb la companyia, defensant sempre els teus interessos.",
   "Només treballem amb les millors companyies, aquelles que ens ofereixen la confiança i seguretat necessàries per als nostres clients.",
   "Busquem la millor assegurança segons els teus interessos. Perquè la millor assegurança és la que millor s'adapta a les teves necessitats.",
   "Treballem amb independència, objectivitat i transparència, això ens permet oferir-te la millor opció d'assegurança.",
   "Posem tota la nostra experiència al teu servei perquè sempre estiguis ben atès davant qualsevol consulta."],
  "comp_et": "Les millors companyies al teu servei", "comp_t": "Som corredors d'assegurances",
  "comp_p": "Això ens permet treballar amb total independència per oferir-te sempre la millor solució, realitzant totes les gestions de les teves assegurances.",
  "inici_title": "Configrup · Corredoria d'assegurances", "inici_desc": "Configrup és una corredoria d'assegurances amb oficines a Vic, Granollers, Vilassar de Mar, Roda de Ter i Barberà del Vallès. Assegurances per a particulars i empreses.",
  # assegurances
  "ass_title": "Assegurances per a particulars i empreses · Configrup", "ass_desc": "Assegurances de cotxe, moto, autocaravana, llar, salut, vida, comerç, PIME, responsabilitat civil, ciber i moltes més.",
  "ass_h1": "Quina assegurança necessites?", "soc_part": "Sóc particular", "soc_emp": "Sóc empresa",
  "ass_part_t": "Assegurances per a particulars", "ass_part_p": ["T'oferim les millors assegurances perquè tu i els teus estigueu sempre ben protegits.", "Com a corredors treballem amb les millors companyies per proporcionar-te la millor solució asseguradora en cada moment."],
  "ass_emp_t": "Assegurances per a empreses", "ass_emp_p": ["Els negocis s'enfronten a multitud de riscos amb la seva activitat empresarial.", "Els nostres professionals especialitzats en assegurances per a empreses analitzen els vostres riscos per oferir-vos la millor solució asseguradora per al vostre negoci."],
  "altre_t": "Busques algun altre tipus d'assegurança?", "altre_p": "Explica'ns què necessites i et proporcionarem una solució a mida.", "tajudem": "T'ajudem",
  "mes_info": "Més informació", "web_externa": "Web de Conficaravan",
  "aseso_t": "Necessites assessorament?", "aseso_p": "El nostre equip de professionals està aquí per ajudar-te.", "consultans": "Consulta'ns",
  "camper_t": "Assegurança de Camper / Autocaravana",
  # nosaltres
  "nos_title": "Sobre nosaltres · Configrup", "nos_desc": "Configrup és la corredoria d'assegurances que treballa per oferir-te la millor solució asseguradora, amb un tracte personalitzat.",
  "nos_h1": "Creixem junts", "nos_sub": "La nostra professionalitat, solvència i ètica ens defineixen.", "nos_et": "Sobre nosaltres",
  "nos_p1": "Configrup som la corredoria d'assegurances que treballa per oferir-te la millor <a href=\"{ass}\">solució asseguradora</a>, atenent les teves necessitats específiques amb <strong>un tracte personalitzat</strong>.",
  "nos_p2": "Et proporcionem una <strong>gestió integral de totes les teves assegurances</strong>, amb un servei de qualitat gràcies al nostre equip d'alt nivell professional. <strong>Protegint i vetllant el teu patrimoni personal i professional</strong>.",
  "nos_valors": [("handshake", "Confiança", "La nostra relació amb els clients es fonamenta en el respecte, la responsabilitat i la confidencialitat."), ("shield", "Seguretat", "Treballem des de la professionalitat per a proporcionar tranquil·litat a tots els nostres clients."), ("star", "Servei", "Tots els nostres esforços estan orientats a aconseguir l'excel·lència en una gestió solvent.")],
  "nos_cita": "Treballem cada dia per oferir-te el millor servei.",
  "va_t": "El nostre valor afegit", "va_p": ["Pertànyer a Configrup és formar part d'una empresa amb una dilatada experiència en el sector assegurador, sense perdre mai la nostra independència. És disposar d'un assessorament professional per a la teva seguretat.", "Significa gaudir de tots els recursos i coneixement per a l'estudi dels riscos, tramitació de pòlisses, gestió de sinistres; així com la resolució de conflictes que puguin sorgir amb les companyies.", "L'equip de professionals de Configrup ens esforcem cada dia al màxim per protegir els interessos dels nostres clients, amb voluntat de fer-los sentir part d'una gran empresa, en constant expansió i evolució, i en qui confiar."],
  "nos_of_t": "Les nostres oficines", "nos_of_p": "Som a prop teu, amb oficines a Osona, el Vallès i el Maresme.",
  # contacte
  "con_title": "Contacte · Configrup", "con_desc": "Truca'ns, escriu-nos o vine a qualsevol de les nostres oficines. Estarem encantats d'atendre't.",
  "con_h1": "Parlem?", "con_p": "Pots trucar-nos, contactar per correu electrònic o, si tens temps, venir-nos a veure a les nostres oficines. Sigui com sigui estarem encantats d'atendre't.",
  "form_t": "Formulari de contacte", "telefon": "Telèfon", "correu": "Correu electrònic", "horari": "Horari",
  "horari_rows": [("De dilluns a divendres", ""), ("Matins", "9:00 - 14:00"), ("Tardes", "16:00 - 18:00"), ("Intensiu", "9:00 - 14:00")],
  "xarxes": "Xarxes socials", "of_t": "Les nostres oficines", "of_p": "Tria l'oficina que et quedi més a prop.",
  "mapa_titol": "Mapa de les oficines de Configrup",
  # legal
  "legal_titles": {"legal": "Avís legal", "priv": "Política de privacitat", "cook": "Política de galetes", "trans": "Política de transparència"},
  "map_h1": "Mapa web",
 },
 "es": {
  "lang": "es", "altre": "ca", "altre_nom": "CA", "altre_titol": "Català",
  "topbar": "Correduría de seguros · Vic · Granollers · Vilassar de Mar · Roda de Ter · Barberà del Vallès",
  "truca": "Llámanos", "acces": "Acceso clientes",
  "nav": {"inici": "Inicio", "ass": "Seguros", "nos": "Nosotros", "con": "Contacto"},
  "menu_obrir": "Abrir el menú",
  "enllacos": "Enlaces", "legal_t": "Información legal", "contacte_t": "Contacto", "oficines_t": "Oficinas",
  "legal_links": {"legal": "Aviso legal", "priv": "Privacidad", "cook": "Cookies", "trans": "Transparencia", "map": "Mapa web"},
  "canal": "Canal de denuncias", "maps": "Abrir en Google Maps", "com_arribar": "Cómo llegar",
  "peu_text": "Somos corredores de seguros. Trabajamos con total independencia para ofrecerte siempre la mejor solución.",
  "drets": "Todos los derechos reservados.", "pendent": "Pendiente de confirmar",
  "wa_aria": "Escríbenos por WhatsApp",
  "cookie_t": "Usamos cookies", "cookie_p": "Usamos cookies y otras tecnologías de seguimiento para mejorar tu experiencia de navegación en nuestro sitio web, para mostrarte contenido personalizado y anuncios interesantes para ti, para analizar nuestro tráfico y entender de dónde vienen nuestros visitantes.",
  "cookie_si": "Estoy de acuerdo", "cookie_no": "Declino", "cookie_mes": "Más información",
  "f_nom": "Nombre completo", "f_email": "Email", "f_tel": "Teléfono", "f_assumpte": "Asunto", "f_missatge": "Mensaje",
  "f_check": "He leído y acepto la", "f_priv": "Política de privacidad", "f_enviar": "Enviar",
  "f_gracies_t": "Muchas gracias por contactar con nosotros", "f_gracies_p": "Nos pondremos en contacto contigo lo antes posible.",
  "m_titol": "Nos pondremos en contacto contigo", "m_text": "Rellena el formulario y nos pondremos en contacto contigo.",
  "contactans": "Contáctanos", "tancar": "Cerrar",
  "slides": [
   ("slider_coche.jpg", "Tú conduce tranquilo.<br>Lo demás es cosa nuestra.", "Tu seguro de coche o moto con las mejores coberturas y al mejor precio.", "link", "Saber más"),
   ("slider_salud.jpg", "Ante todo, la salud.", "Cuida de ellos con los mejores seguros de salud.", "modal", "Consúltanos"),
   ("slider_hogar.jpg", "Tu hogar siempre bien protegido.", "Sabemos que tu hogar es tu refugio, por eso te ayudamos a protegerlo.", "link", "Saber más"),
   ("slider_pensiones.jpg", "Asegura tu vida para proteger su futuro.", "Te ayudamos a mantenerlos protegidos cuando más lo necesiten.", "modal", "Consúltanos"),
  ],
  "dia": "Diapositiva",
  "esp_t": "Somos especialistas en <span>confianza y seguridad</span>",
  "esp_p": ["En Configrup te ofrecemos el seguro que mejor se adapta a ti, con las coberturas adecuadas para cada momento.", "Y lo más importante, estamos contigo cuando lo necesitas."],
  "valors": [("handshake", "Confianza", "Hablamos con confianza"), ("shield", "Seguridad", "Ofrecemos seguridad"), ("star", "Servicio", "Vocación de servicio")],
  "part_et": "Particulares", "part_t": "Seguros para particulares", "part_b": "Todas las personas somos diferentes, los seguros también.",
  "part_p": "¿Buscas un seguro de coche, moto, salud, vida o hogar? Te ofrecemos la mejor solución aseguradora para cubrir todas tus necesidades.",
  "part_links": [("car", "Seguro Auto", "coche"), ("home", "Seguro Hogar", "hogar"), ("users", "Seguro Vida", "vida"), ("caravan", "Seguro Autocaravana", "@conficaravan")],
  "descobreix": "Descúbrelos todos", "part_xip": "Para ti y los tuyos",
  "parlem_t": "¿Hablamos?", "parlem_p": "Contactamos contigo y te ayudamos a encontrar tu seguro.", "et_truquem": "Te llamamos",
  "emp_et": "Empresas y autónomos", "emp_t": "Seguros para empresas", "emp_b": "Las empresas evolucionan y se enfrentan a nuevos retos. Nosotros estamos a tu lado para cubrir los riesgos.",
  "emp_p": "Asesoramos a empresas y autónomos sobre las mejores coberturas y creamos un plan 100% personalizado.",
  "emp_links": [("store", "Seguro Comercio", "comercio"), ("factory", "Seguro PIME", "pime"), ("clipboard", "Seguro Baja laboral", "baja"), ("scale", "Seguro Responsabilidad civil", "responsabilidad")],
  "emp_xip": "Plan 100% personalizado",
  "perque_et": "Por qué nosotros", "perque_t": "¿Por qué escoger Configrup?", "perque_p": "Nuestra experiencia y profesionalidad a tu servicio.", "sobre": "Sobre nosotros",
  "motius": ["Estamos a tu lado. Te escuchamos y hacemos todas las gestiones con la compañía por ti, defendiendo siempre tus intereses.",
   "Solo trabajamos con las mejores compañías, aquellas que nos ofrecen la confianza y seguridad necesarias para nuestros clientes.",
   "Buscamos el mejor seguro según tus intereses. Porque el mejor seguro es aquel que mejor se adapta a tus necesidades.",
   "Trabajamos con independencia, objetividad y transparencia, esto nos permite ofrecerte siempre la mejor opción de seguro.",
   "Ponemos toda nuestra experiencia a tu servicio para que siempre te sientas bien atendido ante cualquier consulta."],
  "comp_et": "Las mejores compañías a tu servicio", "comp_t": "Somos corredores de seguros",
  "comp_p": "Esto nos permite trabajar con total independencia para ofrecerte siempre la mejor solución, ocupándonos de todas las gestiones de tus seguros.",
  "inici_title": "Configrup · Correduría de seguros", "inici_desc": "Configrup es una correduría de seguros con oficinas en Vic, Granollers, Vilassar de Mar, Roda de Ter y Barberà del Vallès. Seguros para particulares y empresas.",
  "ass_title": "Seguros para particulares y empresas · Configrup", "ass_desc": "Seguros de coche, moto, autocaravana, hogar, salud, vida, comercio, PIME, responsabilidad civil, ciber y muchos más.",
  "ass_h1": "¿Qué seguro necesitas?", "soc_part": "Soy particular", "soc_emp": "Soy empresa",
  "ass_part_t": "Seguros para particulares", "ass_part_p": ["Te ofrecemos los mejores seguros para que tú y los tuyos estéis siempre bien protegidos.", "Como corredores, trabajamos con las mejores compañías para proporcionarte la mejor solución aseguradora en cada momento."],
  "ass_emp_t": "Seguros para empresas", "ass_emp_p": ["Los negocios se enfrentan a multitud de riesgos en su actividad empresarial.", "Nuestros profesionales especializados en seguros para empresas analizan vuestros riesgos para ofreceros la mejor solución aseguradora para vuestro negocio."],
  "altre_t": "¿Estás buscando otro tipo de seguro?", "altre_p": "Explícanos qué necesitas y te proporcionaremos una solución a medida.", "tajudem": "Te ayudamos",
  "mes_info": "Más información", "web_externa": "Web de Conficaravan",
  "aseso_t": "¿Necesitas asesoramiento?", "aseso_p": "Nuestro equipo de profesionales está aquí para ayudarte.", "consultans": "Consúltanos",
  "camper_t": "Seguro de Camper / Autocaravana",
  "nos_title": "Sobre nosotros · Configrup", "nos_desc": "Configrup es la correduría de seguros que trabaja para ofrecerte la mejor solución aseguradora, con un servicio personalizado.",
  "nos_h1": "Creciendo juntos", "nos_sub": "Nuestra profesionalidad, solvencia y ética nos definen.", "nos_et": "Sobre nosotros",
  "nos_p1": "Configrup somos la correduría de seguros que trabaja para ofrecerte la mejor <a href=\"{ass}\">solución aseguradora</a>, atendiendo tus necesidades específicas con un <strong>servicio personalizado</strong>.",
  "nos_p2": "Te proporcionamos una <strong>gestión integral de todos tus seguros</strong>, con un servicio de calidad gracias a nuestro equipo de alto nivel profesional. <strong>Protegiendo y cuidando de tu patrimonio personal y profesional</strong>.",
  "nos_valors": [("handshake", "Confianza", "Nuestra relación con los clientes se basa en el respeto, la responsabilidad y la confidencialidad."), ("shield", "Seguridad", "Trabajamos desde la profesionalidad para proporcionar tranquilidad a todos nuestros clientes."), ("star", "Servicio", "Todos nuestros esfuerzos están orientados a conseguir la excelencia en una gestión solvente.")],
  "nos_cita": "Trabajamos cada día para ofrecerte el mejor servicio.",
  "va_t": "Nuestro valor añadido", "va_p": ["Ser de Configrup es formar parte de una empresa con una dilatada experiencia en el sector asegurador, sin perder nunca nuestra independencia. Es disponer de un asesoramiento profesional para tu seguridad.", "Significa gozar de todos los recursos y conocimiento para el estudio de los riesgos, tramitación de pólizas, gestión de siniestros; así como la resolución de conflictos que puedan surgir con las diferentes compañías.", "El equipo de profesionales de Configrup nos esforzamos al máximo todos los días para proteger los intereses de nuestros clientes, con la voluntad de hacerles sentir parte de una gran empresa, en constante expansión y evolución, y en quien confiar."],
  "nos_of_t": "Nuestras oficinas", "nos_of_p": "Estamos cerca de ti, con oficinas en Osona, el Vallès y el Maresme.",
  "con_title": "Contacto · Configrup", "con_desc": "Llámanos, escríbenos o pásate por cualquiera de nuestras oficinas. Estaremos encantados de atenderte.",
  "con_h1": "¿Hablamos?", "con_p": "Puedes llamarnos, contactar por email o, si tienes tiempo, pasarte por nuestras oficinas. Sea como sea estaremos encantados de atenderte.",
  "form_t": "Formulario de contacto", "telefon": "Teléfono", "correu": "Correo electrónico", "horari": "Horario",
  "horari_rows": [("De lunes a viernes", ""), ("Mañana", "9:00 - 14:00"), ("Tarde", "16:00 - 18:00"), ("Intensivo", "9:00 - 14:00")],
  "xarxes": "Redes sociales", "of_t": "Nuestras oficinas", "of_p": "Elige la oficina que te quede más cerca.",
  "mapa_titol": "Mapa de las oficinas de Configrup",
  "legal_titles": {"legal": "Aviso legal", "priv": "Política de privacidad", "cook": "Política de cookies", "trans": "Política de transparencia"},
  "map_h1": "Mapa web",
 },
}

HX = {"ca": {"descobreix": "Descobreix les assegurances", "ess_et": "La nostra essència", "ess_t": "Confiança, seguretat i servei", "ess_p": "Tres valors que defineixen la manera com treballem amb cadascun dels nostres clients, cada dia."},
      "es": {"descobreix": "Descubre nuestros seguros", "ess_et": "Nuestra esencia", "ess_t": "Confianza, seguridad y servicio", "ess_p": "Tres valores que definen la manera en que trabajamos con cada uno de nuestros clientes, cada día."}}
PICONS = {"coche": "car", "moto": "moto", "camper": "caravan", "caravana": "caravan", "offroad": "mountain", "hogar": "home", "salud": "heart", "accidentes": "bandage", "comunidad": "building", "vida": "users", "decesos": "flower", "viaje": "plane", "alquiler": "key", "mascotas": "paw", "bicicletas": "bike", "embarcaciones": "boat", "comercio": "store", "pime": "factory", "responsabilidad": "scale", "do": "brief", "ciber": "cyber", "baja": "clipboard", "accidente_convenio": "bandage", "salud_laboral": "heart", "medioambiental": "leaf", "construccion": "hardhat", "decenal": "home", "transportes": "truck"}
COMP = ['allianz','arag','asefa','axa','calife','catalana','cosalud','crouco','dkv','fiatc','generali','genesis','liberty','lloyds','markel','mmt','mussap','mutuacat','plus','prevision','reale','vital','zurich']
COMP_NOM = {"mmt": "MMT Seguros", "dkv": "DKV", "axa": "AXA", "arag": "ARAG", "fiatc": "FIATC", "mutuacat": "Mutua Catalana", "prevision": "Previsión Mallorquina", "catalana": "Catalana Occidente", "plus": "Plus Ultra", "vital": "Vital Seguro", "lloyds": "Lloyd's"}

def link_prod(L, key):
    if key == "@conficaravan": return CONFICARAVAN, True
    return f'{PAG[L]["ass"]}#{key}', False

# ---------------- plantilla comuna ----------------
def head(L, page, title, desc, bodyclass=""):
    t = T[L]; P = PAG[L]
    nav = "".join(f'<a href="{P[k]}"{" class=\"actiu\" aria-current=\"page\"" if k==page else ""}>{t["nav"][k]}</a>' for k in ("inici","ass","nos"))
    altre = PAG[t["altre"]][page] if page in PAG[t["altre"]] else "index.html"
    alts = f'<link rel="canonical" href="https://{DOMINI}/{L}/{P.get(page,"index.html")}">' + "".join(f'<link rel="alternate" hreflang="{l}" href="https://{DOMINI}/{l}/{PAG[l].get(page,"index.html")}">' for l in ("ca","es"))
    return f'''<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0b1a3c">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="../img/configrup-logo.png">
{alts}
<link rel="icon" href="../img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../css/estil.css">
</head>
<body class="{bodyclass}" data-lang="{L}">
<div class="avis-inc"><div class="wrap">{ic("shield")}<span>{AVIS[L]["barra"]}</span> <a href="{P["inc"]}">{AVIS[L]["barra_mes"]} →</a></div></div>
<div class="topbar"><div class="wrap">
  <span class="esquerra">{E(t["topbar"])}</span>
  <span class="dreta"><a href="{TEL_H}">{ic("phone")}{t["truca"]} {TEL}</a><a href="mailto:{MAIL}" class="esquerra">{ic("mail")}{MAIL}</a></span>
</div></div>
<header class="cap"><div class="wrap">
  <a class="logo" href="{P["inici"]}" aria-label="Configrup"><img src="../img/configrup-logo.png" alt="ConfiGrup Corredoria d'assegurances" width="832" height="257"></a>
  <nav class="menu" id="menu">{nav}<a href="{P["con"]}" class="btn btn-blau">{t["nav"]["con"]} {ic("arrow")}</a><a class="idioma" href="../{t["altre"]}/{altre}" hreflang="{t["altre"]}" title="{t["altre_titol"]}">{t["altre_nom"]}</a></nav>
  <button class="hamburguesa" aria-label="{t["menu_obrir"]}" aria-expanded="false" aria-controls="menu"><span></span></button>
</div></header>
<main>
'''

def dialog_avis(L):
    a = AVIS[L]; P = PAG[L]
    return f'''<dialog id="dlg-avis" class="dlg-avis" aria-labelledby="dlg-avis-t"><div class="dlg-sol">
  <button class="tancar" aria-label="{a["tancar"]}">{ic("x")}</button>
  <span class="etiqueta">{a["etiqueta"]}</span>
  <h3 id="dlg-avis-t">ConfiGrup Brokers</h3>
  <p>{a["p1"]}</p>
  <p><strong>{a["p2"]}</strong></p>
  <p>{a["p3"].format(inc=P["inc"])}</p>
  <div class="bts"><a class="btn btn-blau" href="{P["inc"]}">{a["boto"]} {ic("arrow")}</a><button class="btn btn-linia tancar-avis">{a["tancar"]}</button></div>
</div></dialog>'''

def foot(L, avis=True):
    t = T[L]; P = PAG[L]
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n.capitalize()}"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg></a>' for n,(u,p) in SOC.items())
    ofs = "".join(f'<li><b>{o["nom"]}</b><br>{"<span class=\"pendent\">"+t["pendent"]+"</span>" if o["pendent"] else E(o["adr"][L])+"<br>"+E(o["cp"][L])}</li>' for o in OFICINES)
    return f'''</main>
<footer class="peu"><div class="wrap">
  <div class="peu-grid">
    <div>
      <img class="logo-peu" src="../img/configrup-logo-negatiu.png" alt="ConfiGrup" width="832" height="257">
      <p>{t["peu_text"]}</p>
      <ul class="peu-contacte"><li><a href="mailto:{MAIL}">{ic("mail")}{MAIL}</a></li><li><a href="{TEL_H}">{ic("phone")}{TEL}</a></li></ul>
      <div class="xarxes">{soc}</div>
    </div>
    <div><h4>{t["enllacos"]}</h4><ul>
      <li><a href="{P["inici"]}">{t["nav"]["inici"]}</a></li><li><a href="{P["ass"]}">{t["nav"]["ass"]}</a></li>
      <li><a href="{P["nos"]}">{t["nav"]["nos"]}</a></li><li><a href="{P["con"]}">{t["nav"]["con"]}</a></li>
    </ul></div>
    <div><h4>{t["legal_t"]}</h4><ul>
      {"".join(f'<li><a href="{P[k]}">{v}</a></li>' for k,v in t["legal_links"].items() if k!="map")}
      <li><a href="{CANAL}" target="_blank" rel="noopener">{t["canal"]}</a></li>
      <li><a href="{P["inc"]}">{INCI[L]["t"].split(" relaciona")[0]}</a></li>
      <li><a href="{P["map"]}">{t["legal_links"]["map"]}</a></li>
    </ul></div>
    <div><h4>{t["oficines_t"]}</h4><ul class="peu-oficines">{ofs}</ul><p class="peu-mapa"><a href="{P["con"]}#oficines">{t["com_arribar"]} →</a></p></div>
  </div>
  <div class="peu-baix"><span>© <span class="any">2026</span> Configrup. {t["drets"]}</span><span>{t["topbar"].split(" · ")[0]}</span></div>
</div></footer>
<a class="whatsapp" href="{wa(L)}" target="_blank" rel="noopener" aria-label="{t["wa_aria"]}">{WA}</a>
<div class="galetes" role="dialog" aria-label="{t["cookie_t"]}">
  <strong>{t["cookie_t"]}</strong>
  <p>{t["cookie_p"]} <a href="{P["cook"]}" class="blau">{t["cookie_mes"]}</a></p>
  <div class="bts"><button class="btn btn-blau" data-galetes="si">{t["cookie_si"]}</button><button class="btn btn-linia" data-galetes="no">{t["cookie_no"]}</button></div>
</div>
{dialog_simple(L)}
{dialog_avis(L) if avis else ""}
<script src="../js/principal.js"></script>
</body>
</html>
'''

def form(L, missatge=True, assumpte=False, boto=None, extra=""):
    t = T[L]
    return f'''<form class="form" data-form>{extra}
  <div class="camps form">
    <div><label>{t["f_nom"]}<input name="nom" required autocomplete="name"></label></div>
    <div class="doble"><div><label>{t["f_email"]}<input type="email" name="email" required autocomplete="email"></label></div>
    <div><label>{t["f_tel"]}<input type="tel" name="telefon" required autocomplete="tel"></label></div></div>
    {f'<div><label>{t["f_assumpte"]}<input name="assumpte"></label></div>' if assumpte else ''}
    {f'<div><label>{t["f_missatge"]}<textarea name="missatge"></textarea></label></div>' if missatge else ''}
    <label class="check"><input type="checkbox" required> <span>{t["f_check"]} <a href="{PAG[L]["priv"]}" target="_blank">{t["f_priv"]}</a>.</span></label>
    <button class="btn btn-blau" type="submit">{boto or t["f_enviar"]} {ic("arrow")}</button>
  </div>
  <div class="gracies" role="status"><strong>{t["f_gracies_t"]}</strong>{t["f_gracies_p"]}</div>
</form>'''

def dialog_simple(L):
    t = T[L]
    return f'''<dialog id="dlg-simple" aria-labelledby="dlg-simple-t"><div class="dlg-sol">
  <button class="tancar" aria-label="{t["tancar"]}">{ic("x")}</button>
  <h3 id="dlg-simple-t">{t["m_titol"]}</h3><p>{t["m_text"]}</p>
  {form(L, missatge=True)}
</div></dialog>'''

def w(L, name, s):
    os.makedirs(os.path.join(OUT, L), exist_ok=True)
    open(os.path.join(OUT, L, name), "w", encoding="utf-8").write(s)

def logos():
    l = "".join(f'<img src="../img/companyies/{c}.jpg" alt="{COMP_NOM.get(c, c.capitalize())}" width="150" height="75">' for c in COMP)
    return l + l.replace('alt="', 'aria-hidden="true" alt="')

def oficines_html(L, amb_mapa=True):
    t = T[L]
    cards = "".join(f'''<div class="oficina{" pendent" if o["pendent"] else ""}" data-of="{o["id"]}" tabindex="0">
      <span class="ic">{ic("pin")}</span>
      <div><h4>{o["nom"]}</h4><p>{E(o["adr"][L])}<br>{E(o["cp"][L])}</p>
      <p class="of-tel"><a href="{TEL_H}">{ic("phone")}{TEL}</a></p>
      <a href="{o["maps"]}" target="_blank" rel="noopener">{t["maps"]} →</a></div></div>''' for o in OFICINES)
    data = json.dumps([{"id": o["id"], "nom": o["nom"], "adr": o["adr"][L], "cp": o["cp"][L], "lat": o["lat"], "lng": o["lng"], "maps": o["maps"], "pendent": o["pendent"], "tel": TEL} for o in OFICINES], ensure_ascii=False)
    mapa = f'<div class="mapa" id="mapa" role="region" aria-label="{t["mapa_titol"]}"></div><script>window.OFICINES={data};window.TXT_MAPS={json.dumps(t["maps"])};</script>' if amb_mapa else ""
    return f'<div class="oficines-grid">{cards}</div>{mapa}'

def run(L):
    t = T[L]; P = PAG[L]
    # ---------- INICI ----------
    slides = ""
    for i,(img,h,p,acc,bt) in enumerate(t["slides"]):
        boto = f'<a class="btn btn-blau" href="{P["ass"]}" tabindex="{0 if i==0 else -1}">{bt} {ic("arrow")}</a>' if acc=="link" else f'<button class="btn btn-blau" data-obrir="simple" tabindex="{0 if i==0 else -1}">{bt} {ic("arrow")}</button>'
        slides += f'''<div class="slide{" activa" if i==0 else ""}" aria-hidden="{"false" if i==0 else "true"}" style="background-image:url('../img/slider/{img}')">
      <div class="wrap"><div class="slide-text"><h2>{h}</h2><p>{E(p)}</p>{boto}</div></div></div>'''
    punts = "".join(f'<button aria-label="{t["dia"]} {i+1}"{" class=\"activa\"" if i==0 else ""}></button>' for i in range(len(t["slides"])))
    def plinks(items):
        out = ""
        for icn, tx, key in items:
            href, ext = link_prod(L, key)
            out += f'<a href="{href}"{" target=\"_blank\" rel=\"noopener\"" if ext else ""}>{ic(icn)}<span>{tx}</span>{"<small>↗</small>" if ext else ""}</a>'
        return out
    fotos = "".join(f'<img src="../img/slider/{img}" alt=""{" class=\"activa\"" if i==0 else ""} width="1600" height="1020"{"" if i==0 else " loading=\"lazy\""}>' for i,(img,*_) in enumerate(t["slides"]))
    fpunts = "".join(f'<button aria-label="{t["dia"]} {i+1}"{" class=\"activa\"" if i==0 else ""}></button>' for i in range(len(t["slides"])))
    acc = ""
    for (img,h,p,act,bt),(icn,key) in zip(t["slides"],[("car","coche"),("heart","salud"),("home","hogar"),("users","vida")]):
        tit = h.replace("<br>"," ")
        if act=="link":
            acc += f'<a href="{P["ass"]}#{key}"><span>{ic(icn)}</span><h3>{tit}</h3><p>{E(p)}</p><span class="mes">{bt} →</span></a>'
        else:
            acc += f'<button type="button" data-obrir="simple"><span>{ic(icn)}</span><h3>{tit}</h3><p>{E(p)}</p><span class="mes">{bt} →</span></button>'
    valors_ess = "".join(f'<div class="valor apareix"><div class="ic">{ic(a)}</div><small>{b.upper()}</small><h3>{c}</h3><p>{d}</p></div>' for (a,b,c),(_,_,d) in zip(t["valors"],t["nos_valors"]))
    valors = "".join(f'<div class="valor-c"><span class="ic">{ic(a)}</span><div><small>{b.upper()}</small><h3>{c}</h3></div></div>' for a,b,c in t["valors"])
    motius = "".join(f'<div class="motiu{" llum" if i==0 else ""}"><p>{E(m)}</p></div>' for i,m in enumerate(t["motius"]))
    index = head(L, "inici", t["inici_title"], t["inici_desc"]) + f'''
<section class="hero-c">
  <div class="text">
    <span class="etiqueta">{t["topbar"].split(" · ")[0]}</span>
    <h1>{t["esp_t"]}</h1>
    <p>{" ".join(E(p) for p in t["esp_p"])}</p>
    <div class="accions"><a class="btn btn-blau" href="{P["ass"]}">{HX[L]["descobreix"]} {ic("arrow")}</a><button class="btn btn-transp" data-obrir="simple">{t["et_truquem"]}</button></div>
  </div>
  <div class="foto" data-rotar>{fotos}<div class="foto-punts">{fpunts}</div></div>
</section>
<section class="accessos"><div class="wrap"><div class="graella-a">{acc}</div></div></section>
<section class="seccio alt essencia"><div class="wrap">
  <div class="cap-centre apareix"><span class="etiqueta">{HX[L]["ess_et"]}</span><h2>{HX[L]["ess_t"]}</h2><p>{HX[L]["ess_p"]}</p></div>
  <div class="valors">{valors_ess}</div>
</div></section>
<section class="seccio alt"><div class="wrap bloc">
  <div class="bloc-img apareix"><img src="../img/img_particulares.jpg" alt="" width="600" height="382" loading="lazy"><div class="xip"><span class="ic">{ic("user")}</span>{t["part_xip"]}</div></div>
  <div class="apareix">
    <span class="etiqueta">{t["part_et"]}</span>
    <h2>{t["part_t"]}</h2>
    <p><strong>{t["part_b"]}</strong></p>
    <p>{E(t["part_p"])}</p>
    <div class="llista-prod">{plinks(t["part_links"])}</div>
    <a class="btn btn-linia" href="{P["ass"]}">{t["descobreix"]} {ic("arrow")}</a>
  </div>
</div></section>
<section class="wrap cta-wrap">
  <div class="cta apareix">
    <div><h2>{t["parlem_t"]}</h2><p>{t["parlem_p"]}</p></div>
    <button class="btn btn-blau" data-obrir="simple">{t["et_truquem"]} {ic("phone")}</button>
  </div>
</section>
<section class="seccio"><div class="wrap bloc invers">
  <div class="bloc-img apareix"><img src="../img/img_empresas.jpg" alt="" width="600" height="382" loading="lazy"><div class="xip"><span class="ic">{ic("brief")}</span>{t["emp_xip"]}</div></div>
  <div class="apareix">
    <span class="etiqueta">{t["emp_et"]}</span>
    <h2>{t["emp_t"]}</h2>
    <p><strong>{t["emp_b"]}</strong></p>
    <p>{E(t["emp_p"])}</p>
    <div class="llista-prod">{plinks(t["emp_links"])}</div>
    <a class="btn btn-linia" href="{P["ass"]}#div-empreses">{t["descobreix"]} {ic("arrow")}</a>
  </div>
</div></section>
<section class="seccio alt"><div class="wrap">
  <div class="cap-centre apareix"><span class="etiqueta">{t["perque_et"]}</span><h2>{t["perque_t"]}</h2><p>{t["perque_p"]}</p><p><a class="blau" href="{P["nos"]}"><strong>{t["sobre"]} →</strong></a></p></div>
  <div class="motius" data-llum>{motius}</div>
</div></section>
<section class="seccio"><div class="wrap companyies">
  <div class="apareix"><span class="etiqueta">{t["comp_et"]}</span><h2>{t["comp_t"]}</h2><p class="intro">{t["comp_p"]}</p></div>
  <div class="carrusel apareix"><div class="pista">{logos()}</div></div>
</div></section>
''' + foot(L)
    w(L, P["inici"], index)

    # ---------- ASSEGURANCES ----------
    D = PRODS[L]; prods = D["prods"]
    def card(k):
        icn = PICONS.get(k, "shield")
        if k == "camper":
            return f'<a class="prod" href="{CONFICARAVAN}" target="_blank" rel="noopener"><span class="ic">{ic(icn)}</span><h3>{t["camper_t"]}</h3><span class="mes">{t["web_externa"]} ↗</span></a>'
        return f'<button class="prod" data-prod="{k}"><span class="ic">{ic(icn)}</span><h3>{E(marca(prods[k]["t"]))}</h3><span class="mes">{t["mes_info"]} {ic("arrow")}</span></button>'
    part = list(D["order"]["part"]); part.insert(part.index("moto")+1, "camper")
    altre = f'<button class="prod altre" data-obrir="simple"><span class="ic">{ic("plus")}</span><h3>{t["altre_t"]}</h3><p>{t["altre_p"]}</p><span class="mes">{t["tajudem"]} {ic("arrow")}</span></button>'
    dades = {k: {"t": marca(v["t"]), "p": [marca(x) for x in v["p"]], "i": PICONS.get(k, "shield")} for k, v in prods.items() if k not in ("final", "simple_form")}
    ass = head(L, "ass", t["ass_title"], t["ass_desc"]) + f'''
<section class="cap-pagina amb-foto" style="--foto:url('../img/fons/bk_seguros_top.jpg')"><div class="wrap">
  <span class="etiqueta">{t["nav"]["ass"]}</span>
  <h1>{t["ass_h1"]}</h1>
  <div class="botons-tipus"><a class="btn btn-blau" href="#div-particulars">{t["soc_part"]}</a><a class="btn btn-transp" href="#div-empreses">{t["soc_emp"]}</a></div>
</div></section>
<section class="seccio" id="div-particulars"><div class="wrap">
  <div class="intro-panell"><h2>{t["ass_part_t"]}</h2>{"".join(f'<p class="intro">{p}</p>' for p in t["ass_part_p"])}</div>
  <div class="graella">{"".join(card(k) for k in part)}{altre}</div>
</div></section>
<section class="seccio alt" id="div-empreses"><div class="wrap">
  <div class="intro-panell"><h2>{t["ass_emp_t"]}</h2>{"".join(f'<p class="intro">{p}</p>' for p in t["ass_emp_p"])}</div>
  <div class="graella">{"".join(card(k) for k in D["order"]["emp"])}</div>
</div></section>
<section class="wrap cta-wrap" style="padding:80px 24px 100px">
  <div class="cta"><div><h2>{t["aseso_t"]}</h2><p>{t["aseso_p"]}</p></div><button class="btn btn-blau" data-obrir="simple">{t["consultans"]} {ic("arrow")}</button></div>
</section>
<dialog id="dlg" aria-labelledby="dlg-t">
  <div class="dlg">
    <div class="dlg-text"><span class="dlg-ic"></span><h2 id="dlg-t"></h2><div class="cos"></div></div>
    <div class="dlg-form"><button class="tancar" aria-label="{t["tancar"]}">{ic("x")}</button>
      <h3>{t["m_titol"]}</h3><p>{t["m_text"]}</p>
      {form(L, missatge=False, boto=t["f_enviar"])}
    </div>
  </div>
</dialog>
<script>window.PRODUCTES={json.dumps(dades, ensure_ascii=False)};window.ICONES={json.dumps({k: I[v["i"]] for k, v in dades.items()}, ensure_ascii=False)};</script>
''' + foot(L)
    w(L, P["ass"], ass)

    # ---------- NOSALTRES ----------
    nv = "".join(f'<div class="valor apareix"><div class="ic">{ic(a)}</div><small>{b.upper()}</small><h3>{b}</h3><p>{c}</p></div>' for a,b,c in t["nos_valors"])
    nos = head(L, "nos", t["nos_title"], t["nos_desc"]) + f'''
<section class="cap-pagina amb-foto" style="--foto:url('../img/fons/bk_confisegur.jpg')"><div class="wrap">
  <span class="etiqueta">{t["nos_et"]}</span>
  <h1>{t["nos_h1"]}</h1>
  <p class="intro">{t["nos_sub"]}</p>
</div></section>
<section class="seccio"><div class="wrap text-llarg">
  <div class="apareix"><span class="etiqueta">{t["nos_et"]}</span><p class="xifra-cita">{t["nos_cita"]}</p></div>
  <div class="cos apareix"><p>{t["nos_p1"].format(ass=P["ass"])}</p><p>{t["nos_p2"]}</p></div>
</div></section>
<section class="seccio alt"><div class="wrap"><div class="valors">{nv}</div></div></section>
<section class="seccio"><div class="wrap">
  <div class="valor-afegit apareix">
    <div><span class="etiqueta" style="color:#8fa0ff">{t["va_t"]}</span><h2>{t["va_t"]}</h2></div>
    <div>{"".join(f"<p>{E(p)}</p>" for p in t["va_p"])}</div>
  </div>
</div></section>
<section class="seccio alt"><div class="wrap">
  <div class="cap-centre apareix"><span class="etiqueta">{t["oficines_t"]}</span><h2>{t["nos_of_t"]}</h2><p>{t["nos_of_p"]}</p></div>
  {oficines_html(L, amb_mapa=False)}
  <p style="text-align:center;margin-top:32px"><a class="btn btn-linia" href="{P["con"]}#oficines">{t["com_arribar"]} {ic("arrow")}</a></p>
</div></section>
<section class="seccio"><div class="wrap companyies">
  <div><span class="etiqueta">{t["comp_et"]}</span><h2>{t["comp_t"]}</h2><p class="intro">{t["comp_p"]}</p></div>
  <div class="carrusel"><div class="pista">{logos()}</div></div>
</div></section>
''' + foot(L)
    w(L, P["nos"], nos)

    # ---------- CONTACTE ----------
    hor = "".join(f'<b>{a}</b><span>{b}</span>' if b else f'<span class="dies">{a}</span>' for a,b in t["horari_rows"])
    soc = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n.capitalize()}"><svg viewBox="0 0 24 24" aria-hidden="true">{p}</svg></a>' for n,(u,p) in SOC.items())
    con = head(L, "con", t["con_title"], t["con_desc"], "pag-contacte") + f'''
<section class="cap-pagina amb-foto" style="--foto:url('../img/fons/bk_contacto.jpg')"><div class="wrap">
  <span class="etiqueta">{t["nav"]["con"]}</span>
  <h1>{t["con_h1"]}</h1>
  <p class="intro">{t["con_p"]}</p>
</div></section>
<section class="seccio"><div class="wrap">
  <div class="contacte-grid">
    <div class="caixa"><h2 style="font-size:1.8rem;margin-bottom:24px">{t["form_t"]}</h2>{form(L, missatge=True, assumpte=True)}</div>
    <div class="info-c">
      <div class="item"><span class="ic">{ic("phone")}</span><div><h4>{t["telefon"]}</h4><a href="{TEL_H}">{TEL}</a><br><a href="{wa(L)}" target="_blank" rel="noopener">620 957 920 (WhatsApp)</a></div></div>
      <div class="item"><span class="ic">{ic("mail")}</span><div><h4>{t["correu"]}</h4><a href="mailto:{MAIL}">{MAIL}</a></div></div>
      <div class="item"><span class="ic">{ic("clock")}</span><div><h4>{t["horari"]}</h4><div class="horari">{hor}</div></div></div>
      <div class="item"><span class="ic">{ic("users")}</span><div><h4>{t["xarxes"]}</h4><div class="xarxes clara">{soc}</div></div></div>
    </div>
  </div>
</div></section>
<section class="seccio alt" id="oficines"><div class="wrap">
  <div class="cap-centre"><span class="etiqueta">{t["oficines_t"]}</span><h2>{t["of_t"]}</h2><p>{t["of_p"]}</p></div>
  {oficines_html(L)}
</div></section>
<link rel="stylesheet" href="../vendor/leaflet/leaflet.css">
<script src="../vendor/leaflet/leaflet.js" defer></script>
''' + foot(L)
    w(L, P["con"], con)

    # ---------- LEGAL ----------
    src = {"legal": "legal", "priv": "privacidad", "cook": "cookies", "trans": "transparencia"}
    for k, s in src.items():
        body = LEGAL[L][s]
        pg = head(L, k, f'{t["legal_titles"][k]} · Configrup', t["legal_titles"][k]) + f'''
<section class="cap-pagina"><div class="wrap"><span class="etiqueta">{t["legal_t"]}</span><h1>{t["legal_titles"][k]}</h1></div></section>
<section class="seccio" style="padding-top:48px"><div class="wrap text-legal">
<!-- Text legal original de confisergur.com amb la nova raó social CONFIGRUP BROKERS, S.L. i el domini configrup.com. -->
{body}
</div></section>
''' + foot(L)
        w(L, PAG[L][k], pg)
    # ---------- INCIDÈNCIA DE SEGURETAT ----------
    it = INCI[L]["t"]
    pg = head(L, "inc", f'{it} · Configrup', AVIS[L]["p1"]) + f'''
<section class="cap-pagina"><div class="wrap"><span class="etiqueta">{AVIS[L]["etiqueta"]}</span><h1>{it}</h1></div></section>
<section class="seccio" style="padding-top:48px"><div class="wrap text-legal text-inc">
{INCI[L]["body"]}
</div></section>
''' + foot(L, avis=False)
    w(L, P["inc"], pg)
    # ---------- MAPA WEB ----------
    items = [(t["nav"]["inici"], P["inici"]), (t["nav"]["ass"], P["ass"]), (t["nav"]["nos"], P["nos"]), (t["nav"]["con"], P["con"])] + [(v, P[kk]) for kk, v in t["legal_links"].items() if kk != "map"]
    mp = head(L, "map", f'{t["map_h1"]} · Configrup', t["map_h1"]) + f'''
<section class="cap-pagina"><div class="wrap"><span class="etiqueta">Configrup</span><h1>{t["map_h1"]}</h1></div></section>
<section class="seccio" style="padding-top:48px"><div class="wrap mapa-web"><ul>
{"".join(f'<li><a href="{h}">{n}</a></li>' for n,h in items)}
<li><span>{t["nav"]["ass"]}</span><ul>{"".join(f'<li><a href="{P["ass"]}#{k}">{E(marca(prods[k]["t"]))}</a></li>' for k in D["order"]["part"] + D["order"]["emp"])}</ul></li>
<li><a href="{CANAL}" target="_blank" rel="noopener">{t["canal"]}</a></li>
<li><a href="{P["inc"]}">{INCI[L]["t"]}</a></li>
</ul></div></section>
''' + foot(L)
    w(L, P["map"], mp)

for L in ("ca", "es"):
    run(L)

# Arrel: sempre obre en català
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write('''<!DOCTYPE html>
<html lang="ca"><head><meta charset="utf-8"><title>Configrup · Corredoria d'assegurances</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=ca/index.html">
<link rel="alternate" hreflang="ca" href="ca/index.html"><link rel="alternate" hreflang="es" href="es/index.html">
<script>location.replace("ca/index.html")</script>
</head><body><p><a href="ca/index.html">Català</a> · <a href="es/index.html">Castellano</a></p></body></html>''')
# sitemap.xml i robots.txt
urls = [f"https://configrup.com/{L}/{PAG[L][k]}" for L in ("ca","es") for k in ("inici","ass","nos","con","inc","legal","priv","cook","trans")]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nSitemap: https://configrup.com/sitemap.xml\n")
# Netejar les pàgines antigues d'una sola llengua
for f in ("index.html.old",):
    pass
print("ok")
