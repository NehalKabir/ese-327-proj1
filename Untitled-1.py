from ucimlrepo import fetch_ucirepo 
  
# fetch dataset 
iris = fetch_ucirepo(id=53) 
  
# data (as pandas dataframes) 
X = iris.data.features 
y = iris.data.targets 
  
# metadata 
#print(iris.metadata) 
  
# variable information 
#print(iris.variables) 


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
root.PrintTree()   
