class SourceCode:
    def __init__(self, filename: str) -> None:
        self.file = open(filename)
        self.reserved_words: list[str] = [
            "]",
            "[",
            ")",
            "(",
            "}",
            "{",
            ",",
            ";",
            ".",
            "+",
            "*",
            "/",
            "-",
            ">",
            "<",
        ]
        self.two_char = [
            "<-",
            ">=",
            "==",
            "!=",
            "<=",
        ]
        self.check_char = [
            "<",
            ">",
            "=",
            "!",
            "<",
        ]
        # keywords can be a part of identifier and can be identified separated with a space
        self.keywords = [
            "let",
            "call",
            "if",
            "then",
            "else",
            "fi",
            "while",
            "do",
            "od",
            "return",
            "var",
            "array",
            "void",
            "function",
            "main",
        ]

    def read_words(self) -> list[str]:
        state = 0
        word = ""
        word_list: list[str] = []

        while True:

            char = self.file.read(1)

            if not char:
                if word != "":
                    word_list.append(word)
                break
            char = str(char)

            if state == 0:
                if char.isspace():
                    pass
                elif char.isnumeric():
                    state = 1
                    word += char
                elif char in self.check_char:
                    state = 3
                    word += char
                elif char in self.reserved_words:
                    word_list.append(char)
                else:
                    state = 2
                    word += char
            elif state == 1:
                if char.isspace():
                    word_list.append(word)
                    word = ""
                    state = 0
                elif char.isnumeric():
                    word += char
                elif char in self.check_char:
                    word_list.append(word)
                    word = char
                    state = 3
                elif char in self.reserved_words:
                    word_list.append(word)
                    word_list.append(char)
                    word = ""
                    state = 0
                else:
                    state = 2
                    word_list.append(word)
                    word = ""
                    word = char
            elif state == 2:
                if char.isspace():
                    word_list.append(word)
                    word = ""
                    state = 0
                elif char in self.check_char:
                    word += char
                    state = 3
                elif char in self.reserved_words:
                    word_list.append(word)
                    word_list.append(char)

                    word = ""
                    state = 0
                else:
                    word += char
            elif state == 3:
                if (word[-1] + char) in self.two_char:
                    reserved = word[-1] + char

                    if word[:-1]:
                        word_list.append(word[:-1])
                    word_list.append(reserved)

                    word = ""
                    state = 0
                else:
                    if word[:-1]:
                        word_list.append(word[:-1])
                    word_list.append(word[-1])

                    if char.isspace():
                        word = ""
                        state = 0
                    elif char.isnumeric():
                        word = char
                        state = 1
                    elif char in self.check_char:
                        state = 3
                        word = char
                    elif char in self.reserved_words:
                        word_list.append(char)
                        state = 0
                    else:
                        state = 2
                        word = char

            else:
                raise ValueError

        return word_list
