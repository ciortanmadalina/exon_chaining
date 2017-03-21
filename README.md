# Interval Graphs and Exon Chaining
### Madalina Ciortan
### 19/03/2017

## Formal problem
Exon Chaining Problem:  
Given a set of putative exons, find a maximum set of nonoverlapping putative exons.  

_Input_: A set of weighted intervals (putative exons).  
_Output_: A maximum chain of intervals from this set.  


The Exon Chaining problem for n intervals can be solved by dynamic programming
in a graph G on 2n vertices, n of which represent starting (left)
positions of intervals and n of which represent ending (right) positions of intervals,
as in figure 6.26. We assume that the set of left and right interval ends
is sorted into increasing order and that all positions are distinct, forming an
ordered array of vertices (v1, . . . v2n) in graph G.27 There are 3n − 1 edges in
this graph: there is an edge between each li and ri of weight wi for i from 1
to n, and 2n − 1 additional edges of weight 0 which simply connect adjacent
vertices (vi, vi+1) forming a path in the graph from v1 to v2n. In the algorithm
below, si represents the length of the longest path in the graph ending
at vertex vi. Thus, s2n is the solution to the Exon Chaining problem.

### Implementation

The graph described above was implemented as an array of nodes with the following structure:

```buildoutcfg
class Node:
    type: '';#this can be 'L' or 'R'
    nodeValue: 0; #holds the value of the vertex (the index of the point)
    pairValue : 0;# holds the index of the paired value, if Node is a right end point,
    # pair value will be the corresponding left end point and inversly
    weight : 0; #the given weight of the segment
```

This class is sortable ( see implmentation of __lt__) , arranging elements ascendingly by their value
and prioritising right nodes when the same value is common to both left and right ends.

## Pseudocode

Proposed pseudocode

```buildoutcfg
EXONCHAINING(G, n)
1 for i = 1 to 2n
2  si =  0
3 for i =  1 to 2n
4 if vertex vi in G corresponds to the right end of an interval I
5 j  = index of vertex for left end of the interval I
6 w  = weight of the interval I
7 si  = max {sj + w, si−1}
8 else
9 si =  si−1
10 return s2n
```

Implemented solution
```buildoutcfg
exonChaining(G, n)
    for i=1 to 2n
        si = 0
        selectedNodeIndexes = -1
        
    for i = 1 to 2n
     if vertex vi in G corresponds to the right end of an interval I
        j  = index of vertex for left end of the interval I
        w  = weight of the interval I
        si  = max {sj + w, si−1}
        selectedNodeIndexes = i
     else 
        si = si-1
        selectedNodeIndexes[i] =selectedNodeIndexes [i-1]
        
outputSolution(selectedNodeIndexes, G)

    selNode = last selected node index
    while selNode != -1
        print G[selNode]
        selNode -= length of segment given by selNode

```
## Complexity
The complexity of exonChaining method is O(2n) = O(n) (linear).  
The complexity of outputSolution is also linear.  
The complexity of sorting the nodes is the complexity of python's sort method = O(n log n).
## Results
Find input/output results in input/output folders.