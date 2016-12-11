import urllib
from xml.etree import ElementTree
from xml.dom.minidom import parse
# from ebayScrap.ebaysdk.finding import Connection
from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError
# from ebayScrap.ebaysdk.exception import ConnectionError
# import ebayScrap.ebaysdk
import urllib.request
import pickle
from bs4 import BeautifulSoup
import MySQLdb
from clientCareClass import categoryBrowser
from mainApp import loadCategories


def connect():
    try:
        db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="",  # your password
                         db="ebayset")  # name of the data base
    except Exception as e:
        print(e)
        exit()
    return db



def parseItem(item):
    myList = []
    myList.append(item['itemId'])
    myList.append(str(item['title']).encode('utf-8'))
    myList.append(item['primaryCategory']['categoryId'])
    myList.append(str(item['primaryCategory']['categoryName']).encode('utf-8'))
    myList.append(item['galleryURL'])
    myList.append(item['sellingStatus']['currentPrice']['value'])
    if(myList[0] in itemsSet):
        print("Houston we have a problem")
    itemsSet.add(myList[0])
    return myList

def searchForItems(api, category):
    items = []
    response = api.execute('findItemsByCategory', {'categoryId': str(category),'paginationInput':{'entriesPerPage':40}})
    myRes = response.dict()
    if('searchResult' not in myRes.keys()):
        return []
    results = myRes['searchResult']['item']
    for item in results:
        if(item['itemId'] in itemsSet):
            continue
        if('galleryURL' not in item.keys()):
            continue
        items.append(parseItem(item))

    return items

def insertToDb(items,db,subCat):
    with db.cursor() as curs:
        query = "INSERT INTO items (itemId, itemName, categoryId, categoryName, image, price, subCategoryId) VALUES (%s,%s,%s,%s,%s,%s,%s);"
        try:
            curs.executemany(query, [tuple(x+[subCat]) for x in items])
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
            db.close()
            exit()



appId = 'omerShac-GoSwap-PRD-345f30466-968717a1'
api = Connection(appid=appId, config_file=None)
db = connect()
itemsSet = set()
cat = categoryBrowser(loadCategories())
mainCat = cat.getMainCat()
for elem in mainCat:
    subCat = cat.getSubCat(elem[0])[1:]
    for subElem in subCat:
        sub = subElem[0]
        items = searchForItems(api,sub)
        print("Yo")
        insertToDb(items,db,sub)
