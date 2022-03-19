import argparse
from frontend import FrontEnd
from utils import print_graph
from register_allocation import register_allocate

parser = argparse.ArgumentParser(description="DLX compiler 1.0 powered by posgnu")
parser.add_argument(
    "input",
    help="input source file name",
)
parser.add_argument(
    "output",
    help="output file name",
)
parser.add_argument("-g", "--graph", help="show IR graph", action="store_true")
args = parser.parse_args()

if args.graph is not None:
    view = True
else:
    view = False

input_filename = args.input
output_filename = args.output

front = FrontEnd(input_filename)

ir_list = front.generate_IR()

print_graph(ir_list, output_filename + "-IR", view)

# register_allocate(ir_list)

# print_graph(ir_list, output_filename + "-register_allocated")
