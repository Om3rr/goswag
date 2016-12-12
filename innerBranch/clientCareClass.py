from itertools import chain
class userCare:
    def __init__(self, userId, db, catBrowser,graph):
        self.id = userId
        self.db = dbWrapper(db)
        self.swapItem = None
        self.choices = []
        self.cat = catBrowser
        self.tempMainCat = None
        self.graph = graph

    def getListFromCat(self,catId):
        return self.db.getCat(catId)

    def selectItem(self,itemId):
        if(self.swapItem is None):
            self.swapItem = itemId
        else:
            self.choices.append(itemId)

    def endSession(self,user,email):
        self.db.addSwap(user,email, self.swapItem, self.choices)

    def getMsg(self,msg):
        return self.messageParser(msg)

    def messageParser(self,s):
        messageCode = s[0]
        messageInfo = s[1]
        if (messageCode == "getMainCat"):
            return self.cat.getMainCat()
        elif (messageCode == "getSubCategories"):
            self.tempMainCat = messageInfo
            return self.cat.getSubCat(messageInfo)
        elif (messageCode == "getCatElems"):
            return self.db.getItemsByCategory(messageInfo)
        elif (messageCode == "selPic"):
            if(self.swapItem == None):
                self.swapItem = messageInfo
            else:
                self.choices.append(messageInfo)
            return [0]
        elif (messageCode == 'submit'):
            import time
            time.sleep(2)
            mail,name = messageInfo.split('*')
            self.db.addSwap(self.swapItem,self.choices,mail,name)
            self.graph.updateGraph(self.swapItem, self.choices)
            for choice in self.choices:
                score = self.graph.performAstar(self.swapItem,choice)
                if(score == None):
                    continue

            if(score != None):
                return self.db.scoreToWin(score)
            print('no findings buddy, try another thing!')
            return [-1]

        return []


class dbWrapper:
    def __init__(self,db):
        self.db = db
    def getItemsByCategory(self,category):
        a = 'select categoryId, itemName, image from items where subCategoryId = %s \nlimit 32;' %category
        with self.db.cursor() as curs:
            try:
                curs.execute(a)
                results = curs.fetchall()
            except Exception as e:
                print(a)
                return []
        print('found %s items'%len(results))
        return [list(x) for x in results]

    def addSwap(self,swapItem, choices, mail,uname):
        a = 'insert into swaps (userId,igive, iget) values(%s,%s,%s)'
        b = 'insert into userslist(userName,email) values("%s","%s")'%(mail,uname)

        with self.db.cursor() as curs:
            try:
                curs.execute(b)
                curs.executemany(a,[(mail,swapItem,x) for x in choices])
                print('execute succesfuly!')
            except Exception as e:
                print(e)
        self.db.commit()

    def getAllSwaps(self):
        a = 'select igive,iget from swaps'
        with self.db.cursor() as curs:
            try:
                curs.execute(a)
                info = curs.fetchall()
            except Exception as exc:
                print(exc)
        return info

    def scoreToWin(self,score):
        edges = [(score[i],score[i+1]) for i in range(len(score)-1)]
        fullList = []
        a = 'select userId from swaps where igive = %s and iget = %s'
        with self.db.cursor() as curs:
            print(score)
            for elem in edges:
                curs.execute(a %(elem[1],elem[0]))
                fullList.append([elem[0],elem[1],curs.fetchone()[0]])
        print(fullList)

        return fullList






class categoryBrowser:
    def __init__(self, cl):
        self.d = cl

    def getMainCat(self):
        return [(x['id'],x['name']) for x in self.d][1:]

    def getSubCat(self, id, d=None):
        entry = None
        for elem in self.d:
            if(elem['id'] == id):
                entry = elem
                break
        return [('-1','Return to categories')]+[(x['id'],x['name']) for x in entry['sub']]

    def getAllSubSubCategories(self,mainCategory, subCatId):
        entry = None
        for elem in self.d:
            if (elem['id'] == mainCategory):
                entry = elem
                break
        if(not entry):
            return []
        for elem in entry['sub']:
            if(elem['id'] == subCatId):
                newEntry = elem
                break
        if(not entry):
            return []
        l = []
        self.allMySons(newEntry, l)
        return tuple(l)


    def allMySons(self, entry, l):
        if('sub' not in entry.keys()):
            l.append(entry['id'])
            return
        [self.allMySons(elem,l) for elem in entry['sub']]

