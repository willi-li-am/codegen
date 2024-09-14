import os
import sys
import importlib
import ast

class ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imports = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            for alias in node.names:
                self.imports.append(f"{node.module}.{alias.name}")
        self.generic_visit(node)

def is_local_import(module_name):
    # Extract the base module if there are submodules
    base_module = module_name.split('.')[0]
    
    try:
        # Find the module specification (location)
        spec = importlib.util.find_spec(base_module)
        
        if spec is not None:
            # Check if the module file path is within the current working directory (local project)
            module_file = os.path.abspath(spec.origin)
            project_dir = os.getcwd()
            
            return module_file.startswith(project_dir)
        else:
            return False
    except ModuleNotFoundError:
        return False

def parse_repo(repo_path):
    res = {}
    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    content = f.read()
                readable_file_path = file_path.split(repo_path)[1]
                try:
                    tree = ast.parse(content)
                    visitor = ImportVisitor()
                    visitor.visit(tree)
                    res[readable_file_path] = []
                    for import_name in visitor.imports:
                        import_json = {
                            "name": import_name,
                            "is_local": False
                        }
                        res[readable_file_path].append(import_json)
                except SyntaxError:
                    print(f"Skipping file due to syntax error: {file_path}")
    return res
