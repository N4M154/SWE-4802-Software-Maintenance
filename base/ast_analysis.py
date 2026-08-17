import ast

with open("utils/validators.py", "r") as f:
    source = f.read()

tree = ast.parse(source)
print(ast.dump(tree, indent=2))