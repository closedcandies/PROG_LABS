
def gen_bin_tree(height: int=6, root: int=2):
    tree = {root: {'left': None, 'right': None}}
    
    queue = [(root, 0)]
    
    while queue:
        current_node, current_height = queue.pop(0)
        
        if current_height < height:
            left_child = current_node * 3
            right_child = current_node + 4
            
            tree[left_child] = {'left': None, 'right': None}
            tree[right_child] = {'left': None, 'right': None}
            
            tree[current_node]['left'] = left_child
            tree[current_node]['right'] = right_child
            
            queue.append((left_child, current_height + 1))
            queue.append((right_child, current_height + 1))
    
    nodes_to_remove = []
    for node, children in tree.items():
        if children['left'] is None and children['right'] is None:
            nodes_to_remove.append(node)
    
    for node in nodes_to_remove:
        del tree[node]
    
    return tree
    


if __name__ == "__main__":
    tree = gen_bin_tree(height=6, root=2)
    print(tree)