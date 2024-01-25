# Projet Mini interpréteur - Théorie des langages de compilation

- auteurs: Denisa Dudas & Camillia Hammou
- classe: 3ESGI AL1
- présoutenance: 23/01/2024
- soutenance: 22/02/2024

## Description
Mini interpréteur avec AST contenant:
- noms de variables à plusieurs caractères
- affectations
- affichage d’expressions numériques
- evalExpr et evalInst
- instructions conditionnelles
- structures itératives
- affichage de l’arbre de syntaxe (sur la console et avec graphViz)

- Bonus :
    - Fonctions :
        - void sans paramètre
        - void avec paramètre
    - Gestion des erreurs
    - incrémentation, décrementation et affectations élargies : x++, x--, x+=1 ...
    - affichage de l’arbre de syntaxe avec graphViz dans un dossier dedié
    -PrintMultiples
    -PrintString

## Organisation projet
- Structure du projet:
    - dossier miniInterpreteur :
        - dossier treeImages contenant l'affichage des arbres de syntaxe avec graphViz
        - fichier generateTreeGraphviz2
        - fichier my_ast contenant notre ast (parseur, lexeur)
        - fichier my_eval contenant les evalInt et evalExpr
        - fichier my_calc contenant la boucle principale du programme
    - README.md

## Exemples d'utilisation

-------------------affectation simples-------------------
s1 = "var=hello; x=4; print(x);"

s2 = "x=x+3; x=x-12; x=x*5; x=x/8;"

s3 = "x+=9; x-=4; x*=10; x/=5; x--; x++;"

-------------------------if/elseif/else-------------------------
s4 = "if(x<=6){print(x);}"

s5 = "if(x>=7){print(True);} else {print(False);}"

s6 = "if(x>3){print(Bigger);} elseif(x<3){print(Smaller);} else{print(Equal);}"

-------------------boucles while, for-------------------
s7 = "while(x<30){x=x+3;print(x);}"

s8 = """
for (i=0; i<4; i=i+1;) {print(i*i);}
    """

------------------------fonctions------------------------
fonction void sans paramètres
s9 = "function void toto(){print(2);}toto();"

fonction void avec paramètres
s10 = "function void toto(x, y){print(x+y);}toto(2,3);"


### Informations
- Python 3.11.6
- ply, graphviz
- visual studio code
