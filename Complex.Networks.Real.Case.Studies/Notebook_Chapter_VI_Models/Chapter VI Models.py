#!/usr/bin/env python
# coding: utf-8

# # Chapter VI Models

# In[ ]:


get_ipython().run_line_magic('pylab', 'inline')


# ### The [Fibonacci sequence](http://en.wikipedia.org/wiki/Fibonacci_number) is a sequence in math that starts with 0 and 1, and then each successive entry is the sum of the previous two. Thus, the sequence goes 0,1,1,2,3,5,8,13,21,34,55,89,...
# 
# ### Let's compute the Fibonacci sequence up to some number **n**:

# In[ ]:


def fibonacci(sequence_length):
    "Return the Fibonacci sequence of length *sequence_length*"
    sequence = [0,1]
    if sequence_length < 1:
        print "Fibonacci sequence only defined for length 1                or greater"
        return
    if 0 < sequence_length < 3:
        return sequence[:sequence_length]
    for i in range(2,sequence_length): 
        sequence.append(sequence[i-1]+sequence[i-2])
    return sequence

fibonacci(12)


# ### Lotka-Volterra differntial equations

# In[ ]:


from sympy import *


# In[ ]:


#defining the variables and parameters
var('y z')
var('alfa beta gamma delta', positive=True)


# In[ ]:


#defining the equations
dy = alfa*z*y - beta*y
dz = gamma*z - delta*z*y


# In[ ]:


#solving the Lotka Volterra equations
(y0, z0), (y1, z1) = solve([dy, dz], (y, z))
A = Matrix((dy, dz))
print A


# In[ ]:


#computing the Jacobian
Jacobian = A.jacobian((y, z)); Jacobian
B = Jacobian.subs(y, y0).subs(z, z0)
C = Jacobian.subs(y, y1).subs(z, z1)
print B,C


# In[ ]:


#stability of the fixed points
solutionB=B.eigenvals()
solutionC=C.eigenvals()
print solutionB,solutionC


# ### Generating Random Networks (Erdos-Renyi)

# In[ ]:


import networkx as nx
import random

Number_of_nodes=10
p=0.4

G=nx.Graph()
for n in range(Number_of_nodes): 
    G.add_node(n)

node_list=G.nodes()

#generate the graph adding ad edge for each possible couple of nodes
for i1 in range(len(node_list)-1):
    for i2 in range(i1+1,len(node_list)):
        if random.random()<p:
            G.add_edge(node_list[i1],node_list[i2])

pos=nx.circular_layout(G)   
nx.draw(G, pos,with_labels=True)
 


# ### Randomizing Graphs

# In[ ]:


number_of_swaps=2

while number_of_swaps>0:
    #pick at random a couple of edges and verify 
    #they don't share nodes
    edges_to_swap=random.sample(G.edges(),2)
    e0=edges_to_swap[0]
    e1=edges_to_swap[1]

    if len(set([e0[0],e0[1],e1[0],e1[1]]))<4: continue

    #check if the edge already exists and eventually add it
    if not G.has_edge(e0[0],e1[1]):
        G.add_edge(e0[0],e1[1])
    G.remove_edge(e0[0], e0[1])
    if not G.has_edge(e0[1],e1[0]):
        G.add_edge(e0[1],e1[0])
    G.remove_edge(e1[0], e1[1])

    number_of_swaps-=1

pos=nx.circular_layout(G)   
nx.draw(G, pos,with_labels=True)


# ### Configuration model

# In[ ]:


degree_sequence=[6, 4, 3, 2, 1, 1, 1]

#this generate the list of uppercast chars as labels for the nodes
uppercase_char_list=[chr(i) for i in xrange(65,91)]

degree_sequence.sort(reverse=True)
#degree sequence
print "degree sequence:",degree_sequence

stub_list=[]

for deg in degree_sequence:
    label=uppercase_char_list.pop(0)
    for stub in range(deg):
        stub_list.append(label)


print "ordered stub labels",stub_list

random.shuffle(stub_list)

print "shuffled stub labels",stub_list

MG = nx.MultiGraph()

while stub_list!=[]:
    node1=stub_list.pop(0)
    node2=stub_list.pop(0)
    MG.add_edge(node1,node2)

print "graph edge list:",MG.edges()


# ### Gravity Model

# In[ ]:


import scipy.optimize as optimization
import numpy

# Generate artificial data = straight line with a=0 and b=1
# plus some noise.
xdata = numpy.array([0.0,1.0,2.0,3.0,4.0,5.0])
ydata = numpy.array([0.1,0.9,2.2,2.8,3.9,5.1])

sigma = numpy.array([1.0,1.0,1.0,1.0,1.0,1.0])

# Initial guess.
x0    = numpy.array([0.0, 0.0, 0.0])

#defining the gravitational function
def func(x, a, b, c):
    return a + b*x + c*x*x

#optimization
import scipy.optimize as optimization

print optimization.curve_fit(func, xdata, ydata, x0, sigma)


# ### Fitness Model

# In[ ]:


import math

G=nx.Graph()

#this is our z(N)
ave_value=1.0
N=5000
    
def fitness_function():
    return random.expovariate(4.0/ave_value)

def generate_function(x1,x2):
    if x1+x2-ave_value<0.0:
        return 0
    else:
        return 1
    
for n in range(N):
    G.add_node(n,fitness=fitness_function())

node_list=G.nodes()
    
#generate the graph adding ad edge for each possible couple of nodes
for i1 in range(len(node_list)-1):
    for i2 in range(i1+1,len(node_list)):
        x1=G.node[node_list[i1]]['fitness']
        x2=G.node[node_list[i2]]['fitness']
        if generate_function(x1,x2)==1:
            G.add_edge(node_list[i1],node_list[i2])

degree_sequence=sorted(nx.degree(G).values(),reverse=True)

hist(degree_sequence,bins=15)


# ### Barabasi-Albert Model

# In[ ]:


N0=6
p=0.6
new_nodes=1000

G=nx.gnp_random_graph(N0, p)

for eti in range(new_nodes):
    m=3
    new_eti="_"+str(eti)
    target_nodes=[]
    while m!=0:
        part_sum=0.0
        rn=random.random()
        for n in G.nodes():
            base=part_sum
            step=part_sum+G.degree(n)/(G.number_of_edges()*2.0)
            part_sum=part_sum+G.degree(n)/(G.number_of_edges()*2.0)
            if rn>=base and rn<step:
                if n in target_nodes: break
                target_nodes.append(n)
                m=m-1
                break
                
    for n_tar in target_nodes:
        G.add_edge(new_eti,n_tar)

degree_sequence=sorted(nx.degree(G).values(),reverse=True)

hist(degree_sequence,bins=15)


# In[ ]:




