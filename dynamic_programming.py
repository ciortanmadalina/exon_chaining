print('test')
from ast import literal_eval #this facilitates parsing input tuples

class Node:
    type: '';
    index: 0;
    pairIndex : 0;
    weight : 0;

    def __init__(self, index, pairIndex, type, weight):
        self.type = type
        self.pairIndex = pairIndex
        self.index = index
        self.weight = weight

    def __repr__(self):
        '''
        Override to string method to get some meaningful debug messages
        :return:
        '''
        if self.type == 'R':
            return 'Right Node index : %s, left index : %s , weight : %s \n' %(self.index, self.pairIndex, self.weight)
        else:
            return 'Left Node index : %s\n' % (self.index)

    def __lt__(self, other):
        '''
        Override compartor method in order to be able to stort left and right vertices
        by index, prioritising right nodes when indexes are identical
        :param other:
        :return:
        '''
        if self.index == other.index :
            return self.type == 'R'
        else:
            return self.index < other.index

    def prettyPrint(self):
        if self.type == 'R':
            return "( %s, %s )  %s " % (self.pairIndex, self.index, self.weight)
        else:
            return self.index

def getInputFromFile(filename):
    f = open(filename, 'r')
    segments_string = f.readline()
    l = literal_eval(segments_string)
    left = [(x[0]) for x in l]
    right = [(x[1]) for x in l]
    print(l)
    weights = [int(i) for i in f.readline().split(',')]
    f.close()
    return left, right, weights


def segmentsToGraph(left, right, weights):
    '''
    Graph will have a structure like
    [Left Node index : 1
    , Left Node index : 2
    , Right Node index : 3, left index : 2 , weight : 3
    , Left Node index : 4
    , Right Node index : 5, left index : 1 , weight : 5
    , Left Node index : 6
    , Left Node index : 7
    , Right Node index : 8, left index : 4 , weight : 6
    , Left Node index : 9
    , Right Node index : 10, left index : 9 , weight : 1
    , Left Node index : 11
    , Right Node index : 12, left index : 6 , weight : 10
    , Left Node index : 13
    , Right Node index : 14, left index : 13 , weight : 0
    , Right Node index : 15, left index : 11 , weight : 7
    , Left Node index : 16
    , Right Node index : 17, left index : 7 , weight : 12
    , Right Node index : 18, left index : 16 , weight : 4
    ]
    :param left:
    :param right:
    :param weights:
    :return:
    '''
    graph = []
    #create vertices for left nodes with no weight
    graph = [ Node(left[i], right[i], 'L', weights[i]) for i in range(len(weights))]
    #create vertices for right nodes with corresponding weight
    graph.extend([Node(right[i], left[i], 'R', weights[i]) for i in range(len(right))])

    graph.sort() # this will invoke __lt__
    return graph

def indexWithValue(graph, value) :
    for i in range(len(graph)):
        if graph[i].index == value:
            return i
    return -1



def exonChaining(graph):
    #print ('graph : ' , graph)
    n = len(graph)

    s = [0 for i in range(n)]
    selectedNodes = [-1 for i in range(n)]
    for i in range(1, n):
        if graph[i].type == 'R' :
            leftIndex = indexWithValue(graph, graph[i].pairIndex )
            if s[i - 1] < s[leftIndex] + graph[i].weight :
                s[i] = s[leftIndex] + graph[i].weight
                selectedNodes[i] = i
                continue
        s[i] = s [i-1]
        selectedNodes[i] = selectedNodes[i - 1]




    return selectedNodes

def printSolution(selectedNodes, graph, fileName):
    #outputFile = open("output/" + fileName, 'w')
    print('graph', graph)
    print('sel nodes', selectedNodes)
    selNode = selectedNodes[-1]
    totalWeight = 0
    while True :
        #outputFile.write(graph[selNode].prettyPrint())
        while graph[selNode].type == 'L':
            print('adjust', selNode)
            selNode -= 1
        if selNode <= -1:
            break
        print(graph[selNode].prettyPrint())
        #print('sel node ', selNode,graph[selNode] )
        totalWeight += graph[selNode].weight
        selNode = selNode - graph[selNode].index + graph[selNode].pairIndex

    print('Total weight : %s' % totalWeight)
    #outputFile.write('Total weight : %s' % totalWeight)
    #outputFile.close()

#########################
#RUN
#########################

#fileName = 'simple'
fileName = 'example'
left, right, weights = getInputFromFile("input/" + fileName)

print('left : ', left)
print('right : ', right)
graph = segmentsToGraph(left, right, weights)
sol = exonChaining(graph)
printSolution(sol, graph, fileName)
