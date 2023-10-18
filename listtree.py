import pandas as pd


class Tree:
    def __init__(self, data):
        self.children = []
        self.connect = None
        self.data = data
        self.count = 1
    def PrintTree(self):
        print(self.data)
        for i in self.children:
            i.PrintTree()
    def PrintConnect(self):
        print(self.data)
        if self.connect != None:
            self.connect.PrintConnect()
    def PrintChildren(self):
            for x in self.children:
                print(x.data)
    def getdata(self):
        return self.data
    def getcount(self):
        return self.count
    def strchild(self):
        sc = []
        for x in self.children:
            sc.append(x.data)
        return sc
    def incc(self):
        self.count=self.count+1

#children = pointer from parent to child
#connect = from child to parent

data1= ['1','2','5',], ['3','4'],['1','3'], ['1','2']
treepoint=[]
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
                    print("current invoice")
                    print(x)
                    print('current stockcode')
                    print(y)
                    print("stockcode found in root children, incrementing coounter")
                    print('========================')
                    d= root.strchild().index(y)
                    root.children[d].incc()
                    hold = root.children[d]
                    count=count+1
                    
                else:
                    print("current invoice")
                    print(x)
                    print('current stockcode')
                    print(y)
                    print("stockcode not found in root children, adding new node")
                    print('========================')
                    treep.append(Tree(y))
                    root.children.append(treep[treecount])
                    treep[treecount].connect = root
                    hold = treep[treecount]
                    count= count+1
                    treecount=treecount+1
                
            else:
                if (y in hold.strchild()):
                    print("current invoice")
                    print(x)
                    print('current stockcode')
                    print(y)
                    print("stockcode found in node children, incrementing coounter")
                    print('========================')
                    d= hold.strchild().index(y)
                    hold.children[d].incc()
                    hold = hold.children[d]
                else:
                    print("current invoice")
                    print(x)
                    print('current stockcode')
                    print(y)
                    print("stockcode not found in node children, adding new node")
                    treep.append(Tree(y))
                    hold.children.append(treep[treecount])
                    treep[treecount].connect = hold
                    hold = treep[treecount]
                    treecount=treecount+1

                    
    print('===================')
            
    root.PrintChildren()
    print('=================')
    print(treep[2].getdata())
    print(treep[2].getcount())
    treep[1].PrintChildren()
    
gentree(data1)


'''
testing random code snippets
f = root

f = root.children[2]
treepoint.append(Tree('lol'))
print(treepoint[0].getdata())
print('1111111')
print(root.children[2].getdata())
print(data1[1].index('4'))'''


'''
print(left.strchild())
print('left2' in left.strchild())
left3 = Tree("left3")
left3.data = "left3"
left.children.append(left3)
print(left in root.children)'''






            
            
