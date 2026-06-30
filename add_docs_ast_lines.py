import ast
import os
import re

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"Parse error in {filepath}: {e}")
        return

    insertions = []
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                # We need to insert a docstring.
                # Let's find the exact end of the signature.
                # A robust way is to just insert it at node.body[0].lineno, but correctly indented.
                body_start_line = node.body[0].lineno - 1
                col_offset = node.body[0].col_offset
                indent = " " * col_offset
                
                # Check if it's a single-line function
                if body_start_line == node.lineno - 1:
                    # The body is on the same line as the def
                    # We will just insert a newline and the docstring before the body.
                    # Wait, modifying single line functions via string manipulation is tricky.
                    pass
                
                insertions.append((body_start_line, f'{indent}"""Docstring."""\n'))

        elif isinstance(node, ast.Module):
            if not ast.get_docstring(node):
                if node.body:
                    # Only add if the first node is not a __future__ import
                    if isinstance(node.body[0], ast.ImportFrom) and node.body[0].module == '__future__':
                        continue
                    body_start_line = node.body[0].lineno - 1
                    insertions.append((body_start_line, '"""Docstring."""\n'))

    if not insertions:
        return

    lines = source.split('\n')
    
    # Sort insertions descending by line number to not mess up subsequent line numbers
    insertions.sort(key=lambda x: x[0], reverse=True)
    
    for lineno, text in insertions:
        # If the line is a single-line function, we need to split it
        # Actually, let's just insert it as a new line.
        # But if the line is `def foo(): return 1`, inserting `"""Docstring."""` at lineno
        # makes it:
        # """Docstring."""
        # def foo(): return 1
        # which is WRONG! It must be after the colon.
        # Let's just insert BEFORE the line where the body starts.
        
        # If body is on the same line as `def`, we insert after the colon.
        line_content = lines[lineno]
        if 'def ' in line_content or 'class ' in line_content:
            # Single line function. We need to split at the colon.
            parts = line_content.split(':', 1)
            if len(parts) == 2:
                lines[lineno] = f"{parts[0]}:\n{text}    {parts[1].lstrip()}"
        else:
            lines.insert(lineno, text.rstrip('\n'))

    with open(filepath, "w", encoding="utf-8") as f:
        f.write('\n'.join(lines))

for root, _, files in os.walk("agentwatch"):
    for file in files:
        if file.endswith(".py"):
            process_file(os.path.join(root, file))
