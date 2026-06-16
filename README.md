# SoulCircle Smart Pass · v2.0

Ecosistema de embajadores de **Soul Lens Studios** — Soul Circle™ + Núcleo Soul™.
Sistema 100% estático, listo para Cloudflare Pages. 

## Estructura (2 dominios)

```
public/   → soullensstudios.live        (pases públicos + SEO)
  embajador/{slug}/index.html           pase de cada embajador
  sitemap.xml · robots.txt · manifest.json
  _headers · _redirects                 config nativa Cloudflare Pages

circle/   → circle.soullensstudios.live (admin · privado)
  admin/    Dashboard (CRM)
  unete/    Intake Soul Circle™
  nucleo/   Intake Núcleo Soul™
  Smart_Pass_MASTER_TEMPLATE.html · embajadores.json
  _headers  (noindex)

tools/    (no se sirven — corren local)
  Generador.py   genera pases desde embajadores.json
  FotoPrep.py    optimiza fotos (resize + WebP + nombrado)

docs/     README de deploy · esquema de datos · reporte de fusión
```

## Deploy en Cloudflare Pages (2 proyectos, mismo repo)

**Proyecto 1 — público**
- Connect to Git → este repo
- Build command: *(ninguno)*
- Build output directory: `public`
- Custom domain: `soullensstudios.live`

**Proyecto 2 — circle (admin)**
- Connect to Git → este repo (Root directory avanzado: `circle`)
- Build command: *(ninguno)* · Output: `circle`
- Custom domain: `circle.soullensstudios.live`
- **Cloudflare Access** (Zero Trust) sobre todo el proyecto → login por email.

## Publicar fotos de un embajador (sin editar HTML)
```
python tools/FotoPrep.py --prefix carlos --in ./crudas --out ./salida
# subir el contenido de ./salida a public/embajador/carlos-mendez/
```
Las fotos aparecen solas (capa <picture> con fallback SVG).

## Pendientes / Fase 2
- Embajadores pendientes (marco, rodrigo, valeria): generar con `tools/Generador.py --todos` y mover a `public/embajador/`.
- Supabase: persistir submissions del intake + DB compartida + auth (cierra el loop intake→dashboard).

—
Soul Lens Studios · Powered by Xplorers Startups · Ed Zam · Mérida, Yucatán
