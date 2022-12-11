import csv
from datetime import date
from datetime import datetime

# Name: - Neeraj Kumar
# ID: - 2047559

class Item:
    def __init__(self, Id="", Name="", Type="", Price=0, Date="", Damaged=''):
        self.id = Id
        self.name = Name
        self.type = Type
        self.price = Price
        self.date = Date
        self.damaged = Damaged

    def getData(self):
        return f'{self.id},{self.name},{self.type},{self.price},{self.date},{self.damaged}'

#reading csv files
def readFile(name, type='csv'):
    if type == 'csv':
        file = open(f"{name}.{type}")
        csvreader = csv.reader(file)
        mylist = []
        for row in csvreader:
            mylist.append(row)
        file.close()
        return mylist
    pass

#sorting arary in descending order
def bubbleSort(array):

    for i in range(len(array)):
        for j in range(0, len(array) - i - 1):
            if int(array[j].price) < int(array[j + 1].price):
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp

    return array

# func returns true if item has not passed the service date else returns false
def validateDate(item):
    today = date.today()
    currentDate = today.strftime("%m/%d/%y")

    # convert string to date object
    d2 = datetime.strptime(currentDate, "%m/%d/%y")
    d1 = datetime.strptime(f"{item.date}", "%m/%d/%Y")

    delta = d2 - d1 
    delta = int(delta.days)

    if delta <= 0:
        return True
    return False


if __name__ == '__main__':
    itemList = []
    manufactureList = readFile("ManufacturerList")
    priceList = readFile('PriceList')
    dateList = readFile('ServiceDatesList')
    query = ''


    for row in manufactureList:
        id = row[0]
        name = row[1].replace(" ", "")
        type = row[2]
        damaged = row[3]

        if id != "":
            s1 = Item(id, name, type, 0, "", damaged)
            itemList.append(s1)

    for row in priceList:
        for i in range(len(itemList)):
            if row[0] == itemList[i].id:
                itemList[i].price = row[1]

    for row in dateList:
        for i in range(len(itemList)):
            if row[0] == itemList[i].id:
                itemList[i].date = row[1]

    for item in itemList:
        print(item.getData())

    while (query != 'q'):

        print("Enter Query")
        print("OR")
        print("Press q to exit")
        print("Query: -", end='  ')
        query = input()

        if query == 'q':
            break

        qlist = query.split(" ")

        if len(qlist) < 2:
            print("No such item in inventory")
            continue

        manufacturer = ''
        itemType = ''
        found = [False, False]

        # Part1: identifying manufacturer name and item type

        for qItem in qlist:
            for item in itemList:
                if qItem == item.name and found[0] == False:
                    manufacturer = item.name
                    found[0] = True
                    break
                elif qItem == item.type and found[1] == False:
                    itemType = item.type
                    found[1] = True
                    break

        # print(f'M,T: {manufacturer} {itemType}')

        if (not found[0]) or (not found[1]):
            print("No such item in inventory")
            continue

        # Part2: Print matched item
        matchedItems = []
        matchedItemPrice = 0

        for item in itemList:
            if item.name == manufacturer and itemType == item.type and item.damaged == '' and validateDate(item):
                matchedItems.append(item)
        
        if len(matchedItems):
            matchedItems = bubbleSort(matchedItems)
            _item = matchedItems[0]
            matchedItemPrice = int(matchedItems[0].price)
            print(f'Your item is: \n{_item.id} {_item.name} {_item.type} {_item.price}')
        else:
            print("No such item in inventory")
            continue

        # Part2: Same item from another manufacturer having closest price
        print('You may, also, consider:')
        factor = 100
        for item in itemList:
            if ((matchedItemPrice + factor) >= int(item.price) >= (matchedItemPrice - factor)) and itemType == item.type and item.damaged == '' and validateDate(item) and manufacturer!=item.name:
                print(f'Your item is: \n{item.id} {item.name} {item.type} {item.price}')