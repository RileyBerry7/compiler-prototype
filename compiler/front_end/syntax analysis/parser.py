# /compiler/front-end/syntax analysis/parser.py

from grammar import CFG

#############################################################################################################
def generate_table(cfg: CFG):
    table = {}

    return table

#############################################################################################################

class parser:
    """
    A Bottom-Up: Shift-Reduce Parser which operates on a parse table, which it generates from
    a provided CFG. The parsing logic emulates a push-down automaton allowing it to interpret
    a Context-Free Grammar.
    """

    def __init__(self, context_free_grammar: CFG
        self.stack = []
        self.parse_table = generate_table()




