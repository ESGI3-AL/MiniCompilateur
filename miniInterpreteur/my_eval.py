# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 28/12/2023                                              *
# * @description: fonctions evalInst et evalExpr                   *
# ******************************************************************


execution_stack = []

env = {}

functions = {}

#--------ajouter un scope de variable pour les fonctions-------------------#
def add_scope(env):
    return {**env}

#-------pour executer une fonction-------------------------------------------#
def execute_function(func_name, call_args):
    global env
    if func_name in functions:
        func_info = functions[func_name]
        params = func_info["params"]
        func_body = func_info["body"]
        return_expr = func_info.get("return")

        if len(params) == len(call_args):
            func_env = add_scope(env)  # Create a new local environment
            for param, arg in zip(params, call_args):
                func_env[param] = evalExpr(arg, env)
            execution_stack.append(func_name)  # Add to execution stack

            print("Before function execution:")
            print("Execution stack:", execution_stack)
            print("Environment:", func_env)

            evalInst(func_body, func_env)
            execution_stack.pop()  # Remove from execution stack

            print("After function execution:")
            print("Execution stack:", execution_stack)
            print("Environment:", func_env)

            if return_expr:
                return_value = evalExpr(return_expr, func_env)
                return return_value
        else:
            print("Error: Number of arguments does not match number of function parameters '{}'. Expected: {}, Received: {}.".format(func_name, len(params), len(call_args)))


#--------------------------------------------pour évaluer des variables----------------------------------------------------------------------------------#
def eval_variable(t, env):
    if t == "True":
        return True
    elif t == "False":
        return False
    elif t in env:
        return env[t]
    elif isinstance(t, str):
        return t
    else:
        return 0

#--------------------------------------------pour évaluer des littéraux----------------------------------------------------------------------------------#
def eval_literal(t):
    return t

#--------------------------------------------pour évaluer des opérateurs----------------------------------------------------------------------------------#
def eval_arithmetic_operator(operator, left_operand, right_operand):
    if operator == '+':
        return left_operand + right_operand
    elif operator == '-':
        return left_operand - right_operand
    elif operator == '*':
        return left_operand * right_operand
    elif operator == '/':
        return left_operand / right_operand

#--------------------------------------------pour évaluer des opérateurs logiques----------------------------------------------------------------------------------#
def eval_logical_operator(operator, left_operand, right_operand):
    if operator == 'AND':
        return left_operand and right_operand
    elif operator == 'OR':
        return left_operand or right_operand
    elif operator == '==':
        return left_operand == right_operand
    elif operator == '<':
        return left_operand < right_operand
    elif operator == '>':
        return left_operand > right_operand
    elif operator == '<=':
        return left_operand <= right_operand
    elif operator == '>=':
        return left_operand >= right_operand
    elif operator == '!=':
        return left_operand != right_operand

#--------------------------------------------pour évaluer des expressions----------------------------------------------------------------------------------#    
def evalExpr(t, env):
    print("- EvalExpr of", t)

    if not isinstance(t, tuple):
        return eval_variable(t, env) if isinstance(t, str) else eval_literal(t)

    operator = t[0]
    if operator in ['+', '-', '*', '/', 'AND', 'OR', '==', '<', '>', '<=', '>=', '!=']:
        left_operand = evalExpr(t[1], env)
        right_operand = evalExpr(t[2], env)

        if operator in ['+', '-', '*', '/']:
            return eval_arithmetic_operator(operator, left_operand, right_operand)
        else:
            return eval_logical_operator(operator, left_operand, right_operand)
    
    elif operator in ["+=", "-=", "*=", "/="] and isinstance(t[1], str):
        var_name = t[1]
        new_value = evalExpr(t[2], env)
        current_value = env.get(var_name, 0)

        if operator == "+=":
            env[var_name] = current_value + new_value
        elif operator == "-=":
            env[var_name] = current_value - new_value
        elif operator == "*=":
            env[var_name] = current_value * new_value
        elif operator == "/=":
            env[var_name] = current_value / new_value

        return env[var_name]
    
    elif operator == "return":
        return evalExpr(t[1], env)
    
    operator = t[0]
    if operator == 'array_access':
        array_name, index = t[1:]
        array = env.get(array_name, [])
        if 0 <= index < len(array):
            return array[index]
        else:
            print(f"Error: Array index out of range. Array '{array_name}' has size {len(array)}, but tried to access index {index}.")
            return "UNKNOWN"

    else:
        print("Unexpected expression structure or operator:", t)
        return "UNKNOWN"

#--------------------------------------------pour évaluer des instructions (assignation, boucles, conditions)----------------------------------------------------------------------------------#

def evalInst(t, env):
    if t == "empty":
        return

    #si pas un tuple alors error
    if type(t) != tuple:
        print("ERROR_EvalInst : Unexpected leaf node:", t)
        return

    instruction_type, *args = t

    if instruction_type == "start":
        evalInst(args[0], env)

        # accès à un élément d'un tableau
    elif instruction_type == "array_access":
        array_name, index = args
        array = env.get(array_name, [])
        if 0 <= index < len(array):
            value = array[index]
            print(f"- Accessed element at index {index} of array '{array_name}': {value}")
            return value
        else:
            print(f"Error: Array index out of range. Array '{array_name}' has size {len(array)}, but tried to access index {index}.")

    # assignations d'une valeur a une variable ou à un tableau
    elif instruction_type == "=":
        target, expr = args
        if isinstance(target, str):
            env[target] = evalExpr(expr, env)
            print(f"- Variable '{target}' updated to: {env[target]}")
        elif isinstance(target, tuple) and target[0] == "array_access":
            array_name, index = target[1:]
            array = env.get(array_name, [])
            if 0 <= index < len(array):
                array[index] = evalExpr(expr, env)
                env[array_name] = array
                print(f"- Array '{array_name}' updated at index {index} to: {array[index]}")
            else:
                print(f"Error: Array index out of range. Array '{array_name}' has size {len(array)}, but tried to assign to index {index}.")

    # création d'un tableau
    elif instruction_type == "array_declaration":
        array_name, size = args
        env[array_name] = [0] * size
        print(f"- Array '{array_name}' created with size {size}")

    elif instruction_type == "array_assignment":
        array_name, index, expr = args
        array = env.get(array_name, [])
        if 0 <= index < len(array):
            array[index] = evalExpr(expr, env)
            env[array_name] = array
            print(f"- Array '{array_name}' updated at index {index} to: {array[index]}")
        else:
            print(f"Error: Array index out of range. Array '{array_name}' has size {len(array)}, but tried to assign to index {index}.")

    elif instruction_type == "array":
        array_name, values = args
        env[array_name] = values
        print(f"- Array '{array_name}' created with values {values}")

    #bloc d'instructions
    elif instruction_type == "node":
        for inst in args:
            evalInst(inst, env)

    elif instruction_type == "print":
        if not isinstance(args, list):
            args = [args]
        results = []
        for expr in args:
            if isinstance(expr, tuple):
                if expr[0] == "array_access":
                    array_name, index = expr[1:]
                    array = env.get(array_name, [])
                    if 0 <= index < len(array):
                        value = array[index]
                        results.append(value)
                    else:
                        print(f"Error: Array index out of range. Array '{array_name}' has size {len(array)}, but tried to access index {index}.")
                else:
                    evaluated_expr = evalExpr(expr, env)
                    results.append(evaluated_expr)
            elif isinstance(expr, str):
                if expr in env:
                    evaluated_expr = evalExpr(expr, env)
                    results.append(evaluated_expr)
                else:
                    results.append(expr.strip('"'))
            else:
                results.append(expr)
        print("- CALC> ", ", ".join(map(str, results)))

    elif instruction_type == "printmultiple":
        results = []
        for expr in args[0]:
            if isinstance(expr, tuple):
                #si tuple on évalue expression
                evaluated_expr = evalExpr(expr, env)
                results.append(evaluated_expr)
            elif isinstance(expr, str):
                #si l'expression = chaîne, von verifie si variable ou chaine
                if expr in env:
                    #si = id, on évalue pour obtenir sa valeur
                    evaluated_expr = evalExpr(expr, env)
                    results.append(evaluated_expr)
                else:
                    #sinon chaine littérale
                    results.append(expr.strip('"'))
            else:
                #si d'autre type de donnée on l'ajoute directement au result 
                results.append(expr)
        print("- MULTIPLE CALC> ", ", ".join(map(str, results)))

    elif instruction_type == "printString":
        string_to_print = args[0]
        if isinstance(string_to_print, str):
            #id = evalue
            if string_to_print in env:
                evaluated_expr = evalExpr(string_to_print, env)
                print("- PRINTSTRING> " + str(evaluated_expr))
            else:
                #sinon print comme elle est
                print("- PRINTSTRING> " + string_to_print)

    elif instruction_type == "assign":
        var_name, var_expr = args
        env[var_name] = evalExpr(var_expr, env)
        print(f"- Variable '{var_name}' updated to: {env[var_name]}")

    elif instruction_type == "assign_op":
        var_name, operation, *expr = args
        if operation == "++":
            env[var_name] += 1
        elif operation == "--":
            env[var_name] -= 1
        elif operation in ["+=", "-=", "*=", "/="]:
            env[var_name] = evalExpr((operation[0], var_name, expr[0]), env)
        print(f"- Variable '{var_name}' updated to: {env[var_name]}")

    elif instruction_type in ["if", "if_else"]:
        condition = evalExpr(args[0], env)
        if_branch = args[1]
        else_branch = args[2] if len(args) > 2 else None

        if condition:
            evalInst(if_branch, env)
        elif else_branch:
            evalInst(else_branch, env)

    elif instruction_type == "while":
        while evalExpr(args[0], env):
            evalInst(args[1], env)

    elif instruction_type == "for":
        init, condition, update, body = args
        evalInst(init, env)
        while evalExpr(condition, env):
            evalInst(body, env)
            evalInst(update, env)

    elif instruction_type == "function":
        _, return_type, func_name, *func_body = t
        if return_type == "void":
            if len(func_body) == 2:  # function avec paramètres
                params, body = func_body
            else:  # function sans param
                params, body = [], func_body[0]
        elif return_type == "value":
            if len(func_body) == 3:  # function avec paramètres
                params, body, return_expr = func_body
            else:  # function sans param
                params, body, return_expr = [], func_body[0], func_body[1]
        else:
            print("ERROR_EvalInst : Unexpected function return type:", return_type)
            return
        functions[func_name] = {"params": params, "body": body, "return": return_expr if return_type == "value" else None}

    elif instruction_type == "call":
        func_name = args[0]
        call_args = args[1] if len(args) > 1 else []  # appel sans arguments
        if func_name in functions:
            return_value = execute_function(func_name, call_args)
            if return_value is not None:
                print(f"- Function '{func_name}' returned: {return_value}")
                return return_value
        else:
            print("ERROR_EvalInst : Unexpected instruction type:", instruction_type)