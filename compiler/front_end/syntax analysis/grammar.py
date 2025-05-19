# /compiler/front-end/syntax-analysis/grammar.py

class CFG:
    """
    Representative class of a Context-Free Grammar.
    """
    def __init__(self, v, t, p, s='S'):
        # A finite set of non-terminal symbols (variables)
        self.non_terminals = v
        # A finite set of terminal symbols
        self.terminals = t
        # A finite set of production rules. Each rule is of the form A → γ,
        self.production_rules = p
        # The start symbol, which is a non-terminal symbol in V.
        self.start_state = s

        self.follow_sets = []
        self.first_sets  = []