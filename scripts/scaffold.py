"""Copy the verified editable scene starter into a new output folder."""
import argparse
from pathlib import Path
import shutil
p=argparse.ArgumentParser()
p.add_argument('--out',required=True,type=Path)
p.add_argument('--reference',required=True,type=Path,help='Path to your own PNG workstation photo')
a=p.parse_args()
skill=Path(__file__).resolve().parents[1]
ref=a.reference.expanduser().resolve()
if not ref.is_file(): p.error(f'Image does not exist: {ref}')
# Build embeds PNG MIME, so require PNG rather than silently mislabelling JPEG.
if ref.read_bytes()[:8] != b'\x89PNG\r\n\x1a\n': p.error('Input must be PNG; explicitly convert other image formats first.')
out=a.out.resolve()
if out.exists(): p.error(f'Refusing to overwrite existing output: {out}')
shutil.copytree(skill/'assets/template',out)
shutil.copy2(ref,out/'reference.png')
(out/'evidence').mkdir()
print(f'Created {out}. Inspect reference.png and adapt src/scene-spec.json AND src/main.js before building.')
