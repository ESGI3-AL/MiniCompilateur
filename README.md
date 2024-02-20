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
    -Pile d'éxécution (suivis de l'ordre des appels de fonction, fonction ajouté, son nom est ajouté a la pile, fonction terminé, nom retiré de la pile, donc on peut voir quelle fonction est en cours d'éxécution pour un moment donnée)
    -return
    -scope des variables
    -tableau (affectation, print, init)

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


### Affectation simples :

s1 = "y=hello; x=4; print(x); print(y);"

s2 = "x=x+3; x=x-12; x=x*5; x=x/8;"

s3 = "x+=9; x-=4; x*=10; x/=5; x--; x++;"


### If/elseif/else :
s4 = "if(x<=6){print(x);}"

s5 = "if(x>=7){print(True);} else {print(False);}"

s6 = "if(x>3){print(Bigger);} elseif(x<3){print(Smaller);} else{print(Equal);}"


### Boucles while, for :
s7 = "while(x<30){x=x+3;print(x);}"

s8 = """
for (i=0; i<4; i=i+1;) {print(i*i);}
    """


### Print :
Print :
s9 = "print(2);"

Print multiple:
s10 = "print(1+5,2,3);"


## Fonctions :
### fonction void sans paramètres :
s11 = "function void toto(){print(2);}toto();"

### fonction void avec 2 paramètres :
s12 = "function void toto(x, y){print(x+y);}toto(2,3);"

### fonction void avec 1 paramètres :
s13 = "function void toto(x){print(x);}toto(2);"

### fonction void avec 3 paramètres :
s14 = "function void toto(x,y,z){print(x+y+z);}toto(1,2,3);"

### fonction value sans paramètres et return :
s15 = "function value toto(){x=5; return x;}toto();"

### fonction value avec paramètres et return :
s16 = "function value toto(a,b){c=a+b ; return c;} toto(3, 5);"

## tableaux
s17 = "array tab[];"

s18 = "array tab[5, 2, 1];"

s20 = "tab[0] = 6;"

s25 = "print(tab[0]);"

s30 = "print(tab[2]);"

## scope des variables
s21 = "function void toto(){x=5;}toto();"
s22 = "function void toto(){x=5;}toto();print(x);" #doit renvoyer x car pas a l'interieur de la fonction
s23 = "function void toto(){x=5;}toto();function void toto(){x=5;}toto();print(x);"

## Pile d'execution
s24 = "function void inner(){print(5);}function void outer(){ x=5;inner();}outer();"

---
## Informations Utiles
- Python 3.11.6
- ply, graphviz
- visual studio code
