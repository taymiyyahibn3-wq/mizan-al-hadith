import os
import re

broken_links = []
md_files = []

for root, _, files in os.walk('docs'):
    for f in files:
        if f.endswith('.md') or f.endswith('.html'):
            md_files.append(os.path.join(root, f))

md_files.append('README.md')

link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

for path in md_files:
    dir_path = os.path.dirname(path)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    for match in link_pattern.finditer(content):
        text, url = match.groups()
        # Skip external URLs, file:// scheme, anchors, mailto
        if url.startswith(('http://', 'https://', 'mailto:', '#', 'file:///')):
            continue
        # Strip anchor from relative URL
        clean_url = url.split('#')[0]
        if not clean_url:
            continue
        
        target = os.path.normpath(os.path.join(dir_path, clean_url))
        if not os.path.exists(target):
            broken_links.append((path, url, target))

print(f"Scanned {len(md_files)} files.")
if broken_links:
    print(f"Found {len(broken_links)} broken relative links:")
    for src, url, tgt in broken_links:
        print(f"  In {src}: link '{url}' -> target '{tgt}' NOT FOUND")
else:
    print("ALL RELATIVE DOCUMENTATION LINKS ARE 100% VALID!")
