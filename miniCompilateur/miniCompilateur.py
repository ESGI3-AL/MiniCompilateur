
#******************************************************************
#? @author: Denisa Dudas & Camillia Hammou                        #
#? @date: 07/01/2024                                              #
#? @description: mini compilateur                                 #
#******************************************************************

from genereTreeGraphviz2 import printTreeGraph
import ply.lex as lex    #lexer
import ply.yacc as yacc  #parser

#! Lexeur

# dictionnaire
reserved = {
   'if' : 'IF',  # mot clé associé à une valeur
   'then' : 'THEN',
   'print' : 'PRINT'
   }

# liste de tokens utilisée dans l'analyseur lexical
tokens = [
    'NAME','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE',
    'LPAREN','RPAREN', 'LBRACE', 'RBRACE', 'COLON', 'AND', 'OR', 'EQUAL', 'EQUALS', 'LOWER','HIGHER',
    'WHILE', 'FOR'
    ]+list(reserved.values())  # ajout du dictionnaire

# règle PLY pour reconnaître les identificateurs ou noms de variables
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

# règle pour reconnaître certains symboles à l'aide de PLY
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUAL  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COLON = r';'
t_AND  = r'\&'
t_OR  = r'\|'
t_EQUALS  = r'=='
t_LOWER  = r'\<'
t_HIGHER  = r'\>'

# règle pour reconnaître les nombres entiers
def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# règle pour ignorer certains caractères
t_ignore = " \t"

# règle pour compter le nombre de nouvelles lignes
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# règle spéciale appelée par le lexer lorsqu'il rencontre un caractère qui ne correspond à aucune des règles définies
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)  # passer au caractère suivant

# Build le lexeur
lexer = lex.lex()

#-----------------------------------------------------------------------------------------------------------------------

#! Parsing rules

# règle de production syntaxique pour le démarrage du parsing
def p_start(t):
    ''' start : linst'''
    t[0] = ('start',t[1])
    print(t[0])
    printTreeGraph(t[0])
    #eval(t[1])
    evalInst(t[1])  # evaluation de l'arbre
names={}

#! evalInst
def evalInst(t):
    print('evalInst', t)
    if t == "empty" : return
    if type(t)!=tuple :
        print('warning')
        return
    if t[0]=='print' :
        print('CALC>', evalExpr(t[1]))
    if t[0]=='assign' :
        names[t[1]]=evalExpr(t[2])
    if t[0]=='bloc' :
        evalInst(t[1])
        evalInst(t[2])

#! evalExpr
def evalExpr(t):
    #print('eval de ',t, type(t), len(t))
    if type(t) is not tuple :
        print('tree not tuple', t)
        return t

    if t[0] == 'START' :
        return evalExpr(t[1])

    if t[0] == 'Num' :
        return t[1]

    if t[0] == 'Expr' :
        left_operand = evalExpr(t[1])
        operator = evalExpr(t[2])
        right_operand = evalExpr(t[3])

        if operator == '+':
            return left_operand + right_operand
        if operator == '-':
            return left_operand - right_operand
        if operator == '*':
            return left_operand * right_operand
        if operator == '/':
            return left_operand / right_operand
        if operator == 'AND':
            return left_operand and right_operand
        if operator == 'OR':
            return left_operand or right_operand

    return 'UNK'

# définition de la structure syntaxique pour les blocs d'instructions
def p_line(t):
    '''linst : linst inst
            | inst '''
    if len(t)== 3 :
        t[0] = ('bloc',t[1], t[2])
    else:
        t[0] = ('bloc',t[1], 'empty')


#! l’affectation et les variables dans les expressions
def p_statement_assign(t):
    'inst : NAME EQUAL expression COLON'
    t[0] = ('assign',t[1], t[3])

#! print
def p_statement_print(t):
    'inst : PRINT LPAREN expression RPAREN COLON'
    t[0] = ('print',t[3])

#! calcul d’expressions arithmétiques et booléennes
def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression OR expression
                  | expression AND expression
                  | expression EQUALS expression
                  | expression LOWER expression
                  | expression HIGHER expression
                  | expression DIVIDE expression'''
    t[0] = (t[2],t[1], t[3])


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]

def p_expression_number(t):
    'expression : NUMBER'

    t[0] = t[1]

def p_expression_name(t):
    'expression : NAME'

    t[0] = t[1]

#! fin calcul d’expressions arithmétiques et booléennes

#! if
def p_statement_if(t):
    'inst : IF LPAREN expression RPAREN LBRACE linst RBRACE'

    # t[0] => construire le noeud (résultat)
    # t[1] => if
    # t[2] => paranthèse gauche
    # t[3] => expression
    # t[4] => paranthèse droite
    # t[5] => accolade gauche
    # t[6] => bloc d'intruction
    # t[7] => accolade droite
    t[0] = ('if', t[3], t[6])

#! while
def p_statement_while(t):
    'inst : WHILE LPAREN expression RPAREN LBRACE linst RBRACE'

    t[0] = ('while', t[3], t[6])

#! for
def p_statement_for(t):
    'inst : FOR LPAREN expression RPAREN LBRACE linst RBRACE'

    t[0] = ('for', t[3], t[6])

# règle spéciale pour la gestion d'erreur
def p_error(t):
    print("Syntax error at '%s'" % t.value)

# Build le parseur
parser = yacc.yacc()

result='print(1+3);x=4;x=x+1;'

# analyse et construit l'arbre syntaxique correspondant
parser.parse(result)
