import sys, os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
import numpy as np

D = os.path.dirname(os.path.abspath(__file__))
CHROME = os.path.expanduser('~/workspace/.tools/chrome-linux64/chrome')

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=['--no-sandbox','--force-device-scale-factor=1'])
    pg = b.new_page(viewport={'width':700,'height':300})
    pg.goto('file://'+os.path.join(D,'signature.html'))
    pg.wait_for_timeout(400)
    el = pg.query_selector('table')
    el.screenshot(path=os.path.join(D,'render.png'))
    b.close()

ren = Image.open(os.path.join(D,'render.png')).convert('RGB')
ref = Image.open(os.path.join(D,'ref.jpg')).convert('RGB').crop((76,176,644,359)).resize((600,194), Image.LANCZOS)
print('render', ren.size, 'ref', ref.size)
if ren.size != (600,194):
    ren = ren.resize((600,194))
diff = ImageChops.difference(ren, ref)
a = np.array(diff).astype(int).sum(axis=2)
print('mean abs diff:', round(a.mean(),2), '| p99:', int(np.percentile(a,99)), '| max:', int(a.max()))
# side by side
sbs = Image.new('RGB',(600*2+10,194),(255,0,0))
sbs.paste(ren,(0,0)); sbs.paste(ref,(610,0))
sbs.save(os.path.join(D,'side_by_side.png'))
# amplified diff heatmap
heat = np.clip(a*2,0,255).astype('uint8')
Image.fromarray(heat).save(os.path.join(D,'diff_heat.png'))
print('saved render.png side_by_side.png diff_heat.png')
