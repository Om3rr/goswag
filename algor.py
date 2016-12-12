from bs4 import BeautifulSoup as soup
import networkx as nx
class soupFacade:
    def __init__(self):
        f = open('categories.xml', 'rb')
        self.soup = soup(f, 'lxml')
        a = self.soup.find_all(text='181077')
        print(a)
        print(a.final_all(name='sub'))
        print('hhh')
        print('hhh')

    def findAncestors(self,id):
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
        return ancestors

    def LCA(self,a,b):
        aAncestors = self.findAncestors(a)
        bAncestors = self.findAncestors(b)
        minA = 0
        minB = 0
        print(aAncestors)
        print(bAncestors)
        for elem in aAncestors:
            if(elem in bAncestors):
                print(aAncestors[0:minA])
                break
            minA+=1
        for elem in bAncestors:
            if (elem in aAncestors):
                print(bAncestors[0:minB])
                break
            minB += 1
        return min(minA,minB)


import matplotlib.pyplot as plt
a = {1:[2,3,4,5,6,7],2:[3,4,5,6,7],3:[4,5,6,7,8,9,0],4:[],5:[],6:[],7:[],8:[],9:[]}
# a = {1444444:[244444],2:[34444441],3:[3214],4:[43215],5:[643,4,234121234,21234,1]}
g = nx.DiGraph()
for key in a.keys():
    g.add_node(key)
    for elem in a[key]:
        g.add_edge(key,elem)
# nx.draw_random(g)
def heuristic(x,y):
    print('running heuristic with %s and %s'%(x,y))
    return x*y

print(nx.astar_path(g,1,9,heuristic))

