
# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 14/01/2024                                              *
# * @description: fonctions evalInst et evalExpr                   *
# ******************************************************************

# dictionnaire vide pour stocker les variables gardés en mémoire
env = {}

#! evaluation des instructions
def evalInst(t):
    print("evalInst", t)
    if t == "empty":
        return

    if type(t) != tuple:
        print("Warning_EvalInst : Unexpected leaf node:", t)
        return

    if t[0] == "print":
        print("CALC>", evalExpr(t[1]))

    if t[0] == "assign":
        if type(t[2]) == tuple and t[2][0] == "Num":
            env[t[1]] = evalExpr(t[2])
        else:
            print("Warning_EvalInst : Unexpected assignment structure:", t)

    if t[0] == "bloc":
        evalInst(t[1])
        evalInst(t[2])

    if t[0] == "assign_op":
        if t[2] == "++":
            env[t[1]] += 1
        elif t[2] == "--":
            env[t[1]] -= 1
        else:
            if t[2] == "+=":
                env[t[1]] += evalExpr(t[3])
            elif t[2] == "-=":
                env[t[1]] -= evalExpr(t[3])
            elif t[2] == "*=":
                env[t[1]] *= evalExpr(t[3])
            elif t[2] == "/=":
                env[t[1]] /= evalExpr(t[3])

    if t[0] == "while":
        while evalExpr(t[1]):
            evalInst(t[2])

    if t[0] == "for":
        evalInst(t[1])
        while evalExpr(t[2]):
            evalInst(t[4])
            evalInst(t[3])


#! evaluation des expressions
def evalExpr(t):
    # print('eval de ',t, type(t), len(t))
    if type(t) is not tuple:  # si ce n'est pas un tuple, c'est une feuille de l'arbre
        return t

    if t[0] == "START":
        return evalExpr(t[1])

    if t[0] == "Num":
        return t[1]

    if t[0] == "Expr":
        left_operand = evalExpr(t[1])
        operator = t[2]
        right_operand = evalExpr(t[3])

        if operator == "+":
            return left_operand + right_operand
        elif operator == "-":
            return left_operand - right_operand
        elif operator == "*":
            return left_operand * right_operand
        elif operator == "/":
            return left_operand / right_operand
        elif operator == "AND":
            return left_operand and right_operand
        elif operator == "OR":
            return left_operand or right_operand
        elif operator == "==":
            return left_operand == right_operand
        elif operator == "<":
            return left_operand < right_operand
        elif operator == ">":
            return left_operand > right_operand
        elif operator == "+=":
            env[left_operand] += right_operand
            return env[left_operand]
        elif operator == "-=":
            env[left_operand] -= right_operand
            return env[left_operand]
        elif operator == "*=":
            env[left_operand] *= right_operand
            return env[left_operand]
        elif operator == "/=":
            env[left_operand] /= right_operand
            return env[left_operand]
        else:
            print("Unexpected binary operator:", operator)
            return "UNKNOWN"
    else:
        print("Unexpected expression structure:", t)
        return "UNKNOWN"
