from src.utils import print_IR, print_graph, line_numbering
from src.frontend import FrontEnd
from src.register_allocation import register_allocate


def test_print_graph():
    front = FrontEnd("./examples/bubble_sort.smpl")
    ir_list = front.generate_IR()

    register_allocate(ir_list)

    print_graph(ir_list, "test_bubble_sort")
