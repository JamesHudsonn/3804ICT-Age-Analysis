import math
from itertools import combinations


class Node:
    # Node class for use within the fp-tree

    # a node has a item (e.g. 'I1' or 'Eggs'), a frequency/support count,
    # a list of pointers to other nodes which are its children
    # and a pointer to its parent
    def __init__(self, item=None, parent=None):
        self.parent = parent
        # during creation of the node, append the new node to the children of its parent
        if parent is not None:
            parent.children.append(self)
        self.item = item
        self.count = 1
        # initialise children to empty list
        self.children = []

    def add(self, item):
        # adding an item to a node. returns the node representing the item added
        # checking if the item already exists as a child of the node
        for child in self.children:
            if item == child.item:
                # it does already exist, so increment its support count
                child.count += 1
                return child

        # item did not exist as a child of the current node. Will have to create it as a new node
        new_node = Node(item, self)
        return new_node


class Tree:
    def __init__(self, dataset, min_sup_count=None, min_sup=0.5):
        self.min_sup = min_sup
        self.min_sup_count = (
            math.ceil(min_sup * len(dataset))
            if min_sup_count is None
            else min_sup_count
        )
        self.total_transactions = len(dataset)
        # root node, usually represented as 'Null' pointer
        self.root = Node()
        # dictionary mapping items to support count. e.g. 'I5' -> 3
        self.frequencies = dict()
        # dictionary mapping items to their unique nodes in the fp-tree
        self.nodes = dict()

        # calculate support count for dataset
        for transaction in dataset:
            # transaction transformed to frozenset to remove any duplicate item entries
            for item in frozenset(transaction):
                self.frequencies[item] = self.frequencies.get(item, 0) + 1

        # remove items from frequencies list that are less than min support
        self.frequencies = {
            item: count
            for item, count in self.frequencies.items()
            if count >= self.min_sup_count
        }

        # sort the frequencies according to count
        # sort function
        def sort_items(item_tuple):
            item, count = item_tuple
            return count

        self.frequencies = {
            item: count
            for item, count in sorted(self.frequencies.items(), key=sort_items)
        }

        # now iterate through dataset and construct fp-tree
        for i in range(len(dataset)):
            # remove items that do not support minimum support threshold
            transaction = [
                item
                for item in dataset[i]
                if self.frequencies.get(item, 0) >= self.min_sup_count
            ]

            # reorder the items within each transaction according to their support
            transaction = sorted(
                transaction, key=lambda item: self.frequencies.get(item), reverse=True
            )

            # remove duplicate items
            cleaned_transaction = []
            [
                cleaned_transaction.append(item)
                for item in transaction
                if item not in cleaned_transaction
            ]

            # at the start of each transaction, node begins as the root node
            node = self.root
            for item in cleaned_transaction:
                node = node.add(item)
                # node is now a node representing the item. Either it is a pre-existing node
                # with its support count incremented, or its a brand new node
                # now we add this node to the nodes dict so that it is easily accessible
                if item in self.nodes:
                    if node not in self.nodes.get(item):
                        self.nodes.get(item).append(node)
                else:
                    self.nodes[item] = [node]

    def __mine(self):
        # mining function

        frequent_itemsets = []
        # iterate through items in increasing order of support count
        for item in self.frequencies:
            frequent_itemsets.append((item, self.frequencies[item]))
            patterns = []
            # iterate through the list of nodes representing the item to extract the prefix paths
            for node in self.nodes[item]:
                # here we are trying to generate a new "transaction" which represents the prefix
                path = []
                curr_node = node.parent
                while curr_node.item is not None:
                    path.append(curr_node.item)
                    curr_node = curr_node.parent
                # this path must be duplicated if it represents multiple transactions.
                # e.g {Milk, Eggs}:2 -> [['Milk', 'Eggs'], ['Milk', 'Eggs']]
                patterns.extend([path] * node.count)
            # construct the conditional fp-tree from the conditional pattern bases
            new_tree = Tree(patterns, min_sup_count=self.min_sup_count)
            # extract the frequent itemsets from the conditional tree
            itemsets = new_tree.__mine()
            for itemset in itemsets:
                # append the current frequent item to the generated itemsets
                frequent_itemsets.append((item,) + itemset)
        return frequent_itemsets

    @staticmethod
    def __generate_subsets(itemset):
        # utility function for generating all non-empty subsets of a given itemset
        # excludes the set including all items (hence range(1, len()) instead of len() + 1)
        return [
            subset
            for subset_size in range(1, len(itemset))
            for subset in combinations(itemset, subset_size)
        ]

    def generate_frequent_itemsets(self):
        # transforms the frequent itemsets generated by the __mine() func
        # into a dictionary where the itemset is the key and the count is the value
        return {frozenset(itemset): count for *itemset, count in self.__mine()}

    def generate_rules(self, frequent_itemsets, min_conf):
        # initialise rules to empty array
        rules = []
        # iterate through all frequent k-itemsets where k > 1
        for itemset in [itemset for itemset in frequent_itemsets if len(itemset) > 1]:
            subsets = self.__generate_subsets(itemset)
            for subset in subsets:
                # set 1 represents the antecedent
                set_1 = frozenset(subset)
                # set 2 represents the consequent
                set_2 = itemset.difference(set_1)
                confidence = (
                    frequent_itemsets[set_1.union(set_2)] / frequent_itemsets[set_1]
                )
                lift = confidence / (frequent_itemsets[set_2] / self.total_transactions)
                if confidence >= min_conf:
                    # append a string representation of the rule if it meets min_conf criteria
                    rules.append(
                        f"{[item for item in set_1]} -> {[item for item in set_2]} | Confidence: {(confidence*100):.2f}% | Lift: {lift:.2f}"
                    )
        return rules

    def print(self):
        # utility function which demonstrates the structure of the fp-tree
        print("Children of root")
        to_print = []
        to_print.extend(self.root.children)
        for node in to_print:
            print(
                f"{node.item}:{node.count}. Parent: {node.parent.item}:{node.parent.count}"
            )
            to_print.extend(node.children)
        print("")
        for item in self.nodes.keys():
            print(
                f'{item}: {[f"{node.item}:{node.count}" for node in self.nodes.get(item)]}'
            )
