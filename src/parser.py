import lexer
from typing import Type, Union


class Statement:
    def __init__(self, statement_inheirt: bool = False) -> None:
        self.statement_inherit = statement_inheirt


class Factor:
    def __init__(self, factor_inheirt: bool = False) -> None:
        self.factor_inheirt = factor_inheirt


class Number(Factor):
    def __init__(self, value: int, factor_inheirt: bool = False) -> None:
        super().__init__(factor_inheirt)
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Op:
    pass


class Plus(Op):
    def __str__(self) -> str:
        return "+"


class Minus(Op):
    def __str__(self) -> str:
        return "-"


class Mul(Op):
    def __str__(self) -> str:
        return "*"


class Div(Op):
    def __str__(self) -> str:
        return "/"


class Term:
    def __init__(self, factors: list[Factor], ops: list[Op]) -> None:
        assert len(factors) == len(ops) + 1
        self.factors = factors
        self.ops = ops

    def __str__(self) -> str:
        return_string = ""
        return_string += str(self.factors[0])

        for factor, op in zip(self.factors[1:], self.ops):
            return_string += str(op)
            return_string += str(factor)

        return return_string


class Expression(Factor):
    def __init__(
        self, terms: list[Term], ops: list[Op], factor_inheirt: bool = False
    ) -> None:
        super().__init__(factor_inheirt)
        assert len(terms) == len(ops) + 1
        self.terms = terms
        self.ops = ops

    def __str__(self) -> str:
        result_string = ""
        result_string += str(self.terms[0])

        for term, op in zip(self.terms[1:], self.ops):
            result_string += str(op)
            result_string += str(term)

        return result_string


class Identifier(Factor):
    def __init__(self, value: str, factor_inheirt: bool = False) -> None:
        super().__init__(factor_inheirt)
        self.value = value

    def __str__(self) -> str:
        return self.value


class FuncCall(Factor, Statement):
    def __init__(
        self,
        id: Identifier,
        arg_list: list[Expression],
        factor_inheirt: bool = False,
        statement_inheirt: bool = False,
    ) -> None:
        assert factor_inheirt or statement_inheirt
        Factor.__init__(self, factor_inheirt)
        Statement.__init__(self, statement_inheirt)
        self.id = id
        self.arg_list = arg_list

    def __str__(self) -> str:
        return f'call {str(self.id)}({", ".join([str(x) for x in self.arg_list])})'


class Designator(Factor):
    def __init__(
        self, id: Identifier, idx_list: list[Expression], factor_inheirt: bool = False
    ) -> None:
        super().__init__(factor_inheirt)
        self.id = id
        self.idx_list = idx_list

    def __str__(self) -> str:
        result_string = str(self.id)
        for idx in self.idx_list:
            result_string += "["
            result_string += str(idx)
            result_string += "]"

        return result_string


class Assignment(Statement):
    def __init__(
        self,
        designator: Designator,
        expression: Expression,
        statement_inheirt: bool = False,
    ) -> None:
        super().__init__(statement_inheirt)
        self.designator = designator
        self.expression = expression

    def __str__(self) -> str:
        return str(self.designator) + " <- " + str(self.expression)


class RelOp:
    pass


class Eq(RelOp):
    def __str__(self) -> str:
        return "=="


class Neq(RelOp):
    def __str__(self) -> str:
        return "!="


class G(RelOp):
    def __str__(self) -> str:
        return ">"


class Ge(RelOp):
    def __str__(self) -> str:
        return ">="


class L(RelOp):
    def __str__(self) -> str:
        return "<"


class Le(RelOp):
    def __str__(self) -> str:
        return "<="


class Relation:
    def __init__(
        self, left: Expression = None, rel_op: RelOp = None, right: Expression = None  # type: ignore
    ) -> None:
        super().__init__()
        self.left = left
        self.rel_op = rel_op
        self.right = right

    def __str__(self) -> str:
        return str(self.left) + str(self.rel_op) + str(self.right)


class IfStatement(Statement):
    def __init__(
        self,
        relation: Relation,
        then_block: list[Statement],
        else_block: list[Statement],
        statement_inheirt: bool = False,
    ) -> None:
        super().__init__(statement_inheirt)
        self.relation = relation
        self.then_block = then_block
        self.else_block = else_block

    def __str__(self) -> str:
        string_dict = {}
        string_dict["relation"] = str(self.relation)
        string_dict["then"] = [str(x) for x in self.then_block]
        string_dict["else"] = [str(x) for x in self.else_block]

        return "IfStatement " + str(string_dict)


class WhileStatement(Statement):
    def __init__(
        self,
        relation: Relation,
        do_block: list[Statement],
        statement_inheirt: bool = False,
    ) -> None:
        super().__init__(statement_inheirt)
        self.relation = relation
        self.do_block = do_block

    def __str__(self) -> str:
        string_dict = {}
        string_dict["relation"] = str(self.relation)
        string_dict["do"] = [str(x) for x in self.do_block]

        return "WhileStatement " + str(string_dict)


class ReturnStatement(Statement):
    def __init__(
        self, value: Union[None, Expression], statement_inheirt: bool = False
    ) -> None:
        super().__init__(statement_inheirt)
        self.value = value

    def __str__(self) -> str:
        return "Return " + str(self.value)


class TrueCondition(Relation):
    def __str__(self) -> str:
        return "True"


class FalseCondition(Relation):
    def __str__(self) -> str:
        return "False"


class TypeDecl:
    pass


class VarDecl:
    def __init__(self, type_decl: TypeDecl, id: Identifier) -> None:
        self.type_decl = type_decl
        self.id = id

    def __str__(self) -> str:
        return str(self.type_decl) + " " + str(self.id)


class FuncBody:
    def __init__(
        self, var_decl: list[VarDecl], state_sequence: list[Statement]
    ) -> None:
        self.var_decl = var_decl
        self.state_sequence = state_sequence

    def __str__(self) -> str:
        string_dict = {}
        string_dict["var_decl"] = [str(x) for x in self.var_decl]
        string_dict["state_sequence"] = [str(x) for x in self.state_sequence]

        return "FuncBody " + str(string_dict)


class FuncDecl:
    def __init__(
        self,
        id: Identifier,
        formal_param: list[Identifier],
        func_body: FuncBody,
        void: bool = False,
    ) -> None:
        self.void = void
        self.id = id
        self.formal_param = formal_param
        self.func_body = func_body

    def __str__(self) -> str:
        string_dict = {}
        string_dict["identifier"] = str(self.id)
        string_dict["formal_param"] = [str(x) for x in self.formal_param]
        string_dict["function_body"] = str(self.func_body)

        if self.void:
            return "void function " + str(string_dict)
        else:
            return "function " + str(string_dict)


class Array(TypeDecl):
    def __init__(self, idx_list: list[int]) -> None:
        super().__init__()
        self.idx_list = idx_list

    def __str__(self) -> str:
        result_string = ""
        for idx in self.idx_list:
            result_string += "["
            result_string += str(idx)
            result_string += "]"

        return "Array" + result_string


class Var(TypeDecl):
    def __str__(self) -> str:
        return "Var"


class Computation:
    def __init__(
        self,
        var_decl: list[VarDecl],
        func_decl: list[FuncDecl],
        state_sequence: list[Statement],
    ) -> None:
        self.var_decl = var_decl
        self.func_decl = func_decl
        self.state_sequence = state_sequence

    def __str__(self) -> str:
        string_dict = {}
        string_dict["var_decl"] = [str(x) for x in self.var_decl]
        string_dict["func_decl"] = [str(x) for x in self.func_decl]
        string_dict["state_sequence"] = [str(x) for x in self.state_sequence]

        return "main " + str(string_dict)


class Parser(lexer.Lexer):
    def __init__(self, filename: str) -> None:
        super().__init__(filename)
        self.token_list = self.tokenization()
        self.current_idx = 0

    def current_cursor(self) -> list[str]:
        return [
            str(x) for x in self.token_list[self.current_idx - 2 : self.current_idx + 2]
        ]

    def next(self) -> lexer.Token:
        if self.current_idx >= len(self.token_list):
            raise ValueError("No more token")

        token = self.token_list[self.current_idx]
        self.current_idx += 1

        return token

    def previous(self) -> lexer.Token:
        if self.current_idx <= 0:
            raise ValueError("No previous token")

        self.current_idx -= 1

        return self.token_list[self.current_idx]

    def generate_AST(self) -> Computation:
        def parse_var_decls() -> list[VarDecl]:
            var_decl_list: list[VarDecl] = []
            while True:
                fisrt_token = self.next()
                if isinstance(fisrt_token, lexer.Var):
                    while True:
                        identifier = self.next()
                        assert isinstance(identifier, lexer.Identifier)
                        var_decl_list.append(
                            VarDecl(Var(), Identifier(identifier.value))
                        )

                        next_token = self.next()
                        if isinstance(next_token, lexer.Comma):
                            pass
                        elif isinstance(next_token, lexer.Semicolon):
                            break
                        else:
                            raise ValueError
                elif isinstance(fisrt_token, lexer.Array):
                    idx_list: list[int] = []
                    while True:
                        assert type(self.next()) == lexer.Left_bracket
                        number = self.next()
                        assert isinstance(number, lexer.Number)
                        assert isinstance(self.next(), lexer.Right_bracket)
                        idx_list.append(number.value)

                        next_token = self.next()
                        if not isinstance(next_token, lexer.Left_bracket):
                            self.previous()
                            break
                        self.previous()

                    while True:
                        identifier = self.next()
                        assert isinstance(identifier, lexer.Identifier)
                        var_decl_list.append(
                            VarDecl(Array(idx_list), Identifier(identifier.value))
                        )

                        next_token = self.next()
                        if isinstance(next_token, lexer.Comma):
                            pass
                        elif isinstance(next_token, lexer.Semicolon):
                            break
                        else:
                            raise ValueError
                else:
                    self.previous()
                    break

            return var_decl_list

        def parse_formal_param() -> list[Identifier]:
            assert isinstance(self.next(), lexer.Left_paren)

            param_list: list[Identifier] = []
            while True:
                next_token = self.next()
                if isinstance(next_token, lexer.Right_paren):
                    break
                elif isinstance(next_token, lexer.Comma):
                    next_token = self.next()

                assert isinstance(next_token, lexer.Identifier)
                param_list.append(Identifier(next_token.value))

            return param_list

        def parse_factor() -> Factor:
            first_token = self.next()
            if isinstance(first_token, lexer.Identifier):
                self.previous()
                return parse_designator(True)
            elif isinstance(first_token, lexer.Number):
                return Number(first_token.value, True)
            elif isinstance(first_token, lexer.Left_paren):
                exp = parse_expression()
                assert isinstance(self.next(), lexer.Right_paren)
                return exp
            elif isinstance(first_token, lexer.Call):
                return parse_func_call(True, False)
            else:
                raise ValueError("No match")

        def is_number(x: Union[Factor, Term]) -> bool:
            if type(x) is Expression:
                if len(x.terms) == 1:
                    return is_number(x.terms[0])
            elif type(x) is Term:
                if len(x.factors) == 1:
                    return is_number(x.factors[0])
            elif type(x) is Number:
                return True
            else:
                return False
            return False

        def get_number(x: Union[Factor, Term]) -> int:
            assert is_number(x)
            if type(x) is Expression:
                return get_number(x.terms[0])
            elif type(x) is Term:
                return get_number(x.factors[0])
            elif type(x) is Number:
                return x.value
            else:
                raise ValueError

        def parse_term() -> Term:
            factor_list: list[Factor] = []
            op_list: list[Op] = []

            factor_list.append(parse_factor())

            while True:
                op = self.next()
                if not isinstance(op, lexer.Mul) and not isinstance(op, lexer.Div):
                    self.previous()
                    break
                if type(op) is lexer.Mul:
                    op_list.append(Mul())
                elif type(op) is lexer.Div:
                    op_list.append(Div())
                else:
                    raise ValueError()

                factor_list.append(parse_factor())

            assert len(factor_list) == len(op_list) + 1

            # Copy propogation
            if all([is_number(x) for x in factor_list]):
                result = get_number(factor_list[0])
                for factor, op in zip(factor_list[1:], op_list):
                    value = get_number(factor)
                    if type(op) is Mul:
                        result *= value
                    elif type(op) is Div:
                        result /= value
                    else:
                        raise ValueError

                factor_list = [Number(int(result), True)]
                op_list = []

            return Term(factor_list, op_list)

        def parse_expression() -> Expression:
            term_list: list[Term] = []
            op_list: list[Op] = []

            term_list.append(parse_term())

            while True:
                op = self.next()
                if not isinstance(op, lexer.Plus) and not isinstance(op, lexer.Minus):
                    self.previous()
                    break
                if type(op) is lexer.Plus:
                    op_list.append(Plus())
                elif type(op) is lexer.Minus:
                    op_list.append(Minus())
                else:
                    raise ValueError()

                term_list.append(parse_term())

            # Copy propagation
            if all([is_number(x) for x in term_list]):
                result = get_number(term_list[0])
                for term, op in zip(term_list[1:], op_list):
                    value = get_number(term)
                    if type(op) is Plus:
                        result += value
                    elif type(op) is Minus:
                        result -= value
                    else:
                        raise ValueError

                term_list = [Term([Number(result, True)], [])]
                op_list = []

            return Expression(term_list, op_list)

        def parse_designator(factor_inherit: bool) -> Designator:
            identifier = self.next()
            assert isinstance(identifier, lexer.Identifier)
            identifier = Identifier(identifier.value)

            idx_list: list[Expression] = []
            if isinstance(self.next(), lexer.Left_bracket):
                self.previous()
                while isinstance(self.next(), lexer.Left_bracket):
                    expression = parse_expression()
                    idx_list.append(expression)
                    assert isinstance(self.next(), lexer.Right_bracket)
                self.previous()
                assert isinstance(self.previous(), lexer.Right_bracket)
                self.next()
            else:
                self.previous()

            return Designator(identifier, idx_list, factor_inherit)

        def parse_assignment(statement_inherit: bool) -> Assignment:
            designator = parse_designator(False)
            assert isinstance(self.next(), lexer.Assign)
            expression = parse_expression()

            return Assignment(designator, expression, statement_inherit)

        def parse_func_call(factor_inherit: bool, statement_inherit: bool) -> FuncCall:
            identifier = self.next()
            assert isinstance(identifier, lexer.Identifier)
            identifier = Identifier(identifier.value)

            # TODO Check if void function is properly used

            if isinstance(self.next(), lexer.Left_paren):
                expression_list: list[Expression] = []
                next_token = self.next()
                if isinstance(next_token, lexer.Right_paren):
                    return FuncCall(
                        identifier, expression_list, factor_inherit, statement_inherit
                    )
                else:
                    self.previous()
                    while True:
                        expression_list.append(parse_expression())
                        if not isinstance(self.next(), lexer.Comma):
                            break
                    return FuncCall(
                        identifier, expression_list, factor_inherit, statement_inherit
                    )
            else:
                self.previous()
                return FuncCall(identifier, [], factor_inherit, statement_inherit)

        def parse_relation() -> Relation:
            exp1 = parse_expression()
            relop = self.next()

            assert isinstance(relop, lexer.Relation)
            if isinstance(relop, lexer.Eq):
                relop = Eq()
            elif isinstance(relop, lexer.Neq):
                relop = Neq()
            elif isinstance(relop, lexer.L):
                relop = L()
            elif isinstance(relop, lexer.Le):
                relop = Le()
            elif isinstance(relop, lexer.G):
                relop = G()
            elif isinstance(relop, lexer.Ge):
                relop = Ge()
            else:
                raise ValueError
            exp2 = parse_expression()

            # Copy propagation
            if is_number(exp1) and is_number(exp2):
                value1 = get_number(exp1)
                value2 = get_number(exp2)
                if type(relop) is Eq:
                    result = value1 == value2
                elif type(relop) is Neq:
                    result = value1 != value2
                elif type(relop) is L:
                    result = value1 < value2
                elif type(relop) is Le:
                    result = value1 <= value2
                elif type(relop) is G:
                    result = value1 > value2
                elif type(relop) is Ge:
                    result = value1 >= value2
                else:
                    raise ValueError

                if result:
                    return TrueCondition()
                else:
                    return FalseCondition()

            return Relation(exp1, relop, exp2)

        def parse_statement() -> list[Statement]:
            first_token = self.next()
            if isinstance(first_token, lexer.Let):
                return [parse_assignment(True)]
            elif isinstance(first_token, lexer.Call):
                # Assert the function is void
                return [parse_func_call(False, True)]
            elif isinstance(first_token, lexer.If):
                # Dead code elimination
                statement = parse_if_statement(True)
                if type(statement.relation) is TrueCondition:
                    return statement.then_block
                elif type(statement.relation) is FalseCondition:
                    return statement.else_block
                else:
                    return [statement]
            elif isinstance(first_token, lexer.While):
                # Dead code elimination
                statement = parse_while_statement(True)
                if type(statement.relation) is TrueCondition:
                    raise ValueError("Infinite loop")
                elif type(statement.relation) is FalseCondition:
                    return []
                else:
                    return [statement]
            elif isinstance(first_token, lexer.Return):
                return [parse_return_statement(True)]
            else:
                raise ValueError

        def parse_state_sequence(
            end_token_class: list[Type[lexer.Token]],
        ) -> list[Statement]:
            statement_list: list[Statement] = []
            next_token = self.next()
            if not any(
                [isinstance(next_token, end_token) for end_token in end_token_class]
            ):
                self.previous()
                while True:
                    statement_list += parse_statement()

                    next_token = self.next()

                    if isinstance(next_token, lexer.Semicolon):
                        next_token = self.next()

                        if any(
                            [
                                isinstance(next_token, end_token)
                                for end_token in end_token_class
                            ]
                        ):
                            break
                        else:
                            self.previous()
                    elif any(
                        [
                            isinstance(next_token, end_token)
                            for end_token in end_token_class
                        ]
                    ):
                        break
                    else:
                        raise ValueError()

            return statement_list

        def parse_if_statement(statement_inheirt: bool) -> IfStatement:
            relation = parse_relation()

            assert isinstance(self.next(), lexer.Then)

            state_sequence1 = parse_state_sequence([lexer.Else, lexer.Fi])
            prev_token = self.previous()

            self.next()
            if isinstance(prev_token, lexer.Else):
                state_sequence2 = parse_state_sequence([lexer.Fi])
            else:
                state_sequence2 = []

            return IfStatement(
                relation, state_sequence1, state_sequence2, statement_inheirt
            )

        def parse_while_statement(statement_inherit: bool) -> WhileStatement:
            relation = parse_relation()

            assert isinstance(self.next(), lexer.Do)

            state_sequence = parse_state_sequence([lexer.Od])

            return WhileStatement(relation, state_sequence, statement_inherit)

        def parse_return_statement(statement_inherit: bool) -> ReturnStatement:
            next_token = self.next()
            # Check all end tokens since we don't know where the return statement is located
            if (
                isinstance(next_token, lexer.Semicolon)
                or isinstance(next_token, lexer.Right_brace)
                or isinstance(next_token, lexer.Else)
                or isinstance(next_token, lexer.Fi)
                or isinstance(next_token, lexer.Od)
            ):
                self.previous()
                return ReturnStatement(None, statement_inherit)
            else:
                self.previous()
                return ReturnStatement(parse_expression(), statement_inherit)

        def parse_func_body() -> FuncBody:
            var_decl_list = parse_var_decls()
            assert isinstance(self.next(), lexer.Left_brace)
            state_sequence = parse_state_sequence([lexer.Right_brace])

            return FuncBody(var_decl_list, state_sequence)

        def parse_func_decls() -> list[FuncDecl]:
            func_decl_list: list[FuncDecl] = []
            while True:
                first_token = self.next()
                if isinstance(first_token, lexer.Void):
                    assert isinstance(self.next(), lexer.Function)
                    void = True
                elif isinstance(first_token, lexer.Function):
                    void = False
                else:
                    self.previous()
                    break

                identifier = self.next()
                assert isinstance(identifier, lexer.Identifier)

                formal_param = parse_formal_param()

                assert isinstance(self.next(), lexer.Semicolon)

                func_body = parse_func_body()

                assert isinstance(self.next(), lexer.Semicolon)

                func_decl_list.append(
                    FuncDecl(
                        Identifier(identifier.value), formal_param, func_body, void
                    )
                )

            return func_decl_list

        def parse_computation() -> Computation:
            assert isinstance(self.next(), lexer.Main)

            var_decl_list = parse_var_decls()
            func_decl_list = parse_func_decls()
            assert isinstance(self.next(), lexer.Left_brace)
            state_sequence = parse_state_sequence([lexer.Right_brace])
            assert isinstance(self.next(), lexer.Dot)

            return Computation(var_decl_list, func_decl_list, state_sequence)

        return parse_computation()
