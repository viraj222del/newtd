import os
import re
import ast
from typing import Dict, Any, List, Set, Tuple, Optional
from collections import defaultdict

# File extensions that support AST parsing (Python)
AST_SUPPORTED_EXTENSIONS = {'.py'}

# Regex patterns for different languages
CLASS_PATTERNS = {
    '.py': r'^\s*class\s+(\w+)(?:\([^)]+\))?\s*:',
    '.js': r'^\s*(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+[\w.]+)?\s*{',
    '.ts': r'^\s*(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+[\w.]+)?(?:\s+implements\s+[\w.,\s]+)?\s*{',
    '.java': r'^\s*(?:public|private|protected)?\s*(?:abstract|final)?\s*class\s+(\w+)(?:\s+extends\s+[\w.]+)?(?:\s+implements\s+[\w.,\s]+)?\s*{',
    '.cs': r'^\s*(?:public|private|protected|internal)?\s*(?:abstract|sealed|static)?\s*class\s+(\w+)(?:\s*:\s*[\w.,\s]+)?\s*{',
    '.cpp': r'^\s*(?:class|struct)\s+(\w+)(?:\s*:\s*(?:public|private|protected)\s+[\w.]+)?\s*{',
    '.c': r'^\s*typedef\s+struct\s+(\w+)',
    '.dart': r'^\s*(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+[\w.]+)?(?:\s+implements\s+[\w.,\s]+)?\s*{',
    '.rs': r'^\s*(?:pub\s+)?(?:struct|enum|impl)\s+(\w+)',
    '.go': r'^\s*type\s+(\w+)\s+struct\s*{',
    '.php': r'^\s*(?:abstract\s+)?(?:final\s+)?class\s+(\w+)(?:\s+extends\s+[\w\\]+)?(?:\s+implements\s+[\w\\,]+)?\s*{',
    '.kt': r'^\s*(?:data\s+|sealed\s+|abstract\s+|open\s+)?(?:class|interface|object)\s+(\w+)(?:\s*:\s*[\w.,\s]+)?\s*{',
}

FUNCTION_PATTERNS = {
    '.py': r'^\s*(?:async\s+)?(?:def|async def)\s+(\w+)\s*\(',
    '.js': r'^\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s+)?\s*\(|(\w+)\s*:\s*\([^)]*\)\s*=>)',
    '.ts': r'^\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|(?:public|private|protected)?\s*(?:async\s+)?(\w+)\s*\(|const\s+(\w+)\s*[:=]\s*(?:async\s+)?)',
    '.java': r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:[\w<>]+\s+)?(\w+)\s*\(',
    '.cs': r'^\s*(?:public|private|protected|internal)?\s*(?:static|virtual|override|async)?\s*(?:[\w<>]+\s+)?(\w+)\s*\(',
    '.cpp': r'^\s*(?:[\w:<>]+\s+)?(\w+)\s*::\s*(\w+)\s*\(|^\s*(?:inline\s+)?(?:[\w:<>]+\s+)?(\w+)\s*\(',
    '.c': r'^\s*(?:[\w\s]+\s+)?(\w+)\s*\(',
    '.dart': r'^\s*(?:[\w<>]+\s+)?(\w+)\s*\([^)]*\)\s*(?::\s*[\w<>]+)?\s*{',
    '.rs': r'^\s*(?:pub\s+)?(?:async\s+)?fn\s+(\w+)\s*\(',
    '.go': r'^\s*func\s+(?:\(\s*[\w*]+\s+[\w]+\s*\)\s+)?(\w+)\s*\(',
    '.php': r'^\s*(?:public|private|protected)?\s*(?:static)?\s*(?:function\s+|fn\s+)(\w+)\s*\(',
    '.kt': r'^\s*(?:fun\s+|override\s+fun\s+|private\s+fun\s+|public\s+fun\s+)(\w+)\s*\(',
}

LOOP_PATTERNS = {
    '.py': [r'^\s*for\s+', r'^\s*while\s+', r'^\s*async\s+for\s+'],
    '.js': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*for\s*\([\w\s]+\s+in\s+', r'^\s*for\s*\([\w\s]+\s+of\s+'],
    '.ts': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*for\s*\([\w\s]+\s+in\s+', r'^\s*for\s*\([\w\s]+\s+of\s+'],
    '.java': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*for\s*\([\w\s]+\s*:\s*'],
    '.cs': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*foreach\s*\('],
    '.cpp': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*for\s*\([\w\s]+\s*:\s*'],
    '.c': [r'^\s*for\s*\(', r'^\s*while\s*\('],
    '.dart': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*for\s*\([\w\s]+\s+in\s+'],
    '.rs': [r'^\s*for\s+', r'^\s*while\s+', r'^\s*loop\s+'],
    '.go': [r'^\s*for\s+', r'^\s*for\s+[\w]+\s*:=\s*range'],
    '.php': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*foreach\s*\('],
    '.kt': [r'^\s*for\s*\(', r'^\s*while\s*\(', r'^\s*for\s*\([\w\s]+\s+in\s+'],
}

VARIABLE_PATTERNS = {
    '.py': [r'^\s*([\w_][\w\d_]*)\s*=', r'^\s*([\w_][\w\d_]*)\s*:\s*[\w\[\]]+'],
    '.js': [r'^\s*(?:var|let|const)\s+([\w_$][\w\d_$]*)'],
    '.ts': [r'^\s*(?:var|let|const)\s+([\w_$][\w\d_$]*)\s*[:=]'],
    '.java': [r'^\s*(?:[\w<>\[\]\s]+\s+)([\w_][\w\d_]*)\s*[=;]'],
    '.cs': [r'^\s*(?:[\w<>\[\]\s]+\s+)([\w_][\w\d_]*)\s*[=;]'],
    '.cpp': [r'^\s*(?:[\w:<>\[\]\s&*]+\s+)([\w_][\w\d_]*)\s*[=;]'],
    '.c': [r'^\s*(?:[\w\s*\[\]]+\s+)([\w_][\w\d_]*)\s*[=;]'],
    '.dart': [r'^\s*(?:var|final|const|[\w<>]+\s+)([\w_][\w\d_]*)\s*[:=]'],
    '.rs': [r'^\s*(?:let|mut\s+let|const)\s+([\w_][\w\d_]*)\s*[:=]'],
    '.go': [r'^\s*(?:var|const)\s+([\w_][\w\d_]*)\s*[\w=]'],
    '.php': [r'^\s*(?:\$)([\w_][\w\d_]*)'],
    '.kt': [r'^\s*(?:var|val)\s+([\w_][\w\d_]*)'],
}


class CodeStructure:
    """Represents structural elements extracted from a file."""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.classes: List[Dict[str, Any]] = []
        self.functions: List[Dict[str, Any]] = []
        self.variables: List[Dict[str, Any]] = []
        self.loops: List[Dict[str, Any]] = []
        self.imports: List[str] = []
        self.class_usage: Dict[str, List[str]] = defaultdict(list)  # class_name -> [files that use it]
        self.function_variable_usage: Dict[str, List[Dict[str, Any]]] = defaultdict(list)  # function_name -> [{'var': name, 'line': num, 'type': 'local'|'member'|'global'}]


class NodeVisitor(ast.NodeVisitor):
    """Custom visitor to track parent nodes."""
    def __init__(self, structure: CodeStructure):
        self.structure = structure
        self.current_class = None
        self.class_stack = []
        self.current_function = None
        self.function_stack = []
        self.class_members_cache = {}  # Cache class members for each class
    
    def visit_ClassDef(self, node):
        methods = []
        members = []
        
        # Extract base classes
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif hasattr(ast, 'unparse'):
                try:
                    bases.append(ast.unparse(base))
                except:
                    bases.append(str(base))
        
        # Store current class context
        old_class = self.current_class
        self.current_class = node.name
        self.class_stack.append(node.name)
        
        # Visit class body to extract methods and members
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item.name)
            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        if target.id not in members:
                            members.append(target.id)
                    elif isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self':
                        if target.attr not in members:
                            members.append(target.attr)
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    if item.target.id not in members:
                        members.append(item.target.id)
                elif isinstance(item.target, ast.Attribute) and isinstance(item.target.value, ast.Name) and item.target.value.id == 'self':
                    if item.target.attr not in members:
                        members.append(item.target.attr)
        
        self.structure.classes.append({
            'name': node.name,
            'line': node.lineno,
            'methods': methods,
            'members': members,
            'inheritance': bases,
            'loc': len([n for n in node.body if not isinstance(n, (ast.Expr, ast.Pass))])
        })
        
        # Cache class members for variable usage tracking
        self.class_members_cache[node.name] = members
        
        # Visit children
        self.generic_visit(node)
        
        # Restore previous class context
        self.current_class = old_class
        if self.class_stack:
            self.class_stack.pop()
    
    def visit_FunctionDef(self, node):
        # Track both top-level functions and methods
        params = [arg.arg for arg in node.args.args]
        func_full_name = f"{self.current_class}.{node.name}" if self.current_class else node.name
        
        if not self.current_class:
            # Top-level function
            self.structure.functions.append({
                'name': node.name,
                'line': node.lineno,
                'parameters': params,
                'async': False
            })
        
        # Set current function context for variable tracking
        old_function = self.current_function
        self.current_function = func_full_name
        self.function_stack.append(func_full_name)
        
        # Visit function body to track variable usage
        self.generic_visit(node)
        
        # Restore previous function context
        self.current_function = old_function
        if self.function_stack:
            self.function_stack.pop()
    
    def visit_AsyncFunctionDef(self, node):
        # Track both top-level functions and methods
        params = [arg.arg for arg in node.args.args]
        func_full_name = f"{self.current_class}.{node.name}" if self.current_class else node.name
        
        if not self.current_class:
            # Top-level function
            self.structure.functions.append({
                'name': node.name,
                'line': node.lineno,
                'parameters': params,
                'async': True
            })
        
        # Set current function context for variable tracking
        old_function = self.current_function
        self.current_function = func_full_name
        self.function_stack.append(func_full_name)
        
        # Visit function body to track variable usage
        self.generic_visit(node)
        
        # Restore previous function context
        self.current_function = old_function
        if self.function_stack:
            self.function_stack.pop()
    
    def visit_Import(self, node):
        for alias in node.names:
            self.structure.imports.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node):
        if node.module:
            self.structure.imports.append(node.module)
        self.generic_visit(node)
    
    def visit_For(self, node):
        self.structure.loops.append({
            'type': 'for',
            'line': node.lineno
        })
        self.generic_visit(node)
    
    def visit_AsyncFor(self, node):
        self.structure.loops.append({
            'type': 'async_for',
            'line': node.lineno
        })
        self.generic_visit(node)
    
    def visit_While(self, node):
        self.structure.loops.append({
            'type': 'while',
            'line': node.lineno
        })
        self.generic_visit(node)
    
    def visit_Assign(self, node):
        # Only track module-level variables
        if not self.current_class:
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_info = {
                        'name': target.id,
                        'line': node.lineno
                    }
                    # Avoid duplicates
                    if not any(v['name'] == target.id and abs(v['line'] - node.lineno) < 10 for v in self.structure.variables):
                        self.structure.variables.append(var_info)
        self.generic_visit(node)
    
    def visit_AnnAssign(self, node):
        # Only track module-level variables
        if not self.current_class and isinstance(node.target, ast.Name):
            var_info = {
                'name': node.target.id,
                'line': node.lineno
            }
            if not any(v['name'] == node.target.id and abs(v['line'] - node.lineno) < 10 for v in self.structure.variables):
                self.structure.variables.append(var_info)
        self.generic_visit(node)
    
    def visit_Name(self, node):
        """Track variable name usage within functions."""
        if self.current_function and isinstance(node.ctx, (ast.Load, ast.Store)):
            var_name = node.id
            
            # Skip Python built-ins and common keywords
            if var_name in ['self', 'cls', 'True', 'False', 'None', 'print', 'len', 'str', 'int', 'list', 'dict', 'set', 'tuple']:
                self.generic_visit(node)
                return
            
            # Determine variable type
            var_type = 'local'  # Default to local
            if self.current_class:
                # Check if it's a class member
                class_members = self.class_members_cache.get(self.current_class, [])
                if var_name in class_members:
                    var_type = 'member'
                elif var_name not in ['self']:  # Check if it's a parameter
                    # Check if it's in module-level variables
                    if any(v['name'] == var_name for v in self.structure.variables):
                        var_type = 'global'
            
            # Track variable usage
            usage_info = {
                'var': var_name,
                'line': node.lineno,
                'type': var_type
            }
            
            # Avoid duplicates (same variable on same line)
            if not any(u['var'] == var_name and u['line'] == node.lineno 
                      for u in self.structure.function_variable_usage[self.current_function]):
                self.structure.function_variable_usage[self.current_function].append(usage_info)
        
        self.generic_visit(node)
    
    def visit_Attribute(self, node):
        """Track attribute access (e.g., self.member, obj.attr)."""
        if self.current_function and isinstance(node.ctx, (ast.Load, ast.Store)):
            # Check if it's self.attribute (class member access)
            if isinstance(node.value, ast.Name) and node.value.id == 'self':
                var_name = node.attr
                var_type = 'member'
                
                usage_info = {
                    'var': var_name,
                    'line': node.lineno,
                    'type': var_type
                }
                
                # Avoid duplicates
                if not any(u['var'] == var_name and u['line'] == node.lineno 
                          for u in self.structure.function_variable_usage[self.current_function]):
                    self.structure.function_variable_usage[self.current_function].append(usage_info)
        
        self.generic_visit(node)


def analyze_python_file(file_path: str, content: str) -> CodeStructure:
    """Analyze Python file using AST parsing."""
    structure = CodeStructure(file_path)
    
    try:
        tree = ast.parse(content, filename=file_path)
        visitor = NodeVisitor(structure)
        visitor.visit(tree)
    except (SyntaxError, ValueError):
        # If AST parsing fails, fall back to regex patterns
        structure = analyze_file_with_regex(file_path, content)
    
    return structure


def analyze_file_with_regex(file_path: str, content: str) -> CodeStructure:
    """Analyze file using regex patterns (for non-Python files)."""
    structure = CodeStructure(file_path)
    ext = os.path.splitext(file_path)[1]
    
    if ext not in CLASS_PATTERNS and ext not in FUNCTION_PATTERNS:
        return structure
    
    lines = content.split('\n')
    current_class = None
    class_stack = []
    brace_count = 0
    in_class = False
    
    for line_num, line in enumerate(lines, 1):
        stripped = line.strip()
        
        # Extract classes
        if ext in CLASS_PATTERNS:
            class_match = re.search(CLASS_PATTERNS[ext], line)
            if class_match:
                class_name = class_match.group(1)
                # Extract inheritance
                inheritance = []
                if '(' in line and ')' in line:
                    paren_content = re.search(r'\(([^)]+)\)', line)
                    if paren_content:
                        inheritance = [x.strip() for x in paren_content.group(1).split(',')]
                
                structure.classes.append({
                    'name': class_name,
                    'line': line_num,
                    'methods': [],
                    'members': [],
                    'inheritance': inheritance,
                    'loc': 0
                })
                current_class = len(structure.classes) - 1
                in_class = True
                brace_count = line.count('{') - line.count('}')
        
        # Extract functions
        if ext in FUNCTION_PATTERNS:
            func_match = re.search(FUNCTION_PATTERNS[ext], line)
            if func_match:
                func_name = func_match.group(1) if func_match.group(1) else (
                    func_match.group(2) if len(func_match.groups()) > 1 and func_match.group(2) else func_match.group(0).split()[0]
                )
                
                func_info = {
                    'name': func_name,
                    'line': line_num,
                    'parameters': [],
                    'async': 'async' in line
                }
                
                # Try to extract parameters
                param_match = re.search(r'\(([^)]*)\)', line)
                if param_match:
                    params_str = param_match.group(1)
                    params = [p.strip().split()[0] if p.strip() else '' for p in params_str.split(',') if p.strip()]
                    func_info['parameters'] = params
                
                if in_class and current_class is not None:
                    structure.classes[current_class]['methods'].append(func_name)
                else:
                    structure.functions.append(func_info)
        
        # Extract loops
        if ext in LOOP_PATTERNS:
            for pattern in LOOP_PATTERNS[ext]:
                if re.search(pattern, line):
                    loop_type = 'for' if 'for' in pattern.lower() else 'while'
                    if 'async' in pattern.lower():
                        loop_type = 'async_for'
                    structure.loops.append({
                        'type': loop_type,
                        'line': line_num
                    })
                    break
        
        # Extract variables
        if ext in VARIABLE_PATTERNS:
            for pattern in VARIABLE_PATTERNS[ext]:
                var_match = re.search(pattern, line)
                if var_match:
                    var_name = var_match.group(1)
                    if var_name and var_name not in ['if', 'for', 'while', 'class', 'def', 'function']:
                        var_info = {
                            'name': var_name,
                            'line': line_num
                        }
                        
                        if in_class and current_class is not None:
                            if var_name not in structure.classes[current_class]['members']:
                                structure.classes[current_class]['members'].append(var_name)
                        else:
                            # Avoid duplicates
                            if not any(v['name'] == var_name and abs(v['line'] - line_num) < 5 for v in structure.variables):
                                structure.variables.append(var_info)
                        break
        
        # Track class scope with braces
        if in_class:
            brace_count += line.count('{') - line.count('}')
            if brace_count <= 0:
                in_class = False
                current_class = None
    
    return structure


def track_class_usage(blueprint_data: Dict[str, CodeStructure], repo_path: str) -> Dict[str, CodeStructure]:
    """Track where classes are used/referenced across the codebase."""
    # Build class name to file mapping
    class_to_files: Dict[str, List[str]] = defaultdict(list)
    for file_path_rel, structure in blueprint_data.items():
        for cls in structure.classes:
            class_to_files[cls['name']].append(file_path_rel)
    
    # Find class usage in imports and references
    for file_path_rel, structure in blueprint_data.items():
        file_path_abs = os.path.join(repo_path, file_path_rel)
        content = ""
        try:
            with open(file_path_abs, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except:
            continue
        
        # Check imports and class references
        for class_name, defining_files in class_to_files.items():
            # Skip if this file defines the class
            if file_path_rel in defining_files:
                continue
            
            # Check for imports or references to the class
            patterns = [
                rf'import.*{re.escape(class_name)}',
                rf'from.*import.*{re.escape(class_name)}',
                rf'\b{re.escape(class_name)}\s*\(',
                rf'\b{re.escape(class_name)}\s*[=:]',
                rf'new\s+{re.escape(class_name)}',
                rf'extends\s+{re.escape(class_name)}',
                rf':\s*{re.escape(class_name)}',
            ]
            
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    structure.class_usage[class_name].extend(defining_files)
                    break
    
    return blueprint_data


def analyze_codebase_blueprint(repo_path: str, all_file_data: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze codebase structure and create a blueprint.
    Returns a dictionary with structural information.
    """
    blueprint_data: Dict[str, CodeStructure] = {}
    
    print("📐 Analyzing codebase structure...")
    
    for file_path_rel, file_data in all_file_data.items():
        if not isinstance(file_data, dict) or file_data.get('loc', 0) == 0:
            continue
        
        file_path_abs = os.path.join(repo_path, file_path_rel)
        if not os.path.exists(file_path_abs):
            continue
        
        ext = os.path.splitext(file_path_rel)[1]
        if ext not in CLASS_PATTERNS and ext not in FUNCTION_PATTERNS:
            continue
        
        try:
            with open(file_path_abs, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
        
        # Use AST for Python, regex for others
        if ext == '.py':
            structure = analyze_python_file(file_path_abs, content)
        else:
            structure = analyze_file_with_regex(file_path_abs, content)
        
        blueprint_data[file_path_rel] = structure
    
    # Track class usage across files
    blueprint_data = track_class_usage(blueprint_data, repo_path)
    
    # Convert to serializable format
    result = {
        '_blueprint': {}
    }
    
    for file_path, structure in blueprint_data.items():
        result['_blueprint'][file_path] = {
            'classes': structure.classes,
            'functions': structure.functions,
            'variables': structure.variables,
            'loops': structure.loops,
            'imports': structure.imports,
            'class_usage': dict(structure.class_usage),
            'function_variable_usage': {k: v for k, v in structure.function_variable_usage.items()}
        }
    
    # Generate summary statistics
    total_classes = sum(len(s.classes) for s in blueprint_data.values())
    total_functions = sum(len(s.functions) for s in blueprint_data.values())
    total_variables = sum(len(s.variables) for s in blueprint_data.values())
    total_loops = sum(len(s.loops) for s in blueprint_data.values())
    
    # Find most reused classes
    class_reuse_count: Dict[str, int] = defaultdict(int)
    for structure in blueprint_data.values():
        for class_name, using_files in structure.class_usage.items():
            class_reuse_count[class_name] += len(using_files)
    
    result['_blueprint_stats'] = {
        'total_classes': total_classes,
        'total_functions': total_functions,
        'total_variables': total_variables,
        'total_loops': total_loops,
        'total_files_analyzed': len(blueprint_data),
        'most_reused_classes': sorted(class_reuse_count.items(), key=lambda x: x[1], reverse=True)[:10]
    }
    
    return result

