import frontend
import graph_coloring
import utils


def resolve_phi(bb_list: list[frontend.BasicBlock]):

    for current_bb in bb_list:
        if current_bb.name == "join-if":
            assert current_bb.cond_bb
            new_inst_list: list[frontend.InstElement] = []
            for inst in current_bb.instructions:
                if type(inst) is frontend.Phi:
                    if (
                        isinstance(inst.left, frontend.Instruction)
                        and inst.reg_num != inst.left.reg_num
                    ):
                        current_bb.prevs[0].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=inst.left.reg_num)
                        )
                    elif type(inst.left) is int:
                        current_bb.prevs[0].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=str(inst.left))
                        )
                    elif type(inst.left) is frontend.Offset:
                        raise NotImplemented

                    if (
                        isinstance(inst.right, frontend.Instruction)
                        and inst.reg_num != inst.right.reg_num
                    ):
                        current_bb.prevs[1].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=inst.right.reg_num)
                        )
                    elif type(inst.right) is int:
                        current_bb.prevs[1].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=str(inst.right))
                        )
                    elif type(inst.left) is frontend.Offset:
                        raise NotImplemented
                else:
                    new_inst_list.append(inst)

            current_bb.instructions = new_inst_list
        elif current_bb.name == "join-while":
            new_inst_list: list[frontend.InstElement] = []
            for inst in current_bb.instructions:
                if type(inst) is frontend.Phi:

                    if (
                        isinstance(inst.left, frontend.Instruction)
                        and inst.reg_num != inst.left.reg_num
                    ):
                        current_bb.prevs[1].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=inst.left.reg_num)
                        )
                    elif type(inst.left) is int:
                        current_bb.prevs[1].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=str(inst.left))
                        )
                    elif type(inst.left) is frontend.Offset:
                        raise NotImplemented

                    if (
                        isinstance(inst.right, frontend.Instruction)
                        and inst.reg_num != inst.right.reg_num
                    ):
                        current_bb.prevs[0].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=inst.right.reg_num)
                        )
                    elif type(inst.right) is int:
                        current_bb.prevs[1].instructions.append(
                            frontend.Mov(x=inst.reg_num, y=str(inst.right))
                        )
                    elif type(inst.right) is frontend.Offset:
                        raise NotImplemented

                else:
                    new_inst_list.append(inst)
            current_bb.instructions = new_inst_list


def build_interference_graph_bb(
    bb: frontend.BasicBlock, live_set: set[int], graph: graph_coloring.Graph
) -> set[int]:
    inst_list = bb.instructions + []
    inst_list.reverse()

    for inst in inst_list:
        if isinstance(inst, frontend.Instruction):
            if (
                type(inst) is frontend.Nop
                or type(inst) is frontend.Beq
                or type(inst) is frontend.Bge
                or type(inst) is frontend.Bgt
                or type(inst) is frontend.Ble
                or type(inst) is frontend.Blt
                or type(inst) is frontend.Bne
                or type(inst) is frontend.Bra
            ):
                continue
            assert inst.line_number is not None

            if type(inst) is not frontend.Phi:
                live_set.discard(inst.line_number)
            for live_idx in live_set:
                graph.add_edge(inst.line_number, live_idx)

            if type(inst) is frontend.Phi:
                pass
                """
                if isinstance(inst.left, frontend.Instruction):
                    assert inst.left.line_number
                    live_set.add(inst.left.line_number)
                if isinstance(inst.right, frontend.Instruction):
                    assert inst.right.line_number
                    live_set.add(inst.right.line_number)
                """
            elif type(inst) is frontend.Call:
                assert inst.call_arg is not None
                for inst in inst.call_arg:
                    if isinstance(inst, frontend.Instruction):
                        assert inst.line_number is not None
                        live_set.add(inst.line_number)
            elif (
                type(inst) is frontend.Beq
                or type(inst) is frontend.Bge
                or type(inst) is frontend.Bgt
                or type(inst) is frontend.Ble
                or type(inst) is frontend.Blt
                or type(inst) is frontend.Bne
                or type(inst) is frontend.Bra
            ):
                if isinstance(inst.x, frontend.Instruction):
                    assert inst.x.line_number is not None
                    live_set.add(inst.x.line_number)
            else:
                if isinstance(inst.x, frontend.Instruction):
                    assert inst.x.line_number is not None
                    live_set.add(inst.x.line_number)
                if isinstance(inst.y, frontend.Instruction):
                    assert inst.y.line_number is not None
                    live_set.add(inst.y.line_number)
        else:
            raise NotImplemented

    return live_set


def register_allocate(function_list: list[tuple[str, list[frontend.BasicBlock]]]):
    for id, bb_list in function_list:
        total_inst_num = utils.line_numbering([(id, bb_list)])
        inst_list = utils.decompose_bb([(id, bb_list)])
        bb_list = utils.linearize_bb([(id, bb_list)])
        assert total_inst_num == len(inst_list)

        graph = graph_coloring.Graph(inst_list)
        live_set: set[int] = set()

        # Generate edges
        live_set = build_interference_graph_bbs(
            bb_list[-1], bb_list[0], live_set, graph
        )
        assert not live_set

        graph.cluster_phi()
        num_of_reg = graph.coloring()
        resolve_phi(bb_list)

    return


def build_inference_graph_if(
    join_bb: frontend.BasicBlock,
    cond_bb: frontend.BasicBlock,
    live_set: set[int],
    graph: graph_coloring.Graph,
) -> set[int]:
    live_set1 = build_interference_graph_bb(join_bb, live_set, graph)

    then_phi: list[int] = []
    else_phi: list[int] = []
    phi_list: list[int] = []
    for inst in join_bb.instructions:
        if isinstance(inst, frontend.Instruction):
            if type(inst) is frontend.Phi:
                assert inst.line_number is not None
                phi_list.append(inst.line_number)
                if isinstance(inst.left, frontend.Instruction):
                    assert inst.left.line_number
                    then_phi.append(inst.left.line_number)
                if isinstance(inst.right, frontend.Instruction):
                    assert inst.right.line_number
                    else_phi.append(inst.right.line_number)
        else:
            raise NotImplemented

    live_set2 = live_set1.copy()
    live_set3 = live_set1.copy()
    for line_num in phi_list:
        live_set2.remove(line_num)
        live_set3.remove(line_num)
    for line_num in then_phi:
        live_set2.add(line_num)
    for line_num in else_phi:
        live_set3.add(line_num)

    live_set2 = build_interference_graph_bbs(
        join_bb.prevs[0], cond_bb, live_set2, graph
    )
    live_set3 = build_interference_graph_bbs(
        join_bb.prevs[1], cond_bb, live_set3, graph
    )

    live_set4 = live_set2.union(live_set3)
    live_set4 = build_interference_graph_bb(cond_bb, live_set4, graph)

    return live_set4


def build_inference_graph_while(
    join_bb: frontend.BasicBlock, live_set0: set[int], graph: graph_coloring.Graph
) -> set[int]:
    live_set1 = build_interference_graph_bb(join_bb, live_set0, graph)

    do_phi: list[int] = []
    pre_phi: list[int] = []
    phi_list: list[int] = []
    for inst in join_bb.instructions:
        if isinstance(inst, frontend.Instruction):
            if type(inst) is frontend.Phi:
                assert inst.line_number is not None
                phi_list.append(inst.line_number)
                if isinstance(inst.right, frontend.Instruction):
                    assert inst.right.line_number
                    do_phi.append(inst.right.line_number)
                if isinstance(inst.left, frontend.Instruction):
                    assert inst.left.line_number
                    pre_phi.append(inst.left.line_number)

    for line_num in do_phi:
        live_set1.add(line_num)

    live_set2 = build_interference_graph_bbs(
        join_bb.prevs[0], join_bb, live_set1, graph
    )
    live_set3 = build_interference_graph_bb(join_bb, live_set2, graph)

    for line_num in phi_list:
        live_set3.discard(line_num)
    for line_num in pre_phi:
        live_set3.add(line_num)

    return live_set3


def build_interference_graph_bbs(
    bb_start: frontend.BasicBlock,
    bb_end: frontend.BasicBlock,
    live_set: set[int],
    graph: graph_coloring.Graph,
) -> set[int]:
    current_bb = bb_start

    while True:
        if current_bb is bb_end:
            break

        if current_bb.name == "join-if":
            assert current_bb.cond_bb
            assert len(current_bb.prevs) == 2
            live_set = build_inference_graph_if(
                current_bb, current_bb.cond_bb, live_set, graph
            )

            assert len(current_bb.cond_bb.prevs) == 1
            current_bb = current_bb.cond_bb.prevs[0]
        elif current_bb.name == "join-while":
            assert len(current_bb.prevs) == 2

            live_set = build_inference_graph_while(current_bb, live_set, graph)
            current_bb = current_bb.prevs[1]
        elif current_bb.name is None:
            assert len(current_bb.prevs) == 1
            live_set = build_interference_graph_bb(current_bb, live_set, graph)
            current_bb = current_bb.prevs[0]
        else:
            pass

    return live_set
