# In cấu trúc cây
def print_tree(node, level=0):
    print("  " * level + node.name)
    for child in node.children.values():
        print_tree(child, level + 1)