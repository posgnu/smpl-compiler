import frontend
import graphviz


def draw_link_func_call(
    dot: graphviz.Digraph, function_list: list[tuple[str, list[frontend.BasicBlock]]]
) -> None:
    bb_list = linearize_bb(function_list)

    for bb in bb_list:
        inst_list = bb.instructions
        called_function_list: list[str] = []
        for inst in inst_list:
            if type(inst) is frontend.Call:
                function_id = inst.call_id
                if (
                    function_id != "InputNum"
                    and function_id != "OutputNum"
                    and function_id != "OutputNewLine"
                ):
                    assert function_id is not None
                    called_function_list.append(function_id)

        for called_function in called_function_list:
            called_function_head = None
            for id, bbs in function_list:
                if id == called_function:
                    called_function_head = bbs[0]
                    break
            assert called_function_head is not None
            assert bb.name is not None
            assert called_function_head.name is not None

            dot.edge(
                bb.name,
                called_function_head.name,
                color="red",
                label=f"Call {called_function}",
                fontcolor="red",
            )


def print_graph(
    function_list: list[tuple[str, list[frontend.BasicBlock]]], dir: str, view:bool
) -> None:
    line_numbering(function_list)
    for id, bbs in function_list:
        bbs[0].name = f"function {id}"

    bb_list = linearize_bb(function_list)
    dot = graphviz.Digraph(node_attr={"shape": "record"})
    current_bb_number = 0

    # Draw nodes
    for bb in bb_list:
        if bb.name is not None:
            node_name = f"BB{current_bb_number} ({bb.name})"
        else:
            node_name = f"BB{current_bb_number}"
        inst_str = [str(x) for x in bb.instructions]
        node_content = "{" + f'{"|".join(inst_str)}' + "}"
        node_label = f"<b>{node_name}| {node_content}"
        bb.name = node_name
        dot.node(name=node_name, label=node_label)

        current_bb_number += 1

    # Draw edges
    for bb in bb_list:
        if len(bb.nexts) == 2:
            dot.edge(bb.name, bb.nexts[0].name, label="False")
            dot.edge(bb.name, bb.nexts[1].name, label="True")
        elif len(bb.nexts) == 1:
            neighbor = bb.nexts[0]
            dot.edge(bb.name, neighbor.name)
        elif len(bb.nexts) == 0:
            pass
        else:
            raise ValueError()

        for neighbor in bb.doms:
            dot.edge(
                bb.name,
                neighbor.name,
                label="Dominate",
                fontcolor="blue",
                color="blue",
                style="dotted",
            )

    draw_link_func_call(dot, function_list)

    dot.render(directory=dir, view=view)


def linearize_bb(
    function_list: list[tuple[str, list[frontend.BasicBlock]]]
) -> list[frontend.BasicBlock]:
    bb_list: list[frontend.BasicBlock] = []
    for _, bbs in function_list:
        bb_list += bbs

    return bb_list


def graph_pruning() -> None:
    raise NotImplemented


def decompose_bb(
    function_list: list[tuple[str, list[frontend.BasicBlock]]]
) -> list[frontend.Instruction]:
    result: list[frontend.InstElement] = []

    for (_, bb_list) in function_list:
        for bb in bb_list:
            for inst in bb.instructions:
                if isinstance(inst, frontend.Instruction):
                    result.append(inst)
                elif type(inst) is frontend.InstructionSet:
                    result += inst.instructions

    return result


def print_IR(function_list: list[tuple[str, list[frontend.BasicBlock]]]) -> None:
    line_numbering(function_list)

    for inst in decompose_bb(function_list):
        if isinstance(inst, frontend.Instruction):
            print(inst)
        elif type(inst) is frontend.InstructionSet:
            inst_set = inst
            for inst in inst_set.instructions:
                print(inst)
        else:
            raise ValueError


def line_numbering(function_list: list[tuple[str, list[frontend.BasicBlock]]]) -> int:
    current_line_num = 0
    for inst in decompose_bb(function_list):
        if isinstance(inst, frontend.Instruction):
            inst.set_line_number(current_line_num)
            current_line_num += 1
        elif type(inst) is frontend.InstructionSet:
            inst_set = inst
            for inst in inst_set.instructions:
                inst.set_line_number(current_line_num)
                current_line_num += 1
        else:
            raise ValueError

    return current_line_num
