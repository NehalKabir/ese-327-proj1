import pandas as pd

class TreeNode:
    def __init__(self, data, parent=None):
        self.data = data
        self.count = 1
        self.children = {}
        self.parent = parent

def extract_data(filename, columns):
    data = pd.read_excel(filename)
    df = pd.DataFrame(data, columns=columns)
    return df

def make_transaction_list(df):
    transactions = df.groupby('Invoice')['StockCode'].apply(list).tolist()
    return transactions

def construct_fptree(transactions, min_support):
    root = TreeNode(None)
    header_table = {}
    
    for transaction in transactions:
        current = root
        for item in transaction:
            if item in current.children:
                current = current.children[item]
                current.count += 1
            else:
                new_node = TreeNode(item, parent=current)
                current.children[item] = new_node
                current = new_node
                if item in header_table:
                    header_table[item].append(current)
                else:
                    header_table[item] = [current]

    return root, header_table

def mine_fptree(header_table, min_support, prefix, frequent_item_sets):
    for item, nodes in header_table.items():
        support = sum(node.count for node in nodes)
        if support >= min_support:
            new_frequent_set = prefix + [item]
            frequent_item_sets.append(new_frequent_set)
            conditional_transactions = []
            for node in nodes:
                conditional_base = []
                count = node.count
                parent = node.parent
                while parent.data is not None:
                    conditional_base.append(parent.data)
                    parent = parent.parent
                if conditional_base:    
                    conditional_transactions.extend([conditional_base] * count)
            conditional_tree, conditional_header = construct_fptree(conditional_transactions, min_support)
            if conditional_header:
                mine_fptree(conditional_header, min_support, new_frequent_set, frequent_item_sets)

def apriori(df, min_support):
    transactions = make_transaction_list(df)
    print("constructing fptree..")
    root, header_table = construct_fptree(transactions, min_support)
    print("finished constructing tree")
    frequent_item_sets = []
    print("mining fptree..")
    mine_fptree(header_table, min_support, [], frequent_item_sets)
    print("finished mining")
    return frequent_item_sets

def main():
    min_support = 1
    
    filename = 'online_100.xlsx'
    columns = ['Invoice', 'StockCode']
    df = extract_data(filename, columns)
    
    df['StockCode'] = df['StockCode'].astype(str)

    print(len(df))
    frequent_item_sets = apriori(df, min_support)
    '''
    #textbook example
    data1= [['2','1','5'], ['2','4'],['2','3'], ['2','1', '4'], ['1', '3'], ['2','3'], ['1', '3'], ['2','1', '3', '5'], ['2','1', '3',]]    
    dataTree1, header_table = construct_fptree(data1, min_support)
    frequent_item_sets = []
    mine_fptree(header_table, min_support, [], frequent_item_sets)
    '''
    print("The frequent item sets are: ")
    filtered_list = [sublist for sublist in frequent_item_sets if len(sublist) > 1]
    for item_set in frequent_item_sets:
        print(item_set)

if __name__ == "__main__":
    main()
