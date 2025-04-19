# tokens.py
from enum import Enum, auto
from string import punctuation
from .file_writer import FileWriter

####################################################################################

class Token:
    def __init__(self, token_type: "TokenType", lexeme: str, line: int, column: int):
        self.type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

####################################################################################

class TokenStream:
    def __init__(self):
        self.__stream = []
        self.length = 0

    def add(self, token: Token):
        self.__stream.append(token)
        self.length += 1

    def display(self, out_file: str):
        output = FileWriter(out_file)
        line_buffer = []
        last_line = 1
        for token in self.__stream:
            if token.line == last_line:
                line_buffer.append(token.type.name)
            else:
                output.write_line(" ".join(line_buffer))
                line_buffer = [token.type.name]
                last_line = token.line
        if line_buffer:
            output.write_line(" ".join(line_buffer))

####################################################################################

class TokenType(Enum):
    # =========================
    # Literals & Indentation
    # =========================
    IDENTIFIER     = auto()
    INT_LITERAL    = auto()
    FLOAT_LITERAL  = auto()
    STRING_LITERAL = auto()
    CHAR_LITERAL   = auto()
    INDENT         = auto()
    DEDENT         = auto()
    END_OF_LINE    = auto()
    END_OF_FILE    = auto()
    UNKNOWN        = auto()
    COMMENT        = auto()

    # =========================
    # Keywords
    # =========================
    ALIGNAS        = auto()
    ALIGNOF        = auto()
    AND            = auto()
    AND_EQ         = auto()
    ASM            = auto()
    AUTO           = auto()
    BITAND         = auto()
    BITOR          = auto()
    BOOL           = auto()
    BREAK          = auto()
    CASE           = auto()
    CATCH          = auto()
    CHAR           = auto()
    CHAR8_T        = auto()
    CHAR16_T       = auto()
    CHAR32_T       = auto()
    CLASS          = auto()
    COMPL          = auto()
    CONCEPT        = auto()
    CONST          = auto()
    CONSTEVAL      = auto()
    CONSTEXPR      = auto()
    CONSTINIT      = auto()
    CONST_CAST     = auto()
    CONTINUE       = auto()
    CO_AWAIT       = auto()
    CO_RETURN      = auto()
    CO_YIELD       = auto()
    DECLTYPE       = auto()
    DEFAULT        = auto()
    DELETE         = auto()
    DO             = auto()
    DOUBLE         = auto()
    DYNAMIC_CAST   = auto()
    ELSE           = auto()
    ENUM           = auto()
    EXPLICIT       = auto()
    EXPORT         = auto()
    EXTERN         = auto()
    FALSE          = auto()
    FINAL          = auto()
    FLOAT          = auto()
    FOR            = auto()
    FRIEND         = auto()
    GOTO           = auto()
    IF             = auto()
    INLINE         = auto()
    INT            = auto()
    LONG           = auto()
    MUTABLE        = auto()
    NAMESPACE      = auto()
    NEW            = auto()
    NOEXCEPT       = auto()
    NOT            = auto()
    NOT_EQ         = auto()
    NULLPTR        = auto()
    OPERATOR       = auto()
    OR             = auto()
    OR_EQ          = auto()
    PRIVATE        = auto()
    PROTECTED      = auto()
    PUBLIC         = auto()
    REGISTER       = auto()
    REINTERPRET_CAST = auto()
    REQUIRES       = auto()
    RETURN         = auto()
    SHORT          = auto()
    SIGNED         = auto()
    SIZEOF         = auto()
    STATIC         = auto()
    STATIC_ASSERT  = auto()
    STATIC_CAST    = auto()
    STRUCT         = auto()
    SWITCH         = auto()
    TEMPLATE       = auto()
    THIS           = auto()
    THREAD_LOCAL   = auto()
    THROW          = auto()
    TRUE           = auto()
    TRY            = auto()
    TYPEDEF        = auto()
    TYPEID         = auto()
    TYPENAME       = auto()
    UNION          = auto()
    UNSIGNED       = auto()
    USING          = auto()
    VIRTUAL        = auto()
    VOID           = auto()
    VOLATILE       = auto()
    WCHAR_T        = auto()
    WHILE          = auto()
    XOR            = auto()
    XOR_EQ         = auto()

    # =========================
    # Operators & Punctuation
    # =========================
    PLUS           = auto()
    MINUS          = auto()
    STAR           = auto()
    SLASH          = auto()
    PERCENT        = auto()
    INCREMENT      = auto()
    DECREMENT      = auto()
    ASSIGN         = auto()
    PLUS_EQ        = auto()
    MINUS_EQ       = auto()
    STAR_EQ        = auto()
    SLASH_EQ       = auto()
    PERCENT_EQ     = auto()
    AND_EQ_OP      = auto()
    OR_EQ_OP       = auto()
    XOR_EQ_OP      = auto()
    SHL_EQ         = auto()
    SHR_EQ         = auto()
    EQ             = auto()
    NEQ            = auto()
    LT             = auto()
    GT             = auto()
    LTE            = auto()
    GTE            = auto()
    LOGICAL_AND    = auto()
    LOGICAL_OR     = auto()
    LOGICAL_NOT    = auto()
    BIT_AND        = auto()
    BIT_OR         = auto()
    BIT_XOR        = auto()
    BIT_NOT        = auto()
    SHL            = auto()
    SHR            = auto()
    CONDITIONAL    = auto()
    COLON          = auto()
    COMMA          = auto()
    DOT            = auto()
    ARROW          = auto()
    ARROW_STAR     = auto()
    DOT_STAR       = auto()
    SCOPE          = auto()
    NEW_ARRAY      = auto()
    DELETE_ARRAY   = auto()
    LBRACE         = auto()
    RBRACE         = auto()
    LBRACKET       = auto()
    RBRACKET       = auto()
    LPAREN         = auto()
    RPAREN         = auto()
    SEMICOLON      = auto()
    ELLIPSIS       = auto()
    HASH           = auto()
    HASH_HASH      = auto()
    AT             = auto()

####################################################################################

# Map lexemes to TokenType
# (Include all keyword and operator mappings as before)

token_dict = {
    # Keywords
    "alignas": TokenType.ALIGNAS,
    "alignof": TokenType.ALIGNOF,
    "and": TokenType.AND,
    "and_eq": TokenType.AND_EQ,
    "asm": TokenType.ASM,
    "auto": TokenType.AUTO,
    "bitand": TokenType.BITAND,
    "bitor": TokenType.BITOR,
    "bool": TokenType.BOOL,
    "break": TokenType.BREAK,
    "case": TokenType.CASE,
    "catch": TokenType.CATCH,
    "char": TokenType.CHAR,
    "char8_t": TokenType.CHAR8_T,
    "char16_t": TokenType.CHAR16_T,
    "char32_t": TokenType.CHAR32_T,
    "class": TokenType.CLASS,
    "compl": TokenType.COMPL,
    "concept": TokenType.CONCEPT,
    "const": TokenType.CONST,
    "consteval": TokenType.CONSTEVAL,
    "constexpr": TokenType.CONSTEXPR,
    "constinit": TokenType.CONSTINIT,
    "const_cast": TokenType.CONST_CAST,
    "continue": TokenType.CONTINUE,
    "co_await": TokenType.CO_AWAIT,
    "co_return": TokenType.CO_RETURN,
    "co_yield": TokenType.CO_YIELD,
    "decltype": TokenType.DECLTYPE,
    "default": TokenType.DEFAULT,
    "delete": TokenType.DELETE,
    "do": TokenType.DO,
    "double": TokenType.DOUBLE,
    "dynamic_cast": TokenType.DYNAMIC_CAST,
    "else": TokenType.ELSE,
    "enum": TokenType.ENUM,
    "explicit": TokenType.EXPLICIT,
    "export": TokenType.EXPORT,
    "extern": TokenType.EXTERN,
    "false": TokenType.FALSE,
    "final": TokenType.FINAL,
    "float": TokenType.FLOAT,
    "for": TokenType.FOR,
    "friend": TokenType.FRIEND,
    "goto": TokenType.GOTO,
    "if": TokenType.IF,
    "inline": TokenType.INLINE,
    "int": TokenType.INT,
    "long": TokenType.LONG,
    "mutable": TokenType.MUTABLE,
    "namespace": TokenType.NAMESPACE,
    "new": TokenType.NEW,
    "noexcept": TokenType.NOEXCEPT,
    "not": TokenType.NOT,
    "not_eq": TokenType.NOT_EQ,
    "nullptr": TokenType.NULLPTR,
    "operator": TokenType.OPERATOR,
    "or": TokenType.OR,
    "or_eq": TokenType.OR_EQ,
    "private": TokenType.PRIVATE,
    "protected": TokenType.PROTECTED,
    "public": TokenType.PUBLIC,
    "register": TokenType.REGISTER,
    "reinterpret_cast": TokenType.REINTERPRET_CAST,
    "requires": TokenType.REQUIRES,
    "return": TokenType.RETURN,
    "short": TokenType.SHORT,
    "signed": TokenType.SIGNED,
    "sizeof": TokenType.SIZEOF,
    "static": TokenType.STATIC,
    "static_assert": TokenType.STATIC_ASSERT,
    "static_cast": TokenType.STATIC_CAST,
    "struct": TokenType.STRUCT,
    "switch": TokenType.SWITCH,
    "template": TokenType.TEMPLATE,
    "this": TokenType.THIS,
    "thread_local": TokenType.THREAD_LOCAL,
    "throw": TokenType.THROW,
    "true": TokenType.TRUE,
    "try": TokenType.TRY,
    "typedef": TokenType.TYPEDEF,
    "typeid": TokenType.TYPEID,
    "typename": TokenType.TYPENAME,
    "union": TokenType.UNION,
    "unsigned": TokenType.UNSIGNED,
    "using": TokenType.USING,
    "virtual": TokenType.VIRTUAL,
    "void": TokenType.VOID,
    "volatile": TokenType.VOLATILE,
    "wchar_t": TokenType.WCHAR_T,
    "while": TokenType.WHILE,
    "xor": TokenType.XOR,
    "xor_eq": TokenType.XOR_EQ,

    # Operators & punctuation
    "+": TokenType.PLUS,
    "-": TokenType.MINUS,
    "*": TokenType.STAR,
    "/": TokenType.SLASH,
    "%": TokenType.PERCENT,
    "++": TokenType.INCREMENT,
    "--": TokenType.DECREMENT,
    "=": TokenType.ASSIGN,
    "+=": TokenType.PLUS_EQ,
    "-=": TokenType.MINUS_EQ,
    "*=": TokenType.STAR_EQ,
    "/=": TokenType.SLASH_EQ,
    "%=": TokenType.PERCENT_EQ,
    "&=": TokenType.AND_EQ_OP,
    "|=": TokenType.OR_EQ_OP,
    "^=": TokenType.XOR_EQ_OP,
    "<<=": TokenType.SHL_EQ,
    ">>=": TokenType.SHR_EQ,
    "==": TokenType.EQ,
    "!=": TokenType.NEQ,
    "<": TokenType.LT,
    ">": TokenType.GT,
    "<=": TokenType.LTE,
    ">=": TokenType.GTE,
    "&&": TokenType.LOGICAL_AND,
    "||": TokenType.LOGICAL_OR,
    "!": TokenType.LOGICAL_NOT,
    "&": TokenType.BIT_AND,
    "|": TokenType.BIT_OR,
    "^": TokenType.BIT_XOR,
    "~": TokenType.BIT_NOT,
    "<<": TokenType.SHL,
    ">>": TokenType.SHR,
    "?": TokenType.CONDITIONAL,
    ":": TokenType.COLON,
    ",": TokenType.COMMA,
    ".": TokenType.DOT,
    "...": TokenType.ELLIPSIS,
    "->": TokenType.ARROW,
    "->*": TokenType.ARROW_STAR,
    ".*": TokenType.DOT_STAR,
    "::": TokenType.SCOPE,
    "new[]": TokenType.NEW_ARRAY,
    "delete[]": TokenType.DELETE_ARRAY,
    "{": TokenType.LBRACE,
    "}": TokenType.RBRACE,
    "[": TokenType.LBRACKET,
    "]": TokenType.RBRACKET,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ";": TokenType.SEMICOLON,
    "#": TokenType.HASH,
    "##": TokenType.HASH_HASH,
    "@": TokenType.AT,
    "}": TokenType.RBRACE,
    "(": TokenType.LPAREN,
    ")": TokenType.RPAREN,
    ";": TokenType.SEMICOLON,
    "//": TokenType.COMMENT,
    "/*": TokenType.COMMENT,
}

# Sets for quick membership checks
punctuations = set(p for p in token_dict if token_dict[p] in {
    TokenType.LBRACE, TokenType.RBRACE, TokenType.LBRACKET, TokenType.RBRACKET,
    TokenType.LPAREN, TokenType.RPAREN, TokenType.COLON, TokenType.SEMICOLON,
    TokenType.DOT, TokenType.ELLIPSIS, TokenType.HASH, TokenType.HASH_HASH,
    TokenType.AT
})

operators = set(p for p in token_dict if token_dict[p] not in punctuations and token_dict[p] != TokenType.COMMENT)

keywords = { kw for kw, ttype in token_dict.items() if ttype.name in TokenType.__members__ and TokenType[ttype.name].name == ttype.name and ttype.name.isupper() }
