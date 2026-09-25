from html import escape
from pathlib import Path
import re
import base64

source = Path('REVIEW2_SUBMISSION.md').read_text()
output = []
in_code = False
paragraph = []

def inline(text):
    text = re.sub(r'!\[([^]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" width="680">', text)
    text = re.sub(r'<img ([^>]+)>', r'<img \1>', text)
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    return text

def flush():
    if paragraph:
        output.append('<p>' + inline(' '.join(paragraph)) + '</p>')
        paragraph.clear()

for raw in source.splitlines():
    line = raw.strip()
    if line.startswith('```'):
        flush()
        if not in_code:
            output.append('<pre>')
        else:
            output.append('</pre>')
        in_code = not in_code
        continue
    if in_code:
        output.append(escape(raw) + '\n')
        continue
    if not line:
        flush()
        continue
    image = re.match(r'<img\s+([^>]+)>', line)
    if image:
        flush()
        image_attributes = image.group(1)
        source_match = re.search(r'src="screenshots/([^" ]+)"', image_attributes)
        if source_match:
            image_path = Path('screenshots') / source_match.group(1)
            image_data = base64.b64encode(image_path.read_bytes()).decode('ascii')
            image_attributes = image_attributes.replace(
                source_match.group(0),
                'src="data:image/png;base64,' + image_data + '"',
            )
        output.append('<div class="evidence-image"><img ' + image_attributes + '></div>')
        continue
    if line.startswith('# '):
        flush(); output.append('<h1>' + inline(line[2:]) + '</h1>'); continue
    if line.startswith('## '):
        flush(); output.append('<h2>' + inline(line[3:]) + '</h2>'); continue
    if line.startswith('### '):
        flush(); output.append('<h3>' + inline(line[4:]) + '</h3>'); continue
    if line == '---':
        flush(); output.append('<hr>'); continue
    if line.startswith('> '):
        flush(); output.append('<div class="placeholder">' + inline(line[2:]) + '</div>'); continue
    if line.startswith('- '):
        flush(); output.append('<p class="bullet">&#8226; ' + inline(line[2:]) + '</p>'); continue
    if re.match(r'^\d+\. ', line):
        flush(); output.append('<p class="bullet">' + inline(line) + '</p>'); continue
    if line.startswith('|'):
        flush(); output.append('<p class="table-line">' + inline(line.replace('|', '  |  ')) + '</p>'); continue
    paragraph.append(line)
flush()

html = '''<!doctype html><html><head><meta charset="utf-8"><title>Framewise Review 2 Submission</title>
<style>
@page { size: A4; margin: 18mm; } body { font-family: Arial, sans-serif; color:#202124; font-size:10.5pt; line-height:1.45; } h1 { color:#b00020; font-size:22pt; margin:0 0 8pt; } h2 { color:#b00020; font-size:16pt; border-bottom:1px solid #ddd; padding-bottom:4pt; margin-top:20pt; } h3 { color:#333; font-size:12.5pt; margin-top:16pt; } p { margin:6pt 0; } code, pre { font-family: 'Courier New', monospace; } code { background:#f0f0f0; padding:1pt 3pt; } pre { background:#f3f3f3; border:1px solid #ddd; padding:8pt; white-space:pre-wrap; font-size:8pt; } .placeholder { border:1px dashed #999; min-height:45pt; padding:10pt; margin:8pt 0; color:#555; } .evidence-image { margin:12pt 0 20pt; page-break-inside:avoid; } .evidence-image img { max-width:100%; height:auto; } .bullet { margin-left:14pt; } .table-line { font-family:Arial; font-size:9pt; } hr { border:0; border-top:1px solid #ddd; margin:16pt 0; } strong { font-weight:700; }
</style></head><body>''' + ''.join(output) + '</body></html>'
Path('REVIEW2_SUBMISSION.html').write_text(html)
