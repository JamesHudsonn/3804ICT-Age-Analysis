import math

from fptree import Tree

dataset_1 = [
    ["A", "B", "C", "D", "E", "F"],
    ["B", "C", "D", "E", "F", "G"],
    ["A", "D", "E", "H"],
    ["A", "D", "F", "I", "J"],
    ["B", "D", "E", "K"],
]
min_sup_count_1 = 3

dataset_2 = [
    ["E", "A", "D", "B"],
    ["D", "A", "C", "E", "B"],
    ["C", "A", "B", "E"],
    ["B", "A", "D"],
    ["D"],
    ["D", "B"],
    ["A", "D", "E"],
    ["B", "C"],
]
min_sup_count_2 = 3

dataset_3 = [
    ["M", "O", "N", "K", "E", "Y"],
    ["D", "O", "N", "K", "E", "Y"],
    ["M", "A", "K", "E"],
    ["M", "U", "C", "K", "Y"],
    ["C", "O", "O", "K", "E"],
]
min_sup_count_3 = 3

dataset_4 = [
    ["Bread", "Butter", "Milk"],
    ["Bread", "Butter"],
    ["Beer", "Cookies", "Diapers"],
    ["Milk", "Diapers", "Bread", "Butter"],
    ["Beer", "Diapers"],
]
min_sup_count_4 = 2

dataset_5 = [
    [
        "Apple",
        "Banana",
        "Guava",
        "Eggs",
        "Milk",
        "Steak",
        "Yogurt",
        "Tomatos",
        "Onion",
        "Nuts",
    ],
    [
        "Apple",
        "Banana",
        "Orange",
        "Eggs",
        "Milk",
        "Pork",
        "Potatos",
        "Onion",
        "Choclate",
    ],
    ["Spinach", "Eggs", "Milk", "Yogurt", "Bagel", "Onion", "Watermelon"],
    ["Pineapple", "Banana", "Eggs", "Lemon", "Steak", "Broccolli", "Onion", "Lamb"],
    [
        "Apple",
        "Banana",
        "Beer",
        "Lettuce",
        "Ice cream",
        "Tomatos",
        "Grape",
        "Strawberry",
    ],
]
min_sup_count_5 = math.ceil(0.3 * len(dataset_5))

dataset_6 = [
    ["Milk", "Onion", "Nutmeg", "Kidney Beans", "Eggs", "Yogurt"],
    ["Dill", "Onion", "Nutmeg", "Kidney Beans", "Eggs", "Yogurt"],
    ["Milk", "Apple", "Kidney Beans", "Eggs"],
    ["Milk", "Unicorn", "Corn", "Kidney Beans", "Yogurt"],
    ["Corn", "Onion", "Onion", "Kidney Beans", "Ice cream", "Eggs"],
]
min_sup_6 = 0.5

dataset_lec = [
    ["I1", "I2", "I5"],
    ["I2", "I4"],
    ["I2", "I3"],
    ["I1", "I2", "I4"],
    ["I1", "I3"],
    ["I2", "I3"],
    ["I1", "I3"],
    ["I1", "I2", "I3", "I5"],
    ["I1", "I2", "I3"],
]
min_sup_count_lec = 2

min_conf = 0.4
fp_tree = Tree(dataset_6, min_sup=0.5)
# fp_tree.print()
frequent_itemsets = fp_tree.generate_frequent_itemsets()
for itemset, sup_count in frequent_itemsets.items():
    str = "{"
    for item in itemset:
        str += f"{item}, "
    str = str[:-2]
    str += "}"
    print(f"{str} | sup_count: {sup_count}")
rules = fp_tree.generate_rules(frequent_itemsets, 0.7)
print(f"total rules: {len(rules)}")
for rule in rules:
    print(rule)
