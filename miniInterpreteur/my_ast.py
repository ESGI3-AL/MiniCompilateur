
# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 25/12/2023                                              *
# * @description: mini compilateur                                 *
# ******************************************************************

from genereTreeGraphviz2 import printTreeGraph
import ply.lex as lex  # lexer
import ply.yacc as yacc  # parser

#! Lexeur

# dictionnaire
reserved = {
    "if": "IF",  # mot clé associé à une valeur;
    "else": "ELSE",
    "elseif": "ELSEIF",
    "print": "PRINT",
    "printString": "PRINTSTRING",
    "while": "WHILE",
    "for": "FOR",
    "function": "FUNCTION",
    "void": "VOID",
    "value": "VALUE",
    "return": "RETURN",
    "array": "ARRAY",
}

# liste de tokens utilisée dans l'analyseur lexical
tokens = [
    "ID",
    "NUMBER",
    "INCREMENT",
    "DECREMENT",
    "PLUSEQUAL",
    "MINUSEQUAL",
    "TIMESEQUAL",
    "DIVIDEEQUAL",
    "LOWEQUAL",
    "HIGHEQUAL",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "LBRACKET",
    "RBRACKET",
    "SEMICOLON",
    "COMMA",
    "AND",
    "OR",
    "EQUALS",
    "EQUAL",
    "LOWER",
    "HIGHER",
    "STRING",
] + list(
    reserved.values() # ajout du dictionnaire
)


# règle PLY pour reconnaître les identificateurs ou noms de variables
def t_ID(t):
    r"[a-zA-Z_][a-zA-Z_0-9]*"  # variable/fonction
    t.type = reserved.get(t.value, "ID")  # Check for reserved words
    return t


# règle pour reconnaître certains symboles à l'aide de PLY, r = raw
t_INCREMENT = r"\+\+"
t_DECREMENT = r"--"
t_PLUSEQUAL = r"\+="
t_MINUSEQUAL = r"-="
t_TIMESEQUAL = r"\*="
t_DIVIDEEQUAL = r"/="
t_LOWEQUAL = r"<="
t_HIGHEQUAL = r">="
t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_SEMICOLON = r";"
t_COMMA = r"\,"
t_AND = r"\&\&"
t_OR = r"\|\|"
t_EQUALS = r"=="
t_EQUAL = r"="
t_LOWER = r"\<"
t_HIGHER = r"\>"
t_STRING = r'"[^"]*"'


# règle pour reconnaître les nombres entiers
def t_NUMBER(t):
    r"\d+"
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
    r"\n+"
    t.lexer.lineno += t.value.count("\n")


# règle spéciale appelée par le lexer lorsqu'il rencontre un caractère qui ne correspond à aucune des règles définies
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)  # passer au caractère suivant


# Build le lexeur
lexer = lex.lex()

# -----------------------------------------------------------------------------------------------------------------------

#! Parsing rules


#! règle de production syntaxique pour le démarrage du parsing
def p_start(t):
    """start : linst"""
    t[0] = ("start", t[1])
    print(t[0])
    printTreeGraph(t[0])  # à decommenté si besoin pour afficher l'arbre
    # eval(t[1])
    # evalInst(t[1])  # evaluation de l'arbre


#! définition de la structure syntaxique pour les blocs d'instructions
def p_line(t):
    """linst : linst inst
             | inst"""  # linst peut etre une séquence de deux elements ou une seule instruction
    if len(t) == 3:  # verification si séquence de 2 elements (linst et inst) => liste-instructions & instructions
        t[0] = ("node", t[1], t[2])  # si oui, on construit un tuple
    else:  # sinon on a un seul element
        t[0] = t[1]


#! affectation des variables dans les expressions
def p_statement_assign(t):
    # affectation variable, incrementation et decrementation variable
    """inst : ID EQUAL expression SEMICOLON
            | ID INCREMENT SEMICOLON
            | ID DECREMENT SEMICOLON
            | ID PLUSEQUAL expression SEMICOLON
            | ID MINUSEQUAL expression SEMICOLON
            | ID TIMESEQUAL expression SEMICOLON
            | ID DIVIDEEQUAL expression SEMICOLON
            """
    if t[2] == '=':
        t[0] = ("=", t[1], t[3])
    elif t[2] == '++' or t[2] == "--":     # incrémenter/decrémenter
        t[0] = ("=", t[1], (t[2][0], t[1], 1))
    elif t[2] == '+=' or t[2] == '-=' or t[2] == '*=' or t[2] == '/=':
        t[0] = ("=", t[1], (t[2][0], t[1], t[3]))


def p_statement_print(t):
    """inst : PRINT LPAREN string RPAREN SEMICOLON
            | PRINT LPAREN ID RPAREN SEMICOLON"""
    t[0] = ("printString", t[3])


#! Règle pour l'impression multiple
def p_statement_print_multiple(t):
    "inst : PRINT LPAREN expr_list RPAREN SEMICOLON"
    t[0] = ("printmultiple", t[3])


#! printString
def p_statement_print_string(t):
    "inst : PRINTSTRING LPAREN STRING RPAREN SEMICOLON"
    t[0] = ("printString", t[3])


#! Règle pour une chaîne de caractères
def p_string(t):
    """
    string : STRING
    """
    t[0] = t[1]


#! Règle pour une liste d'expressions
def p_expr_list(t):
    """
    expr_list : expression
              | expr_list COMMA expression
    """
    if len(t) == 2:  # Un seul élément
        t[0] = [t[1]]
    else:  # Plusieurs éléments
        t[0] = t[1] + [t[3]]


#! calcul d’expressions arithmétiques et booléennes
def p_expression_binop(t):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQUALS expression
                  | expression OR expression
                  | expression AND expression
                  | expression LOWER expression
                  | expression HIGHER expression
                  | expression LOWEQUAL expression
                  | expression HIGHEQUAL expression
                  """
    t[0] = (t[2], t[1], t[3])


def p_expression_group(t):
    "expression : LPAREN expression RPAREN"
    t[0] = t[2]


def p_expression_number(t):
    "expression : NUMBER"

    t[0] = t[1]


def p_expression_name(t):
    "expression : ID"

    t[0] = t[1]


#! fin calcul d’expressions arithmétiques et booléennes


#! if
def p_statement_if(t):
    "inst : IF LPAREN expression RPAREN LBRACE linst RBRACE"

    # t[0] => construire le noeud (résultat)
    # t[1] => if
    # t[2] => paranthèse gauche
    # t[3] => expression
    # t[4] => paranthèse droite
    # t[5] => accolade gauche
    # t[6] => bloc d'intruction
    # t[7] => accolade droite
    t[0] = ("if", t[3], t[6])


#! if, else
def p_statement_if_else(t):
    "inst : IF LPAREN expression RPAREN LBRACE linst RBRACE ELSE LBRACE linst RBRACE"

    # t[8] => else
    # t[9] => accolade gauche
    # t[10] => bloc d'intruction
    # t[11] => accolade droite
    t[0] = ("if_else", t[3], t[6], t[10])


#! if, elseif, else
def p_statement_if_elseif_else(t):
    "inst : IF LPAREN expression RPAREN LBRACE linst RBRACE ELSEIF LPAREN expression RPAREN LBRACE linst RBRACE ELSE LBRACE linst RBRACE"

    t[0] = ("if_elseif_else", t[3], t[6], t[10], t[13], t[17])


#! while
def p_statement_while(t):
    "inst : WHILE LPAREN expression RPAREN LBRACE linst RBRACE"
    t[0] = ("while", t[3], t[6])


#! for
def p_statement_for(t):
    "inst : FOR LPAREN inst expression SEMICOLON inst RPAREN LBRACE linst RBRACE"

    # t[0] => construire le noeud (résultat)
    # t[1] => for
    # t[2] => paranthèse gauche
    # t[3] => instruction
    # t[4] => point-virgule
    # t[5] => expression
    # t[6] => point-virgule
    # t[7] => incrémentation boucle
    t[0] = ("for", t[3], t[4], t[6], t[9])


#! fonction void sans paramètres
def p_void_function_without_params(t):
    "inst : FUNCTION VOID ID LPAREN RPAREN LBRACE linst RBRACE"
    t[0] = ("function", t[2], t[3], t[7])


#! appel de fonction void sans paramètres
def p_function_call_without_params(t):
    "inst : ID LPAREN RPAREN SEMICOLON"
    t[0] = ("call", t[1])


#! fonction void avec paramètres
def p_void_function_with_params(t):
    "inst : FUNCTION VOID ID LPAREN params RPAREN LBRACE linst RBRACE"
    t[0] = ("function", t[2], t[3], t[5], t[8])


#! appel de fonction void avec paramètres
def p_function_call_with_params(t):
    "inst : ID LPAREN params RPAREN SEMICOLON"
    t[0] = ("call", t[1], t[3])


#! règles pour avoir des paramètres
def p_params(t):
    'params : param'
    t[0] = [t[1]]


def p_params_multiple(t):
    'params : param COMMA params'
    t[0] = [t[1]] + t[3]


def p_param(t):
    '''param : expression'''
    t[0] = t[1]
#!-----------------------------------

#! fonction value sans paramètres et return
def p_function_value_without_params(t):
    "inst : FUNCTION VALUE ID LPAREN RPAREN LBRACE linst return_statement RBRACE"
    t[0] = ("function", t[2], t[3], t[7], t[8])


#! fonction value avec paramètres et return
def p_function_value_with_params(t):
    "inst : FUNCTION VALUE ID LPAREN params RPAREN LBRACE linst return_statement RBRACE"
    t[0] = ("function", t[2], t[3], t[5], t[8], t[9])


#! règle pour gérer le return
def p_return_statement(t):
    "return_statement : RETURN expression SEMICOLON"
    t[0] = ("return", t[2])


#! règle pour déclarer un tableau vide
def p_empty_array_declaration(t):
    "inst : ARRAY ID LBRACKET RBRACKET SEMICOLON"
    t[0] = ("array", t[2], [])


#! règle pour déclarer un tableau
def p_array_declaration_single_element(t):
    "inst : ARRAY ID LBRACKET expression RBRACKET SEMICOLON"
    t[0] = ("array", t[2], t[4])


#! règle pour déclarer un tableau avec plusieurs éléments
def p_array_declaration_multiple_elements(t):
    "inst : ARRAY ID LBRACKET expr_list RBRACKET SEMICOLON"
    t[0] = ("array", t[2], t[4])


#! règle pour accéder à un élément du tableau
def p_array_access(t):
    "inst : ID LBRACKET expression RBRACKET SEMICOLON"
    t[0] = ("array_access", t[1], t[3])


#! règle pour modifier un élément du tableau
def p_array_assignment(t):
    "inst : ID LBRACKET expression RBRACKET EQUAL expression SEMICOLON"
    t[0] = ("array_assignment", t[1], t[3], t[6])

def p_expression_array_access(t):
    "expression : ID LBRACKET expression RBRACKET"
    t[0] = ("array_access", t[1], t[3])


# règle spéciale pour la gestion d'erreur
def p_error(t):
    if t is not None:
        print(f"Syntax error at '{t.value}' {t.lineno}:{t.lexpos}")
    else:
        print("Syntax error: unexpected end of input")


# Build le parseur
parser = yacc.yacc()

# ----------------------- fonctions ----------------------------------
# fonction void sans paramètres
s11 = "function void toto(){print(2);}toto();"

# fonction void avec 2 paramètres
s12 = "function void toto(x, y){print(x+y);}toto(2,3);"

# fonction void avec 1 paramètres
s13 = "function void toto(x){print(x);}toto(2);"

# fonction void avec 3 paramètres
s14 = "function void toto(x,y,z){print(x+y+z);}toto(1,2,3);"

# fonction value sans paramètres et return
s15 = "function value toto(){x=5; return x;}toto();"

# fonction value avec paramètres et return
s16 = "function value toto(a,b){c=a+b ; return c;} toto(3, 5);"

# ----------------------- tableaux ----------------------------------
s17 = "array tab[];"

s18 = "array tab[5, 2, 1];"

s20 = "tab[0] = 6;"

s25 = "print(tab[0]);"

s30 = "print(tab[2]);"

#-------------------scope des variables-------------------------------
s21 = "function void toto(){x=5;}toto();"
s22 = "function void toto(){x=5;}toto();print(x);" #doit renvoyer x car pas a l'interieur de la fonction
s23 = "function void toto(){x=5;}toto();function void toto(){x=5;}toto();print(x);"

#----------------------Pile d'execution--------------------------------
s24 = "function void inner(){print(5);}function void outer(){ x=5;inner();}outer();"


#analyse et construit l'arbre syntaxique correspondant
parser.parse(s20)
