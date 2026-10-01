import ast
import os

missing = []
for root, _, files in os.walk('src'):
    for file in files:
        if file.endswith('.py'):
            path = os.path.join(root, file)
            with open(path) as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        missing.append(f"{path}: {node.name}")

if missing:
    print("Missing docstrings in:")
    for m in missing:
        print(m)
else:
    print("All functions and classes have docstrings.")
