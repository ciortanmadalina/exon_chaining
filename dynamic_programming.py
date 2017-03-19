from ast import literal_eval #this facilitates parsing input tuples

class Node:
    type: '';#this can be 'L' or 'R'
    nodeValue: 0; #holds the value of the vertex (the index of the point)
    pairValue : 0;# holds the index of the paired value, if Node is a right end point,
    # pair value will be the corresponding left end point and inversly
    weight : 0; #the given weight of the segment

    def __init__(self, nodeValue, pairValue, type, weight):
        self.type = type
        self.pairValue = pairValue
        self.nodeValue = nodeValue
        self.weight = weight

    def __repr__(self):
        '''
        Override to string method to get some meaningful debug messages
        :return:
        '''
        if self.type == 'R':
            return 'R value : %s, L value : %s , weight : %s \n' %(self.nodeValue, self.pairValue, self.weight)
        else:
            return 'L value: %s\n' % (self.nodeValue)

    def __lt__(self, other):
        '''
        Override compartor method in order to be able to stort left and right vertices
        by nodeValue, prioritising right nodes when nodeValuees are identical
        :param other:
        :return:
        '''
        if self.nodeValue == other.nodeValue :
            return self.type == 'R'
        else:
            return self.nodeValue < other.nodeValue

    def prettyPrint(self):
        if self.type == 'R':
            return "( %s, %s )  %s " % (self.pairValue, self.nodeValue, self.weight)
        else:
            return self.nodeValue

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
    [L value: 1
    , L value: 2
    , R value : 3, L value : 2 , weight : 3
    , L value: 4
    , R value : 5, L value : 1 , weight : 5
    , L value: 6
    , L value: 7
    , R value : 8, L value : 4 , weight : 6
    , L value: 9
    , R value : 10, L value : 9 , weight : 1
    , L value: 11
    , R value : 12, L value : 6 , weight : 10
    , L value: 13
    , R value : 14, L value : 13 , weight : 0
    , R value : 15, L value : 11 , weight : 7
    , L value: 16
    , R value : 17, L value : 7 , weight : 12
    , R value : 18, L value : 16 , weight : 4
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
        if graph[i].nodeValue == value:
            return i
    return -1



def exonChaining(graph):
    n = len(graph)

    #this structure will keep the weights helping to decide whether to select current node or not
    s = [0 for i in range(n)]

    #this structure will be explored in order to reconstruct selected nodes
    selectedNodeIndexes = [-1 for i in range(n)] #initialize with -1 as no nodes are selected
    for i in range(1, n):
        if graph[i].type == 'R' :
            leftIndex = indexWithValue(graph, graph[i].pairValue )
            if s[i - 1] < s[leftIndex] + graph[i].weight :
                s[i] = s[leftIndex] + graph[i].weight
                selectedNodeIndexes[i] = i
                continue
        s[i] = s [i-1]
        selectedNodeIndexes[i] = selectedNodeIndexes[i - 1]

    return selectedNodeIndexes

def printSolution(selectedNodeIndexes, graph, fileName):
    outputFile = open("output/" + fileName, 'w')

    selNode = selectedNodeIndexes[-1] #iterate from the last selected node
    #based on its length (nodeValue - pairValue) we visit only the points whose
    #selection built the final solution

    totalWeight = 0
    while True :

        #we explore as part of the solution only right edges, after substracting
        #the legth of the segment it is possible to end up on a left node because
        #an index can be both a left and a right edge. So if current node is a left
        #edge, we find the neared right edge
        while graph[selNode].type == 'L':
            selNode -= 1

        if selNode <= -1: #stop when we reached no selection
            break

        outputFile.write(str(graph[selNode].prettyPrint() + '\n'))
        print(graph[selNode].prettyPrint())

        totalWeight += graph[selNode].weight
        selNode = selNode - graph[selNode].nodeValue + graph[selNode].pairValue

    print('Total weight : %s' % totalWeight)
    outputFile.write('Total weight : %s' % totalWeight)
    outputFile.close()

#########################
#RUN
#########################

# fileName = 'simple'
fileName = 'example'
left, right, weights = getInputFromFile("input/" + fileName)

graph = segmentsToGraph(left, right, weights)
sol = exonChaining(graph)
printSolution(sol, graph, fileName)
