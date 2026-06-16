#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generar_smart_pass.py
Soul Circle™ Smart Pass Generator v2.0 (fusión unificada)
Soul Lens Studios · Powered by Xplorers Startups
Arquitecto: Ed Zam · Mérida, Yucatán

USO:
  python generar_smart_pass.py                    # Genera todos los activos
  python generar_smart_pass.py anais-hidalgo      # Genera uno específico
  python generar_smart_pass.py --lista            # Lista todos los embajadores
  python generar_smart_pass.py --pendientes       # Solo los que faltan fotos
  python generar_smart_pass.py --todos            # Activos + pendientes

REQUISITOS: Python 3.8+ · Sin dependencias externas
"""

import json
import os
import sys
import re
from urllib.parse import quote
from pathlib import Path
from datetime import datetime
import unicodedata

# ════════════════════════════════════════════════
# CONFIGURACIÓN
# ════════════════════════════════════════════════
BASE_DIR     = Path(__file__).parent
TEMPLATE     = BASE_DIR / "Smart_Pass_MASTER_TEMPLATE.html"
DB_FILE      = BASE_DIR / "SoulCircle_SmartPass_v2.0_Embajadores.json"
# Fallback al nombre genérico si no existe el canónico
if not DB_FILE.exists():
    _alt = BASE_DIR / "embajadores.json"
    if _alt.exists(): DB_FILE = _alt
OUTPUT_DIR   = BASE_DIR / "output_smart_passes"
LOG_FILE     = BASE_DIR / "generador.log"

SITE_BASE    = "https://soullensstudios.live"
PASS_URL     = f"{SITE_BASE}/embajador/"

# ════════════════════════════════════════════════
# LOGGER
# ════════════════════════════════════════════════
def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ════════════════════════════════════════════════
# CARGAR DATOS
# ════════════════════════════════════════════════
def cargar_db():
    if not DB_FILE.exists():
        log(f"ERROR: No se encontró {DB_FILE}", "ERROR")
        sys.exit(1)
    with open(DB_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("embajadores", [])

def cargar_template():
    if not TEMPLATE.exists():
        log(f"ERROR: No se encontró {TEMPLATE}", "ERROR")
        log("Asegúrate de que Smart_Pass_MASTER_TEMPLATE.html esté en el mismo directorio.", "ERROR")
        sys.exit(1)
    with open(TEMPLATE, encoding="utf-8") as f:
        return f.read()

# ════════════════════════════════════════════════
# GENERADOR DE VARIABLES
# ════════════════════════════════════════════════
def enc(s):
    """URL-encode para VCF y WhatsApp"""
    return quote(str(s or ""), safe="")

def generar_variables(e):
    """Construye el diccionario completo de 38 variables para un embajador."""

    nombre    = e.get("nombre_completo", "")
    first     = e.get("nombre_first", nombre.split()[0] if nombre else "")
    last      = e.get("nombre_last", " ".join(nombre.split()[1:]) if " " in nombre else "")
    slug      = e.get("slug", "")
    pass_id   = e.get("pass_id", "")
    wa        = e.get("wa_number", "")
    city      = e.get("schema_locality", e.get("ciudad", "Mérida").split(",")[0].strip())
    region    = e.get("schema_region", "Yucatán")
    titulo    = e.get("titulo_hero", "")
    rol       = e.get("rol_corto", "")
    rol_cred  = e.get("rol_credencial", "Embajador/a de Expansión · AI Soul Lens Studios")
    band      = e.get("band_label", "Arquitecto/a Fundador/a")
    origen    = e.get("origen", "")
    bio       = e.get("bio_html", "")
    quote_txt = e.get("quote", "")
    meta_desc = e.get("meta_description", "")

    # Mercados → HTML pills
    mercados_html = "\n    ".join(
        f'<span class="mpill">{m}</span>' for m in e.get("mercados", [])
    )

    # WhatsApp messages
    wa_hero   = enc(f"Hola, te contacto desde el Smart Pass de {nombre} · Soul Lens Studios.")
    wa_bottom = enc(f"Hola, te contacto desde el Smart Pass de {nombre} · Soul Lens Studios. Quisiera explorar cómo pueden ayudar a mi negocio.")

    # VCF
    vcf_fn = enc(f"{nombre} · Soul Lens Studios")
    vcf_n  = enc(f"{last};{first};;;")
    vcf_t  = enc(titulo)

    def _ascii(s): return ''.join(c for c in unicodedata.normalize('NFD', str(s)) if unicodedata.category(c)!='Mn')
    img_prefix   = _ascii(first).lower().strip().replace(' ', '-')
    vcf_filename = (_ascii(first).strip() + '_' + _ascii(last).strip() + '_SoulLens.vcf').replace(' ', '_')

    # Meta
    page_title  = f"{nombre} · Smart Pass Soul Circle™ · Soul Lens Studios"
    meta_suffix = f"{titulo} — {SITE_BASE}"
    og_desc     = meta_desc or f"Conecta con {nombre} — {rol} en {city}. Soul Lens Studios · Soul Circle™."
    twitter_d   = og_desc
    schema_job  = e.get("schema_job_title", f"{rol} · Soul Lens Studios")

    # CTAs
    cta_label  = f"Hablar con {first}"
    cta_bottom = (f"Escríbele a {first} directo. Sin formularios, sin esperas. "
                  "Una conversación honesta — y el equipo de Soul Lens Studios "
                  "te dice exactamente qué necesita tu negocio para posicionarse.")

    # Hobbies
    hobbies    = e.get("hobbies", [{}] * 5)
    hbb_vars   = {}
    for i in range(5):
        h = hobbies[i] if i < len(hobbies) else {}
        hbb_vars[f"HBB_NOMBRE_{i}"] = h.get("nombre", "")
        hbb_vars[f"HBB_SUB_{i}"]    = h.get("sub", "")

    vars_map = {
        "PASS_ID":          pass_id,
        "SLUG":             slug,
        "WA_NUMBER":        wa,
        "WA_TEXT_HERO":     wa_hero,
        "WA_TEXT_BOTTOM":   wa_bottom,
        "VCF_FN":           vcf_fn,
        "VCF_N":            vcf_n,
        "VCF_TITLE":        vcf_t,
        "SCHEMA_JOB_TITLE": schema_job,
        "SCHEMA_LOCALITY":  city,
        "SCHEMA_REGION":    region,
        "PAGE_TITLE":       page_title,
        "META_TITLE_SUFFIX":meta_suffix,
        "META_DESC":        meta_desc or og_desc,
        "OG_DESC":          og_desc,
        "TWITTER_DESC":     twitter_d,
        "NOMBRE_COMPLETO":  nombre,
        "NOMBRE_FIRST":     first,
        "NOMBRE_LAST":      last,
        "TITULO_HERO":      titulo,
        "ROL_CORTO":        rol,
        "ROL_CREDENCIAL":   rol_cred,
        "BAND_LABEL":       band,
        "ORIGEN":           origen,
        "BIO_HTML":         bio,
        "QUOTE":            quote_txt,
        "CTA_WA_LABEL":     cta_label,
        "CTA_BOTTOM_TEXT":  cta_bottom,
        "MERCADOS_PILLS":   mercados_html,
        "IMG_PREFIX":       img_prefix,
        "VCF_FILENAME":     vcf_filename,
        **hbb_vars,
    }

    return vars_map

# ════════════════════════════════════════════════
# INYECTOR DE VARIABLES
# ════════════════════════════════════════════════
def inyectar(template, vars_map):
    """Reemplaza todas las {{VARIABLES}} en el template."""
    html = template
    for key, val in vars_map.items():
        html = html.replace(f"{{{{{key}}}}}", str(val or ""))

    # Verificar variables no reemplazadas
    restantes = re.findall(r"\{\{([^}]+)\}\}", html)
    if restantes:
        log(f"  ⚠ Variables sin reemplazar: {restantes}", "WARN")

    return html

# ════════════════════════════════════════════════
# GENERADOR PRINCIPAL
# ════════════════════════════════════════════════
def generar(embajador, template):
    """Genera el Smart Pass HTML de un embajador."""
    slug    = embajador.get("slug", "")
    pass_id = embajador.get("pass_id", "")
    nombre  = embajador.get("nombre_completo", "")

    log(f"Generando: {nombre} · {pass_id}")

    vars_map = generar_variables(embajador)
    html     = inyectar(template, vars_map)

    # Nombre del archivo
    fname = f"Smart_Pass_{slug}_{pass_id}.html"
    fpath = OUTPUT_DIR / fname

    OUTPUT_DIR.mkdir(exist_ok=True)
    try:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(html)
        size = fpath.stat().st_size // 1024
        log(f"  ✓ {fname} ({size}KB) → {PASS_URL}{slug}/")
        return fpath
    except OSError as e:
        log(f"  ✗ Error al escribir {fname}: {e}", "ERROR")
        return None

# ════════════════════════════════════════════════
# COMANDOS
# ════════════════════════════════════════════════
def cmd_lista(embajadores):
    """Lista todos los embajadores con su estado."""
    print("\n" + "═" * 60)
    print("  Soul Circle™ Smart Pass System · Embajadores 2026")
    print("═" * 60)
    sc = [e for e in embajadores if e.get("programa") == "SC"]
    ns = [e for e in embajadores if e.get("programa") == "NS"]

    for grupo, nombre in [(sc, "Soul Circle™"), (ns, "Núcleo Soul™")]:
        print(f"\n  {nombre}:")
        for e in grupo:
            estado  = e.get("estado", "—")
            fotos   = e.get("fotos", {})
            slug    = e.get("slug", "")
            pass_id = e.get("pass_id", "")
            slots   = [fotos.get("hero"), fotos.get("perfil"), fotos.get("og")] + fotos.get("galeria", [])
            ok      = sum(1 for s in slots if s)
            total   = len(slots)
            pct     = round(ok / total * 100) if total else 0
            icono   = "✓" if estado == "activo" else "⏳"
            print(f"  {icono} {e.get('nombre_completo', '').ljust(22)} "
                  f"{pass_id.ljust(24)} "
                  f"fotos {pct:3d}%  {slug}")

    print("\n" + "═" * 60)
    activos  = sum(1 for e in embajadores if e.get("estado") == "activo")
    pend     = sum(1 for e in embajadores if e.get("estado") == "pendiente")
    print(f"  Total: {len(embajadores)} · Activos: {activos} · Pendientes: {pend}")
    print("═" * 60 + "\n")

def cmd_pendientes(embajadores):
    """Muestra embajadores con fotos incompletas."""
    print("\n📷 Fotos pendientes:\n")
    for e in embajadores:
        fotos = e.get("fotos", {})
        pend  = fotos.get("pendientes", [])
        if pend:
            first   = e.get("nombre_first", "")
            fn_low  = first.lower()
            print(f"  {e.get('nombre_completo')} · {e.get('pass_id')}")
            for p in pend:
                if p == "hero":
                    print(f"    → {fn_low}-hero.jpg · 1080×1920px")
                elif p == "perfil":
                    print(f"    → {fn_low}-perfil.jpg · 400×400px")
                elif p == "og":
                    print(f"    → og.jpg · 1200×630px")
                else:
                    num = p.replace("gal-", "")
                    print(f"    → {fn_low}-{num}.jpg · 400×576px")
            print()

# ════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════
def main():
    args      = sys.argv[1:]
    template  = cargar_template()
    todos     = cargar_db()

    if not args or args[0] == "--todos":
        # Generar todos los activos (o todos si --todos)
        filtro = todos if "--todos" in args else [e for e in todos if e.get("estado") == "activo"]
        log(f"Generando {len(filtro)} Smart Passes...")
        for e in filtro:
            generar(e, template)
        log(f"✓ Completado. Archivos en: {OUTPUT_DIR}/")

    elif args[0] == "--lista":
        cmd_lista(todos)

    elif args[0] == "--pendientes":
        cmd_pendientes(todos)

    else:
        # Buscar por slug
        slug   = args[0].lower().strip()
        match  = next((e for e in todos if e.get("slug") == slug), None)
        if not match:
            # Buscar por nombre parcial
            match = next((e for e in todos
                         if slug in e.get("nombre_completo", "").lower()
                         or slug in e.get("slug", "")), None)
        if not match:
            log(f"ERROR: No se encontró embajador con slug o nombre '{slug}'", "ERROR")
            log("Usa --lista para ver todos los slugs disponibles.", "INFO")
            sys.exit(1)
        generar(match, template)
        log("✓ Smart Pass generado correctamente.")

if __name__ == "__main__":
    main()
