import pandas as pd
import copy

def extractex(filename, col):
    data = pd.read_excel(filename) 
    df = pd.DataFrame(data, columns=col)
    #print(df)
    return df

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

class Tree:
    def __init__(self, data):
        self.children = []
        self.connect = None
        self.same = None
        self.data = data
        self.count = 1
    def __str__(self):
        return f"Item: {self.data} count: {self.count}"
    def PrintTree(self):
        print(self.data)
        for i in self.children:
            i.PrintTree()
    def PrintConnect(self):
        print(self.data)
        if self.connect != None:
            self.connect.PrintConnect()
    def PrintChildren(self):
        print(self.data)
        if self.children != []:
            for x in self.children:
                print(x.data)
    def getdata(self):
        return self.data
    def getcount(self):
        return self.count
    def strchild(self): #get children
        sc = []
        for x in self.children:
            sc.append(x.data)
        return sc
    def incc(self):
        self.count=self.count+1

def gentree(data):
    root = Tree("root")
    hold = root
    treep=[]
    treecount=0
    for x in data:
        count = 0
        for y in x:
            if count == 0:
                if (y in root.strchild()):
                    #print("current invoice")
                    #print(x)
                    #print('current stockcode')
                    #print(y)
                    #print("stockcode found in root children, incrementing coounter")
                    #print('========================')
                    d= root.strchild().index(y)
                    root.children[d].incc()
                    hold = root.children[d]
                    count=count+1
                    
                else:
                    #print("current invoice")
                    #print(x)
                    #print('current stockcode')
                    #print(y)
                    #print("stockcode not found in root children, adding new node")
                    #print('========================')
                    treep.append(Tree(y))
                    root.children.append(treep[treecount])
                    treep[treecount].connect = root
                    hold = treep[treecount]
                    count= count+1
                    treecount=treecount+1
                
            else:
                if (y in hold.strchild()):
                    #print("current invoice")
                    #print(x)
                    #print('current stockcode')
                    #print(y)
                    #print("stockcode found in node children, incrementing coounter")
                    #print('========================')
                    d= hold.strchild().index(y)
                    hold.children[d].incc()
                    hold = hold.children[d]
                else:
                    #print("current invoice")
                    #print(x)
                    #print('current stockcode')
                    #print(y)
                    #print("stockcode not found in node children, adding new node")
                    treep.append(Tree(y))
                    hold.children.append(treep[treecount])
                    treep[treecount].connect = hold
                    hold = treep[treecount]
                    treecount=treecount+1

                    
    #print('===================')
            
    #root.PrintChildren()
    #print('=================')
    #print(treep[2].getdata())
    #print(treep[2].getcount())
    #treep[1].PrintChildren()
    return root

def makePointers(start, dataTree, itemCounts):
    out =[]   
    for x in dataTree.children:
        if x.data == start.data:
            out.append(x)
        elif itemCounts[x.data] >=itemCounts[start.data] :
            out2 = (makePointers(start, x, itemCounts))
            if out2: #check if list is empty
                out.extend(out2)
    return out

def makePointerList(itemCounts, dataTree, threshold):
    pointerList = []
    for index, count in itemCounts.items():
        if count >= threshold: #threshold value
            temp = Tree(index)
            listOfItemNodes = makePointers(temp, dataTree, itemCounts)
            temp.same = listOfItemNodes[0]
            for x in range(len(listOfItemNodes) - 1):
                listOfItemNodes[x].same = listOfItemNodes[x + 1]
            pointerList.append(temp)
    return pointerList

def findFreqSets(pointerList, threshold):
    freqItems = []
    for i in reversed(pointerList):
        temp = copy.deepcopy(i)
        totalBranch = []
        added = False
        while temp.same != None:
            temp = temp.same
            countVal = temp.count
            if countVal >= threshold and added == False:
                tempList = [temp]
                freqItems.append(tempList)
                added = True
            temp2 = copy.deepcopy(temp.connect)
            curBranch = []
            while temp2.data != "root":
                temp2.count = countVal
                curBranch.append(temp2)
                temp2 = temp2.connect
            curBranch.reverse()
            if curBranch:
                totalBranch.append(curBranch)
        if(len(totalBranch) == 1):
            totalBranch[0].append(i)
            freqItems.append(totalBranch[0])
        elif(len(totalBranch) > 1):
            tempTreeData = genTreeData(totalBranch)
            tempTree = gentree(tempTreeData)
            tempStockcode = makeTempSeries(totalBranch)
            print(tempStockcode)
            tempPointers = makePointerList(tempStockcode, tempTree, threshold)
            tempItems = findFreqSets(tempPointers, threshold)
            for j in tempItems: #CHECK THIS PART
                j.append(temp)
            freqItems.extend(tempItems)
    return freqItems

def genTreeData(branchList):
    output = []
    for i in branchList:
        curList = []
        for item in i:
            curList.append(item.data)
        for j in range(i[0].count):
            output.append(curList)
    return output

def makeTempSeries(data_count_list):
    # Create a dictionary to store the counts for each unique "data" value
    counts_dict = {}
    
    # Iterate through the list of DataCount objects and update the counts
    for i in data_count_list:
        for item in i:
            data = item.data
            count = item.count
            if data in counts_dict:
                counts_dict[data] += count
            else:
                counts_dict[data] = count
    
    # Create a Pandas Series from the counts dictionary
    counts_series = pd.Series(counts_dict)
    
    return counts_series


threshold = 2
#extracts the first 2 coumns to be used for the transaction
n = 'filtered_excel_file.xlsx'
co= ['Invoice', 'StockCode']
#df= extractex(n, co)
data = pd.read_excel('filtered_excel_file.xlsx') 
df = pd.DataFrame(data, columns=['Invoice', 'StockCode'])
print(df)
invoice = df['Invoice']
stockCode = df['StockCode']

#get count of stock code 
#val_count returs the count of each item and even sorts in decreasing order
stockcode_counts = df['StockCode'].value_counts()
print(stockcode_counts)

transaction_data = df[['Invoice', 'StockCode']]
# Use the MakeTransactionList function on the 'transaction_data' DataFrame
ordered_transaction_list = MakeTransactionList(transaction_data['Invoice'], transaction_data['StockCode'])

dataTree = gentree(ordered_transaction_list)

pointerList = makePointerList(stockcode_counts, dataTree, threshold)

a = findFreqSets(pointerList, threshold)
filtered_list = [inner_list for inner_list in a if len(inner_list) > 1]
for inner_list in filtered_list:
        data_list = [obj.data for obj in inner_list]
        print(data_list)


'''
data1= ['1','2','5',], ['3','4'],['1','3'], ['1','2']
treepoint=[]    
dataTree1 = gentree(data1)
#dataTree1.PrintTree()
stockData1 = {'1': 3, '2': 2, '3': 2, '4': 1, '5': 1}
ser = pd.Series(data=stockData1, index=['1', '2', '3', '4', '5'])
#print(ser)

pointerList = makePointerList(ser, dataTree1, threshold)
a = findFreqSets(pointerList, threshold)
print("done")
'''
'''
#textbook example
data1= [['2','1','5'], ['2','4'],['2','3'], ['2','1', '4'], ['1', '3'], ['2','3'], ['1', '3'], ['2','1', '3', '5'], ['2','1', '3',]]    
dataTree1 = gentree(data1)
#dataTree1.PrintTree()
stockData1 = {'2': 7, '1': 6, '3': 6, '4': 2, '5': 2}
ser = pd.Series(data=stockData1, index=['1', '2', '3', '4', '5'])
#print(ser)

pointerList = makePointerList(ser, dataTree1, threshold)
a = findFreqSets(pointerList, threshold)
filtered_list = [inner_list for inner_list in a if len(inner_list) > 1]
for inner_list in filtered_list:
        data_list = [obj.data for obj in inner_list]
        print(data_list)
    '''
