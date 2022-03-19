from src.frontend import FrontEnd


def test_bubble_sort():
    front = FrontEnd("./examples/bubble_sort.smpl")
    front.generate_IR()


def test_function_assignment():
    front = FrontEnd("./examples/function_assignment.smpl")
    front.generate_IR()


def test_copy_propagation():
    front = FrontEnd("./examples/copy_propagation.smpl")
    front.generate_IR()


def test_uninitialized_variable():
    front = FrontEnd("./examples/uninitialized_variable.smpl")
    front.generate_IR()


def test_nested_expression():
    front = FrontEnd("./examples/nested_expression.smpl")
    front.generate_IR()


def test_dead_code_elimination():
    front = FrontEnd("./examples/dead_code_elimination.smpl")
    front.generate_IR()


def test_function_parameter_assignment():
    front = FrontEnd("./examples/function_parameter_assignment.smpl")
    front.generate_IR()


def test_random():
    dir = "./examples/random"
    from os import listdir
    from os.path import isfile, join

    onlyfiles = [f for f in listdir(dir) if isfile(join(dir, f))]
    for filename in onlyfiles:
        path = join(dir, filename)
        front = FrontEnd(str(path))
        front.generate_IR()
