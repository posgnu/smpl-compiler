from src.utils import print_IR, print_graph
from src.frontend import FrontEnd


def test_print_IR():
    front = FrontEnd("./examples/simple_if.smpl")
    print_IR(front.generate_IR())


def test_print_graph():
    front = FrontEnd("./examples/bubble_sort.smpl")
    print_graph(front.generate_IR(), "test_bubble_sort")


def test_print_graph_real1():
    front = FrontEnd("./examples/random/real1.smpl")
    print_graph(front.generate_IR(), "test_real1")


def test_print_graph_real2():
    front = FrontEnd("./examples/random/real2.smpl")
    print_graph(front.generate_IR(), "test_real2")


def test_print_graph_real3():
    front = FrontEnd("./examples/random/real3.smpl")
    print_graph(front.generate_IR(), "test_real3")
