# Reporte de Fusión — Ecosistema de Embajadores
## SoulCircle Smart Pass · v1.0 → v2.0 (Fusión Unificada)
### Soul Lens Studios · Powered by Xplorers Startups · Ed Zam · Mérida, Yucatán

---

## 1. Esquema canónico declarado

**`band_label` + `fotos.galeria` · `programa: SC/NS`**

Decidido por evidencia: 4 de 5 componentes (Intake SC, Intake NS, Embajadores.json,
Generador) ya hablaban este esquema. El Dashboard era el único outlier y fue alineado.

---

## 2. Fracturas resueltas

| # | Fractura | Severidad | Resolución |
|---|----------|-----------|------------|
| B1 | Dashboard usaba `band`/`gal`; el resto `band_label`/`galeria` | CRÍTICO | Dashboard alineado al canon (19 `band_label`, 24 `galeria`, 0 legacy). Reconstrucción token-level, sin inyección de bloques. |
| B2 | Intake_NS nunca seleccionaba su config `int` (se quedaba en `ext`) | CRÍTICO | `let programa = (PROG_LOCKED === 'NS') ? 'int' : 'ext'`. NS ahora emite prefijo `PASS-NS-2026` y banda `Soul Origen™`. |
| B3 | Intake emitía `programa: ext/int`; el sistema filtra por `SC/NS` | CRÍTICO | La salida ahora emite `programa: PROG_LOCKED` (`SC`/`NS`). Un solo idioma punta a punta. |
| B4 | Generador buscaba `embajadores.json` ≠ archivo real | ESTRATÉGICO | Apunta a `SoulCircle_SmartPass_v2.0_Embajadores.json` (+ fallback). |
| B5 | Deriva de versión (archivos v1.0 vs _meta 2.0) | ESTRATÉGICO | Paquete, archivos y `_meta` unificados en v2.0. |
| B6 | Intake_NS arrastraba el campo `por_que_sc` | ESTRATÉGICO | Renombrado a `por_que_ns` (6 ocurrencias). |

**Falso positivo descartado:** posible crash por `PROG_CONFIG[programa]` undefined —
verificado, no existía (era el tail de `data._programa`).

---

## 3. Validación final

- Motor end-to-end: **9/9 Smart Passes generados, cero variables sin reemplazar.**
- Prefijos NS correctos: `PASS-NS-2026-EDW-R`, `PASS-NS-2026-VAL-M`.
- Balance de JS: Dashboard, Intake_SC, Intake_NS, 404 → todos `{}=0 ()=0 []=0`.
- Sin funciones duplicadas: `showView()=1`, `navTo()=1`.
- Dashboard: 0 referencias legacy `band`/`gal` restantes.
- WhatsApp único (`5215644844928`) y arquitectura de 2 dominios coherente.

---

## 4. Contrato de datos unificado (referencia)

```
Captación (Intake SC/NS)
  └─ emite: { ..., band_label, fotos:{hero,perfil,og,galeria[]}, programa:'SC'|'NS' }
        ↓
Admin (Dashboard)  ── lee/escribe el MISMO esquema ──┐
        ↓                                            │
Motor (Generador.py + MASTER_TEMPLATE)               │
  └─ DB: SoulCircle_SmartPass_v2.0_Embajadores.json ─┘
        ↓
Pase público  → soullensstudios.live/embajador/[slug]/
```

---

## 5. Decisión abierta (nomenclatura de versión)

Dos planos de versión conviven por diseño:
- **PASS / Plantilla** → `Prototipo v1.0` (correcto: etapa prototipo, sin fotos reales).
- **SISTEMA** → Dashboard "System v1.0" / Intake "Generator v1.0".

Pendiente de tu sign-off: subir las etiquetas de SISTEMA a v2.0 y dejar el PASS en
`Prototipo v1.0` hasta que entren fotos reales (futuro `Prototipo v1.1`).

---

## 6. Estructura de deploy

```
soullensstudios.live/embajador/[slug]/   → pases públicos (generados)
circle.soullensstudios.live/             → dashboard + intakes
  ├── /              → Dashboard
  ├── /unete/        → Intake_SC
  └── /nucleo/       → Intake_NS
```

—
SoulCircle Smart Pass v2.0 · Fusión unificada · Generado por Ed Zam


---

## 7. Auditoría de deploy — Round 2 (cableado · carga · SEO · a11y)

### Cableado corregido
- **Hub** enlazaba a nombres viejos (`circle-intake-SC.html`, `circle-admin-dashboard-v3.html`, `README_deploy.md`). Reapuntado a rutas de producción: `/unete/`, `/nucleo/`, `/admin/` (circle.soullensstudios.live) + docs v2.0.

### Pase público — corregido y optimizado
- **vCard:** el atributo `download` estaba hardcodeado a `Anais_Hidalgo_SoulLens.vcf` en todo pase. Ahora `{{VCF_FILENAME}}` → cada quien descarga su propio contacto (acentos normalizados: `Lucia_Garcia`, `Sofia_Ruiz`).
- **Imágenes:** referencias de slot pasaron de `anais-*.jpg` semánticas a `{{IMG_PREFIX}}-hero/-01…-09.jpg` per-embajador y numéricas — alineadas con el generador (`--pendientes`) y los docs de deploy.
- **CLS:** ejemplos de imagen ahora con `width`/`height` (hero 1080×1920, galería 400×576), hero con `fetchpriority="high"`, galería con `loading="lazy"`.
- **Carga:** `dns-prefetch` para fonts + `preconnect`/`dns-prefetch` para YouTube (el iframe ya cargaba diferido vía `data-src`).
- **Accesibilidad:** `.skip-link` + target `#sp-content`, `:focus-visible`, `<noscript>` con fallback a WhatsApp.
- **Residual de nombre:** 0 ocurrencias de "anais" en pases de otros embajadores (antes 25, incl. labels/alts en comentarios).

### Validación de código
- **JS parseado con Node** (`node --check`): Dashboard, Intake_SC (×2), Intake_NS (×2) y pase generado → **6/6 scripts sintácticamente válidos.**
- El conteo de brackets marcaba `()`=+2 en el pase: confirmado **benigno** (paréntesis dentro de strings `rgba(...)` y callbacks), no error de sintaxis.
- 9/9 pases regenerados con **cero variables sin reemplazar**.

### Infra verificada (sin cambios necesarios)
- SEO meta del pase: charset, lang, viewport (sin `user-scalable=no`), canonical, OG completo, Twitter card, JSON-LD (Person/Organization/PostalAddress). Tier-1.
- Robots: AI crawlers bienvenidos (GPTBot, anthropic-ai, Claude-Web, PerplexityBot, Google-Extended) + Sitemap.
- JSON (manifest/schema/vercel): válidos. Server configs (Apache/Vercel/Netlify): rutas y cache-control correctos.
- Copy: 0 vocabulario prohibido (`empresa`/`submarca`/`básico`/`sencillo`).

**Estado: deploy-ready.**


---

## 8. Pipeline de fotos reales — Upload-driven (v2.0)

**Problema resuelto:** antes, publicar una foto exigía editar el HTML a mano (reemplazar el SVG por `<img>`). Ahora las fotos se publican **subiendo archivos**, sin tocar código.

### Mecanismo (en los 11 slots del pase)
Cada slot (hero · perfil · galería ×9) renderiza una capa `<picture>` real **sobre** el placeholder SVG:
```
<picture>
  <source srcset="{prefix}-01.webp" type="image/webp">   ← WebP (más liviano)
  <img class="photo-real" src="{prefix}-01.jpg" width="400" height="576" loading="lazy"
       onload="…loaded (fade-in)…" onerror="…se retira, queda el SVG…">
</picture>
<svg> … placeholder editorial … </svg>                     ← fallback
```
- Foto existe → el `<img>` carga y cubre el placeholder (fade-in).
- Foto ausente (404) → el `<img>` se retira solo, queda el SVG. **Sin errores visibles.**

### Optimización de carga
- **WebP + fallback JPG** vía `<picture>` (≈30-40% menos peso en navegadores modernos).
- `width`/`height` en todos los slots (anti-CLS) · galería `loading="lazy"` · hero `fetchpriority="high"` (LCP).

### Herramienta: `SoulCircle_SmartPass_v2.0_FotoPrep.py`
Toma las fotos crudas de un embajador y entrega los archivos listos:
```
python SoulCircle_SmartPass_v2.0_FotoPrep.py --prefix carlos --in ./crudas --out ./carlos-mendez
```
- Redimensiona a spec (hero 1080×1920 · perfil 400×400 · og 1200×630 · galería 400×576), cover-crop.
- Comprime JPG (q82, progresivo) + genera WebP (q80).
- Nombra solo: `carlos-hero.jpg/.webp`, `carlos-01.jpg/.webp` … `carlos-09`, `carlos-perfil`, y `og.jpg` genérico.
- Reconoce slots por nombre crudo (`hero*`, `perfil*`, `og*`, `01*`/`gal-3`/`03_evento`…).

### Flujo operativo
```
Fotos crudas → FotoPrep.py → subir salida a /embajador/{slug}/ → fotos vivas
```
Cero edición de HTML. Cero regeneración. Aplica igual a Soul Circle™ y Núcleo Soul™.
