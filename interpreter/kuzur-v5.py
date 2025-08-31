#!/usr/bin/env python3
"""
Kuzur v1.3 — CLI-only interpreter
Features:
 - Variables, arithmetic, strings, booleans
 - if / elif / else
 - while, for, do-while
 - break, continue
 - functions with return
 - built-ins: print, input, len, int, str
 - Blocks with { ... } and single-line comments //...
 - CLI flags: --version / -V, --help / -h
"""

from dataclasses import dataclass
from typing import Any, List, Dict, Optional
import sys
import re
import traceback

# ---------------- Metadata ----------------
KUZUR_NAME = "Kuzur"
KUZUR_VERSION = "1.0.0"

# ------------------ Lexer ------------------

TOKENS = [
    ("NUMBER",  r"\d+(?:\.\d+)?"),
    ("STRING",  r'"([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\''),
    ("IDENT",   r"[A-Za-z_][A-Za-z0-9_]*"),
    ("OP",      r"==|!=|<=|>=|&&|\|\||[+\-*/%<>=!();,{}]|\(|\)|\{|\}|,"),
    ("NEWLINE", r"\n"),
    ("SKIP",    r"[ \t\r]+"),
    ("COMMENT", r"//.*"),
]

# Compile master pattern
master_pat = re.compile("|".join(f"(?P<{name}>{pat})" for name, pat in TOKENS))

KEYWORDS = {
    "if", "elif", "else", "while", "for", "do", "func", "return",
    "true", "false", "break", "continue"
}

@dataclass
class Token:
    type: str
    value: str
    pos: int

class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.tokens: List[Token] = []
        self.i = 0
        self._tokenize()
        self.tokens.append(Token("EOF", "", len(text)))

    def _tokenize(self):
        for m in master_pat.finditer(self.text):
            kind = m.lastgroup
            value = m.group()
            if kind in ("SKIP", "COMMENT"):
                continue
            if kind == "IDENT" and value in KEYWORDS:
                kind = value.upper()
            if kind == "STRING":
                value = self._unescape_string(value)
            self.tokens.append(Token(kind, value, m.start()))

    def _unescape_string(self, s: str) -> str:
        inner = s[1:-1]
        return bytes(inner, "utf-8").decode("unicode_escape")

    def peek(self) -> Token:
        return self.tokens[self.i]

    def next(self) -> Token:
        tok = self.tokens[self.i]
        self.i += 1
        return tok

    def match(self, *types: str) -> Optional[Token]:
        if self.peek().type in types:
            return self.next()
        return None

    def expect(self, t: str) -> Token:
        tok = self.next()
        if tok.type != t:
            raise SyntaxError(f"Expected {t} but got {tok.type} at {tok.pos}")
        return tok

# ------------------ AST Nodes ------------------

@dataclass
class Expr: pass

@dataclass
class Number(Expr):
    value: float

@dataclass
class String(Expr):
    value: str

@dataclass
class Boolean(Expr):
    value: bool

@dataclass
class Var(Expr):
    name: str

@dataclass
class Unary(Expr):
    op: str
    right: Expr

@dataclass
class Binary(Expr):
    left: Expr
    op: str
    right: Expr

@dataclass
class Call(Expr):
    callee: Expr
    args: List[Expr]

@dataclass
class Stmt: pass

@dataclass
class ExprStmt(Stmt):
    expr: Expr

@dataclass
class Assign(Stmt):
    name: str
    expr: Expr

@dataclass
class Block(Stmt):
    statements: List[Stmt]

@dataclass
class If(Stmt):
    branches: List[tuple]
    else_block: Optional[Block]

@dataclass
class While(Stmt):
    cond: Expr
    body: Block

@dataclass
class For(Stmt):
    var: str
    start: Expr
    end: Expr
    body: Block

@dataclass
class DoWhile(Stmt):
    body: Block
    cond: Expr

@dataclass
class FuncDef(Stmt):
    name: str
    params: List[str]
    body: Block

@dataclass
class Return(Stmt):
    expr: Optional[Expr]

@dataclass
class BreakStmt(Stmt): pass

@dataclass
class ContinueStmt(Stmt): pass

# ------------------ Parser ------------------

PRECEDENCE = {
    "||": 1, "&&": 2,
    "==": 3, "!=": 3, "<": 4, ">": 4, "<=": 4, ">=": 4,
    "+": 5, "-": 5,
    "*": 6, "/": 6, "%": 6,
}

class Parser:
    def __init__(self, lex: Lexer):
        self.l = lex

    def parse(self) -> Block:
        stmts: List[Stmt] = []
        while self.l.peek().type != "EOF":
            if self.l.match("NEWLINE"):
                continue
            stmts.append(self.statement())
        return Block(stmts)

    def statement(self) -> Stmt:
        tok = self.l.peek()
        if tok.type == "IF": return self.if_stmt()
        if tok.type == "WHILE": return self.while_stmt()
        if tok.type == "FOR": return self.for_stmt()
        if tok.type == "DO": return self.do_while_stmt()
        if tok.type == "FUNC": return self.func_def()
        if tok.type == "RETURN":
            self.l.next()
            expr = None if self.l.peek().type in ("NEWLINE", "}", "EOF") else self.expression()
            return Return(expr)
        if tok.type == "BREAK":
            self.l.next(); return BreakStmt()
        if tok.type == "CONTINUE":
            self.l.next(); return ContinueStmt()
        if tok.type == "IDENT" and self._is_assignment():
            name = self.l.next().value
            # next token should be OP with value '='
            eq = self.l.expect("OP")
            if eq.value != "=":
                raise SyntaxError(f"Expected '=' for assignment at {eq.pos}")
            return Assign(name, self.expression())
        return ExprStmt(self.expression())

    def _is_assignment(self) -> bool:
        idx = self.l.i
        ident = self.l.peek()
        if ident.type != "IDENT":
            return False
        self.l.next()
        nxt = self.l.peek()
        self.l.i = idx
        return nxt.type == "OP" and nxt.value == "="

    def block(self) -> Block:
        tok = self.l.next()
        if tok.type != "OP" or tok.value != "{":
            raise SyntaxError(f"Expected '{{' but got {tok.value}")
        stmts: List[Stmt] = []
        while not (self.l.peek().type == "OP" and self.l.peek().value == "}"):
            if self.l.match("NEWLINE"):
                continue
            stmts.append(self.statement())
            while self.l.match("NEWLINE"):
                pass
        self.l.expect("OP")  # consume '}'
        return Block(stmts)

    def if_stmt(self) -> If:
        branches: List[tuple] = []
        self.l.expect("IF")
        self.l.expect("OP")  # '('
        cond = self.expression()
        self.l.expect("OP")  # ')'
        blk = self.block()
        branches.append((cond, blk))
        while self.l.peek().type == "ELIF":
            self.l.next()
            self.l.expect("OP")
            c = self.expression()
            self.l.expect("OP")
            b = self.block()
            branches.append((c, b))
        else_block = None
        if self.l.peek().type == "ELSE":
            self.l.next()
            else_block = self.block()
        return If(branches, else_block)

    def while_stmt(self) -> While:
        self.l.expect("WHILE")
        self.l.expect("OP")  # '('
        cond = self.expression()
        self.l.expect("OP")  # ')'
        body = self.block()
        return While(cond, body)

    def for_stmt(self) -> For:
        self.l.expect("FOR")
        self.l.expect("OP")  # '('
        var = self.l.expect("IDENT").value
        self.l.expect("OP")  # '='
        start = self.expression()
        self.l.expect("OP")  # ';'
        end = self.expression()
        self.l.expect("OP")  # ')'
        body = self.block()
        return For(var, start, end, body)

    def do_while_stmt(self) -> DoWhile:
        self.l.expect("DO")
        body = self.block()
        self.l.expect("WHILE")
        self.l.expect("OP")  # '('
        cond = self.expression()
        self.l.expect("OP")  # ')'
        return DoWhile(body, cond)

    def func_def(self) -> FuncDef:
        self.l.expect("FUNC")
        name = self.l.expect("IDENT").value
        self.l.expect("OP")  # '('
        params: List[str] = []
        if not (self.l.peek().type == "OP" and self.l.peek().value == ")"):
            while True:
                params.append(self.l.expect("IDENT").value)
                if self.l.peek().type == "OP" and self.l.peek().value == ",":
                    self.l.next(); continue
                break
        self.l.expect("OP")  # ')'
        body = self.block()
        return FuncDef(name, params, body)

    def expression(self, prec=0) -> Expr:
        tok = self.l.next()
        if tok.type == "NUMBER":
            left: Expr = Number(float(tok.value))
        elif tok.type == "STRING":
            left = String(tok.value)
        elif tok.type == "TRUE":
            left = Boolean(True)
        elif tok.type == "FALSE":
            left = Boolean(False)
        elif tok.type == "IDENT":
            left = Var(tok.value)
        elif tok.type == "OP" and tok.value in ("+", "-", "!"):
            right = self.expression(7)
            left = Unary(tok.value, right)
        elif tok.type == "OP" and tok.value == "(":
            left = self.expression()
            self.l.expect("OP")  # ')'
        else:
            raise SyntaxError(f"Unexpected token {tok.type} at {tok.pos}")

        while True:
            nxt = self.l.peek()
            if nxt.type == "OP" and nxt.value == "(":
                self.l.next()
                args: List[Expr] = []
                if not (self.l.peek().type == "OP" and self.l.peek().value == ")"):
                    while True:
                        args.append(self.expression())
                        if self.l.peek().type == "OP" and self.l.peek().value == ",":
                            self.l.next(); continue
                        break
                self.l.expect("OP")  # ')'
                left = Call(left, args)
                continue
            if nxt.type == "OP" and nxt.value in PRECEDENCE:
                op_prec = PRECEDENCE[nxt.value]
                if op_prec <= prec:
                    break
                op = self.l.next().value
                right = self.expression(op_prec)
                left = Binary(left, op, right)
                continue
            break
        return left

# ------------------ Interpreter ------------------

class ReturnSignal(Exception):
    def __init__(self, value): self.value = value

class BreakSignal(Exception): pass
class ContinueSignal(Exception): pass

class Environment:
    def __init__(self, parent: Optional['Environment']=None):
        self.parent = parent
        self.values: Dict[str, Any] = {}

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise NameError(f"Undefined variable '{name}'")

    def set(self, name: str, value: Any):
        if name in self.values:
            self.values[name] = value
            return
        if self.parent and self._has_in_chain(name):
            self.parent.set(name, value)
            return
        self.values[name] = value

    def _has_in_chain(self, name: str) -> bool:
        env = self.parent
        while env:
            if name in env.values:
                return True
            env = env.parent
        return False

class Function:
    def __init__(self, name: str, params: List[str], body: Block, closure: Environment):
        self.name = name
        self.params = params
        self.body = body
        self.closure = closure

    def __call__(self, interpreter: 'Interpreter', args: List[Any]):
        if len(args) != len(self.params):
            raise TypeError(f"{self.name} expects {len(self.params)} args, got {len(args)}")
        local = Environment(self.closure)
        for p, a in zip(self.params, args):
            local.set(p, a)
        try:
            interpreter.exec_block(self.body, local)
        except ReturnSignal as r:
            return r.value
        return None

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self._install_builtins()

    def _install_builtins(self):
        self.globals.set("print", self._builtin_print)
        self.globals.set("input", self._builtin_input)
        self.globals.set("len", lambda interp, args: len(str(args[0])))
        self.globals.set("int", lambda interp, args: int(float(args[0])))
        self.globals.set("str", lambda interp, args: str(args[0]))

    def _builtin_print(self, interp, args):
        print(*args)
        return None

    def _builtin_input(self, interp, args):
        prompt = args[0] if args else ""
        return input(str(prompt))

    def _truthy(self, value):
        return bool(value)

    def eval_expr(self, env: Environment, e: Expr):
        if isinstance(e, Number):
            v = e.value
            return int(v) if float(v).is_integer() else v
        if isinstance(e, String):
            return e.value
        if isinstance(e, Boolean):
            return e.value
        if isinstance(e, Var):
            return env.get(e.name)
        if isinstance(e, Unary):
            r = self.eval_expr(env, e.right)
            if e.op == "+":
                return +r
            if e.op == "-":
                return -r
            if e.op == "!":
                return not self._truthy(r)
        if isinstance(e, Binary):
            l = self.eval_expr(env, e.left)
            r = self.eval_expr(env, e.right)
            if e.op == "+":
                # string concat if either is string
                if isinstance(l, str) or isinstance(r, str):
                    return str(l) + str(r)
                return l + r
            if e.op == "-":
                return l - r
            if e.op == "*":
                return l * r
            if e.op == "/":
                return l / r
            if e.op == "%":
                return l % r
            if e.op == "==":
                return l == r
            if e.op == "!=":
                return l != r
            if e.op == "<":
                return l < r
            if e.op == "<=":
                return l <= r
            if e.op == ">":
                return l > r
            if e.op == ">=":
                return l >= r
            if e.op == "&&":
                return self._truthy(l) and self._truthy(r)
            if e.op == "||":
                return self._truthy(l) or self._truthy(r)
        if isinstance(e, Call):
            fn = self.eval_expr(env, e.callee)
            if callable(fn):
                return fn(self, [self.eval_expr(env, a) for a in e.args])
            raise TypeError("Not callable")
        raise RuntimeError(f"Unknown expression {e}")

    def exec_stmt(self, env: Environment, s: Stmt):
        if isinstance(s, ExprStmt):
            self.eval_expr(env, s.expr)
        elif isinstance(s, Assign):
            val = self.eval_expr(env, s.expr)
            env.set(s.name, val)
        elif isinstance(s, Block):
            self.exec_block(s, Environment(env))
        elif isinstance(s, If):
            for cond, blk in s.branches:
                if self._truthy(self.eval_expr(env, cond)):
                    self.exec_block(blk, Environment(env))
                    return
            if s.else_block:
                self.exec_block(s.else_block, Environment(env))
        elif isinstance(s, While):
            while self._truthy(self.eval_expr(env, s.cond)):
                try:
                    self.exec_block(s.body, Environment(env))
                except BreakSignal:
                    break
                except ContinueSignal:
                    continue
        elif isinstance(s, For):
            start = self.eval_expr(env, s.start)
            end = self.eval_expr(env, s.end)
            env.set(s.var, start)
            while env.get(s.var) <= end:
                try:
                    self.exec_block(s.body, Environment(env))
                except BreakSignal:
                    break
                except ContinueSignal:
                    pass
                env.set(s.var, env.get(s.var) + 1)
        elif isinstance(s, DoWhile):
            while True:
                try:
                    self.exec_block(s.body, Environment(env))
                except BreakSignal:
                    break
                except ContinueSignal:
                    pass
                if not self._truthy(self.eval_expr(env, s.cond)):
                    break
        elif isinstance(s, FuncDef):
            env.set(s.name, Function(s.name, s.params, s.body, env))
        elif isinstance(s, Return):
            v = self.eval_expr(env, s.expr) if s.expr else None
            raise ReturnSignal(v)
        elif isinstance(s, BreakStmt):
            raise BreakSignal()
        elif isinstance(s, ContinueStmt):
            raise ContinueSignal()
        else:
            raise RuntimeError(f"Unknown statement type: {s}")

    def exec_block(self, block: Block, env: Environment):
        for stmt in block.statements:
            self.exec_stmt(env, stmt)

    def run(self, code: str, *, env: Optional[Environment] = None):
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        self.exec_block(ast, env or self.globals)

# ------------------ CLI ------------------

def print_usage(progname: str):
    print(f"Usage: kuzur  <program.kz>")
    print()
    print("Options:")
    print("  -V, --version     Print Kuzur version and exit")
    print("  -h, --help        Show this help message")
    print()
    print("Examples:")
    print(f"  kuzur myprogram.kz")
    print(f"  kuzur --version")

def main(argv: List[str]):
    if len(argv) >= 2:
        arg = argv[1]
        if arg in ("-V", "--version"):
            print(f"{KUZUR_NAME} {KUZUR_VERSION}")
            return 0
        if arg in ("-h", "--help"):
            print_usage(argv[0])
            return 0
        # run file
        if arg.endswith(".kz"):
            try:
                with open(arg, "r", encoding="utf-8") as f:
                    code = f.read()
                Interpreter().run(code)
                return 0
            except FileNotFoundError:
                print(f"File not found: {arg}", file=sys.stderr)
                return 2
            except Exception:
                traceback.print_exc()
                return 1
        else:
            print_usage(argv[0])
            return 2
    else:
        print_usage(argv[0])
        return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
