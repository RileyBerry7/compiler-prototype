# cpp_cfg.py

import grammar
from compiler.front_end.lexical_analysis.tokens import TokenType

############################################################################

# All possible C++ tokens
terminals = set(TokenType)

# Starting Non-Terminal
start_state = 'S'

# All possible variables
nnon_terminals = {
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
production_rules = {}


CPP_CFG = grammar.CFG(non_terminals,
                      terminals,
                      production_rules,
                      start_state)

