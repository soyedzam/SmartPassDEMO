#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SoulCircle Smart Pass · FotoPrep v2.0
Soul Lens Studios · Powered by Xplorers Startups · Ed Zam

Optimiza, redimensiona, comprime y nombra las fotos de un embajador
para que se publiquen subiéndolas a su carpeta — sin editar HTML.

USO:
  python SoulCircle_SmartPass_v2.0_FotoPrep.py --prefix carlos --in ./crudas --out ./carlos-mendez

Las fotos crudas se reconocen por palabra clave en el nombre:
  hero* perfil* og*  y  01* 02* ... 09*  (o gal1, gal01, etc.)
Genera por cada una un .jpg comprimido + un .webp (más liviano).

REQUISITOS: Python 3.8+ · Pillow (pip install pillow)
"""
import sys, argparse, re
from pathlib import Path
try:
    from PIL import Image, ImageOps
except ImportError:
    print("✗ Falta Pillow. Instala con:  pip install pillow"); sys.exit(1)

# slot -> (ancho, alto)  según spec del Smart Pass
SPECS = {
    "hero":   (1080, 1920),
    "perfil": (400, 400),
    "og":     (1200, 630),
    **{f"{i:02d}": (400, 576) for i in range(1, 10)},
}
JPG_Q, WEBP_Q = 82, 80

def slot_de(nombre):
    n = nombre.lower()
    if "hero" in n:   return "hero"
    if "perfil" in n or "avatar" in n: return "perfil"
    if "og" in n:     return "og"
    m = re.search(r'(?<![0-9])0*([1-9])(?![0-9])', n)   # 1..9 / 01..09 / 03_evento / gal-3
    if m: return f"{int(m.group(1)):02d}"
    return None

def procesar(src, slot, prefix, out):
    w, h = SPECS[slot]
    img = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    img = ImageOps.fit(img, (w, h), Image.LANCZOS, centering=(0.5, 0.4))  # cover-crop, leve sesgo arriba
    # 'og' es genérico por carpeta (lo lee el meta og:image) y solo en JPG (compat. social)
    if slot == "og":
        img.save(out / "og.jpg", "JPEG", quality=JPG_Q, optimize=True, progressive=True)
        kj = (out / "og.jpg").stat().st_size // 1024
        return f"og.jpg  →  {w}×{h}  ·  jpg {kj}KB  (preview social)"
    base = out / f"{prefix}-{slot}"
    img.save(f"{base}.jpg",  "JPEG", quality=JPG_Q, optimize=True, progressive=True)
    img.save(f"{base}.webp", "WEBP", quality=WEBP_Q, method=6)
    kj = Path(f"{base}.jpg").stat().st_size // 1024
    kw = Path(f"{base}.webp").stat().st_size // 1024
    return f"{prefix}-{slot}  →  {w}×{h}  ·  jpg {kj}KB / webp {kw}KB"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", required=True, help="prefijo del embajador, ej: carlos")
    ap.add_argument("--in",  dest="inp", required=True, help="carpeta de fotos crudas")
    ap.add_argument("--out", required=True, help="carpeta de salida (lista para subir)")
    a = ap.parse_args()
    inp, out = Path(a.inp), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)

    crudas = [p for p in inp.iterdir() if p.suffix.lower() in (".jpg",".jpeg",".png",".webp",".heic",".tif",".tiff")]
    if not crudas:
        print(f"✗ Sin imágenes en {inp}"); sys.exit(1)

    print(f"\n  FotoPrep · embajador '{a.prefix}'  ({len(crudas)} fotos crudas)\n" + "─"*54)
    hechos = set()
    for p in sorted(crudas):
        slot = slot_de(p.stem)
        if not slot:
            print(f"  ⚠ ignorada (sin slot reconocible): {p.name}"); continue
        if slot in hechos:
            print(f"  ⚠ slot '{slot}' duplicado, ignoro: {p.name}"); continue
        try:
            print("  ✓ " + procesar(p, slot, a.prefix, out)); hechos.add(slot)
        except Exception as e:
            print(f"  ✗ error en {p.name}: {e}")

    faltan = [s for s in SPECS if s not in hechos]
    print("─"*54)
    print(f"  Listas: {len(hechos)}/{len(SPECS)}  →  {out}/")
    if faltan: print(f"  Faltan: {', '.join(faltan)}")
    print(f"\n  Subir el contenido de {out}/ a la carpeta del embajador.")
    print("  Las fotos aparecen solas en el Smart Pass (sin editar HTML).\n")

if __name__ == "__main__":
    main()
