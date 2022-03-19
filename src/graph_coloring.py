from typing import Union
import frontend


class Node:
    def __init__(self, line_num_list: list[int]) -> None:
        self.line_num_list = line_num_list


class Graph:
    def __init__(self, inst_list: list[frontend.Instruction]) -> None:
        self.adj_list: dict[Node, list[Node]] = {}
        self.node_list: list[Node] = []
        self.inst_list = inst_list
        self.current_color_num = 0

        for inst in inst_list:
            assert inst.line_number is not None
            if (
                type(inst) is not frontend.Nop
                and type(inst) is not frontend.Beq
                and type(inst) is not frontend.Bge
                and type(inst) is not frontend.Bgt
                and type(inst) is not frontend.Ble
                and type(inst) is not frontend.Blt
                and type(inst) is not frontend.Bne
                and type(inst) is not frontend.Bra
            ):
                self.node_list.append(Node([inst.line_number]))

        for node in self.node_list:
            self.adj_list[node] = []

    def find_node(self, line_num: int) -> Union[Node, None]:
        for node in self.node_list:
            if line_num in node.line_num_list:
                return node

    def cluster_phi(self) -> None:
        for inst in self.inst_list:
            assert inst.line_number is not None
            if type(inst) is frontend.Phi:
                phi_line_num = inst.line_number
                phi_node = self.find_node(phi_line_num)
                assert phi_node

                for y in [inst.left, inst.right]:
                    if not isinstance(y, frontend.Instruction):
                        continue

                    assert y.line_number is not None
                    y_node = self.find_node(y.line_number)
                    assert y_node
                    if y_node not in self.adj_list[phi_node]:
                        assert len(y_node.line_num_list) == 1
                        phi_node.line_num_list.append(y_node.line_num_list[0])
                        self.adj_list[phi_node] += self.adj_list[y_node]
                        self.node_list.remove(y_node)
                        del self.adj_list[y_node]

    def add_edge(self, line_num1: int, line_num2: int) -> None:
        node1 = self.find_node(line_num1)
        node2 = self.find_node(line_num2)
        assert node1, f"{line_num1} , {line_num2}"
        assert node2, line_num2

        if node2 not in self.adj_list[node1]:
            self.adj_list[node1].append(node2)
        if node1 not in self.adj_list[node2]:
            self.adj_list[node2].append(node1)

    # Greedy algorithm:
    #   1. Pick the highest cost node
    #   2. Color it with an availabe color
    #   3. Repeat until coloring all nodes
    def coloring(self) -> int:
        node_set: list[Node] = [] + self.node_list
        while node_set:
            x = self.pick_high_cost_node(node_set)
            node_set.remove(x)

            used_color: list[int] = []
            for neighbor in self.adj_list[x]:
                if self.inst_list[neighbor.line_num_list[0]].reg_num is not None:
                    used_color.append(self.inst_list[neighbor.line_num_list[0]].reg_num)

            available_color = 0
            while True:
                if available_color in used_color:
                    available_color += 1
                else:
                    break
            if available_color > self.current_color_num:
                self.current_color_num = available_color

            for line_num in x.line_num_list:
                self.inst_list[line_num].reg_num = available_color

        for node in self.node_list:
            for line_num in node.line_num_list:
                assert self.inst_list[line_num].reg_num is not None

        return self.current_color_num + 1

    def pick_high_cost_node(self, l: list[Node]) -> Node:
        candidate: Union[Node, None] = None
        for node in l:
            if (
                candidate is None
                or self.inst_list[candidate.line_num_list[0]].cost
                < self.inst_list[node.line_num_list[0]].cost
            ):
                candidate = node
        assert candidate is not None

        return candidate
