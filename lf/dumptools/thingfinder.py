import ast
import inspect
import linecache
from math import inf
import sys
from warnings import warn


class _ThingFinder(ast.NodeVisitor):
    """Class for finding python "things" in a given source code given a variable name.

    :param source: The source in which the thing is searched.
    :param var_name: The name of the variable that's searched for.
    :param max_n: Stop searching after this number of statements from the bottom
        of the module.
    """

    def __init__(self, source, var_name, max_n=inf):
        self.source = source
        self.var_name = var_name
        self.statement_n = 0
        self.max_n = max_n
        self._result = None

    def found_something(self):
        return self._result is not None

    def visit_Module(self, node):
        for i, statement in enumerate(node.body[::-1]):
            if i > self.max_n:
                return
            self.visit(statement)
            if self.found_something():
                self.statement_n = i
                return

    def visit_ClassDef(self, node):
        # don't search definitions
        pass

    def visit_FunctionDef(self, node):
        # don't search definitions
        pass

    def deparse(self):
        return ast.get_source_segment(self.source, self._result)

    def node(self):
        #TODO: correctly inherit (is not always _result)
        return self._result


class _NameFinder(_ThingFinder):
    pass


class _FunctionDefFinder(_NameFinder):
    def visit_FunctionDef(self, node):
        if node.name == self.var_name:
            self._result = node

    def deparse(self):
        res = ''
        for decorator in self._result.decorator_list:
            res += f'@{ast.get_source_segment(self.source, decorator)}\n'
        res += ast.get_source_segment(self.source, self._result)
        return self._fix_indent(res)

    @staticmethod
    def _fix_indent(source):
        lines = source.split('\n')
        res = []
        n_indent = None
        for line in lines:
            if not line.startswith(' '):
                res.append(line)
            else:
                if n_indent is None:
                    n_indent = len(line) - len(line.lstrip(' '))
                res.append(' ' * 4 + line[n_indent:])
        return '\n'.join(res)



class _ClassDefFinder(_NameFinder):
    def visit_ClassDef(self, node):
        if node.name == self.var_name:
            self._result = node

    def deparse(self):
        res = ''
        for decorator in self._result.decorator_list:
            res += f'@{ast.get_source_segment(self.source, decorator)}\n'
        res += ast.get_source_segment(self.source, self._result)
        return res


class _ImportFinder(_NameFinder):
    def visit_Import(self, node):
        for name in node.names:
            if name.asname == self.var_name:
                self._result = name
                return
            if name.asname is None and name.name == self.var_name:
                self._result = name
                return

    def deparse(self):
        name = self._result
        res = f'import {name.name}'
        if name.asname is not None:
            res += f' as {name.asname}'
        return res

    def node(self):
        # TODO: cache deparse?
        return ast.parse(self.deparse()).body[0]


class _ImportFromFinder(_NameFinder):
    def visit_ImportFrom(self, node):
        for name in node.names:
            if name.asname == self.var_name:
                self._result = (node.module, name)
                return
            if name.asname is None and name.name == self.var_name:
                self._result = (node.module, name)
                return

    def deparse(self):
        module, name = self._result
        res = f'from {module} import {name.name}'
        if name.asname is not None:
            res += f' as {name.asname}'
        return res

    def node(self):
        # TODO: cache deparse?
        return ast.parse(self.deparse()).body[0]


class _AssignFinder(_NameFinder):
    def visit_Assign(self, node):
        for target in node.targets:
            if self._parse_target(target):
                self._result = node
                return

    def _parse_target(self, target):
        if isinstance(target, ast.Name) and target.id == self.var_name:
            return True
        elif isinstance(target, ast.Tuple):
            for sub_target in target.elts:
                if self._parse_target(sub_target):
                    return True
        return False

    def deparse(self):
        try:
            source = self._result._source
        except AttributeError:
            source = self.source
        return f'{self.var_name} = {ast.get_source_segment(source, self._result.value)}'


class _CallFinder(_ThingFinder):
    def visit_Call(self, node):
        if node.func.id == self.var_name:
            self._result = node

    def find(self):
        tree = ast.parse(self.source)
        self.visit(tree)
        if self.found_something():
            return self._get_name(self._result), *_get_call_signature(self.source)
        raise ThingNotFound(f'Did not find call of "{self.var_name}".')

    def _get_name(self, call: ast.Call):
        return ast.get_source_segment(self.source, call.func)


def _get_call_assignments(args, source, values, keywords):
    argnames = [x.arg for x in args.args]
    pos_only_argnames = [x.arg for x in args.posonlyargs]
    all_argnames = pos_only_argnames + argnames
    defaults = {
        name: ast.get_source_segment(source, val)
        for name, val in zip(argnames[::-1], args.defaults[::-1])
    }
    kwonly_defaults = {
        ast.get_source_segment(source, name): ast.get_source_segment(source, val)
        for name, val in zip(args.kwonlyargs, args.kw_defaults)
        if val is not None
    }
    res = {}
    for name, val in kwonly_defaults.items():
        try:
            res[name] = keywords[name]
        except KeyError:
            res[name] = val

    for name, val in zip(all_argnames, values):
        res[name] = val

    if args.vararg is not None:
        res[args.vararg.arg] = '[' + ', '.join(values[len(all_argnames):]) + ']'

    kwargs = {}
    for name, val in keywords.items():
        if name in res:
            continue
        if name in argnames:
            res[name] = val
        else:
            print(name)
            kwargs[name] = val

    if kwargs and not set(kwargs) == {None}:
        assert args.kwarg is not None, 'Keyword args given, but no **kwarg present.'
        res[args.kwarg.arg] = '{' + ', '.join(f"'{k}': {v}" for k, v in kwargs.items()) + '}'

    for name, val in defaults.items():
        if name not in res:
            res[name] = val

    return res


def _get_call_signature(source: str):
    """Get the call signature of a string containing a call.

    :param source: String containing a call (e.g. "a(2, b, c=100)")
    :returns: A tuple with a list of positional arguments and a list of keyword arguments.
    """
    call = ast.parse(source).body[0].value
    if not isinstance(call, ast.Call):
        return [], {}
    args = [ast.get_source_segment(source, arg) for arg in call.args]
    kwargs = {
        kw.arg: ast.get_source_segment(source, kw.value) for kw in call.keywords
    }
    return args, kwargs


class Scope:
    def __init__(self, module, def_source, scopelist):
        self.module = module
        self.def_source = def_source
        self.scopelist = scopelist

    @classmethod
    def toplevel(cls, module):
        """Create a top-level scope (i.e. module level, no nesting). """
        return cls(module, '', [])

    @classmethod
    def empty(cls):
        return cls(None, '', [])

    @classmethod
    def from_source(cls, def_source, lineno, call_source, module=None, drop_n=0, calling_scope=None):
        tree = ast.parse(def_source)
        branch = _find_branch(tree, lineno)
        function_defs = [x for x in branch if isinstance(x, ast.FunctionDef)]
        if drop_n > 0:
            function_defs = function_defs[:-drop_n]

        # get call assignments for inner function
        # def f(a, b, c=3):
        #    ...
        # and
        # -> f(1, 2)
        # makes
        # a = 1
        # b = 2
        # c = 3
        # ...
        values, keywords = _get_call_signature(call_source)
        args = function_defs[-1].args
        assignments = _get_call_assignments(args, def_source, values, keywords)
        call_assignments = []
        for k, v in assignments.items():
            src = f'{k} = {v}'
            assignment = ast.parse(src).body[0]
            assignment._source = src
            assignment._scope = calling_scope
            call_assignments.append(assignment)

        scopelist = []
        for fdef in function_defs[::-1]:
            module_node = ast.Module()
            module_node.body = []
            module_node.body = fdef.body
            scopelist.append((fdef.name, module_node))

        # add call assignments to inner scope
        scopelist[0][1].body = call_assignments + scopelist[0][1].body

        return cls(module, def_source, scopelist)

    def from_level(self, i):
        return type(self)(self.module, self.def_source, self.scopelist[i:])

    def up(self):
        return type(self)(self.module, self.def_source, self.scopelist[1:])

    def global_(self):
        return type(self)(self.module, self.def_source, [])

    def unscoped(self, varname):
        if not self.scopelist:
            return varname
        return f'{"_".join(x[0] for x in self.scopelist)}_{varname}'

    def __repr__(self):
        return f'Scope[{".".join(x[0] for x in self.scopelist)}]'

    def __len__(self):
        return len(self.scopelist)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))


def find_in_function_def(var_name, source, lineno, call_source):
    """Find where *var_name* was assigned.

    :param var_name: Name of the variable to look for.
    :param source: Source string.
    :param lineno: Line number in the function to search in (this is being used to determine in
        which function scope to search).
    :param call_source: Source of the function call (e.g. `"f(123, b=1)"`). This is being used to
        determine argument values.
    """
    scope = Scope.from_source(source, lineno, call_source)
    return find_in_scope(var_name, scope)


def find_in_scope(var_name, scope):
    for _scopename, tree in scope.scopelist:
        try:
            source, node = find_in_source(var_name, scope.def_source, tree=tree)
            try:
                scope = node._scope
            except AttributeError:
                pass
            return (source, node), scope
        except ThingNotFound:
            scope = scope.up()
            continue
    if scope.module is None:
        raise ThingNotFound(f'{var_name} not found in function hierarchy.')
    return find(var_name, scope.module), scope.global_()


def find_in_source(var_name: str, source: str, tree=None):
    if tree is None:
        tree = ast.parse(source)
    min_n = inf
    best = None
    finder_clss = _NameFinder.__subclasses__()
    for finder_cls in finder_clss:
        finder = finder_cls(source, var_name, max_n=min_n - 1)
        finder.visit(tree)
        if finder.found_something() and finder.statement_n < min_n:
            best = finder
            min_n = finder.statement_n
    if best is None:
        raise ThingNotFound(f'{var_name} not found.')
    return best.deparse(), best.node()


def find_in_module(var_name: str, module):
    """Find the piece of code in the module *module* that assigned a value to the
    variable with name *var_name*.

    :param var_name: Name of the variable to look for.
    :param module: Module to search.
    :returns: Tuple with source code segment and corresponding ast node.
    """
    source = inspect.getsource(module)
    return find_in_source(var_name, source)


def _find_branch(node, lineno):
    try:
        start, end = node.lineno, node.end_lineno
        if not start <= lineno <= end:
            return False
    except AttributeError:
        start = end = '?'

    child_nodes = list(ast.iter_child_nodes(node))
    if not child_nodes and start != '?':
        return [node]

    for child_node in child_nodes:
        res = _find_branch(child_node, lineno)
        if res:
            return [node] + res

    if start == '?':
        return False

    return [node]


def _count_leading_whitespace(line: str):
    i = 0
    for char in line:
        if char == ' ':
            i += 1
            continue
        return i


def _ipython_history():
    """Get the list of commands executed by IPython, ordered from oldest to newest. """
    return [
        ''.join(lines)
        for k, (_, _, lines, _)
        in linecache.cache.items()
        if k.startswith('<ipython-')
        or 'ipykernel' in k
    ]


def find_in_ipython(var_name: str):
    source = node = None
    for cell in _ipython_history()[::-1]:
        try:
            source, node = find_in_source(var_name, cell)
        except (ThingNotFound, SyntaxError):
            continue
        break
    if source is None:
        raise ThingNotFound(f'"{var_name}" not found.')
    return source, node


def find(var_name: str, module=None):
    """Find the piece of code in the module *module* that assigned a value to the
    variable with name *var_name*. If *module* is not specified, this uses `__main__`.

    :param var_name: Name of the variable to look for.
    :param module: Module to search.
    :returns: Tuple with source code segment and corresponding ast node.
    """
    if module is None:
        module = sys.modules['__main__']
    try:
        return find_in_module(var_name, module)
    except TypeError:
        return find_in_ipython(var_name)


class ThingNotFound(Exception):
    pass
