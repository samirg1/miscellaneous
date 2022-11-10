# bst.py
# Date: 03-10-2022
# Author: Samir Gupta

from __future__ import annotations

from abc import abstractmethod
from typing import Generic, Protocol, TypeVar, cast


# comparable protocol
class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: _K, __other: _K) -> bool:
        pass


# type variables to use in tree
_K = TypeVar("_K", bound=Comparable)
_I = TypeVar("_I")


class TreeNode(Generic[_K, _I]):
    """Node class represent BST nodes."""

    def __init__(self, key: _K, item: _I = None) -> None:
        """
        Initialises the node with a key and optional item
        and sets the left and right pointers to None
        :complexity: O(1)
        """
        self.key: _K = key
        self.item = item
        self.left: TreeNode[_K, _I] | None = None
        self.right: TreeNode[_K, _I] | None = None

    def __str__(self):
        """
        Returns the string representation of a node
        :complexity: O(N) where N is the size of the item
        """
        return "({0}, {1})".format(self.key, self.item)


class BinarySearchTree(Generic[_K, _I]):
    """Basic binary search tree."""

    def __init__(self) -> None:
        """
        Initialises an empty Binary Search Tree
        :complexity: O(1)
        """

        self.root: TreeNode[_K, _I] | None = None
        self._length = 0

    def is_empty(self) -> bool:
        """
        Checks to see if the bst is empty
        :complexity: O(1)
        """
        return self.root is None

    def __len__(self) -> int:
        """Returns the number of nodes in the tree."""
        return self._length

    def __contains__(self, key: _K) -> bool:
        """
        Checks to see if the key is in the BST
        :complexity: see __getitem__(self, key: K) -> (K, I)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: _K) -> _I:
        """
        Attempts to get an item in the tree, it uses the Key to attempt to find it
        :complexity best: O(CompK) finds the item in the root of the tree
        :complexity worst: O(CompK * D) item is not found, where D is the depth of the tree
        CompK is the complexity of comparing the keys
        """
        return cast(_I, self.__get_tree_node_by_key(key).item)

    def __get_tree_node_by_key(self, key: _K) -> TreeNode[_K, _I]:
        return self.__get_tree_node_by_key_aux(cast(TreeNode[_K, _I], self.root), key)

    def __get_tree_node_by_key_aux(self, current: TreeNode[_K, _I], key: _K) -> TreeNode[_K, _I]:
        if current is None:  # base case: empty
            raise KeyError("Key not found: {0}".format(key))
        elif key == current.key:  # base case: found
            return current
        elif key < current.key:
            return self.__get_tree_node_by_key_aux(cast(TreeNode[_K, _I], current.left), key)
        else:  # key > current.key
            return self.__get_tree_node_by_key_aux(cast(TreeNode[_K, _I], current.right), key)

    def __getitem_aux(self, current: TreeNode[_K, _I], key: _K) -> _I:
        if current is None:  # base case: empty
            raise KeyError("Key not found: {0}".format(key))
        elif key == current.key:  # base case: found
            return cast(_I, current.item)
        elif key < current.key:
            return self.__getitem_aux(cast(TreeNode[_K, _I], current.left), key)
        else:  # key > current.key
            return self.__getitem_aux(cast(TreeNode[_K, _I], current.right), key)

    def __setitem__(self, key: _K, item: _I) -> None:
        self._length += 1
        self.root = self.__insert_aux(cast(TreeNode[_K, _I], self.root), key, item)

    def __insert_aux(self, current: TreeNode[_K, _I], key: _K, item: _I) -> TreeNode[_K, _I]:
        """
        Attempts to insert an item into the tree, it uses the Key to insert it
        :complexity best: O(CompK) inserts the item at the root.
        :complexity worst: O(CompK * D) inserting at the bottom of the tree
        where D is the depth of the tree
        CompK is the complexity of comparing the keys
        """
        if current is None:  # base case: at the leaf
            current = TreeNode(key, item)
            self._length += 1
        elif key < current.key:
            current.left = self.__insert_aux(cast(TreeNode[_K, _I], current.left), key, item)
        elif key != current.key and not key < current.key:
            current.right = self.__insert_aux(cast(TreeNode[_K, _I], current.right), key, item)
        else:  # key == current.key
            raise ValueError("Inserting duplicate item")
        return current

    def __delitem__(self, key: _K) -> None:
        self._length -= 1
        self.root = self.__delete_aux(cast(TreeNode[_K, _I], self.root), key)

    def __delete_aux(self, current: TreeNode[_K, _I], key: _K) -> TreeNode[_K, _I] | None:
        """
        Attempts to delete an item from the tree, it uses the Key to
        determine the node to delete.
        """

        if current is None:  # key not found
            raise ValueError("Deleting non-existent item")
        elif key < current.key:
            current.left = self.__delete_aux(cast(TreeNode[_K, _I], current.left), key)
        elif key != current.key and not key < current.key:
            current.right = self.__delete_aux(cast(TreeNode[_K, _I], current.right), key)
        else:  # we found our key => do actual deletion
            if self._is_leaf(current):
                self._length -= 1
                return None
            elif current.left is None:
                self._length -= 1
                return current.right
            elif current.right is None:
                self._length -= 1
                return current.left

            # general case => find a successor
            succ = self._get_successor(current)
            current.key = cast(TreeNode[_K, _I], succ).key
            current.item = cast(TreeNode[_K, _I], succ).item
            current.right = self.__delete_aux(current.right, cast(TreeNode[_K, _I], succ).key)

        return current

    def __get_minimal(self, current: TreeNode[_K, _I]) -> TreeNode[_K, _I]:
        """
        Get a node having the smallest key in the current sub-tree.
        :complexity worst: O(n)
        In the worst case the tree is very unbalanced and therefore it must go
        through every node to find the minimal node. Hence the complexity is
        proportional to n.

        :complexity best: O(1)
        In the best case, it is possible for the tree to be very unbalanced,
        such that the all the nodes are to the right.

        I rejected a recursive solution as even though it is a one liner,
        the use of recursion in this case is not advantagous, as it would
        store the previous stack frames in the computers memory, even though
        these are not actually used, therefore it is less memory efficient.
        """
        while current.left:  # get the smallest value in this node
            current = current.left
        return current

        ## recursive implementation ##
        # return self.get_minimal(current.left) if current.left else current

    def _get_successor(self, current: TreeNode[_K, _I]) -> TreeNode[_K, _I] | None:
        """
        Get successor of the current node.
        It should be a child node having the smallest key among all the
        larger keys.

        :complexity worst: O(n) - this function calls get_minimal once, which is
        worst case O(n). The if statment is constant time and hence, the
        function remains O(n)

        :complexity best: O(1). The best case complexity is the same
        as is for the function get_minimal.
        """
        return self.__get_minimal(current.right) if current.right else None

    def _is_leaf(self, current: TreeNode[_K, _I]) -> bool:
        """Simple check whether or not the node is a leaf."""

        return current.left is None and current.right is None

    def __repr__(self) -> str:
        return self.__draw()

    def __draw(self) -> str:
        """Draw the tree in the terminal."""
        output = ""

        def draw_aux(current: TreeNode[_K, _I], prefix: str = "", final: str = "") -> None:
            """Draw a node and then its children."""
            nonlocal output
            if current is not None:
                real_prefix = prefix[:-2] + final
                output += f"{real_prefix}{current.key}\n"

                if current.left or current.right:
                    draw_aux(cast(TreeNode[_K, _I], current.left), prefix=prefix + "\u2551 ", final="\u255f\u2500")
                    draw_aux(cast(TreeNode[_K, _I], current.right), prefix=prefix + "  ", final="\u2559\u2500")
            else:
                real_prefix = prefix[:-2] + final
                output += f"{real_prefix}\n"

        draw_aux(cast(TreeNode[_K, _I], self.root))
        return output
