# Projet Mini interpréteur - Théorie des langages de compilation

- auteurs: Denisa Dudas & Camillia Hammou
- classe: 3ESGI AL1
- présoutenance: 23/01/2024
- soutenance: 22/02/2024

## Description
Mini interpréteur avec AST contenant:
- evalExpr et evalInst
- IF, WHILE ET FOR
- Fonctions :
    - void sans paramètre
    - void avec paramètre
    - paramètres et return
- Gestion du scope des variables
- Récursivité terminale
- Variables globales

## Organisation projet

## Exemples d'utilisation

- affectation, print -> miniInterpréteur.py
s1='x=4;x=x+3;print(x);'

- affectation élargie, affectation -> miniInterpréteur.py
s2='x=9; x+=4; x++; print(x);'

- while, for -> miniInterpréteur.py
s3=’’’x=4;while(x<30){x=x+3;print(x);} ; for(i=0 ;i<4 ;i=i+1 ;){print(i*i) ;} ;’’’

- fonctions void avec paramètres -> miniInterpréteur.py
s4='fonctionVoid toto(a, b){print(a+b) ;} toto(3, 5) ;’

- fonctions value avec paramètres et return explicite -> miniInterpréteur.py
s5='fonctionValue toto(a, b){c=a+b ;return c ;} toto(3, 5) ;’

- fonctions value avec paramètres et return implicite -> miniInterpréteur.py
s5='fonctionValue toto(a, b){c=a+b ; toto=c ;} toto(3, 5) ;’

- fonctions value avec paramètres et return coupe circuit -> miniInterpréteur.py
s6='fonctionValue toto(a, b){c=a+b ;return c ; print(666) ;} x=toto(3, 5) ; print(x) ;’

- fonctions value avec paramètres, return coupe circuit et scope des variables -> miniInterpréteur.py
s7='fonctionValue toto(a, b){if(a==0) return b ; c=toto(a-1, b-1) ;return c ; print(666) ;} x=toto(3, 5) ; print(x) ;’

### Informations
- Python 3.11.6
- ply, graphviz
- visual studio code
