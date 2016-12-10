
class userCare:
    def __init__(self, userId, db):
        self.id = userId
        self.db = dbWrapper(db)
        self.swapItem = None
        self.choices = []

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
        if (messageCode == "getCatElems"):
            return self.db.getItemsByCategory(messageInfo)
        if (messageCode == "newImageSelect"):
            print("image number %s selected" %messageInfo)
            return 'returnCategories'
        return []


class dbWrapper:
    def __init__(self,db):
        self.db = db
    def getItemsByCategory(self,category):
        a = 'select itemId, itemName, image from items where categoryId = %s limit 100' %category
        with self.db.cursor() as curs:
            curs.execute(a)
            results = curs.fetchall()
        return [list(x) for x in results]