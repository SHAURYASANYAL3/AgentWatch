import ast
import os

def insert_docstrings(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    lines = source.splitlines()

    insertions = {}

    def add_insertion(lineno, col_offset, text):
        if lineno not in insertions:
            insertions[lineno] = []
        insertions[lineno].append((col_offset, text))

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                # The body starts at node.body[0].lineno
                # We want to insert the docstring just before the first line of the body.
                body_start = node.body[0].lineno - 1
                col_offset = node.body[0].col_offset
                indent = " " * col_offset
                insertions[body_start] = [f'{indent}"""Docstring."""']

        elif isinstance(node, ast.Module):
            if not ast.get_docstring(node):
                if node.body:
                    body_start = node.body[0].lineno - 1
                    insertions[body_start] = ['"""Docstring."""']

    if not insertions:
        return

    new_lines = []
    for i, line in enumerate(lines):
        if i in insertions:
            for ins in insertions[i]:
                new_lines.append(ins)
        new_lines.append(line)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines) + "\n")

for root, _, files in os.walk("agentwatch"):
    for file in files:
        if file.endswith(".py"):
            try:
                insert_docstrings(os.path.join(root, file))
            except Exception as e:
                print(f"Error on {file}: {e}")
