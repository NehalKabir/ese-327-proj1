import pandas as pd

#TODO: make excel file a function
data = pd.read_excel('C:\Class Folders\ESE327\mainProject\online_retail_II.xlsx') 
df = pd.DataFrame(data, columns=['Invoice', 'StockCode'])
print(df)

invoice = df['Invoice']
stockCode = df['StockCode']

#get count of stock code 
#val_count returs the count of each item and even sorts in decreasing order
stockcode_counts = df['StockCode'].value_counts()

# Print the counts.
print(stockcode_counts)
transaction_data = df[['Invoice', 'StockCode']]

# Define the MakeTransactionList function (as previously corrected)
def MakeTransactionList(invoice, itemCode):
    transactionList = []
    curInvoice = invoice[0]
    curTransaction = []
    for i in range(0, invoice.size):
        if invoice[i] == curInvoice:
            curTransaction.append(itemCode[i])
        else:
            transactionList.append(curTransaction)
            curTransaction = [itemCode[i]]  # Start a new transaction
            curInvoice = invoice[i]
    transactionList.append(curTransaction)
    transactionList.sort(key=len, reverse=True)
    return transactionList

# Use the MakeTransactionList function on the 'transaction_data' DataFrame
ordered_transaction_list = MakeTransactionList(transaction_data['Invoice'], transaction_data['StockCode'])

# Print the ordered_transaction_list
for transaction in ordered_transaction_list:
    print(transaction)

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

