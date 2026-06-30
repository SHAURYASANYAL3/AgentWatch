import os
import libcst as cst

class DocstringAdder(cst.CSTTransformer):
    def _add_docstring(self, node):
        if node.get_docstring() is None:
            # We need to insert a SimpleStatementLine containing an Expr with a SimpleString
            docstring_node = cst.SimpleStatementLine(
                body=[cst.Expr(value=cst.SimpleString(value='"""Docstring."""'))]
            )
            # Prepend to the body
            new_body = (docstring_node,) + node.body.body
            
            return node.with_changes(body=node.body.with_changes(body=new_body))
        return node

    def leave_FunctionDef(self, original_node, updated_node):
        return self._add_docstring(updated_node)

    def leave_ClassDef(self, original_node, updated_node):
        return self._add_docstring(updated_node)

    def leave_Module(self, original_node, updated_node):
        # Optional: Add module docstrings safely
        return updated_node

def process_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        
        module = cst.parse_module(source)
        modified_module = module.visit(DocstringAdder())
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(modified_module.code)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    for root, _, files in os.walk("agentwatch"):
        for file in files:
            if file.endswith(".py"):
                process_file(os.path.join(root, file))
