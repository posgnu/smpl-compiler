from src.lexer import *


def test_lexer():
    lexer = Lexer("./examples/bubble_sort.smpl")
    token_list = lexer.tokenization()
