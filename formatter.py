import re


def format_report(report: str) -> str:
    """
    Converts markdown report to HTML for Streamlit rendering.
    Handles headers, bold, bullet points, and citation markers.
    """
    html = report

    # H2 headers
    html = re.sub(r'^## (.+)$', r'<h3 style="color:#1a56a0;margin-top:1.2rem;margin-bottom:0.4rem">\1</h3>', html, flags=re.MULTILINE)
    # H3 headers
    html = re.sub(r'^### (.+)$', r'<h4 style="color:#333;margin-top:1rem">\1</h4>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    # Citation markers — style them
    html = re.sub(r'\[(\d+)\]', r'<sup style="color:#4a90e2;font-weight:600">[\1]</sup>', html)
    # Bullet points
    lines = html.split('\n')
    in_list = False
    result = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                result.append('<ul style="margin:0.4rem 0 0.4rem 1.2rem">')
                in_list = True
            result.append(f'<li style="margin:0.2rem 0">{stripped[2:]}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if stripped:
                result.append(f'<p style="margin:0.5rem 0;line-height:1.75">{line}</p>')
    if in_list:
        result.append('</ul>')

    return '\n'.join(result)
