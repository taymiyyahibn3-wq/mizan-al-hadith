import json

with open('openapi_extracted.json', 'r', encoding='utf-8') as f:
    spec = json.load(f)

lines = []
lines.append('# MĪZĀN AL-ḤADĪTH — REST API ENDPOINT REFERENCE\n')
lines.append('**Document Identifier:** `docs/api/endpoint-reference.md`  ')
lines.append(f'**Total Endpoints Documented:** {len(spec.get("paths", {}))} Paths (95 operations)  ')
lines.append('**OpenAPI Version:** 3.1.0  \n')
lines.append('---\n')
lines.append('## 1. Master Endpoint Index\n')
lines.append('| Method | Endpoint Path | Summary / Purpose | Category |')
lines.append('| :--- | :--- | :--- | :--- |')

items = []
for path, methods in spec.get('paths', {}).items():
    for method, op in methods.items():
        if method.lower() not in ('get', 'post', 'put', 'delete', 'patch'):
            continue
        tag = (op.get('tags') or ['General'])[0]
        summary = op.get('summary') or op.get('description') or 'Endpoint operation'
        summary = summary.replace('\n', ' ').strip()
        items.append((method.upper(), path, tag, summary, op))

for m, p, t, s, _ in sorted(items, key=lambda x: (x[2], x[1], x[0])):
    lines.append(f'| `{m}` | `{p}` | {s} | {t} |')

lines.append('\n---\n')
lines.append('## 2. Detailed Endpoint Specifications\n')

current_tag = ''
for m, p, t, s, op in sorted(items, key=lambda x: (x[2], x[1], x[0])):
    if t != current_tag:
        current_tag = t
        lines.append(f'\n### Category: {current_tag}\n')
    lines.append(f'#### `{m}` `{p}`')
    lines.append(f'**Summary:** {s}\n')
    
    # Parameters
    params = op.get('parameters', [])
    if params:
        lines.append('**Parameters:**')
        lines.append('| Name | In | Required | Type | Description |')
        lines.append('| :--- | :--- | :--- | :--- | :--- |')
        for param in params:
            p_name = param.get('name')
            p_in = param.get('in')
            p_req = 'Yes' if param.get('required') else 'No'
            p_type = param.get('schema', {}).get('type', 'any')
            p_desc = (param.get('description') or '').replace('\n', ' ')
            lines.append(f'| `{p_name}` | {p_in} | {p_req} | `{p_type}` | {p_desc} |')
        lines.append('')
        
    # Request Body
    if 'requestBody' in op:
        rb = op['requestBody']
        content = rb.get('content', {}).get('application/json', {})
        schema = content.get('schema', {})
        ref = schema.get('$ref', '')
        schema_name = ref.split('/')[-1] if ref else 'Inline'
        lines.append(f'**Request Body:** `application/json` (Schema: `{schema_name}`)')
        lines.append('')

    # Responses
    responses = op.get('responses', {})
    lines.append('**Responses:**')
    for code, resp in responses.items():
        desc = resp.get('description', '')
        lines.append(f'- **HTTP {code}:** {desc}')
    lines.append('\n---\n')

with open('docs/api/endpoint-reference.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('Successfully generated docs/api/endpoint-reference.md')
