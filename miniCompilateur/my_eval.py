# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 14/01/2024                                              *
# * @description: fonctions evalInst et evalExpr                   *
# ******************************************************************

# dictionnaire vide pour stocker les variables gardés en mémoire
env = {}

def evalExpr(t, env):
    print("- evalExpr de", t)

    if type(t) is not tuple:
        if isinstance(t, str):  # C'est une variable ou un booléen
            if t == "True": return True
            elif t == "False": return False
            return env.get(t, 0)  # Retourne la valeur de la variable depuis env
        return t  # C'est une valeur littérale

    operator = t[0]
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


def evalInst(t, env):
    if t == "empty":
        return

    if type(t) != tuple:
        print("Warning_EvalInst : Unexpected leaf node:", t)
        return

    if t[0] == "start":
        evalInst(t[1], env)

    elif t[0] == "=":  # Pour les assignations
        var_name = t[1]
        var_value = evalExpr(t[2], env)
        env[var_name] = var_value
        print(f"- Variable '{var_name}' updated to: {env[var_name]}")  # Afficher la valeur mise à jour

    elif t[0] == "node":
        for inst in t[1:]:
            evalInst(inst, env)

    elif t[0] == "print":
        result = evalExpr(t[1], env)
        print("- CALC>", result)

    elif t[0] == "assign":
        env[t[1]] = evalExpr(t[2], env)
        print(f"- Variable '{t[1]}' updated to: {env[t[1]]}")  # Afficher la valeur mise à jour

    elif t[0] == "assign_op":
        var = t[1]
        operation = t[2]
        expr = t[3] if len(t) > 3 else None
        if operation == "++":
            env[var] += 1
        elif operation == "--":
            env[var] -= 1
        elif operation in ["+=", "-=", "*=", "/="]:
            env[var] = evalExpr((operation[0], var, expr), env)
        print(f"- Variable '{var}' updated to: {env[var]}")  # Afficher la valeur mise à jour

    elif t[0] == "if":
        condition = evalExpr(t[1], env)
        if condition:
            evalInst(t[2], env)  # Exécute le bloc "then" si la condition est vraie
        elif len(t) > 3 and t[3][0] == "if_else":
            # Exécute le bloc "elif" s'il existe
            evalInst(t[3], env)
        elif len(t) > 4 and t[4][0] == "else":
            # Exécute le bloc "else" s'il existe
            evalInst(t[4], env)

    elif t[0] == "if_else":
        condition = evalExpr(t[1], env)
        if condition:
            evalInst(t[2], env)  # Exécute le bloc "then" si la condition est vraie
        elif len(t) > 3 and t[3][0] == "if_else":
            # Exécute le bloc "elif" s'il existe
            evalInst(t[3], env)
        elif len(t) > 4 and t[4][0] == "else":
            # Exécute le bloc "else" s'il existe
            evalInst(t[4], env)

    elif t[0] == "else":
        evalInst(t[1], env)  # Exécute le bloc "else"

    elif t[0] == "while":
        while evalExpr(t[1], env):
            evalInst(t[2], env)


    elif t[0] == "for":
        evalInst(t[1], env)  # Initialisation
        while evalExpr(t[2], env):  # Condition
            evalInst(t[4], env)  # Corps de la boucle
            evalInst(t[3], env)  # Incrémentation ou mise à jour

    else:
        print("Warning_EvalInst : Unexpected instruction type:", t[0])
