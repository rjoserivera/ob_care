"""
Script mejorado para analizar tags de Django template
"""
import re

with open('templates/Matrona/detalle_ficha_obstetrica.html', 'r', encoding='utf-8') as f:
    content = f.read()
    lines = content.split('\n')

# Buscar todos los tags if, elif, else, endif
if_pattern = re.compile(r'{%\s*if\s+')
elif_pattern = re.compile(r'{%\s*elif\s+')
else_pattern = re.compile(r'{%\s*else\s*%}')
endif_pattern = re.compile(r'{%\s*endif\s*%}')

stack = []
all_tags = []

for i, line in enumerate(lines, 1):
    # Buscar todos los tipos de tags
    for match in if_pattern.finditer(line):
        stack.append(('if', i, line.strip()))
        all_tags.append((i, 'if', line.strip()))
    
    for match in elif_pattern.finditer(line):
        all_tags.append((i, 'elif', line.strip()))
    
    for match in else_pattern.finditer(line):
        all_tags.append((i, 'else', line.strip()))
    
    for match in endif_pattern.finditer(line):
        all_tags.append((i, 'endif', line.strip()))
        if stack:
            stack.pop()
        else:
            print(f"⚠️  ERROR: endif sin if en línea {i}")
            print(f"    {line.strip()}")

print(f"\n📊 Resumen:")
print(f"Total de if sin cerrar: {len(stack)}\n")

if stack:
    print("❌ Tags if sin cerrar:")
    for tag_type, line_num, content in stack:
        print(f"  Línea {line_num}: {content[:100]}")
        # Mostrar contexto
        print(f"    Contexto:")
        for j in range(max(0, line_num-2), min(len(lines), line_num+1)):
            print(f"      {j+1}: {lines[j][:100]}")
        print()

print(f"\n📋 Todos los tags encontrados:")
for line_num, tag_type, content in all_tags[-20:]:  # Últimos 20
    print(f"  {line_num:4d} [{tag_type:5s}] {content[:80]}")
