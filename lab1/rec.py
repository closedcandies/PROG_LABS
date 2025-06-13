def gen_bin_tree(height: int = 6, root: int = 2, visited=None):
    if visited is None:
        visited = set()
    
    if height == 0 or root in visited:
        return {}

    visited.add(root)
    
    left_child = root * 3
    right_child = root + 4
    
    tree = {
        root: {
            'left': left_child,
            'right': right_child
        }
    }

    # рекурсивно дополняем дерево, избегая повторных узлов
    tree.update(gen_bin_tree(height - 1, left_child, visited))
    tree.update(gen_bin_tree(height - 1, right_child, visited))

    return tree


if __name__ == "__main__":
    tree = gen_bin_tree(height=6, root=2)
    print(tree)