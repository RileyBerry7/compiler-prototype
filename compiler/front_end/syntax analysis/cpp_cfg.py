# cpp_cfg.py

import grammar
from compiler.front_end.lexical_analysis.tokens import TokenType

############################################################################

# All possible C++ tokens
terminals = set(TokenType)

# Starting Non-Terminal
start_state = 'S'

# All possible variables
non_terminals = set("S",
                    "BLOCK",
                    "EXPRESSION",
                    "OPERATOR",
                    "OPERAND",
                    "LINE",
                    "$")

# Rules to yield all terminals
production_rules = {}


CPP_CFG = grammar.CFG(non_terminals,
                      terminals,
                      production_rules,
                      start_state)

