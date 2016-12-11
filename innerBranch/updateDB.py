from mainApp import connect, loadCategories
from clientCareClass import dbWrapper, categoryBrowser
cat = categoryBrowser(loadCategories())
db = connect()

mainCat = cat.getMainCat()
for elem in mainCat:
    subCat = cat.getSubCat(elem[0])[1:]
    for subElem in subCat:
        sub = subElem[0]
        subsub = cat.getAllSubSubCategories(elem[0], subElem[0])
        with db.cursor() as cursor:
            try:
                if(len(subsub) == 1):
                    a = "UPDATE items SET subCategoryId = %s WHERE categoryId = %s;" %(sub, subsub[0])
                else:
                    a = "UPDATE items SET subCategoryId = %s WHERE categoryId IN %s;" %(sub, subsub)
                cursor.execute(a)
                db.commit()
                print("Commited %s"%subElem[1])
            except Exception as e:
                print(e)
                print(a)

