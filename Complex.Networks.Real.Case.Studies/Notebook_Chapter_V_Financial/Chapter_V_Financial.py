#!/usr/bin/env python
# coding: utf-8

# # Chapter V Finance

# In[2]:


get_ipython().run_line_magic('pylab', 'inline')


# ## Connecting with the Yahoo! Finance service

# In[3]:


import yahoo_finance as yf

yahoo = yf.Share('YHOO')
d=yahoo.get_historical('2014-05-19', '2014-05-20')
print "A week of stock daily quotations:"
for e in d:
    print e
print "Info about the company:",yahoo.get_info()
print "Market capitalization in dollars:",yahoo.get_market_cap()


# ## Transaction volumes computation and plotting

# In[4]:


d=yahoo.get_historical('2014-01-01', '2014-12-31')
V = []
for s in d:
    print s['Date'],float(s['Volume'])*float(s['Adj_Close'])
    V.append(float(s['Volume'])*float(s['Adj_Close']))

plot(V)
savefig('yahoo_volume.png')


# # Download NYSE tickers
# ### with all the information related to the market capitalization, sector and industry...
# ### (http://www.nasdaq.com/screening/company-list.aspx)

# In[5]:


get_ipython().system('head ./data/companylist.csv ')


# ## Get Stock Labels, Sector and Industries

# In[8]:


#this code will take approximative 1 hour to retrieve the data
#depending on the internet connection
#if you want to skip this procedure just uncomment the following lines
import sys
f=open("./data/list_stocks_50B_6_may_2016.txt",'r')
list_stocks=[]
while True:
    next_line=f.readline()
    if not next_line: break
    list_stocks.append(tuple(next_line.split('\t')[:-1]))
f.close()
sys.exit(1)

import time

hfile=open("./data/companylist.csv",'r')
#we choose to get only companies with a market capitalisation
#greater than 50B$
cap_threshold=50.0 

list_stocks=[]
nextline=hfile.readline()
while True:
    nextline=hfile.readline()
    if not nextline:
        break
    line=nextline.split(',')
    sym=line[0][1:-1]
    share = yf.Share(sym)
    y_market_cap=share.get_market_cap()
    if not y_market_cap: continue
    #we will exclude stocks with char ’^’ that will
    #give errors in the query process
    if y_market_cap[-1]=='B' and float(y_market_cap         [:-1])>cap_threshold and line[0].find('^')==-1:
        print sym,y_market_cap
        list_stocks.append((line[0][1:-1],line[1][1:-1],                            line[5][1:-1],line[6][1:-1]))
    time.sleep(1)

hfile.close()

print list_stocks[0]


# ## Generate dictionaries for companies, sectors and colors

# In[9]:


diz_sectors={}
for s in list_stocks:
    diz_sectors[s[0]]=s[2]

list_ranking=[]
for s in set(diz_sectors.values()):
    list_ranking.append((diz_sectors.values().count(s),s))

list_ranking.sort(reverse=True)

#list_colors=['red','green','blue','black''cyan','magenta','yellow'] 
list_colors=['0.0', '0.2', '0.4', '0.6','0.7', '0.8', '0.9'] 

#'white' is an extra color for 'n/a' and 'other' sectors

diz_colors={}

#association color and more represented sectors
for s in list_ranking:
    if s[1]=='n/a': 
        diz_colors[s[1]]='white'
        continue
    if list_colors==[]: 
        diz_colors[s[1]]='white'
        continue
    diz_colors[s[1]]=list_colors.pop(0)


# ## Retrieving historical data

# In[10]:


start_period='2013-05-01'
end_period='2014-05-31'
diz_comp={}
for s in list_stocks:
    print s[0]
    stock = yf.Share(s[0])
    diz_comp[s[0]]=stock.get_historical(start_period, end_period)

#create dictionaries of time series for each company
diz_historical={}
for k in diz_comp.keys():
    if diz_comp[k]==[]: continue
    diz_historical[k]={}
    for e in diz_comp[k]:
        diz_historical[k][e['Date']]=e['Close']

for k in diz_historical.keys():
    print k,len(diz_historical[k])


# ## Return of prices

# In[37]:


reference_company='ABEV'
diz_returns={}
d=diz_historical[reference_company].keys()
d.sort()
print len(d),d

for c in diz_historical.keys():
    #check if the company has the whole set of dates
    if len(diz_historical[c].keys())<len(d): continue
    diz_returns[c]={}
    for i in range(1,len(d)):
        #price returns
        diz_returns[c][d[i]]=math.log(         float(diz_historical[c][d[i]]))         -math.log(float(diz_historical[c][d[i-1]]))

print diz_returns[reference_company]


# ## Basic Statistics and the Correlation Coefficient

# In[38]:


#mean
def mean(X):
    m=0.0
    for i in X:
        m=m+i
    return m/len(X)

#covariance
def covariance(X,Y):
    c=0.0
    m_X=mean(X)
    m_Y=mean(Y)
    for i in range(len(X)):
        c=c+(X[i]-m_X)*(Y[i]-m_Y)
    return c/len(X)

#pearson correlation coefficient
def pearson(X,Y):
    return covariance(X,Y)/(covariance(X,X)**0.5 *                             covariance(Y,Y)**0.5)


# ## Correlation of price returns

# In[39]:


def stocks_corr_coeff(h1,h2):
    l1=[]
    l2=[]
    intersec_dates=set(h1.keys()).intersection(set(h2.keys()))
    for d in intersec_dates:
        l1.append(float(h1[d]))
        l2.append(float(h2[d]))
    return pearson(l1,l2)

#correlation with the same company has to be 1!
print stocks_corr_coeff(diz_returns[reference_company],                         diz_returns[reference_company])


# ## Build the correlation Network

# In[40]:


import math
import networkx as nx

corr_network=nx.Graph()

num_companies=len(diz_returns.keys())
for i1 in range(num_companies-1):
    for i2 in range(i1+1,num_companies):
        stock1=diz_returns.keys()[i1]
        stock2=diz_returns.keys()[i2]
        #metric distance
        metric_distance=math.sqrt(2*(1.0-stocks_corr_coeff                (diz_returns[stock1],diz_returns[stock2])))
        #building the network
        corr_network.add_edge(stock1, stock2, weight=metric_distance)

print "number of nodes:",corr_network.number_of_nodes()
print "number of edges:",corr_network.number_of_edges()


# In[ ]:


number of nodes: 123
number of edges: 7503


# ## Minimum Spanning Tree with ([Prim's algorithm](http://en.wikipedia.org/wiki/Prim%27s_algorithm))

# In[41]:


tree_seed=reference_company
N_new=[]
E_new=[]
N_new.append(tree_seed)
while len(N_new)<corr_network.number_of_nodes():
    min_weight=10000000.0
    for n in N_new:
        for n_adj in corr_network.neighbors(n):
            if not n_adj in N_new:
                if corr_network[n][n_adj]['weight']<min_weight:
                    min_weight=corr_network[n][n_adj]['weight']
                    min_weight_edge=(n,n_adj)
                    n_adj_ext=n_adj
    E_new.append(min_weight_edge)
    N_new.append(n_adj_ext)

#generate the tree from the edge list
tree_graph=nx.Graph()
tree_graph.add_edges_from(E_new)

#setting the color attributes for the network nodes
for n in tree_graph.nodes():
    tree_graph.node[n]['color']=diz_colors[diz_sectors[n]]


# ## Printing the Financial Minimum Spanning Tree

# In[51]:


pos=nx.graphviz_layout(tree_graph,prog='neato',                        args='-Gmodel=subset -Gratio=fill')

figure(figsize=(20,20))
nx.draw_networkx_edges(tree_graph,pos,width=2,                        edge_color='black', alpha=0.5, style="solid")
nx.draw_networkx_labels(tree_graph,pos)
for n in tree_graph.nodes():
    nx.draw_networkx_nodes(tree_graph, pos, [n], node_size = 600,     alpha=0.5, node_color = tree_graph.node[n]['color'],     with_labels=True)

axis('off')

savefig('./data/MST_50B_new.png',dpi=600)


# In[ ]:




