import os
import graphviz as gv
import uuid
from datetime import datetime

def printTreeGraph(t):
    timestamp = datetime.now().strftime('%m-%d-%Y_%H:%M:%S')
    filename = f'treeImages/Digraph.gv.{timestamp}'

    graph = gv.Digraph(format='png')
    graph.attr('node', shape='circle')
    addNode(graph, t)

    treeImages = os.path.join(os.getcwd(), 'treeImages')

    # Vérification si le dossier existe, sinon on le crée
    if not os.path.exists(treeImages):
        os.makedirs(treeImages)

    graph.render(filename=filename, cleanup=True)

def addNode(graph, t):
    myId = uuid.uuid4()

    if type(t) != tuple:
        graph.node(str(myId), label=str(t))
        return myId

    graph.node(str(myId), label=str(t[0]))
    for i in range(1, len(t)):
         graph.edge(str(myId), str(addNode(graph, t[i])), arrowsize='0')


    return myId

#printTreeGraph(('*', ('+', 4, 2), 3), 'treeImages/graph')