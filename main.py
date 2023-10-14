import pandas as pd

#TODO: make excel file a function
data = pd.read_excel('C:\Class Folders\ESE327\mainProject\online_retail_II.xlsx') 
df = pd.DataFrame(data, columns=['Invoice', 'StockCode'])
print(df)

invoice = df[0]
stockCode = df[1]

#get count of stock code 
#val_count returs the count of each item and even sorts in decreasing order
stockcode_counts = df[1].value_counts()

# Print the counts.
print(stockcode_counts)

def MakeTransactionList(invoice, itemCode):
    transactionList = []
    curInvoice = invoice[0]
    curTransaction = []
    for i in range(0, invoice.size):
        if invoice[i] == curInvoice:
            curTransaction.append(itemCode[i])
        else:
            transactionList.append(curTransaction)
            curTransaction = []
            curInvoice = invoice[i]
            curTransaction.append(itemCode[i])
    print(transactionList)
    return transactionList

class Tree:
    def __init__(self, data):
        self.children = []
        self.connect = None
        self.data = data
    def PrintTree(self):
        print(self.data)
        for i in self.children:
            i.PrintTree()
    def PrintConnect(self):
        print(self.data)
        if self.connect != None:
            self.connect.PrintConnect()



'''
left = Tree("left")
middle = Tree("middle")
right = Tree("right")
root = Tree("root")
root.children = [left, middle, right]
root.data = "root"
left.data = "left"
right.data = "right"
middle.data = "middle"
middle.connect = right
left2 = Tree("left2")
left2.data = "left2"
left.children = [left2]
root.PrintTree()   '''

