# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 28/12/2023                                              *
# * @description: fonctions evalInst et evalExpr                   *
# ******************************************************************


env = {}

#stockage pour les fonctions
functions = {}


#--------------------------------------------pour évaluer des variables----------------------------------------------------------------------------------#
def eval_variable(t, env):
    if t == "True":
        return True
    elif t == "False":
        return False
    return env.get(t, 0)

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

    #debut d'un nouveau bloc d'instructions
    if instruction_type == "start":
        evalInst(args[0], env)

    #assignations d'une valeur a une variable
    elif instruction_type == "=":
        var_name, var_expr = args
        env[var_name] = evalExpr(var_expr, env)
        print(f"- Variable '{var_name}' updated to: {env[var_name]}")

    #bloc d'instructions
    elif instruction_type == "node":
        for inst in args:
            evalInst(inst, env)

    elif instruction_type == "print":
        if not isinstance(args, list):
            args = [args]
        results = []
        for expr in args:
            if isinstance(expr, str):
                #on verifie si expr = id de variable ou une chaine
                if expr in env:
                    #si id on l'évalue pour avoir sa valeur
                    evaluated_expr = evalExpr(expr, env)
                    results.append(evaluated_expr)
                else:
                    #sinon on le traite comme chaine de caractères
                    results.append(expr.strip('"'))
            elif isinstance(expr, tuple):
                #si tuple on évalue expression
                evaluated_expr = evalExpr(expr, env)
                results.append(evaluated_expr)
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
            func_info = functions[func_name]
            params = func_info["params"]
            func_body = func_info["body"]
            return_expr = func_info.get("return")
            if len(params) == len(call_args):
                func_env = {param: evalExpr(arg, env) for param, arg in zip(params, call_args)} if call_args else {}
                evalInst(func_body, func_env)
                if return_expr:
                    return_value = evalExpr(return_expr, func_env)  # Use func_env here
                    print(f"- Function '{func_name}' returned: {return_value}")
                    return return_value
            else:
                print("Error: Number of arguments does not match number of function parameters '{}'. Expected: {}, Received: {}.".format(func_name, len(params), len(call_args)))
    else:
        print("ERROR_EvalInst : Unexpected instruction type:", instruction_type)
