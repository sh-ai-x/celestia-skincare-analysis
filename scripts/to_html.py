"""Simple notebook → HTML converter."""
import nbformat
from pathlib import Path
import html
import re

nb_path = Path('/Users/sanghee/dev/research_data_ananlysis/docs/reports/20260625-celestia-skincare-ingredients.ipynb')
html_path = Path('/Users/sanghee/dev/research_data_ananlysis/docs/reports/20260625-celestia-skincare-ingredients.html')

with open(nb_path) as f:
    nb = nbformat.read(f, as_version=4)

out = ['<!DOCTYPE html><html lang="ko"><head><meta charset="UTF-8">']
out.append('<title>Celestia Dermatology 스킨케어 성분 분석</title>')
out.append('<style>body{font-family:-apple-system,"Apple SD Gothic Neo","Malgun Gothic",sans-serif;max-width:1100px;margin:40px auto;padding:0 20px;color:#222;line-height:1.6} h1{color:#2c3e50;border-bottom:3px solid #3498db;padding-bottom:10px} h2{color:#34495e;margin-top:40px;border-left:4px solid #3498db;padding-left:12px} h3{color:#555} table{border-collapse:collapse;margin:15px 0} th,td{border:1px solid #ddd;padding:8px 12px} th{background:#3498db;color:white} blockquote{border-left:4px solid #f39c12;padding-left:12px;color:#555;background:#fafafa} pre{background:#f4f4f4;padding:12px;border-radius:4px;overflow-x:auto;white-space:pre-wrap} .cell{margin:20px 0} .code-output{background:#1e1e1e;color:#d4d4d4;padding:12px;border-radius:4px;white-space:pre-wrap} img{max-width:100%;height:auto}</style>')
out.append('</head><body>')

def md_to_html(s):
    s = html.escape(s)
    # Tables (basic)
    lines = s.split('\n')
    result = []
    in_table = False
    in_ul = False
    for line in lines:
        if line.startswith('# '):
            if in_ul: result.append('</ul>'); in_ul=False
            result.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            if in_ul: result.append('</ul>'); in_ul=False
            result.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            if in_ul: result.append('</ul>'); in_ul=False
            result.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('- '):
            if not in_ul: result.append('<ul>'); in_ul=True
            result.append(f'<li>{line[2:]}</li>')
        elif '|' in line and line.count('|') >= 2:
            if in_ul: result.append('</ul>'); in_ul=False
            cells_l = [c.strip() for c in line.split('|')[1:-1]]
            if line.replace('|','').replace('-','').strip() == '':
                continue
            if not in_table:
                result.append('<table>')
                in_table = True
            result.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells_l) + '</tr>')
        elif line.strip() == '':
            if in_ul: result.append('</ul>'); in_ul=False
            if in_table: result.append('</table>'); in_table=False
            result.append('')
        elif line.startswith('> '):
            if in_ul: result.append('</ul>'); in_ul=False
            result.append(f'<blockquote>{line[2:]}</blockquote>')
        else:
            if in_ul: result.append('</ul>'); in_ul=False
            if in_table: result.append('</table>'); in_table=False
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'`(.+?)`', r'<code>\1</code>', line)
            result.append(f'<p>{line}</p>')
    if in_ul: result.append('</ul>')
    if in_table: result.append('</table>')
    return '\n'.join(result)

for cell in nb.cells:
    if cell.cell_type == 'markdown':
        out.append('<div class="cell">')
        out.append(md_to_html(cell.source))
        out.append('</div>')
    elif cell.cell_type == 'code':
        out.append('<div class="cell">')
        out.append('<details open><summary style="cursor:pointer;color:#3498db;font-weight:600">▼ 코드</summary><pre>')
        out.append(html.escape(cell.source))
        out.append('</pre></details>')
        out.append('<div style="margin-top:8px"><strong style="color:#555">▶ 출력:</strong>')
        for output in cell.get('outputs', []):
            if output.output_type == 'stream':
                out.append(f'<div class="code-output">{html.escape(output.text)}</div>')
            elif output.output_type in ('execute_result', 'display_data'):
                if 'text/plain' in output.get('data', {}):
                    out.append(f'<div class="code-output">{html.escape(output["data"]["text/plain"])}</div>')
                if 'image/png' in output.get('data', {}):
                    out.append(f'<img src="data:image/png;base64,{output["data"]["image/png"]}"/>')
        out.append('</div>')
        out.append('<hr style="margin:30px 0;border:0;border-top:1px dashed #ccc"/>')
        out.append('</div>')

out.append('</body></html>')

with open(html_path, 'w') as f:
    f.write('\n'.join(out))
print(f"OK: {html_path} ({html_path.stat().st_size} bytes)")