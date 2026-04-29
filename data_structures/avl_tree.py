from data_structures.arraylist import ArrayList


class AVLNode:
    def __init__(self, key, value):
        self.key = key
        self.values = ArrayList()
        self.values.append(value)
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1


class AVLTree:
    """Self-balancing BST for score range queries and rank lookup."""
    
    def __init__(self):
        self.root = None

    def _height(self, node):
        return node.height if node is not None else 0

    def _size(self, node):
        return node.size if node is not None else 0

    # Update height and size of a node based on its children and values.
    def _update(self, node):
        if node is None:
            return None
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        node.size = len(node.values) + self._size(node.left) + self._size(node.right)
        return node

    # used to determine if tree is unbalanced and which rotations to perform
    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def rotate_right(self, y):
        x = y.left
        t2 = x.right

        x.right = y
        y.left = t2

        self._update(y)
        self._update(x)

        return x


    def rotate_left(self, x):
        y = x.right
        t2 = y.left

        y.left = x
        x.right = t2

        self._update(x)
        self._update(y)

        return y


    def balance(self, node):
        self._update(node)
        balance = self._balance_factor(node)

        if balance > 1:
            if self._balance_factor(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1:
            if self._balance_factor(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node
    def insert(self, key, value):
        self.root = self.insert_node(self.root, key, value)


    def insert_node(self, node, key, value):
        if node is None:
            return AVLNode(key, value)

        if key < node.key:
            node.left = self.insert_node(node.left, key, value)

        elif key > node.key:
            node.right = self.insert_node(node.right, key, value)

        else:
            node.values.append(value)
            self._update(node)
            return node

        return self.balance(node)


    def range_query(self, low, high):
        result = ArrayList()
        self.range_query_node(self.root, low, high, result)
        return result


    def range_query_node(self, node, low, high, result):
        if node is None:
            return

        if low < node.key:
            self.range_query_node(node.left, low, high, result)

        if low <= node.key <= high:
            for item in node.values:
                result.append(item)

        if node.key < high:
            self.range_query_node(node.right, low, high, result)

    def rank_of_key_descending(self, key):
        """Returns 1-based rank for a score key, highest score rank 1."""
        higher_count = self.__count_greater_than(self.root, key)
        return higher_count + 1

    def __count_greater_than(self, node, key):
        if node is None:
            return 0
        if node.key <= key:
            return self.__count_greater_than(node.right, key)
        return len(node.values) + self._size(node.right) + self.__count_greater_than(node.left, key)

    def inorder(self):
        result = ArrayList()
        self.inorder_node(self.root, result)
        return result


    def inorder_node(self, node, result):
        if node is None:
            return

        self.inorder_node(node.left, result)

        for item in node.values:
            result.append(item)

        self.inorder_node(node.right, result)
