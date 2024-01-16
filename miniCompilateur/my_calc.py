
# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 14/01/2024                                              *
# * @description: fonctions evalInst et evalExpr                   *
# ******************************************************************

from my_ast import parser
from my_eval import evalInst

env = {} # Stocker les variable dedans

while True:
    line = input("CALC> ") # Recupérer l'entrée utilisateur
    ast = parser.parse(line)
    evalInst(ast)
