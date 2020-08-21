#!/usr/bin/env python
# coding: utf-8

# # Chapter I - Food Webs

# ## Read the Adjacency Matrix

# In[ ]:


adjacency_matrix=[
                  [0,1,0,1],
                  [1,0,1,1],
                  [0,1,0,0],
                  [1,1,0,0]
                  ]


# ### Browsing the rows

# In[ ]:


for row in adjacency_matrix:
    print row


# ### Browsing the link information

# In[ ]:


for row in adjacency_matrix:
    for a_ij in row:
        print a_ij,
    print "\r"


# ### Directed Networks

# In[ ]:


#in the case of directed networks the adjacency matrix is not symetric, like for Food Wes
#if a non zero element is present in row 2, column 3, this means there is an arc (directed edge)
#from node 2 toward node 3
adjacency_matrix_directed=[
                  [0,1,0,1],
                  [0,0,1,0],
                  [0,0,0,1],
                  [0,0,0,0]
                  ]


# ## Basic Statistics

# In[ ]:


#the number of species is the number of rows or columns of 
#the adjacency matrix
num_species=len(adjacency_matrix_directed[0])

#the number of links or predations is the non zero elements 
#of the adjacency matrix (this holds for directed graphs
num_predations=0
for i in range(num_species):
    for j in range(num_species):
        if adjacency_matrix_directed[i][j]!=0:
            num_predations=num_predations+1

#to check if a specie is a Basal (B), an Intermediate (I) or
#a Top (T) one  we have to check the presence of 1s both in 
#the row and in the column of each specie
row_count=[0,0,0,0]
column_count=[0,0,0,0]
for i in range(num_species):
    for j in range(num_species):
        row_count[i]=row_count[i]+adjacency_matrix_directed[i][j]
        column_count[j]=column_count[j]+         adjacency_matrix_directed[i][j]

number_B=0
number_I=0
number_T=0

for n in range(num_species):
    if row_count[n]==0:
        number_T+=1
        continue
    if column_count[n]==0:
        number_B+=1
        continue
    else:
        number_I+=1
   
print "number of species", num_species
print "number of predations", num_predations
print "classes Basal, Top, Intermediate: ",number_B,number_T,number_I
print "connectance", float(num_predations)/float(num_species**2)


# ## The Degree

# In[ ]:


#for the undirected network
degree_node_2=0
for j in adjacency_matrix[1]:
    degree_node_2=degree_node_2+j
print "degree of node 2:",degree_node_2

#and for the directed case we already calculated the sum over 
#the rows and columns for the adjacency_matrix_directed
out_degree_node_3=row_count[2]
in_degree_node_4=column_count[3]

print "out_degree node 3:",out_degree_node_3
print "in_degree node 4:",in_degree_node_4


# ## Degree in Networkx

# In[ ]:


import networkx as nx

#generate an empty graph
G=nx.Graph()

#define the nodes
G.add_node(1)
G.add_node(2)
G.add_node(3)
G.add_node(4)

#link the nodes
G.add_edge(1,2)
G.add_edge(1,4)
G.add_edge(2,3)
G.add_edge(2,4)

#degree of the node 2
print G.degree(2)


# ### Degree sequence

# In[ ]:


degree_sequence=[]
for row in range(len(adjacency_matrix)):
    degree=0
    for j in adjacency_matrix[row]:
        degree=degree+j
    degree_sequence.append(degree)

print degree_sequence


# ## Histogram

# In[ ]:


# this command is to activate the graphic interface
get_ipython().run_line_magic('pylab', 'inline')


# In[ ]:


import matplotlib.pyplot as plt

plt.hist([1,1,1,1,1,1,1,2,2,2,3,3,4,5],bins=5)
plt.show()


# ## Clustering Coefficient

# In[ ]:


row=1 #stands for the node 2
node_index_count=0
node_index_list=[]
for a_ij in adjacency_matrix[row]:
    if a_ij==1:
        node_index_list.append(node_index_count)
    node_index_count=node_index_count+1    
print "\r"

print node_index_list

#then we will check for all the possible neighbours couples if a link actually exist:

neighb_conn=0
for n1 in node_index_list:
    for n2 in node_index_list:
        if adjacency_matrix[n1][n2]==1:
            neighb_conn=neighb_conn+1
   
#we have indeed counted them twice...
neighb_conn=neighb_conn/2.0

print neighb_conn

#Finally the clustering coefficient for node '2' is given by the expression:

clustering_coefficient=neighb_conn/ (degree_node_2*(degree_node_2-1)/2.0) 

print clustering_coefficient


# ## Generating the bowtie stucture

# In[21]:


get_ipython().system('pip install PyDrive')


# In[ ]:


# Code to read csv file into Colaboratory:!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials# Authenticate and create the PyDrive client.
# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)


# In[ ]:


downloaded = drive.CreateFile({'id':'1TlwzHkK7Ey1CAXCzIOZt94mSkXfu9V0K'})
downloaded.GetContentFile('Ythan_Estuary.txt')


# In[26]:


#loading the network
#file_name="./data/Ythan_Estuary.txt"
#file_name="Ythan_Estuary.txt"

DG = nx.DiGraph()

in_file=open(file_name,'r')
while True:
    next_line=in_file.readline()
    if not next_line:
        break
    next_line_fields=next_line[:-2].split(' ')
    node_a=next_line_fields[1] #there is a space in the beginning 
                               #of each edge
    node_b=next_line_fields[2]
    DG.add_edge(node_a, node_b)

#deleting the environment
DG.remove_node('0')

#getting the biggest strongly connected component
scc=[(len(c),c) for c in sorted( nx.strongly_connected_components                                (DG), key=len, reverse=True)][0][1]

#preparing the IN and OUT component
IN_component=[]
for n in scc:
    for s in DG.predecessors(n):
        if s in scc: continue
        if not s in IN_component:
            IN_component.append(s)
            
OUT_component=[]
for n in scc:
    for s in DG.successors(n):
        if s in scc: continue
        if not s in OUT_component:
            OUT_component.append(s)

#generating the subgraph
bowtie=scc+IN_component+OUT_component
DG_bowtie = DG.subgraph(bowtie)

#defining the proper layout
pos={}
in_y=100.
pos['89']=(150.,in_y)

in_step=700.
for in_n in IN_component:
    pos[in_n]=(100.,in_y)
    in_y=in_y+in_step

out_y=100.
out_step=500.   
for out_n in OUT_component:
    pos[out_n]=(200,out_y)
    out_y=out_y+out_step

pos['90']=(150.,out_y)
    
#plot the bowtie structure
nx.draw(DG_bowtie, pos, node_size=50)

nx.draw_networkx_nodes(DG_bowtie, pos, IN_component,                        node_size=100, node_color='Black')
nx.draw_networkx_nodes(DG_bowtie, pos, OUT_component,                        node_size=100, node_color='White')
nx.draw_networkx_nodes(DG_bowtie, pos, scc,                        node_size=200, node_color='Grey')

savefig('./data/bowtie.png',dpi=600)


# ## Distance with Breadth First Search

# ### create the undirected graph

# In[27]:


#creating the graph
G=nx.Graph()
G.add_edges_from([('A','B'),('A','C'),('C','D'),('C','E'),('D','F'),
('D','H'),('D','G'),('E','H'),('E','I')])

#printing the neighbors of the node 'A'
print G.neighbors('A')

nx.draw(G)


# In[28]:


root_node='A'
queue=[]
queue.append('A')
G.node['A']["distance"]=0
while len(queue):
    working_node=queue.pop(0)
    for n in G.neighbors(working_node):
        if len(G.node[n])==0:
            G.node[n]["distance"]=G.node[working_node]["distance"]+1
            queue.append(n)
for n in G.nodes():
    print n,G.node[n]["distance"]
    


# ## Reading the file with Food Web data

# In[ ]:


file_name="./data/Little_Rock_Lake.txt"

DG = nx.DiGraph()

in_file=open(file_name,'r')
while True:
    next_line=in_file.readline()
    if not next_line:
        break
    next_line_fields=next_line[:-2].split(' ')
    node_a=next_line_fields[1] #there is a space in the beginning 
                               #of each edge
    node_b=next_line_fields[2]
    print node_a,node_b
    DG.add_edge(node_a, node_b)


# ## Trophic Species

# ## Defining the trophic pattern key
# this is a way to generate a unique key starting from the ordered lists of preys and predators attached to nodes

# In[ ]:


def get_node_key(node):
    out_list=[]
    for out_edge in DG.out_edges(node):
        out_list.append(out_edge[1])
    in_list=[]
    for in_edge in DG.in_edges(node):
        in_list.append(in_edge[0])
    out_list.sort()
    out_list.append('-')
    in_list.sort()
    out_list.extend(in_list)
    return out_list


# ## Grouping the Trophic Species and Regenerating the Trophic network

# In[ ]:


def TrophicNetwork(DG):
    trophic={}
    for n in DG.nodes():
        k=tuple(get_node_key(n))
        if not trophic.has_key(k):
            trophic[k]=[]
        trophic[k].append(n)
    for specie in trophic.keys():
        if len(trophic[specie])>1:
            for n in trophic[specie][1:]:
                DG.remove_node(n)
    return DG

#deleting the environment
DG.remove_node('0')

TrophicDG=TrophicNetwork(DG)
print "S:",TrophicDG.number_of_nodes()
print "L:",TrophicDG.number_of_edges()
print "L/S:",float(TrophicDG.number_of_edges())/ TrophicDG.number_of_nodes()


# ## Classes in Food Webs

# In[ ]:


def compute_classes(DG):
    basal_species=[]
    top_species=[]
    intermediate_species=[]
    for n in DG.nodes():
        if DG.in_degree(n)==0:
            basal_species.append(n)
        elif DG.out_degree(n)==0:
            top_species.append(n)
        else:
            intermediate_species.append(n)
    return (basal_species,intermediate_species,top_species)

(B,I,T)=compute_classes(TrophicDG)
print "B:",float(len(B))/(len(B)+len(T)+len(I))
print "I:",float(len(I))/(len(B)+len(T)+len(I))
print "T:",float(len(T))/(len(B)+len(T)+len(I))


# ## Proportion of links among classes and ratio prey/predators

# In[ ]:


def InterclassLinkProportion(DG,C1,C2):
    count=0
    for n1 in C1:
        for n2 in C2:
            if DG.has_edge(n1,n2):
                count+=1
    return float(count)/DG.number_of_edges()
    
print "links in BT:",InterclassLinkProportion(TrophicDG,B,T)
print "links in BI:",InterclassLinkProportion(TrophicDG,B,I)
print "links in II:",InterclassLinkProportion(TrophicDG,I,I)
print "links in IT:",InterclassLinkProportion(TrophicDG,I,T)

#Ratio prey/predators
print "P/R:",float((len(B)+len(I)))/(len(I)+len(T))


# In[ ]:




