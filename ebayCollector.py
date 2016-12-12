import urllib
from xml.etree import ElementTree
from xml.dom.minidom import parse
from ebayScrap.ebaysdk.finding import Connection
from ebayScrap.ebaysdk.exception import ConnectionError
import ebayScrap.ebaysdk
import urllib.request
import pickle
from bs4 import BeautifulSoup
import MySQLdb
from innerBranch.clientCareClass import categoryBrowser
from innerBranch.mainApp import loadCategories
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
    response = api.execute('findItemsByCategory', {'categoryId': str(category)})
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
    query = "INSERT INTO items (itemId, itemName, categoryId, categoryName, image, price) VALUES (%s,%s,%s,%s,%s,%s);"
    try:
        curs.executemany(query, [tuple(x) for x in d])
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
        print(sub)






#
# with db.cursor() as curs:
#     up = curs.execute('select itemId from items')
#     for itemIds in curs.fetchall():
#         itemsSet.add(str(itemIds[0]))
#     t = "Electrical & Test Equipment,Containers & Pre-Fab Buildings,Hand Tools,Industrial Supply/MRO,Industrial Tools,Manufacturing & Woodworking,Medical/Lab Equipment,Metalworking/Milling/Welding,Office Equipment & Supplies,Packing & Posting Supplies,Power Tools,Printing & Graphic Arts,Restaurant & Catering,Retail & Shop Fitting,Telephone & Answering Systems,Video Broadcasting & Recording,Web Domains/ Email/ Software,Other Business & Industrial,Camcorders,Camera Drones,Camera Drone Parts & Accs,Digital Cameras,Camera & Photo Accessories,Film Photography,Flashes & Accessories,Lenses & Filters,Tripods & Supports,Lighting & Studio,Digital Photo Frames,Manuals & Guides,Replacement Parts & Tools,Telescopes & Binoculars,Vintage Photography,Other Photography,Accessories,Antiquarian & Collectable,Audio Books,Calendars,Children's & Young Adults,Textbooks & Education,Food & Drink,Fiction,Non-Fiction,Comics,Magazines,Collections & Lots,Other Books, Comics, Magazines,Agriculture/Farming,Automation, Motors & Drives,Building Materials & Supplies,Businesses For Sale,Electrical & Test Equipment,Containers & Pre-Fab Buildings,Hand Tools,Industrial Supply/MRO,Industrial Tools,Manufacturing & Woodworking,Medical/Lab Equipment,Metalworking/Milling/Welding,Office Equipment & Supplies,Packing & Posting Supplies,Power Tools,Printing & Graphic Arts,Restaurant & Catering,Retail & Shop Fitting,Telephone & Answering Systems,Video Broadcasting & Recording,Web Domains/ Email/ Software,Other Business & Industrial,Aircraft & Aviation,Boats & Watercraft,Campers, Caravans & Motorhomes,Cars,Cars for Salvage,Classic Cars,Commercial Vehicles,Motorcycles & Scooters,Motorcycles for Salvage,Disabled Vehicles,Emergency Vehicles,Go-Karts,Golf Buggies,Military Vehicles,Other Vehicles,Dancewear & Accessories,Erotic Clothing,Fancy Dress & Period Costume,Kids' Clothes, Shoes & Accs.,Men's Accessories,Men's Clothing,Men's Shoes,Vintage Clothing & Accessories,Wedding & Formal Occasion,Women's Accessories,Women's Handbags,Women's Clothing,Women's Shoes,World & Traditional Clothing,Other Clothes,Banknotes,Bullion/Bars,Coins,Historical Medals/Medallions,Share Certificates/Bonds,Tokens,Virtual Currency,Advertising,Animals,Animation,Autographs,Badges/Patches,Blade Accs, Armours & Shields,Bottles & Pots,Breweriana,Casino,Cigarette/Tea/Gum Cards,Clocks,Collectible Card Games,Decorative Ornaments/Plates,Disneyana,Ethnographic,Fantasy/Myth/Magic,Flags,Household,Jukeboxes,Keyrings,Kitchenalia,Masonic,Memorabilia,Metalware,Militaria,Moneyboxes/ Piggy Banks,Non-Sport Trading Cards,Paper & Ephemera,Pens & Writing Equipment,Phone Cards,Photographic Images,Accessories/ Storage,Postcards,Radio/ Television/ Telephony,Religion/ Spirituality,Rocks/ Fossils/ Minerals,Royalty,Science Fiction,Scientific,Sewing/ Fabric/ Textiles,Theatre/ Opera/ Ballet,Tobacciana & Smoking Supplies,Tools & Hardware,Trains/ Railway Models,Transportation,Vanity/ Perfume/ Grooming,Vintage/ Retro,Weird Stuff,Other Collectables,3D Printers & Supplies,Tablets & eBook Readers,Tablet & eBook Reader Accs,Tablet & eBook Reader Parts,Laptops & Netbooks,Desktops & All-in-Ones,Laptop & Desktop Accessories,Computer Cables & Connectors,Computer Components & Parts,Drives, Storage & Blank Media,Enterprise Networking, Servers,Home Networking & Connectivity,Keyboards, Mice & Pointers,Monitors, Projectors & Accs,Power Protection, Distribution,Printers, Scanners & Supplies,Software,Manuals & Resources,Vintage Computing,Other Computers & Networking,Art Supplies,Beads,Candle & Soap Making,Children's Crafts,Fabric,Fabric Painting & Decorating,Decorative & Folk Painting,Floral Supplies,Framing/Matting,Glass Art Supplies,Hand-Crafted Items,Jewellery Making,Leathercrafts,Mosaic,Multi-Purpose Craft Supplies,Needlecrafts & Yarn,Rubber Stamping,Scrapbooking & Paper Crafts,Sewing,Sculpting, Moulding & Ceramics,Woodworking,More Crafts,Dolls, Clothing & Accessories,Dolls' Miniatures & Houses,Bears,Barbecuing & Outdoor Heating,Composting & Garden Waste,Garden Clothing & Gear,Garden Fencing,Garden Hand Tools & Equipment,Garden Lighting,Garden Ornaments,Garden & Patio Furniture,Garden Power Tools & Equipment,Garden Structures & Shade,Hydroponics & Seed Starting,Landscaping & Garden Materials,Lawnmowers,Plants, Seeds & Bulbs,Plant Care, Soil & Accessories,Ponds & Water Features,Swimming Pools & Hot Tubs,Watering Equipment,Weed & Pest Control,Other Garden & Patio,Accommodation,Package Holidays,Short Breaks,Flight Tickets,Train Tickets,Bus/ Coach Tickets,Ferries/ Cruises,Car Hire/ Car Rental,Other Travel,Accessories & Equipment,Brass,Guitars & Basses,Instruction Books & Media,Keyboards & Pianos,Percussion,Pro Audio Equipment,Sheet Music & Song Books,String,Wind & Woodwind,Vintage Musical Instruments,Other Musical Instruments,American Football Memorabilia,Boxing Memorabilia,Cricket Memorabilia,Football Memorabilia,Football Programmes,Football Shirts,Golf Memorabilia,Horse Racing Memorabilia,Ice Hockey Memorabilia,Motor Sport Memorabilia,Olympic Memorabilia,Rugby League Memorabilia,Rugby Union Memorabilia,Sports Stickers, Sets & Albums,Sports Trading Cards,Subbuteo,Tennis Memorabilia,Wrestling Memorabilia,More Sports Memorabilia,Bath & Body,Facial Skin Care,Fragrances,Hair Care & Styling,Health Care,Make-Up,Massage,Mobility, Disability & Medical,Nail Care, Manicure & Pedicure,Natural & Alternative Remedies,Oral Care,Salon & Spa,Shaving & Hair Removal,Sun Care & Tanning,Tattoos & Body Art,Vape Pens, E-Cigarettes & Accs,Vision Care,Vitamins & Dietary Supplements,Other Health & Beauty,Virtual Reality,iPods & MP3 Players,iPod & MP3 Player Accessories,Headphones,Portable Disc Players & Radios,Home Audio & HiFi Separates,Performance & DJ Equipment,Televisions,DVD, Blu-ray & Home Cinema,TV Reception & Set-Top Boxes,TV & Home Audio Accessories,TV & Home Audio Parts,Multipurpose Batteries & Power,Smart Glasses,Manuals & Resources,Vintage Sound & Vision,Other Sound & Vision,UK & Ireland,Overseas,Date-Lined Ceramics,Glass,Porcelain/China,Pottery,Stoneware"
#     k = "Motors & Drives"
#     print(k.replace("&"," "))
#     t = t.replace("&"," ")
#
#     for buzzWord in t.split(','):
#         try:
#             d = searchForItems(api, buzzWord)
#         except Exception as e:
#             continue
#         if(len(d) == 0):
#             continue
#         print("executing %s"%buzzWord)
#         if("&" in buzzWord):
#             continue
#         query = "INSERT INTO items (itemId, itemName, categoryId, categoryName, image, price) VALUES (%s,%s,%s,%s,%s,%s);"
#         try:
#             curs.executemany(query, [tuple(x) for x in d])
#             db.commit()
#         except Exception as e:
#             print(e)
#             db.rollback()
#             db.close()
#             exit()
db.commit()