import csv
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


if __name__ == '__main__':
    itemList = []
    manufactureList = readFile("ManufacturerList")
    priceList = readFile('PriceList')
    dateList = readFile('ServiceDatesList')
    opt = ''

    for row in manufactureList:
        id = row[0]
        name = row[1]
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

    while (opt != '0'):

        print("1: Full Inventery")
        print("2: List Items per Manufacturer")
        print("3: List PastServiceDateInventory")
        print("4: List Damaged Inventory")
        print("0: Exit")
        print("Choose option: - ", end='  ')
        opt = input()

        # FullInventory.csv
        if opt == '0':
            break
        elif opt == "1":
            # sorting
            for i in range(len(itemList)):
                for j in range(0, len(itemList) - i - 1):
                    if itemList[j].name[0] > itemList[j + 1].name[0]:
                        temp = itemList[j]
                        itemList[j] = itemList[j+1]
                        itemList[j+1] = temp

            f = open('FullInventory.csv', 'w')

            writer = csv.writer(f)

            for obj in itemList:
                writer.writerow(obj.getData().split(","))

            f.close()

            print("FullInventory.csv file created.")
            break
        # LaptopInventory.csv
        elif opt == "2":
            # sorting
            for i in range(len(itemList)):
                for j in range(0, len(itemList) - i - 1):
                    if itemList[j].id > itemList[j + 1].id:
                        temp = itemList[j]
                        itemList[j] = itemList[j+1]
                        itemList[j+1] = temp

            brandNames = []

            for obj in itemList:
                if obj.name not in brandNames:
                    brandNames.append(obj.name)
                    pass

            for brand in brandNames:
                temp = brand.split(' ')
                temp = ''.join(temp)

                f = open(f'{temp}Products.csv', 'w')
                writer = csv.writer(f)

                for obj in itemList:
                    if obj.name == brand:
                        writer.writerow(
                            f'{obj.id},{obj.name},{obj.price},{obj.date},{obj.damaged}'.split(','))

                f.close()
            print("Manufacturer specific files created.")
        # DamagedInventory.csv
        elif opt == "4":
            # sorting
            for i in range(len(itemList)):
                for j in range(0, len(itemList) - i - 1):
                    if itemList[j].price < itemList[j + 1].price:
                        temp = itemList[j]
                        itemList[j] = itemList[j+1]
                        itemList[j+1] = temp

            f = open('DamagedInventory.csv', 'w')
            writer = csv.writer(f)

            for obj in itemList:
                if obj.damaged == 'damaged':
                    writer.writerow(
                        f"{obj.id},{obj.name},{obj.type},{obj.price},{obj.date}".split(","))

            f.close()
            print(
                "DamagedInventory.csv file created.")
            break
        # PastServiceDateInventory.csv
        elif opt == "3":

            end_date = '11/22/2022'

            end_date = end_date[:-4] + end_date[-2:]
            print(end_date)
            end_date = datetime.strptime(
                end_date, '%m/%d/%y')

            if end_date < datetime.now():
                print("passed")
            else:
                print("not passed")

            f = open('PastServiceDateInventory.csv', 'w')
            writer = csv.writer(f)

            for obj in itemList:
                end_date = obj.date
                end_date = end_date[:-4] + end_date[-2:]
                end_date = datetime.strptime(
                end_date, '%m/%d/%y')

                if end_date < datetime.now():
                    writer.writerow(
                        f"{obj.id},{obj.name},{obj.type},{obj.price},{obj.date},{obj.damaged}".split(","))

            f.close()
            print("PastServiceDateInventory.csv file created.")
            break
        else:
            print("Invalid command")
