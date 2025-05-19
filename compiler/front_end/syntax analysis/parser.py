# /compiler/front-end/syntax analysis/parser.py

from grammar import CFG
from compiler.front_end.lexical_analysis.tokens import TokenType

#############################################################################################################
def generate_table(cfg: CFG):
    table = {}

    for head, productions in cfg.production_rules.items():
        for prod in productions:
            first = compute_first_of_sequence(cfg, prod)

            for terminal in first - {TokenType.EPSILON}:
                table[(head, terminal)] = prod

            if TokenType.EPSILON in first:
                for terminal in cfg.follow_sets[head]:
                    table[(head, terminal)] = prod

    return table


def compute_first_of_sequence(cfg: CFG, symbols: list):
    first = set()
    for symbol in symbols:
        if symbol in cfg.terminals:
            first.add(symbol)
            break
        elif symbol in cfg.non_terminals:
            first |= cfg.first_sets[symbol] - {TokenType.EPSILON}
            if TokenType.EPSILON not in cfg.first_sets[symbol]:
                break
        else:
            break
    else:
        first.add(TokenType.EPSILON)
    return first
e

#############################################################################################################

class Parser:
    """
    A Bottom-Up: Shift-Reduce Parser which operates on a parse table, which it generates from
    a provided CFG. The parsing logic emulates a push-down automaton allowing it to interpret
    a Context-Free Grammar.
    """

    def __init__(self, context_free_grammar: CFG
        self.stack = []
        self.parse_table = generate_table()

#############################################################################################################


