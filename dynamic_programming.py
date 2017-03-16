print('test')
from ast import literal_eval
def getInputFromFile(filename):
    input = []
    f = open(filename, 'r')
    segments_string = f.readline()

    l = literal_eval(segments_string)
    print(l)
    print([(x[0], x[1]) for x in l])

    weights =  [int(i) for i in f.readline().split(',')]
    print(weights)
    f.close()
    return input


#########################
#RUN
#########################

fileName = 'simple'
input = getInputFromFile("input/" + fileName)