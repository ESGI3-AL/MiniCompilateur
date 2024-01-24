# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 28/12/2023                                              *
# * @description: fonctions evalInst et evalExpr                   *
# ******************************************************************


env = {}

#stockage pour les fonctions
functions = {}
    # Stocker les fonctions avec paramètres dans un dictionnaire
functions_with_params = {}

# Stocker les fonctions sans paramètres dans un dictionnaire séparé
functions_without_params = {}

def evalExpr(t, env):
    print("- EvalExpr of", t)

    #si expression n'est pas un tuple, elle est pas un opérateur
    if type(t) is not tuple:
        if isinstance(t, str):  #on gere les variables et les boolean
            if t == "True": return True
            elif t == "False": return False
            return env.get(t, 0)  # Retourne la valeur de la variable ou 0 si non trouvé
        return t  #Si pas variable alors c'est une valeur littérale (ex: nombre)

    #si tuple, elle possède un opérateur
    operator = t[0]
    #on  gère les opérateurs arithmétiques et logiques
    if operator in ['+', '-', '*', '/', 'AND', 'OR', '==', '<', '>', '<=', '>=', '!=']:
        left_operand = evalExpr(t[1], env)
        right_operand = evalExpr(t[2], env)

        if operator == '+': return left_operand + right_operand
        elif operator == '-': return left_operand - right_operand
        elif operator == '*': return left_operand * right_operand
        elif operator == '/': return left_operand / right_operand
        elif operator == 'AND': return left_operand and right_operand
        elif operator == 'OR': return left_operand or right_operand
        elif operator == '==': return left_operand == right_operand
        elif operator == '<': return left_operand < right_operand
        elif operator == '>': return left_operand > right_operand
        elif operator == '<=': return left_operand <= right_operand
        elif operator == '>=': return left_operand >= right_operand
        elif operator == '!=': return left_operand != right_operand

    # Gestion des opérations d'assignation composées
    elif operator in ["+=", "-=", "*=", "/="] and isinstance(t[1], str):
        var_name = t[1]
        new_value = evalExpr(t[2], env)
        if operator == "+=": env[var_name] = env.get(var_name, 0) + new_value
        elif operator == "-=": env[var_name] = env.get(var_name, 0) - new_value
        elif operator == "*=": env[var_name] = env.get(var_name, 0) * new_value
        elif operator == "/=": env[var_name] = env.get(var_name, 0) / new_value
        return env[var_name]

    else:
        print("Unexpected expression structure or operator:", t)
        return "UNKNOWN"


#pour évaluer des instructions (assignation, boucles, conditions)
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
        print("- CALC>", evalExpr(args[0], env))

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
        #on vérifie si la fonction a des paramètres
        if len(args) == 4:
            _, return_type, func_name, params, body = t
            if return_type == "void":
                functions_with_params[func_name] = {"params": params, "body": body}
        elif len(args) == 3:
            _, return_type, func_name, body = t
            if return_type == "void":
                functions_without_params[func_name] = {"body": body}

    elif instruction_type == "call":
        func_name, *call_args = args #args = le nom de la fonction
        if func_name in functions_with_params:
            func_info = functions_with_params[func_name]
            params = func_info.get("params",[])
            func_body = func_info["body"]
            if len(params) == len(call_args):
                func_env = {param: evalExpr(arg, env) for param, arg in zip(params, call_args)}
                evalInst(func_body, func_env)
                #print("Reussi : Le nombre d'arguments correspond au nombre de paramètres de la fonction '{}'. Attendu : {}, Reçu : {}.".format(func_name, len(params), len(call_args)))
            else:
                print("Error: Number of arguments does not match number of function parameters '{}'. we want : {}, we have : {}.".format(func_name, len(params), len(call_args)))
        elif func_name in functions_without_params:
            func_body = functions_without_params[func_name]["body"]
            evalInst(func_body, env)

    else:
        print("ERROR_EvalInst : Unexpected instruction type:", instruction_type)
