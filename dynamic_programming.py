print('test')
from ast import literal_eval #this facilitates parsing input tuples

class Node:
    isRight: True;
    index: 0;
    pairIndex : 0;
    weight : 0;

    def __init__(self, index, pairIndex, isLeft, weight):
        self.isRight = isLeft
        self.pairIndex = pairIndex
        self.index = index
        self.weight = weight

    def __repr__(self):
        '''
        Override to string method to get some meaningful debug messages
        :return:
        '''
        if self.isRight:
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
            return self.isRight
        else:
            return self.index < other.index

    def prettyPrint(self):
        if self.isRight:
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
    graph = []
    #create vertices for left nodes with no weight
    graph = [ Node(index, None, False, 0) for index in left]
    #create vertices for right nodes with corresponding weight
    graph.extend([Node(right[i], left[i], True, weights[i]) for i in range(len(right))])

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
        if graph[i].isRight :
            leftIndex = indexWithValue(graph, graph[i].pairIndex )
            if s[i - 1] < s[leftIndex] + graph[i].weight :
                s[i] = s[leftIndex] + graph[i].weight
                selectedNodes[i] = i
                continue
        s[i] = s [i-1]
        selectedNodes[i] = selectedNodes[i - 1]




    return selectedNodes

def printSolution(selectedNodes, graph, fileName):
    outputFile = open("output/" + fileName, 'w')

    selNode = selectedNodes[-1]
    totalWeight = 0
    while selNode != -1 :
        #outputFile.write(graph[selNode].prettyPrint())
        print(graph[selNode].prettyPrint())
        totalWeight += graph[selNode].weight
        selNode = selNode - graph[selNode].index + graph[selNode].pairIndex

    print('Total weight : %s' % totalWeight)
    outputFile.write('Total weight : %s' % totalWeight)
    outputFile.close()

#########################
#RUN
#########################

fileName = 'simple'
left, right, weights = getInputFromFile("input/" + fileName)

print('left : ', left)
print('right : ', right)
graph = segmentsToGraph(left, right, weights)
sol = exonChaining(graph)
printSolution(sol, graph, fileName)
