from typing import Union
import parser
import logging
import math


class InstElement:
    pass


class Offset:
    def __init__(self, value: int) -> None:
        self.value = value

    def __eq__(self, __o: object) -> bool:
        if type(__o) is not Offset:
            return False

        return self.value == __o.value


class Instruction(InstElement):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        self.x = x
        self.y = y
        self.assigned_reg = assigned_reg
        self.reg_num: Union[int, None] = None
        self.offset = offset
        self.id = id
        self.call_id = call_id
        self.call_arg = call_arg
        self.line_number = line_number
        self.cost: int = 0

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Instruction):
            return False

        if type(self.x) is not type(__o.x):
            return False
        if isinstance(self.x, Instruction):
            if self.x is not __o.x:
                return False
        else:
            if self.x != __o.x:
                return False

        if type(self.y) is not type(__o.y):
            return False
        if isinstance(self.y, Instruction):
            if self.y is not __o.y:
                return False
        else:
            if self.y != __o.y:
                return False

        if self.id != __o.id:
            return False

        if self.call_id != __o.call_id:
            return False

        return True

    def set_line_number(self, n: int) -> None:
        self.line_number = n

    def __str__(self) -> str:
        assert self.id is not None
        assert self.line_number is not None

        if type(self.x) is int:
            x_str = "#" + str(self.x)
        elif isinstance(self.x, Instruction):
            if self.x.reg_num is not None:
                x_str = f"reg{self.x.reg_num}"
            else:
                assert self.x.line_number is not None
                x_str = "(" + str(self.x.line_number) + ")"
        elif type(self.x) is str:
            x_str = self.x
        else:
            x_str = ""

        if type(self.y) is int:
            y_str = "#" + str(self.y)
        elif isinstance(self.y, Instruction):
            if (
                type(self) is Beq
                or type(self) is Bge
                or type(self) is Bgt
                or type(self) is Ble
                or type(self) is Blt
                or type(self) is Bne
                or type(self) is Bra
            ):
                assert self.y.line_number is not None
                y_str = "(" + str(self.y.line_number) + ")"
            elif self.y.reg_num is not None:
                y_str = f"reg{self.y.reg_num}"
            else:
                assert self.y.line_number is not None
                y_str = "(" + str(self.y.line_number) + ")"
        elif type(self.y) is str:
            y_str = self.y
        else:
            y_str = ""

        if self.reg_num is not None:
            return (
                str(self.line_number)
                + ": "
                + self.id
                + " "
                + x_str
                + ", "
                + y_str
                + " --\\> "
                + f"reg{self.reg_num}"
            )
        else:
            return str(self.line_number) + ": " + self.id + " " + x_str + ", " + y_str


class InstructionSet(InstElement):
    def __init__(self, instructions: list[Instruction]) -> None:
        self.instructions = instructions


class Mov(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "mov", call_id, call_arg, line_number
        )

    def __str__(self) -> str:
        assert self.id is not None
        assert self.line_number is not None

        if type(self.x) is int:
            x_str = f"reg{self.x}"
        else:
            raise ValueError

        if type(self.y) is int:
            y_str = f"reg{self.y}"
        elif type(self.y) is str:
            y_str = f"#{self.y}"
        else:
            raise ValueError

        return str(self.line_number) + ": " + self.id + " " + y_str + " --\\> " + x_str


class Neg(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "neg", call_id, call_arg, line_number
        )


class Add(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "add", call_id, call_arg, line_number
        )


class Sub(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "sub", call_id, call_arg, line_number
        )


class Mul(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "mul", call_id, call_arg, line_number
        )


class Div(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "div", call_id, call_arg, line_number
        )


class Cmp(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "cmp", call_id, call_arg, line_number
        )


class Adda(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "adda", call_id, call_arg, line_number
        )


class Load(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "load", call_id, call_arg, line_number
        )


class Store(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "store", call_id, call_arg, line_number
        )


class Phi(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
        left: Union[int, "Instruction", None, Offset] = None,
        right: Union[int, "Instruction", None, Offset] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "phi", call_id, call_arg, line_number
        )
        self.left = left
        self.right = right

    def __str__(self) -> str:
        assert self.id is not None
        assert self.line_number is not None

        if type(self.left) is int:
            x_str = "#" + str(self.left)
        elif isinstance(self.left, Instruction):
            if self.left.reg_num is not None:
                x_str = f"reg{self.left.reg_num}"
            else:
                assert self.left.line_number is not None
                x_str = "(" + str(self.left.line_number) + ")"
        elif type(self.left) is Offset:
            x_str = "P" + str(self.left.value)
        else:
            x_str = ""

        if type(self.right) is int:
            y_str = "#" + str(self.right)
        elif isinstance(self.right, Instruction):
            if self.right.reg_num is not None:
                y_str = f"reg{self.right.reg_num}"
            else:
                assert self.right.line_number is not None
                y_str = "(" + str(self.right.line_number) + ")"
        elif type(self.right) is Offset:
            y_str = "P" + str(self.right.value)
        else:
            y_str = ""
        if self.reg_num is not None:
            return (
                str(self.line_number)
                + ": "
                + self.id
                + " "
                + x_str
                + ", "
                + y_str
                + " --\\> "
                + f"reg{self.reg_num}"
            )
        else:
            return str(self.line_number) + ": " + self.id + " " + x_str + ", " + y_str

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, Phi):
            return False

        if type(self.left) is not type(__o.left):
            return False
        if isinstance(self.left, Instruction):
            if self.left is not __o.left:
                return False
        elif type(self.left) is Offset:
            if self.left.value != __o.left.value:
                return False
        else:
            if self.left != __o.left:
                return False

        if type(self.right) is not type(__o.right):
            return False
        if isinstance(self.right, Instruction):
            if self.right is not __o.right:
                return False
        elif type(self.right) is Offset:
            if self.right.value != __o.right.value:
                return False
        else:
            if self.right != __o.right:
                return False

        return True


class End(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "end", call_id, call_arg, line_number
        )


class Bra(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "bra", call_id, call_arg, line_number
        )


class Bne(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "bne", call_id, call_arg, line_number
        )


class Beq(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "beq", call_id, call_arg, line_number
        )


class Ble(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "ble", call_id, call_arg, line_number
        )


class Blt(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "blt", call_id, call_arg, line_number
        )


class Bge(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "bge", call_id, call_arg, line_number
        )


class Bgt(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "bgt", call_id, call_arg, line_number
        )


class Read(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "read", call_id, call_arg, line_number
        )


class Write(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "write", call_id, call_arg, line_number
        )


class WriteNL(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "writenl", call_id, call_arg, line_number
        )


class Call(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "call", call_id, call_arg, line_number
        )

    def __str__(self) -> str:
        assert self.call_id is not None
        assert self.call_arg is not None

        args = ""
        for arg in self.call_arg:
            if type(arg) is int:
                args += "#" + str(arg) + ", "
            elif isinstance(arg, Instruction):
                args += "(" + str(arg.line_number) + "),"

        if self.reg_num is not None:
            return (
                str(self.line_number)
                + ": "
                + self.call_id
                + "("
                + args
                + ") --\\> "
                + f"reg{self.reg_num}"
            )
        else:
            return str(self.line_number) + ": " + self.call_id + "(" + args + ")"


class Nop(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "nop", call_id, call_arg, line_number
        )


class Return(Instruction):
    def __init__(
        self,
        x: Union[int, "Instruction", str, None] = None,
        y: Union[int, "Instruction", str, None] = None,
        assigned_reg: bool = False,
        offset: Union[int, None] = None,
        id: Union[str, None] = None,
        call_id: Union[str, None] = None,
        call_arg: Union[list[Union["Instruction", int]], None] = None,
        line_number: Union[int, None] = None,
    ) -> None:
        super().__init__(
            x, y, assigned_reg, offset, "return", call_id, call_arg, line_number
        )


class SSATable:
    def __init__(self) -> None:
        self.table: dict[
            str, Union[Instruction, tuple[int, list[int]], int, None, Offset]
        ] = {}

    def get(self, id: str) -> Union[Instruction, tuple[int, list[int]], int, Offset]:
        if id in self.table:
            inst = self.table[id]
            if inst is not None:
                return inst
            else:
                return 0

        else:
            raise ValueError(f"Undefined identifier {id}")

    def update(
        self,
        id: str,
        inst: Union[Instruction, tuple[int, list[int]], int, Offset, None],
    ) -> None:
        self.table[id] = inst

    def copy(self) -> "SSATable":
        new_ssa_table = SSATable()
        new_ssa_table.table = self.table.copy()

        return new_ssa_table


class CSETable:
    def __init__(self) -> None:
        self.table: dict[str, list[Instruction]] = {}
        self.kill: bool = False

    def lookup(self, inst: Instruction) -> Union[None, Instruction]:
        id = inst.id
        assert id is not None

        if id in self.table:
            cse_list = self.table[id]
            for candidate in cse_list:
                if candidate == inst:
                    return candidate

        return None

    def add(self, inst: Instruction) -> None:
        id = inst.id
        assert id is not None

        if id in self.table:
            self.table[id].append(inst)
        else:
            self.table[id] = [inst]

    def lookup_return(self, inst: Instruction) -> tuple[list[InstElement], Instruction]:
        old = self.lookup(inst)

        if old:
            return [], old
        else:
            self.add(inst)
            return [inst], inst

    def kill_load(self) -> None:
        self.table["load"] = []

    def copy(self) -> "CSETable":
        new_cse_table = CSETable()
        new_cse_table.table = self.table.copy()
        new_cse_table.kill = self.kill

        return new_cse_table


class BasicBlock:
    def __init__(
        self,
        instructions: Union[list[InstElement], None] = None,
        nexts: Union[list["BasicBlock"], None] = None,
        ssa_table: Union[SSATable, None] = None,
        cse_table: Union[CSETable, None] = None,
    ) -> None:
        if instructions is None:
            instructions = []
        if nexts is None:
            nexts = []

        self.prevs: list[BasicBlock] = []
        self.nexts = nexts
        self.SSA_table = ssa_table
        self.CSE_table = cse_table
        self.instructions = instructions
        self.name: Union[str, None] = None
        self.doms: list[BasicBlock] = []
        self.cond_bb: Union[BasicBlock, None] = None


class FrontEnd(parser.Parser):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)

    def operate_var_decl(
        self,
        var_decl_list: list[parser.VarDecl],
        ssa_table: Union[SSATable, None] = None,
    ) -> SSATable:
        if ssa_table is None:
            ssa_table = SSATable()

        base_address = 0

        for var_decl in var_decl_list:
            decl_type = var_decl.type_decl
            id = var_decl.id.value

            if type(decl_type) is parser.Var:
                ssa_table.update(id, None)
            elif type(decl_type) is parser.Array:
                sum_idx = math.prod(decl_type.idx_list)
                ssa_table.update(id, (base_address, decl_type.idx_list))
                base_address += 4 * sum_idx
            else:
                raise ValueError

        return ssa_table

    def operate_formal_param(self, formal_params: list[parser.Identifier]) -> SSATable:
        ssa_table = SSATable()

        for idx, param in enumerate(formal_params):
            id = param.value
            ssa_table.update(id, Offset(idx + 1))

        return ssa_table

    def compute(
        self,
        op: parser.Op,
        x: Union[Instruction, int],
        y: Union[Instruction, int],
        cse_talbe: CSETable,
    ) -> tuple[list[InstElement], Union[Instruction, int]]:
        # Check copy propagation is already done
        # Copy propagation still can be done when a variable is constant
        # assert not (type(x) is int and type(y) is int)

        if type(op) is parser.Plus:
            return cse_talbe.lookup_return(Add(x=x, y=y))
        elif type(op) is parser.Minus:
            return cse_talbe.lookup_return(Sub(x=x, y=y))
        elif type(op) is parser.Mul:
            return cse_talbe.lookup_return(Mul(x=x, y=y))
        elif type(op) is parser.Div:
            return cse_talbe.lookup_return(Div(x=x, y=y))
        else:
            raise ValueError

    def operate_term(
        self, ssa_table: SSATable, cse_table: CSETable, term: parser.Term
    ) -> tuple[list[InstElement], Union[Instruction, int]]:
        list1, x = self.operate_factor(ssa_table, cse_table, term.factors[0])

        for factor, op in zip(term.factors[1:], term.ops):
            list2, y = self.operate_factor(ssa_table, cse_table, factor)
            list1 += list2
            list3, x = self.compute(op, x, y, cse_table)
            list1 += list3

        return list1, x

    def operate_factor(
        self, ssa_table: SSATable, cse_talbe: CSETable, factor: parser.Factor
    ) -> tuple[list[InstElement], Union[Instruction, int]]:
        if type(factor) is parser.Designator:
            return self.operate_designator(ssa_table, cse_talbe, factor, None)
        elif type(factor) is parser.Number:
            return [], factor.value
        elif type(factor) is parser.Expression:
            return self.operate_expression(ssa_table, cse_talbe, factor)
        elif type(factor) is parser.FuncCall:
            inst_list, inst = self.operate_func_call(ssa_table, cse_talbe, factor, True)
            assert type(inst_list) is list
            assert type(inst) is Call

            return inst_list, inst
        else:
            raise ValueError

    def operate_expression(
        self, ssa_table: SSATable, cse_table: CSETable, expression: parser.Expression
    ) -> tuple[list[InstElement], Union[Instruction, int]]:
        list1, x = self.operate_term(ssa_table, cse_table, expression.terms[0])

        for term, op in zip(expression.terms[1:], expression.ops):
            list2, y = self.operate_term(ssa_table, cse_table, term)
            list1 += list2
            list3, x = self.compute(op, x, y, cse_table)
            list1 += list3

        return list1, x

    def operate_designator(
        self,
        ssa_table: SSATable,
        cse_table: CSETable,
        designator: parser.Designator,
        value: Union[int, Instruction, None],
    ) -> tuple[list[InstElement], Union[Instruction, int]]:
        assert designator.factor_inheirt == (value is None)
        is_array = len(designator.idx_list) > 0

        if is_array:
            # Set kill when storing value in memory
            cse_table.kill = True
            return self.access_array(
                ssa_table, cse_table, designator, designator.factor_inheirt, value
            )
        else:
            if designator.factor_inheirt:
                offset_or_variable = ssa_table.get(designator.id.value)
                if type(offset_or_variable) is Offset:
                    list1, list2, ld = self.access_params(
                        cse_table, offset_or_variable, designator.factor_inheirt, value
                    )

                    return list1 + list2, ld
                elif (
                    isinstance(offset_or_variable, Instruction)
                    or type(offset_or_variable) is int
                ):
                    if ssa_table.table[designator.id.value] is None:
                        logging.warning("Uninitialized variable usage")
                    return [], offset_or_variable
                else:
                    logging.error("Missing indices detected")
                    raise ValueError
            else:
                assert value is not None

                assert (
                    type(ssa_table.table[designator.id.value]) is not tuple
                ), "Missing indices detected"
                # Support mutable paramter
                # assert (type(ssa_table.table[designator.id.value]) is not Offset), "Illegal trial to modify parameter"

                ssa_table.update(designator.id.value, value)
                return [], value

    def access_params(
        self,
        cse_table: CSETable,
        offset_or_variable: Offset,
        factor_inheirt: bool,
        value: Union[int, Instruction, None],
    ):
        # Jump ret
        offset = offset_or_variable.value * 4 + 4
        list1, addr = cse_table.lookup_return(Sub(x="FP", y=offset))
        if factor_inheirt:
            list2, ld = cse_table.lookup_return(Load(y=addr))
        else:
            assert value is not None
            list2, ld = cse_table.lookup_return(Store(x=addr, y=value))
        return list1, list2, ld

    def access_array(
        self,
        ssa_table: SSATable,
        cse_table: CSETable,
        designator: parser.Designator,
        factor_inheirt: bool,
        value: Union[int, Instruction, None],
    ):
        array_info = ssa_table.get(designator.id.value)
        assert type(array_info) is tuple
        base_addr, total_idxs = array_info
        assert len(designator.idx_list) == len(total_idxs)
        l, base = cse_table.lookup_return(Add(x="FP", y=base_addr))

        # TODO Copy propagation
        x, y = None, None
        for i, expression in enumerate(designator.idx_list):
            list1, result = self.operate_expression(ssa_table, cse_table, expression)
            element_size = math.prod(total_idxs[i + 1 :])
            list2, x = cse_table.lookup_return(Mul(result, element_size))

            l += list1
            l += list2

            if i > 0:
                assert x is not None and y is not None
                list3, x = cse_table.lookup_return(Add(x=y, y=x))
                l += list3
            y = x

        assert isinstance(x, Instruction)
        # TODO implement instruction set(Adda, Load, Store)
        list1, addr = cse_table.lookup_return(Adda(x=base, y=x))
        if factor_inheirt:
            list2, ld = cse_table.lookup_return(Load(y=addr))
        else:
            assert value is not None
            list2, ld = cse_table.lookup_return(Store(x=addr, y=value))

        assert isinstance(ld, Instruction)

        l += list1
        l += list2
        return l, ld

    def operate_assignment(
        self, ssa_table: SSATable, cse_table: CSETable, assignment: parser.Assignment
    ) -> list[BasicBlock]:
        list1, result1 = self.operate_expression(
            ssa_table, cse_table, assignment.expression
        )
        list2, _ = self.operate_designator(
            ssa_table, cse_table, assignment.designator, result1
        )

        start = BasicBlock(list1 + list2, [], ssa_table.copy(), cse_table.copy())

        return [start]

    def operate_func_call(
        self,
        ssa_table: SSATable,
        cse_table: CSETable,
        func_call: parser.FuncCall,
        is_factor: bool,
    ) -> tuple[Union[list[BasicBlock], list[InstElement]], Union[Instruction, None]]:
        if func_call.factor_inheirt:
            assert is_factor
            inst_list_result: list[InstElement] = []
            arguments: list[Union[Instruction, int]] = []
            for expression in func_call.arg_list:
                inst_list, result = self.operate_expression(
                    ssa_table, cse_table, expression
                )
                inst_list_result += inst_list
                arguments.append(result)
            call_inst = Call(call_id=func_call.id.value, call_arg=arguments)
            inst_list_result.append(call_inst)

            return inst_list_result, call_inst
        elif func_call.statement_inherit:
            assert not is_factor
            inst_list_result: list[InstElement] = []
            arguments: list[Union[Instruction, int]] = []
            for expression in func_call.arg_list:
                inst_list, result = self.operate_expression(
                    ssa_table, cse_table, expression
                )
                inst_list_result += inst_list
                arguments.append(result)
            call_inst = Call(call_id=func_call.id.value, call_arg=arguments)
            inst_list_result.append(call_inst)

            return (
                [
                    BasicBlock(
                        inst_list_result,
                        [],
                        ssa_table.copy(),
                        cse_table.copy(),
                    )
                ],
                None,
            )
        else:
            raise ValueError

    def operate_relation(
        self,
        ssa_table: SSATable,
        cse_table: CSETable,
        relation: parser.Relation,
        is_while: bool = False,
    ) -> tuple[BasicBlock, Instruction]:
        list1, result1 = self.operate_expression(ssa_table, cse_table, relation.left)
        list2, result2 = self.operate_expression(ssa_table, cse_table, relation.right)
        list3, cmp = cse_table.lookup_return(Cmp(x=result1, y=result2))

        if type(relation.rel_op) is parser.Eq:
            if is_while:
                branch_inst = Bne(x=cmp)
            else:
                branch_inst = Beq(x=cmp)
        elif type(relation.rel_op) is parser.Neq:
            if is_while:
                branch_inst = Beq(x=cmp)
            else:
                branch_inst = Bne(x=cmp)
        elif type(relation.rel_op) is parser.G:
            if is_while:
                branch_inst = Ble(x=cmp)
            else:
                branch_inst = Bgt(x=cmp)
        elif type(relation.rel_op) is parser.Ge:
            if is_while:
                branch_inst = Blt(x=cmp)
            else:
                branch_inst = Bge(x=cmp)
        elif type(relation.rel_op) is parser.L:
            if is_while:
                branch_inst = Bge(x=cmp)
            else:
                branch_inst = Blt(x=cmp)
        elif type(relation.rel_op) is parser.Le:
            if is_while:
                branch_inst = Bgt(x=cmp)
            else:
                branch_inst = Ble(x=cmp)
        else:
            raise ValueError

        return (
            BasicBlock(list1 + list2 + list3 + [branch_inst], [], ssa_table, cse_table),
            branch_inst,
        )

    def generate_phi(
        self, ssa_table0: SSATable, ssa_table1: SSATable, ssa_table2: SSATable
    ) -> list[InstElement]:
        assert (
            ssa_table1.table.keys()
            == ssa_table2.table.keys()
            == ssa_table0.table.keys()
        )
        phi_list: list[InstElement] = []
        for key in ssa_table0.table.keys():
            left = ssa_table1.get(key)
            right = ssa_table2.get(key)
            if left != right:
                # Array and params cannot be resolved with phi
                # Support mutable paramter
                assert type(left) is not tuple  # and type(left) is not Offset
                assert type(right) is not tuple  # and type(right) is not Offset

                phi_inst = Phi(left=left, right=right)
                ssa_table0.update(key, phi_inst)
                phi_list.append(phi_inst)

        return phi_list

    def operate_if_statement(
        self, ssa_table: SSATable, cse_table: CSETable, if_statement: parser.IfStatement
    ) -> list[BasicBlock]:
        joint_block = BasicBlock()
        cond_bb, cond_bra = self.operate_relation(
            ssa_table, cse_table, if_statement.relation
        )

        ssa_table1 = ssa_table.copy()
        cse_table1 = cse_table.copy()
        ssa_table2 = ssa_table.copy()
        cse_table2 = cse_table.copy()
        then_bb_list = self.operate_state_sequence(
            ssa_table1, cse_table1, if_statement.then_block
        )
        then_bb_head, then_bb_tail = then_bb_list[0], then_bb_list[-1]

        if if_statement.else_block:
            else_bb_list = self.operate_state_sequence(
                ssa_table2, cse_table2, if_statement.else_block
            )
            else_bb_head, else_bb_tail = else_bb_list[0], else_bb_list[-1]
        else:
            else_bb_head = BasicBlock(ssa_table=ssa_table2, cse_table=cse_table2)
            else_bb_tail = else_bb_head
            else_bb_list = [else_bb_head]

        phi_list = self.generate_phi(ssa_table, ssa_table1, ssa_table2)
        if cse_table1.kill or cse_table2.kill:
            cse_table.kill_load()
        joint_block.instructions += phi_list

        # Branch condition to then_bb
        if not then_bb_head.instructions:
            then_bb_head.instructions.append(Nop())
        first_inst_then = then_bb_head.instructions[0]
        if isinstance(first_inst_then, Instruction):
            cond_bra.y = first_inst_then
        elif isinstance(first_inst_then, InstructionSet):
            cond_bra.y = first_inst_then.instructions[0]
        else:
            raise ValueError

        # Branch else to joint
        if not joint_block.instructions:
            joint_block.instructions.append(Nop())
        first_inst_joint = joint_block.instructions[0]
        assert isinstance(first_inst_joint, Instruction)
        branch_inst = Bra(y=first_inst_joint)
        else_bb_tail.instructions.append(branch_inst)

        # Link BBs
        cond_bb.nexts.append(else_bb_head)
        cond_bb.nexts.append(then_bb_head)
        then_bb_tail.nexts.append(joint_block)
        else_bb_tail.nexts.append(joint_block)
        joint_block.name = "join-if"
        joint_block.cond_bb = cond_bb
        cond_bb.doms.append(then_bb_head)
        cond_bb.doms.append(else_bb_head)
        cond_bb.doms.append(joint_block)

        else_bb_head.prevs.append(cond_bb)
        then_bb_head.prevs.append(cond_bb)
        joint_block.prevs.append(then_bb_tail)
        joint_block.prevs.append(else_bb_tail)

        return [cond_bb] + else_bb_list + then_bb_list + [joint_block]

    def update_right_side_phi(
        self, ssa_table3: SSATable, ssa_table2: SSATable
    ) -> list[Phi]:
        assert ssa_table3.table.keys() == ssa_table2.table.keys()

        additional_phi: list[Phi] = []
        for key in ssa_table3.table.keys():
            left = ssa_table3.get(key)
            right = ssa_table2.get(key)
            if left != right:
                assert type(left) is not tuple and type(left) is not Offset
                assert type(right) is not tuple and type(right) is not Offset

                if type(right) is Phi:
                    right.right = left
                else:
                    # There can be the case where the modificaiton of value appear behind (refer to while_double_cse example)
                    additional_phi.append(Phi(left=right, right=left))
                    ssa_table2.update(key, additional_phi[-1])

        return additional_phi

    def operate_while_statment(
        self,
        ssa_table: SSATable,
        cse_table: CSETable,
        while_statement: parser.WhileStatement,
    ) -> list[BasicBlock]:
        # joint_bb, cond_bra = self.operate_relation(ssa_table, copy.deepcopy(cse_table), while_statement.relation)
        ssa_table1 = ssa_table.copy()
        cse_table1 = cse_table.copy()

        _ = self.operate_state_sequence(
            ssa_table1, cse_table1, while_statement.do_block
        )

        # First generate phi function
        phi_list = self.generate_phi(ssa_table, ssa_table, ssa_table1)
        ssa_table2 = ssa_table

        # Update identifier in relation block(joint block) with the generated phi function
        new_joint_bb, new_cond_bra = self.operate_relation(
            ssa_table2, cse_table, while_statement.relation, True
        )

        ssa_table3 = ssa_table2.copy()
        cse_table2 = cse_table.copy()

        # Update identifier in do block with the generated phi function.
        # However, in this case right side of the generated phi function become invalid.
        # Therefore, we need to update the right side of phi function with the newly generated do block instructions.
        # Those instructions can be found from updated ssa_table3
        new_do_bb_list = self.operate_state_sequence(
            ssa_table3, cse_table2, while_statement.do_block
        )
        new_do_bb_head, new_do_bb_tail = new_do_bb_list[0], new_do_bb_list[-1]

        if cse_table2.kill:
            cse_table2.kill_load()

        # Instead we generate new set of phi funcitons, we fill the right side of phi functions in ssa_table2
        additional_phi = self.update_right_side_phi(ssa_table3, ssa_table2)

        new_joint_bb.instructions = (
            additional_phi + phi_list + new_joint_bb.instructions
        )

        if not new_joint_bb.instructions:
            new_joint_bb.instructions.append(Nop())
        first_inst_joint: InstElement = new_joint_bb.instructions[0]
        assert isinstance(first_inst_joint, Instruction)
        loopback_bra_inst = Bra(y=first_inst_joint)
        new_do_bb_tail.instructions.append(loopback_bra_inst)

        follow_block = BasicBlock(
            instructions=[Nop()],
            ssa_table=ssa_table.copy(),
            cse_table=cse_table.copy(),
        )
        new_cond_bra.y = follow_block.instructions[0]

        # Link BBs
        new_joint_bb.nexts.append(new_do_bb_head)
        new_joint_bb.nexts.append(follow_block)
        new_do_bb_tail.nexts.append(new_joint_bb)
        new_joint_bb.name = "join-while"
        new_joint_bb.doms.append(new_do_bb_head)
        new_joint_bb.doms.append(follow_block)

        new_do_bb_head.prevs.append(new_joint_bb)
        follow_block.prevs.append(new_joint_bb)
        new_joint_bb.prevs.append(new_do_bb_tail)

        return [new_joint_bb] + new_do_bb_list + [follow_block]

    def operate_return_statement(
        self,
        ssa_table: SSATable,
        cse_table: CSETable,
        return_statement: parser.ReturnStatement,
    ) -> list[BasicBlock]:
        return_bb = BasicBlock(ssa_table=ssa_table.copy(), cse_table=cse_table.copy())

        if return_statement.value:
            inst_list, result = self.operate_expression(
                ssa_table, cse_table, return_statement.value
            )
            return_bb.instructions += inst_list
            return_bb.instructions.append(Return(result))
        else:
            return_bb.instructions.append(Return())

        return [return_bb]

    def operate_state_sequence(
        self,
        ssa_table: SSATable,
        cse_table: CSETable,
        state_sequence: list[parser.Statement],
    ) -> list[BasicBlock]:
        head_basic_block: BasicBlock = BasicBlock(
            ssa_table=ssa_table.copy(), cse_table=cse_table.copy()
        )
        bb_list: list[BasicBlock] = [head_basic_block]

        for statement in state_sequence:
            if type(statement) is parser.Assignment:
                bbs = self.operate_assignment(ssa_table, cse_table, statement)
            elif type(statement) is parser.FuncCall:
                (bbs, result) = self.operate_func_call(
                    ssa_table, cse_table, statement, False
                )
                assert result is None
                assert type(bbs) is list
            elif type(statement) is parser.IfStatement:
                bbs = self.operate_if_statement(ssa_table, cse_table, statement)
            elif type(statement) is parser.WhileStatement:
                bbs = self.operate_while_statment(ssa_table, cse_table, statement)
            elif type(statement) is parser.ReturnStatement:
                bbs = self.operate_return_statement(ssa_table, cse_table, statement)
            else:
                raise ValueError

            assert type(bbs[0]) is BasicBlock
            assert type(bbs) is list

            bbs[0].prevs.append(bb_list[-1])
            bb_list[-1].nexts.append(bbs[0])
            bb_list += bbs

        return bb_list

    def operate_func_body(
        self, func_body: parser.FuncBody, ssa_table: SSATable
    ) -> list[BasicBlock]:
        ssa_table = self.operate_var_decl(func_body.var_decl, ssa_table)
        return self.operate_state_sequence(
            ssa_table, CSETable(), func_body.state_sequence
        )

    def operate_func_decl(
        self, func_decls: list[parser.FuncDecl]
    ) -> list[tuple[str, list[BasicBlock]]]:
        basic_block_list: list[tuple[str, list[BasicBlock]]] = []
        for func_decl in func_decls:
            id = func_decl.id.value
            ssa_table = self.operate_formal_param(func_decl.formal_param)
            bb_list = self.operate_func_body(func_decl.func_body, ssa_table)
            basic_block_list.append((id, bb_list))

        return basic_block_list

    def operate_computation(
        self,
        var_decls: list[parser.VarDecl],
        func_decls: list[parser.FuncDecl],
        state_sequence: list[parser.Statement],
    ) -> list[tuple[str, list[BasicBlock]]]:
        ssa_table = self.operate_var_decl(var_decls)
        func_list = self.operate_func_decl(func_decls)

        main_bb_list = self.operate_state_sequence(
            ssa_table, CSETable(), state_sequence
        )

        func_list.append(("main", main_bb_list))
        func_list.reverse()

        return func_list

    def generate_IR(self) -> list[tuple[str, list[BasicBlock]]]:
        ast: parser.Computation = self.generate_AST()
        return self.operate_computation(ast.var_decl, ast.func_decl, ast.state_sequence)
