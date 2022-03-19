from io_interface import SourceCode


class Token:
    pass


class Identifier(Token):
    def __init__(self, value: str) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f'Identifier("{self.value}")'


class Number(Token):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"Number({self.value})"


class Relation(Token):
    def __init__(self) -> None:
        super().__init__()


class Eq(Relation):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Eq()"


class Neq(Relation):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Neq()"


class G(Relation):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "G()"


class Ge(Relation):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Ge()"


class L(Relation):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "L()"


class Le(Relation):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Le()"


class Operator(Token):
    def __init__(self) -> None:
        super().__init__()


class Plus(Operator):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Plus()"


class Minus(Operator):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Minus()"


class Mul(Operator):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Mul()"


class Div(Operator):
    def __init__(self) -> None:
        super().__init__()

    def __str__(self) -> str:
        return "Div()"


class Keyword(Token):
    def __init__(self) -> None:
        super().__init__()


class Right_bracket(Keyword):
    def __str__(self) -> str:
        return "Right_bracket()"


class Left_bracket(Keyword):
    def __str__(self) -> str:
        return "Left_bracket()"


class Right_paren(Keyword):
    def __str__(self) -> str:
        return "Right_paren()"


class Left_paren(Keyword):
    def __str__(self) -> str:
        return "Left_paren()"


class Right_brace(Keyword):
    def __str__(self) -> str:
        return "Right_brace()"


class Left_brace(Keyword):
    def __str__(self) -> str:
        return "Left_brace()"


class Let(Keyword):
    def __str__(self) -> str:
        return "Let()"


class Assign(Keyword):
    def __str__(self) -> str:
        return "Assign()"


class Call(Keyword):
    def __str__(self) -> str:
        return "Call()"


class Comma(Keyword):
    def __str__(self) -> str:
        return "Comma()"


class If(Keyword):
    def __str__(self) -> str:
        return "If()"


class Then(Keyword):
    def __str__(self) -> str:
        return "Then()"


class Else(Keyword):
    def __str__(self) -> str:
        return "Else()"


class Fi(Keyword):
    def __str__(self) -> str:
        return "Fi()"


class While(Keyword):
    def __str__(self) -> str:
        return "While()"


class Do(Keyword):
    def __str__(self) -> str:
        return "Do()"


class Od(Keyword):
    def __str__(self) -> str:
        return "Od()"


class Return(Keyword):
    def __str__(self) -> str:
        return "Return()"


class Semicolon(Keyword):
    def __str__(self) -> str:
        return "Semicolon()"


class Var(Keyword):
    def __str__(self) -> str:
        return "Var()"


class Array(Keyword):
    def __str__(self) -> str:
        return "Array()"


class Void(Keyword):
    def __str__(self) -> str:
        return "Void()"


class Function(Keyword):
    def __str__(self) -> str:
        return "Function()"


class Main(Keyword):
    def __str__(self) -> str:
        return "Main()"


class Dot(Keyword):
    def __str__(self) -> str:
        return "Dot()"


class Lexer(SourceCode):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)

    def tokenization(self) -> list[Token]:
        token_list: list[Token] = []
        keywords: dict[str, Keyword] = {
            "]": Right_bracket,
            "[": Left_bracket,
            ")": Right_paren,
            "(": Left_paren,
            "}": Right_brace,
            "{": Left_brace,
            "let": Let,
            "<-": Assign,
            "call": Call,
            ",": Comma,
            "if": If,
            "then": Then,
            "else": Else,
            "fi": Fi,
            "while": While,
            "do": Do,
            "od": Od,
            "return": Return,
            ";": Semicolon,
            "var": Var,
            "array": Array,
            "void": Void,
            "function": Function,
            "main": Main,
            ".": Dot,
        }  # type: ignore

        for word in self.read_words():
            if word.isnumeric():
                token_list.append(Number(int(word)))
            elif word == "==":
                token_list.append(Eq())
            elif word == "!=":
                token_list.append(Neq())
            elif word == "<":
                token_list.append(L())
            elif word == "<=":
                token_list.append(Le())
            elif word == ">":
                token_list.append(G())
            elif word == ">=":
                token_list.append(Ge())
            elif word == "+":
                token_list.append(Plus())
            elif word == "-":
                token_list.append(Minus())
            elif word == "*":
                token_list.append(Mul())
            elif word == "/":
                token_list.append(Div())
            elif word in keywords.keys():
                token_list.append(keywords[word]())  # type: ignore
            else:
                token_list.append(Identifier(word))

        return token_list
