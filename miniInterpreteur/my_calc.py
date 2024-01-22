
# ******************************************************************
# * @author: Denisa Dudas & Camillia Hammou                        *
# * @date: 05/01/2024                                              *
# * @description: Boucle pour evaluer les input utilisateur        *
# ******************************************************************

from my_ast import parser
from my_eval import evalInst

env = {}

while True:
    line = input("CALC> ")
    ast = parser.parse(line)
    evalInst(ast, env)
