from Tokens import *
from Errors import RTError
from Lexer import *
from Nodes import *
from Parser import *
import os
from math import isnan, sqrt
from copy import deepcopy

#Context
class Context(object):
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

    def copy(self):
        new_context = Context(self.display_name, self.parent, self.parent_entry_pos)
        new_context.symbol_table = self.symbol_table.copy()
        return new_context

    def __repr__(self):
        return f"<{self.display_name}>"

#Symbol Table
class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.consts = []
        self.certains = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def get_certainity(self, name):
        certainity = self.certains.get(name, None)
        if certainity is None and self.parent:
            return self.parent.get(name)
        return certainity

    def set(self, name, value, certain, index=None):
        if name in self.consts:
            return None, RTError
        if index == None:
            self.symbols[name] = value
            self.certains[name] = certain
        else:
            key = self.get(name)
            if isinstance(key, List):
                if index.value < len(key.elements):
                    if isinstance(value, List):
                        key.elements[int(index.value)] = List(value.elements[:])
                    else:
                        key.elements[int(index.value)] = value
                    return key, None
                else:
                    return None, None
        return self.symbols.get(name, None), None

    def const_set(self, name, value, certain, index=None):
        got = self.get(name)
        if name in self.consts:
            return None, RTError
        self.symbols[name] = value
        self.certains[name] = certain
        self.consts.append(name)
        return value, None

    def remove(self, name):
        del self.symbols[name]

    def copy(self):
        new_table = SymbolTable(self.parent)
        new_table.symbols = self.symbols
        return new_table

    def __repr__(self):
        return f"{str(self.symbols)} -> {self.parent}"

#Interpreter
class Compiler:
    def visit(self, node, context, certain):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context, certain)

    def no_visit_method(self, node, context, certain):
        raise Exception (f"visit_{type(node).__name__} method is undefined")

    def visit_NumberNode(self, node, context, certain):
        return RTResult().success(f"new BasicNumber({node.tok.value})")

    def visit_StringNode(self, node, context, certain):
        return RTResult().success(f"new BasicString(\"{node.tok.value}\")")

    def visit_ListNode(self, node, context, certain):
        res = RTResult()
        elements = []
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context, certain)))
            if res.should_return(): return res
        return res.success(f"new BasicArray([{', '.join(elements)}])")

    def visit_StatementsNode(self, node, context, certain):
        res = RTResult()
        elements = []
        for element_node in node.statement_nodes:
            elements.append(res.register(self.visit(element_node, context, certain)))
            if res.should_return(): return res
        elements[-1] += ";"
        return res.success(';\n'.join(elements))

    def visit_VarAccessNode(self, node, context, certain):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                context,
                f"'{var_name}' defined nahi hai",
            ))
        return res.success(f"{node.var_name_tok.value}.copy()")

    def visit_VarAssignNode(self, node, context, certain):
        res = RTResult()
        var_name = node.var_name_tok.value
        var_type = node.var_type.value
        index = node.index_node
        error = None
        if index:
            index = res.register(self.visit(index, context, certain))
            if res.should_return(): return res
        value = res.register(self.visit(node.value_node, context, certain))
        if res.should_return(): return res
        certainity = certain
        if var_name in context.symbol_table.symbols:
            certainity = context.symbol_table.get_certainity(var_name)
            if certainity:
                declaration = False
            else:
                declaration = True
        else:
            declaration = True

        if var_type == "ABSE":
            _, error = context.symbol_table.const_set(var_name, value, certainity)
        else:
            _, error = context.symbol_table.set(var_name, value, certainity, index)
        if error == RTError:
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                context,
                f"Mustakil value change nahi kar sakte"
            ))

        if (value == None) or (error):
            return res.failure(RTError(
                node.pos_start, node.pos_end,
                context,
                f"'{var_name}' list form mein defined nahi hai"
            ))
        result = f"{('const ' if var_type == 'ABSE' else 'var ') if declaration else ''}{var_name}{f'.value[{index}.value]' if index else ''} = {value}"
        return res.success(result)

    def visit_BinOpNode(self, node, context, certain):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context, certain))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context, certain))
        if res.should_return(): return res
        if node.op_tok.type == TT_PLUS:
            result = f"({left}.added_to({right}))"
        elif node.op_tok.type == TT_MINUS:
            result = f"({left}.subbed_by({right}))"
        elif node.op_tok.type == TT_MUL:
            result = f"({left}.multed_by({right}))"
        elif node.op_tok.type == TT_DIV:
            result = f"({left}.dived_by({right}))"
        elif node.op_tok.type == TT_POW:
            result = f"({left}.powed_by({right}))"
        elif node.op_tok.type == TT_MOD:
            result = f"({left}.moded_by({right}))"
        elif node.op_tok.type == TT_EE:
            result = f"({left}.get_comparison_eq({right}))"
        elif node.op_tok.type == TT_NE:
            result = f"({left}.get_comparison_ne({right}))"
        elif node.op_tok.type == TT_LT:
            result = f"({left}.get_comparison_lt({right}))"
        elif node.op_tok.type == TT_GT:
            result = f"({left}.get_comparison_ge({right}))"
        elif node.op_tok.type == TT_LTE:
            result = f"({left}.get_comparison_lte({right}))"
        elif node.op_tok.type == TT_GTE:
            result = f"({left}.get_comparison_gte({right}))"
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result = f"({left}.anded_by({right}))"
        elif node.op_tok.matches(TT_KEYWORD, 'YA'):
            result = f"({left}.ored_by({right}))"
        return res.success(result)

    def visit_IfNode(self, node, context, certain):
        res = RTResult()
        resultstatement = ""
        times = 0
        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context, certain))
            if res.should_return(): return res
            expr_value = res.register(self.visit(expr, context, False))
            if res.should_return(): return res
            if should_return_null:
                resultstatement += ((f"if (({condition_value}).is_true()) ") if times == 0 else (f"else if (({condition_value}).is_true()) ")) + "{" + f"{indentator(expr_value)}" "\n} "
            else:
                resultstatement += f"({condition_value}).is_true() ? " + f" {expr_value} : "
            times += 1
        if node.else_case:
            else_case, should_return_null = node.else_case
            else_value = res.register(self.visit(else_case, context, False))
            if res.should_return(): return res
            else_value = indentator(else_value) if should_return_null else else_value
            if should_return_null:
                resultstatement += "else { " + else_value + "\n}"
            else:
                resultstatement += f"{else_value}"
        elif resultstatement.endswith(": "):
            resultstatement += "new NullObject()"
        return res.success(resultstatement)

    def visit_ForNode(self, node, context, certain):
        res = RTResult()
        elements = []
        start_value = res.register(self.visit(node.start_value_node, context, certain))
        if res.should_return(): return res
        variablenode = VarAssignNode(node.var_name_tok, Token(TT_KEYWORD, "RAKHO"), node.start_value_node, None)
        initialization = res.register(self.visit(variablenode, context, certain))
        if res.should_return(): return res
        end_value = res.register(self.visit(node.end_value_node, context, certain))
        if res.should_return(): return res
        if node.step_value_node:
            rhs = BinOpNode(VarAccessNode(node.var_name_tok), Token(TT_PLUS), node.step_value_node)
            variablenode = VarAssignNode(node.var_name_tok, Token(TT_KEYWORD, "RAKHO"), rhs, None)
            increment = res.register(self.visit(variablenode, context, certain))
            if res.should_return(): return res
        else:
            rhs = BinOpNode(VarAccessNode(node.var_name_tok), Token(TT_PLUS), NumberNode(Token(TT_INT, 1, node.pos_start, node.pos_end)))
            variablenode = VarAssignNode(node.var_name_tok, Token(TT_KEYWORD, "RAKHO"), rhs, None)
            increment = res.register(self.visit(variablenode, context, certain))
            if res.should_return(): return res
        body = res.register(self.visit(node.body_node, context, False))
        if res.should_return(): return res
        if node.should_return_null:
            resultstatement = f"for ({initialization}; (forcond({start_value}, {end_value}, ({node.var_name_tok.value}).copy())).is_true(); {increment})" + "{" + indentator(body) + "\n}"
        else:
            assignments = f"let elements09017 = [];\n"
            loop = f"for ({initialization}; (forcond({start_value}, {end_value}, ({node.var_name_tok.value}).copy())).is_true(); {increment})" + "{" + indentator(f"elements09017.push({body})") + "\n}"
            resultstatement = "function () " + "{\n" + indentator(assignments + loop + f"\nreturn new BasicArray(elements09017);\n") + "\n}" + "()"
        return res.success(resultstatement)

    def visit_WhileNode(self, node, context, certain):
        res = RTResult()
        elements = []
        condition = res.register(self.visit(node.condition_node, context, certain))
        if res.should_return(): return res
        value = res.register(self.visit(node.body_node, context, False))
        if res.should_return(): return res
        if node.should_return_null:
            resultstatement = f"while (({condition}).is_true()) " + "{" + f"{indentator(value)}" + "\n}"
        else:
            assignments = "let elements09017 = [];\n"
            loop = f"while (({condition}).is_true()) " + "{\n" + indentator(f"{f'elements09017.push({value})'}") + "\n};"
            resultstatement = "function () " + "{" + indentator(assignments + loop + f"\nreturn new BasicArray(elements09017);\n") +"\n}"+"()"
        return res.success(resultstatement)
        return res.success(null if node.should_return_null else List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context, certain):
        res = RTResult()
        number = res.register(self.visit(node.node, context, certain))
        if res.should_return(): return res
        if node.op_tok.type == TT_MINUS:
            number = f"({number}.multed_by(new BasicNumber(-1)))"
        elif node.op_tok.matches(TT_KEYWORD, 'NAHI'):
            number = f"{number}.notted()"
        return res.success(number)

    def visit_TryNode(self, node, context, certain):
        res = RTResult()
        try_block = res.register(self.visit(node.try_block, context, False))
        if res.should_return(): return res
        except_block = res.register(self.visit(node.except_block, context, False))
        if res.should_return(): return res
        result = f"try" + "{ " + indentator(f"{'return ' if node.may_return else ''}{try_block}") + "}\n catch {" + indentator(f"{'return ' if node.may_return else ''}{except_block}") + "}"
        if node.may_return:
            result = "function () " + "{" + indentator(result) + "\n}()"
        return res.success(result)

    def visit_FuncDefNode(self, node, context, certain):
        res = RTResult()
        func_name = node.var_name_tok.value if node.var_name_tok else None
        new_context = Context(str(id(node)), context.copy(), node.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        for arg in arg_names:
            new_context.symbol_table.set(arg, "new BasicNumber(3)", certain)
        arg_names_string = f"{', '.join(arg_names)}"
        if func_name:
            context.symbol_table.set(func_name, func_name, certain)
        func_body = res.register(self.visit(node.body_node, new_context, certain))
        if res.should_return(): return res
        if node.should_auto_return:
            function = f"function {func_name if func_name else ''}({arg_names_string}) " + "{" + indentator("return " + func_body) + "\n}"
        else:
            function = f"function {func_name if func_name else ''}({arg_names_string}) " + "{" + indentator(func_body) + "\n}"
        return res.success(function)

    def visit_CallNode(self, node, context, certain):
        res = RTResult()
        args = []
        value_to_call = res.register(self.visit(node.node_to_call, context, certain))
        if res.should_return(): return res
        if isinstance(value_to_call, VarAccessNode):
            value_to_call = res.register(self.visit(node.node_to_call, context, certain))
            if res.should_return(): return res
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context, certain)))
            if res.should_return(): return res
        arg_string = f"{', '.join(args)}"
        funcall = f"({value_to_call})({arg_string})"
        return res.success(funcall)

    def visit_ReturnNode(self, node, context, certain):
        res = RTResult()
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context, certain))
            if res.should_return(): return res
        else:
            value = "new NullObject()"

        return res.success("return " + value)

    def visit_ContinueNode(self, node, context, certain):
        return RTResult().success("continue")

    def visit_BreakNode(self, node, context, certain):
        return RTResult().success("break")

    def visit_AssertNode(self, node, context, certain):
        res = RTResult()
        assertion = res.register(self.visit(node.node_to_assert, context, certain))
        if res.should_return(): return res
        result = f"if (({assertion}.notted()).is_true()) " + "{" + indentator("throw new RTError('Jo ap ne kaha wo sahi nahi hai')") + "\n}"
        return res.success(result)

def indentator(string):
    string = "\n" + string + "\n"
    indentlist = string.split("\n")
    index = 0
    while index < len(indentlist):
        indentlist[index] = "\t"+indentlist[index]
        index += 1
    return "\n".join(indentlist)

#run
context = Context('<main>')
global_symbol_table = SymbolTable()
context.symbol_table = global_symbol_table
null = nullObject()
galat = Boolean(0)
sahi = Boolean(1)
inf = Infinity()
global_symbol_table.const_set("khali", null, True)
global_symbol_table.const_set("galat", galat, True)
global_symbol_table.const_set("sahi", sahi, True)
global_symbol_table.const_set("lamehdood", inf, True)
global_symbol_table.set("LIKHO", "print", True)
global_symbol_table.set("LINE_LIKHO", "println", True)
global_symbol_table.set("LIKHO_WAPIS", "print_ret", True)
global_symbol_table.set("PUCHO", "input", True)
global_symbol_table.set("MANGO_INT", "input_int", True)
global_symbol_table.set("SAAF", "clear", True)
global_symbol_table.set("KYA_NUM", "is_number", True)
global_symbol_table.set("KYA_STR", "is_string", True)
global_symbol_table.set("KYA_LIST", "is_list", True)
global_symbol_table.set("KYA_KAM", "is_function", True)
global_symbol_table.set("DALO", "append", True)
global_symbol_table.set("NIKAL", "pop", True)
global_symbol_table.set("MILAO", "extend", True)
global_symbol_table.set("LIST", "list", True)
global_symbol_table.set("STR", "str", True)
global_symbol_table.set("NUM", "num", True)
global_symbol_table.set("ALAG", "split", True)
global_symbol_table.set("JODH", "join", True)
global_symbol_table.set("LAMBAI", "len", True)
global_symbol_table.set("CHALAO", "run", True)
global_symbol_table.set("STR_CHALAO", 'exec', True)
global_symbol_table.set("STR_WAPIS_CHALAO", 'eval', True)
global_symbol_table.set("MATH_SQRT", "math_sqrt", True)


def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error
    compiler = Compiler()
    result = compiler.visit(ast.node, context, True)
    return result.value, result.error
