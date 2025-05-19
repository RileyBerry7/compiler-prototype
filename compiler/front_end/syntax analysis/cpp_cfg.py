# cpp_cfg.py

import grammar
from compiler.front_end.lexical_analysis.tokens import TokenType

############################################################################

# All possible C++ tokens
terminals = set(TokenType)

# Starting Non-Terminal
start_state = 'S'

# All possible variables
non_terminals = {
    # start symbol
    "TranslationUnit",      # entire source file

    # top-level
    "DeclarationSeq",       # sequence of declarations/definitions
    "Declaration",          # e.g. int x;   or   void f() { … }

    # function parts
    "FunctionDefinition",   # return-type, name, params, body
    "ParameterList",        # ( type id, type id, … )

    # types
    "TypeSpecifier",        # int, float, MyClass, …

    # declarators
    "Declarator",           # pointer, array, identifier

    # statements
    "StatementSeq",         # { stmt stmt … }
    "Statement",            # expression-stmt | if-stmt | for-stmt | return-stmt | …

    "ExpressionStatement",  # expr ;
    "IfStatement",          # if (expr) stmt [ else stmt ]
    "ForStatement",         # for ( … ) stmt
    "ReturnStatement",      # return [expr] ;

    # expressions
    "Expression",           # the generic E
    "AssignmentExpr",       # E = E
    "ConditionalExpr",      # E ? E : E
    "LogicalOrExpr",        # E || E
    "LogicalAndExpr",       # E && E
    "EqualityExpr",         # E == E | E != E
    "RelationalExpr",       # E < E | E > E | …
    "AdditiveExpr",         # E + E | E - E
    "MultiplicativeExpr",   # E * E | E / E | E % E
    "UnaryExpr",            # +E | -E | !E | *E | &E
    "PrimaryExpr",          # identifier | literal | ( Expression )

    # literals & identifiers (could be tokens instead)
    "Identifier",           # variable or function names
    "Literal",              # integer, floating, string, char, bool

    # auxiliary
    "ArgumentList",         # in a function call: ( E, E, … )
    "PostfixExpr",          # E [ E ] | E ( ArgumentList? ) | E . id | E -> id
}

# Rules to yield all terminals
production_rules = {
"Expression": [["AssignmentExpr"]],

"AssignmentExpr": [
    ["LogicalOrExpr", TokenType.ASSIGN, "AssignmentExpr"],
    ["LogicalOrExpr"]
],

"LogicalOrExpr": [
    ["LogicalOrExpr", TokenType.LOGICAL_OR, "LogicalAndExpr"],
    ["LogicalAndExpr"]
],

"LogicalAndExpr": [
    ["LogicalAndExpr", TokenType.LOGICAL_AND, "EqualityExpr"],
    ["EqualityExpr"]
],

"EqualityExpr": [
    ["EqualityExpr", TokenType.EQ, "RelationalExpr"],
    ["EqualityExpr", TokenType.NEQ, "RelationalExpr"],
    ["RelationalExpr"]
],

"RelationalExpr": [
    ["RelationalExpr", TokenType.LT, "AdditiveExpr"],
    ["RelationalExpr", TokenType.GT, "AdditiveExpr"],
    ["RelationalExpr", TokenType.LTE, "AdditiveExpr"],
    ["RelationalExpr", TokenType.GTE, "AdditiveExpr"],
    ["AdditiveExpr"]
],

"AdditiveExpr": [
    ["AdditiveExpr", TokenType.PLUS, "MultiplicativeExpr"],
    ["AdditiveExpr", TokenType.MINUS, "MultiplicativeExpr"],
    ["MultiplicativeExpr"]
],

"MultiplicativeExpr": [
    ["MultiplicativeExpr", TokenType.STAR, "UnaryExpr"],
    ["MultiplicativeExpr", TokenType.SLASH, "UnaryExpr"],
    ["MultiplicativeExpr", TokenType.PERCENT, "UnaryExpr"],
    ["UnaryExpr"]
],

"UnaryExpr": [
    [TokenType.PLUS, "UnaryExpr"],
    [TokenType.MINUS, "UnaryExpr"],
    [TokenType.LOGICAL_NOT, "UnaryExpr"],
    [TokenType.BIT_NOT, "UnaryExpr"],
    ["PrimaryExpr"]
],

"PrimaryExpr": [
    ["Literal"],
    ["Identifier"],
    [TokenType.LPAREN, "Expression", TokenType.RPAREN]
]}


CPP_CFG = grammar.CFG(non_terminals,
                      terminals,
                      production_rules,
                      start_state)

