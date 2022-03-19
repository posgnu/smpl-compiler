from src.parser import *
import src.lexer


def test_next():
    parser = Parser("./examples/bubble_sort.smpl")
    assert type(parser.next()) == src.lexer.Main


def test_previous():
    parser = Parser("./examples/bubble_sort.smpl")
    assert type(parser.next()) == src.lexer.Main
    assert type(parser.previous()) == src.lexer.Main


def test_AST():
    parser = Parser("./examples/bubble_sort.smpl")
    ast = parser.generate_AST()
    # print(ast)


def test_AST_function_assignment():
    parser = Parser("./examples/function_assignment.smpl")
    ast = parser.generate_AST()
    # print(ast)


def test_copy_propagation():
    parser = Parser("./examples/copy_propagation.smpl")
    ast = parser.generate_AST()
    # print(ast)


def test_nested_expression():
    parser = Parser("./examples/nested_expression.smpl")
    ast = parser.generate_AST()
    # print(ast)


def test_dead_code_elimination():
    parser = Parser("./examples/dead_code_elimination.smpl")
    ast = parser.generate_AST()
    # print(ast)


def test_random():
    dir = "./examples/random"
    from os import listdir
    from os.path import isfile, join

    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    for filename in onlyfiles:
        path = join(dir, filename)
        parser = Parser(str(path))
        ast = parser.generate_AST()
