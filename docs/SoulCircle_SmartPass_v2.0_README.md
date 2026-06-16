# Soul Circle™ · Smart Pass System 2026
## Guía de Deploy Completa
### Soul Lens Studios · Powered by Xplorers Startups

---

## ESTRUCTURA COMPLETA DEL SISTEMA

```
Soul Circle™ Smart Pass System 2026
├── FORMULARIOS DE REGISTRO (embajadores los llenan)
│   ├── circle-intake-SC.html         ← Soul Circle™ · Arquitectos Fundadores
│   └── circle-intake-NS.html         ← Núcleo Soul™ · Soul Origen™
│
├── ADMIN DASHBOARD (solo Ed Zam + Val Mosquera)
│   └── circle-admin-dashboard-v3.html
│
├── GENERADOR DE SMART PASSES
│   ├── Smart_Pass_MASTER_TEMPLATE.html   ← NO editar nunca
│   ├── embajadores.json                  ← Fuente de verdad
│   ├── generar_smart_pass.py             ← Motor Python
│   └── output_smart_passes/              ← HTMLs generados (auto-creado)
│
├── ARCHIVOS DE DEPLOY
│   ├── sitemap.xml
│   ├── robots.txt
│   ├── schema.json
│   ├── manifest.json
│   ├── .htaccess                ← Apache
│   ├── vercel.json              ← Vercel
│   └── _redirects               ← Netlify / Cloudflare Pages
│
└── DOCUMENTACIÓN
    ├── SoulCircle_Schema_Datos_9x16_v2.html
    └── SoulCircle_Schema_Datos_v2.docx
```

---

## ESTRUCTURA EN EL SERVIDOR

```
circle.soullensstudios.live/           ← Admin + formularios
├── index.html                         ← circle-admin-dashboard-v3.html
├── unete/
│   └── index.html                     ← circle-intake-SC.html
├── nucleo/
│   └── index.html                     ← circle-intake-NS.html
├── Smart_Pass_MASTER_TEMPLATE.html    ← Necesario para generar en dashboard
├── manifest.json
└── robots.txt

soullensstudios.live/                  ← Smart Passes públicos
├── sitemap.xml
├── robots.txt
├── schema.json
├── manifest.json
├── .htaccess
└── embajador/
    ├── anais-hidalgo/
    │   ├── index.html                 ← Smart Pass HTML
    │   ├── anais-hero.jpg             ← 1080×1920px
    │   ├── anais-perfil.jpg           ← 400×400px
    │   ├── og.jpg                     ← 1200×630px
    │   └── anais-01.jpg … 09.jpg      ← 400×576px c/u
    ├── carlos-mendez/
    ├── valentina-flores/
    ├── lucia-garcia/
    ├── sofia-ruiz/
    └── edwin-rodriguez/
```

---

## PASO A PASO: DEPLOY COMPLETO

### PASO 1 — Servidor (Apache/Netlify/Vercel/Cloudflare)

**Apache:**
```bash
# Subir .htaccess a la raíz de soullensstudios.live/
# Subir .htaccess a circle.soullensstudios.live/
```

**Netlify / Cloudflare Pages:**
```bash
# Subir _redirects a la raíz
# No necesitas .htaccess
```

**Vercel:**
```bash
# vercel.json ya está configurado
vercel --prod
```

---

### PASO 2 — Admin Dashboard

```bash
# Subir a circle.soullensstudios.live/
circle-admin-dashboard-v3.html  → index.html
Smart_Pass_MASTER_TEMPLATE.html → Smart_Pass_MASTER_TEMPLATE.html
```

---

### PASO 3 — Formularios de registro

```bash
# circle.soullensstudios.live/unete/
circle-intake-SC.html → unete/index.html

# circle.soullensstudios.live/nucleo/
circle-intake-NS.html → nucleo/index.html
```

---

### PASO 4 — Archivos SEO y PWA

```bash
# Subir a soullensstudios.live/
sitemap.xml
robots.txt
schema.json
manifest.json
.htaccess    (solo Apache)
```

---

### PASO 5 — Generar Smart Passes

```bash
# En tu máquina local — requiere Python 3.8+
# Todos los archivos en la misma carpeta:
# Smart_Pass_MASTER_TEMPLATE.html + embajadores.json + generar_smart_pass.py

# Ver todos los embajadores
python3 generar_smart_pass.py --lista

# Generar todos los activos
python3 generar_smart_pass.py

# Generar uno específico
python3 generar_smart_pass.py anais-hidalgo

# Ver fotos pendientes
python3 generar_smart_pass.py --pendientes
```

---

### PASO 6 — Subir Smart Passes

Para cada embajador generado:

```bash
# 1. Renombrar el HTML
mv Smart_Pass_anais-hidalgo_PASS-SLS-2026-ANA-H.html index.html

# 2. Crear carpeta en el servidor
# soullensstudios.live/embajador/anais-hidalgo/

# 3. Subir archivos:
# index.html
# anais-hero.jpg    (1080×1920px)
# anais-perfil.jpg  (400×400px)
# og.jpg            (1200×630px)
# anais-01.jpg … anais-09.jpg (400×576px)

# 4. URL final:
# https://soullensstudios.live/embajador/anais-hidalgo/
```

---

### PASO 7 — Verificar Open Graph (WhatsApp preview)

```
https://developers.facebook.com/tools/debug/
URL: https://soullensstudios.live/embajador/anais-hidalgo/
```

---

## FLUJO OPERATIVO DIARIO

```
NUEVO EMBAJADOR:
1. Embajador llena circle.soullensstudios.live/unete/
2. Descarga su JSON
3. Equipo SLS añade el JSON a embajadores.json
4. python3 generar_smart_pass.py [slug]
5. Subir HTML + fotos al servidor
6. URL activa: soullensstudios.live/embajador/[slug]/
7. Embajador comparte su URL
```

---

## ESPECIFICACIONES DE FOTOS

| Slot | Nombre de archivo | Dimensiones | Formato |
|------|-------------------|-------------|---------|
| Hero | `[nombre]-hero.jpg` | 1080×1920px | JPG/WebP |
| Perfil | `[nombre]-perfil.jpg` | 400×400px | JPG/WebP |
| OG/WhatsApp | `og.jpg` | 1200×630px | JPG |
| Galería 1-9 | `[nombre]-01.jpg` … | 400×576px | JPG/WebP |

Nomenclatura: nombre en minúsculas sin acentos.
`Anais Hidalgo` → `anais`
Ejemplo: `anais-hero.jpg`, `anais-01.jpg`

---

## CONVENCIÓN DE PASS IDs

```
Soul Circle™:  PASS-SLS-2026-[3LETRAS]-[INICIAL]
Núcleo Soul™:  PASS-NS-2026-[3LETRAS]-[INICIAL]

Anais Hidalgo    → PASS-SLS-2026-ANA-H
Carlos Méndez    → PASS-SLS-2026-CAR-M
Edwin Rodríguez  → PASS-NS-2026-EDW-R
```

---

## PROGRAMAS DEL ECOSISTEMA

| Programa | Band label | Pass prefix | Acceso al formulario |
|----------|-----------|-------------|---------------------|
| Soul Circle™ | Arquitecto/a Fundador/a | PASS-SLS-2026 | circle.soullensstudios.live/unete/ |
| Núcleo Soul™ | Soul Origen™ | PASS-NS-2026 | circle.soullensstudios.live/nucleo/ |

---

## CONTACTO

**Ed Zam** · Arquitecto de Realidades
Xplorers Startups · Soul Lens Studios
M�rida, Yucatán · México

**Val Mosquera** · CEO · Soul Lens Studios

---

*Soul Circle™ Smart Pass System v2.0*
*Powered by Xplorers Startups*
*Ciclo Fundador 2026 · 02 jun – 30 nov*
