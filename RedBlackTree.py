class Node:
    def __init__(self, key, color="RED"):
        self.key = key
        self.color = color  # New nodes are always RED
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0, "BLACK")  # Sentinel node
        self.root = self.TNULL

    def insert(self, key):
        new_node = Node(key)
        new_node.left = self.TNULL
        new_node.right = self.TNULL
        parent = None
        current = self.root

        while current != self.TNULL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if not parent:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = "RED"
        self._fix_insert(new_node)

    def _fix_insert(self, node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.left:
                uncle = node.parent.parent.right
                if uncle and uncle.color == "RED":  # Case 1: Recoloring
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:  # Case 2 & 3: Rotations
                    if node == node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._right_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.left
                if uncle and uncle.color == "RED":  # Case 1: Recoloring
                    node.parent.color = "BLACK"
                    uncle.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:  # Case 2 & 3: Rotations
                    if node == node.parent.left:
                        node = node.parent
                        self._right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self._left_rotate(node.parent.parent)

        self.root.color = "BLACK"

    def delete(self, key):
        self._delete_node(self.root, key)

    def _delete_node(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.key == key:
                z = node
                break
            elif key < node.key:
                node = node.left
            else:
                node = node.right

        if z == self.TNULL:
            print("Key not found in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._min_value_node(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self._fix_delete(x)

    def _fix_delete(self, node):
        while node != self.root and node.color == "BLACK":
            if node == node.parent.left:
                sibling = node.parent.right
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    node.parent.color = "RED"
                    self._left_rotate(node.parent)
                    sibling = node.parent.right
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    sibling.color = "RED"
                    node = node.parent
                else:
                    if sibling.right.color == "BLACK":
                        sibling.left.color = "BLACK"
                        sibling.color = "RED"
                        self._right_rotate(sibling)
                        sibling = node.parent.right
                    sibling.color = node.parent.color
                    node.parent.color = "BLACK"
                    sibling.right.color = "BLACK"
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling.color == "RED":
                    sibling.color = "BLACK"
                    node.parent.color = "RED"
                    self._right_rotate(node.parent)
                    sibling = node.parent.left
                if sibling.left.color == "BLACK" and sibling.right.color == "BLACK":
                    sibling.color = "RED"
                    node = node.parent
                else:
                    if sibling.left.color == "BLACK":
                        sibling.right.color = "BLACK"
                        sibling.color = "RED"
                        self._left_rotate(sibling)
                        sibling = node.parent.left
                    sibling.color = node.parent.color
                    node.parent.color = "BLACK"
                    sibling.left.color = "BLACK"
                    self._right_rotate(node.parent)
                    node = self.root

        node.color = "BLACK"

    def _transplant(self, u, v):
        if not u.parent:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _left_rotate(self, node):
        y = node.right
        node.right = y.left
        if y.left != self.TNULL:
            y.left.parent = node
        y.parent = node.parent
        if not node.parent:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y

    def _right_rotate(self, node):
        y = node.left
        node.left = y.right
        if y.right != self.TNULL:
            y.right.parent = node
        y.parent = node.parent
        if not node.parent:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y

    def _min_value_node(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def inorder(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        return self._inorder(node.left) + [(node.key, node.color)] + self._inorder(node.right) if node != self.TNULL else []
# Test Cases for Red-Black Tree
rbt = RedBlackTree()
rbt.insert(10)
rbt.insert(20)
rbt.insert(30)
rbt.insert(40)
rbt.insert(50)
rbt.insert(60)
rbt.insert(70)
rbt.insert(25)
print("Red-Black Tree root:", rbt.inorder())  # Root should follow RBT rules

print("Red-Black Tree inorder after insertion:", rbt.inorder())

rbt.delete(25)
print("Red-Black Tree inorder after deleting the key is:", rbt.inorder())

rbt.delete(30)
print("Red-Black Tree inorder after deleting the key is:", rbt.inorder())

rbt.delete(10)
print("Red-Black Tree inorder after deleting the key is:", rbt.inorder())