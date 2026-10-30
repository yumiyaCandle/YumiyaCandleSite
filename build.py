"""Génère nuvo-boutique.html : le site en un seul fichier, photos incluses.
Usage : python3 build.py [fichier_sortie] [--fragment]"""
import base64, re, sys
args = [a for a in sys.argv[1:] if not a.startswith('--')]
out = args[0] if args else 'nuvo-boutique.html'
s = open('index.html').read()
names = sorted(set(re.findall(r"img/(\w+)\.jpg", s)))
data = {n: 'data:image/jpeg;base64,' + base64.b64encode(open(f'img/{n}.jpg', 'rb').read()).decode() for n in names}
imgs = 'const IMG = {' + ','.join(f'"img/{n}.jpg":"{d}"' for n, d in data.items()) + '};\n'
s = re.sub(r'<img([^>]*?) src="(img/\w+\.jpg)"', r'<img\1 data-src="\2"', s)
s = s.replace("img:'img/", "img:IMG['img/").replace(".jpg', tag", ".jpg'], tag").replace(' loading="lazy"', '')
s = s.replace("<script>\n", "<script>\n" + imgs + "document.querySelectorAll('img[data-src]').forEach(i => i.src = IMG[i.dataset.src]);\n", 1)
if '--fragment' in sys.argv:  # version sans <html>/<head>/<body>, pour l'aperçu en ligne
    head = re.search(r'<head>(.*?)</head>', s, re.S).group(1)
    head = re.sub(r'<meta (charset|name="viewport")[^>]*>\n?', '', head)
    body = re.search(r'<body>(.*)</body>', s, re.S).group(1)
    s = head.strip() + '\n' + body.strip() + '\n'
open(out, 'w').write(s)
print(out, len(s) // 1024, 'Ko')
