from math import floor
from random import sample


class Node:

    def __init__(self, value=None):
        self.left = None
        self.right = None
        self.value = value


class BST:

    def __init__(self, array=None):
        if array is None:
            array = []
        self.init_array = sorted(array)
        print('Building a binary search tree based on the list of values below:')
        print(self.init_array)
        self.root_node = self.array_to_bst()

    def find_root_node(self):
        print(self.init_array)
        root_index = self.find_midpoint()

        return Node(self.init_array[root_index])

    def find_midpoint(self):
        return floor(len(self.init_array) / 2)

    def array_to_bst(self, left=0, right=None):
        if right is None:
            right = len(self.init_array) - 1

        if left > right:
            return None

        midpoint = int(left + (right - left) / 2)
        value = Node(self.init_array[midpoint])

        value.left = self.array_to_bst(left, midpoint - 1)
        value.right = self.array_to_bst(midpoint + 1, right)

        return value

    def insert(self, value, node='root'):
        """inserts new value as a leaf node"""
        if node == 'root':
            node = self.root_node
        if self.look_for(value):
            print(f'{value} is already in the tree!')
            return

        if value > node.value:
            if node.right:
                self.insert(value, node.right)
            else:
                node.right = Node(value)
        else:
            if node.left:
                self.insert(value, node.left)
            else:
                node.left = Node(value)

    def delete(self, value):
        node_to_delete = self.look_for(value)
        if not node_to_delete:
            return

        child_nodes = self.count_children(node_to_delete)
        if child_nodes == 2:
            self.delete_two_children_node(value)
        elif child_nodes == 1:
            self.delete_single_child_node(value)
        else:
            self.delete_leaf_node(value)

    def look_for(self, value, node='root'):
        """returns a node with matching value"""
        if not node:
            return

        if node == 'root':
            node = self.root_node

        if node.value == value:
            return node

        if value > node.value:
            return self.look_for(value, node.right)
        else:
            return self.look_for(value, node.left)

    def find_parent_node(self, value, node='root'):
        """returns a parent of a node with provided value"""
        if node == 'root':
            node = self.root_node

        parent_node = self.check_child_nodes(value, node)
        if parent_node:
            return parent_node

        if value > node.value:
            if node.right:
                return self.find_parent_node(value, node.right)
        else:
            if node.left:
                return self.find_parent_node(value, node.left)

    def delete_two_children_node(self, value):
        node = self.look_for(value)
        next_biggest = self.find_next_biggest(node)
        self.delete(next_biggest.value)
        node.value = next_biggest.value

    def find_next_biggest(self, node):
        """returns node with next biggest value (right once, then left as much as possible)"""
        if node.right:
            node = node.right
            return self.get_leftmost_node(node)

    def get_leftmost_node(self, node):
        if node.left:
            node = node.left
        else:
            return node

        return self.get_leftmost_node(node)

    def delete_leaf_node(self, value):
        """find parent node and change pointer to None, return if child node has a child"""
        parent_node = self.find_parent_node(value)
        if not parent_node:
            return

        child_node = self.get_child_node(parent_node, value)

        if child_node.left or child_node.right:
            return

        if parent_node.right:
            if parent_node.right.value == value:
                parent_node.right = None
        if parent_node.left:
            if parent_node.left.value == value:
                parent_node.left = None

    def delete_single_child_node(self, value):
        parent_node = self.find_parent_node(value)
        if not parent_node:
            return
        pointer = self.get_child_node_pointer(parent_node, value)
        node = self.get_child_node(parent_node, value)
        self.change_pointer(parent_node, node, pointer)

    def change_pointer(self, parent_node, node, pointer):
        """Used while deleting SINGLE CHILD node, points the parent to lower node's only child"""
        if node:
            if node.left:
                if pointer == 'left':
                    parent_node.left = node.left
                elif pointer == 'right':
                    parent_node.right = node.left
            if node.right:
                if pointer == 'left':
                    parent_node.left = node.right
                elif pointer == 'right':
                    parent_node.right = node.right

    def get_child_node_pointer(self, parent_node, value):
        if parent_node.left:
            if parent_node.left.value == value:
                return 'left'
        if parent_node.right:
            if parent_node.right.value == value:
                return 'right'
        else:
            return

    def get_child_node(self, parent_node, value):
        if parent_node.left:
            if parent_node.left.value == value:
                return parent_node.left
        if parent_node.right:
            if parent_node.right.value == value:
                return parent_node.right
        return

    def count_children(self, node):
        children = 0
        if node.left:
            children += 1
        if node.right:
            children += 1
        return children

    def check_child_nodes(self, value, node):
        """returns a node with matching value or None"""
        if node.left:
            if node.left.value == value:
                return node
        if node.right:
            if node.right.value == value:
                return node
        return

    # ANALYZE RECURSIVE CALLS HERE AGAIN
    ####################################################
    def max_depth(self, node='root'):
        if node == 'root':
            node = self.root_node
        if not node:
            return 0

        depth_left = self.max_depth(node.left)
        depth_right = self.max_depth(node.right)
        return max(depth_left, depth_right) + 1
    ####################################################

    def is_balanced(self, node='root'):
        if node == 'root':
            node = self.root_node
        if not node:
            return

        left = self.max_depth(node.left)
        right = self.max_depth(node.right)
        if abs(left - right) <= 1:
            return True
        else:
            return False

    def to_array(self, node='root', array='empty'):
        """Converts BST to ordered Array (in-order traversal)"""
        if node == 'root':
            node = self.root_node
        if array == 'empty':
            array = []
        if not node:
            return array

        self.to_array(node.left, array)
        array.append(node.value)
        self.to_array(node.right, array)

        return array

    def rebalance(self):
        if self.is_balanced():
            print('BST is already balanced.')
            return
        self.init_array = self.to_array()
        self.root_node = self.array_to_bst()

    def print_tree(self, node='root', prefix='', is_left=True):
        if node == 'root':
            node = self.root_node
        if node:
            if node.right:
                self.print_tree(node.right, f"{prefix}{'|    ' if is_left else '     '}", False)
            print(f"{prefix}{'└───' if is_left else '┌───'}" + "<" + str(node.value) + ">")
            if node.left:
                self.print_tree(node.left, f"{prefix}{'     ' if is_left else '|    '}", True)


# --------------DRIVER SCRIPT-------------- #

# List of random integers with no duplicate values
starting_list = list(set(sample(range(1, 101), 15)))

# Build a tree and print it
tree = BST(starting_list)
tree.print_tree()

# Insert nodes
print('---------------------------------------------------------')
print('Inserting 0, 50, 150 into BST')
tree.insert(0)
tree.insert(50)
tree.insert(150)
tree.print_tree()

# Delete leaf node
print('---------------------------------------------------------')
print('Deleting node with value: 50 (leaf node)')
tree.delete(50)
tree.print_tree()

# Inserting nodes to force off-balance state, then rebalancing the tree
print('---------------------------------------------------------')
print('Inserting more nodes...')
tree.insert(160)
tree.insert(170)
tree.print_tree()
print('This tree is not balanced now!')
print('is_balanced returned ' + str(tree.is_balanced()) + '\n')
print('Rebalancing the tree...')
tree.rebalance()
tree.print_tree()
if tree.is_balanced():
    print('Now it looks balanced to me.')

# Asking for input to delete nodes
val = int

try:
    while val or val == 0:
        val = int(input('Insert value to delete or press enter to exit: '))
        tree.delete(val)
        tree.print_tree()
except ValueError:
    print('Bye!')

# TODO: analyze that pesky recursion at line 202
