class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        return self._balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            min_larger_node = self._min_value_node(node.right)
            node.key = min_larger_node.key
            node.right = self._delete(node.right, min_larger_node.key)

        return self._balance(node)

    def _balance(self, node):
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1:  # Left Heavy
            if self._get_balance(node.left) < 0:  
                node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1:  # Right Heavy
            if self._get_balance(node.right) > 0:
                node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node  # Already balanced

    def _left_rotate(self, node):
        new_root = node.right
        node.right = new_root.left
        new_root.left = node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))
        return new_root

    def _right_rotate(self, node):
        new_root = node.left
        node.left = new_root.right
        new_root.right = node
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        new_root.height = 1 + max(self._get_height(new_root.left), self._get_height(new_root.right))
        return new_root

    def _get_height(self, node):
        return node.height if node else 0

    def _get_balance(self, node):
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        return self._inorder(node.left) + [node.key] + self._inorder(node.right) if node else []
# **Testing AVL Tree with Insert & Delete**
avl = AVLTree()
avl.insert(50)
avl.insert(30)
avl.insert(70)
avl.insert(20)
avl.insert(10)
avl.insert(40)
avl.insert(60)
avl.insert(80)
print("AVL Tree inorder after insertion:",avl.inorder())

avl.delete(30)  # Deleting a node with two children
print("AVL Tree inorder after deleting the key is:", avl.inorder())

avl.delete(10)  # Deleting a node with one child
print("AVL Tree inorder after deleting the key is:", avl.inorder())

avl.delete(50)  # Deleting a leaf node
print("AVL Tree inorder after deleting the key is:", avl.inorder())
