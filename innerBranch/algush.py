from bs4 import BeautifulSoup as soup
import networkx as nx
import math
class soupFacade:
    def __init__(self):
        self.factor = lambda x:math.sin(x/2)*3
        f = open('categories.xml', 'rb')
        self.soup = soup(f, 'lxml')
        self.loadAncestors()

    def loadAncestors(self):
        try:
            with open('ancestors.pickle', 'rb') as f:
                self.ancestors = pickle.load(f)
        except Exception as e:
            self.ancestors = dict()

    def findAncestors(self,id):
        if(id in self.ancestors.keys()):
            return self.ancestors[id]
        try:
            elem = self.soup.find_all(lambda x: x.text == id)[0]
            elem = elem.parent
            ancestors = []
            ancestors.append((elem.id.text, elem.catname.text))
            while (elem.id.text != '-1'):
                try:
                    elem = elem.parent.parent
                    ancestors.append((elem.id.text, elem.catname.text))
                except Exception as e:
                    print(e)
                    break
            self.ancestors[id] = ancestors
        except Exception as e:
            print('something went wrong')
            return []
        return ancestors

    def LCA(self,a,b):
        print('trying to go from %s to %s'%(a,b))
        aAncestors = self.findAncestors(a)
        bAncestors = self.findAncestors(b)
        minA = 0
        minB = 0
        for elem in aAncestors:
            if(elem in bAncestors):
                break
            minA+=1
        for elem in bAncestors:
            if (elem in aAncestors):
                break
            minB += 1
        return self.factor(min(minA,minB))

    def pickleSave(self):
        with open('ancestors.pickle', 'wb') as f:
            pickle.dump(self.ancestors,f)


import pickle
class graphManager:
    def __init__(self,db):
        self.soup = soupFacade()
        self.db = db
        self.loadGraph()

    def loadGraph(self):
        try:
            with open('lastGraph.pickle','rb') as f:
                self.graph = pickle.load(f)
        except Exception as e:
            print('cant find pickle loading from db.')
            info = self.db.getAllSwaps()
            self.graph = nx.DiGraph()
            for row in info:
                give,get = row
                self.graph.add_edge(get,give)

    def updateGraph(self,swapItem,choices):
        self.graph.add_node(swapItem)
        for elem in choices:
            self.graph.add_edge(elem,swapItem)


    def performAstar(self,idFrom,idTo):
        print('performing astar')
        try:
            score = nx.astar_path(self.graph,idFrom,idTo,self.soup.LCA)
            return score
        except nx.NetworkXNoPath as np:
            print("no results buddy")
            return None

    def pickleSave(self):
        print('saving my pickles!')
        self.soup.pickleSave()
        with open('lastGraph.pickle', 'wb') as f:
            pickle.dump(self.graph, f)



