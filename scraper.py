import urllib
from xml.etree import ElementTree
from xml.dom.minidom import parse
from xml.dom.minidom import parseString
from ebayScrap.ebaysdk.finding import Connection
from ebayScrap.ebaysdk.exception import ConnectionError
import ebayScrap.ebaysdk
from bs4 import BeautifulSoup
# '''
# itemId - 0
# itemName - 1
# categoryName - 2
# itemPrice - 3
# pictureLink - 4
#
# '''
#
#
#
# def parseItem(item):
#     myList = []
#     myList.append(item['itemId'])
#     myList.append(item['title'])
#     myList.append(item['primaryCategory']['categoryName'])
#     myList.append(item['galleryURL'])
#     myList.append(item['sellingStatus']['currentPrice']['value'])
#     return myList
#
#
# # appId = 'omerShac-GoSwap-PRD-345f30466-968717a1'
# # try:
# #     api = Connection(appid=appId, config_file=None)
# #     response = api.execute('findItemsAdvanced',
# #                            {'keywords': 'frisbee',
# #                             'category': ''})
# #     myRes = response.dict()
# #     results = myRes['searchResult']['item']
# #     for item in results:
# #         print(parseItem(item))
# #         continue
# #
#
# #
# # except ConnectionError as e:
# #     print(e.message)
# # except Exception as e:
# #     print(e)
#
# import urllib.request
# import pickle
# def getCategoryChilds(cid):
#     subCatL = []
#     with urllib.request.urlopen('http://open.api.ebay.com/Shopping?callname=GetCategoryInfo&appid=omerShac-GoSwap-PRD-345f30466-968717a1&siteid=0&CategoryID=%s&version=729&IncludeSelector=ChildCategories' %cid) as response:
#         root = parse(response)
#         for subCat in root.getElementsByTagName('Category'):
#
#             d = dict()
#             id = subCat.getElementsByTagName('CategoryID')[0].firstChild.nodeValue
#             if(id == cid):
#                 continue
#             d['id'] = id
#             d['name'] = subCat.getElementsByTagName('CategoryName')[0].firstChild.nodeValue
#             try:
#                 print("Checking for %s id number %s" % (d['name'], id))
#             except Exception as e:
#                 print("nvm..")
#             if(subCat.getElementsByTagName('LeafCategory')[0].firstChild.nodeValue == 'true'):
#                 subCatL.append(d)
#                 continue
#             d['sub'] = getCategoryChilds(d['id'])
#             subCatL.append(d)
#     return subCatL
# a = getCategoryChilds(-1)
import dicttoxml
import pickle
with open('categoriesNew','rb') as f:
    a = pickle.load(f)
myDick = dict()
myDick['elems'] = a
d = dicttoxml.dicttoxml(myDick, attr_type=False)
with open('categories.xml','wb') as f:
    f.write(parseString(d).toprettyxml(encoding='utf-8'))
# with open('categoriesNew','wb') as f:
#     pickle.dump(a, f)