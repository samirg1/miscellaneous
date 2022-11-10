# avl.py
# Date: 03-10-2022
# Author: Samir Gupta

from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, TypeVar, cast

from bst import BinarySearchTree, TreeNode


# comparable protocol
class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: _K, __other: _K) -> bool:
        pass


# type variables to use in tree
_K = TypeVar("_K", bound=Comparable)
_I = TypeVar("_I")


class AVLTreeNode(TreeNode[_K, _I]):
    """Node class for AVL trees.
    Objects of this class have an additional variable - height.
    """

    def __init__(self, key: _K, item: _I = None) -> None:
        """
        Initialises the node with a key and optional item
        and sets the left and right pointers to None
        :complexity: O(1)
        """
        super().__init__(key, item)  # type: ignore
        self.height = 1
        self.right_count = 0  # keep track of total nodes in the right subtree


class AVLTree(BinarySearchTree[_K, _I]):
    """Self-balancing binary search tree using rebalancing by sub-tree rotations of Adelson-Velsky and Landis (AVL)."""

    def __init__(self) -> None:
        """
        Initialises an empty Binary Search Tree
        :complexity: O(1)
        """
        super().__init__()

    def __repr__(self) -> str:
        return super().__repr__()

    def get_height(self, current: AVLTreeNode[_K, _I]) -> int:
        """
        Get the height of a node. Return current.height if current is
        not None. Otherwise, return 0.
        :complexity: O(1)
        """

        if current is not None:
            return current.height
        return 0

    def __get_balance(self, current: AVLTreeNode[_K, _I]) -> int:
        """
        Compute the balance factor for the current sub-tree as the value
        (right.height - left.height). If current is None, return 0.
        :complexity: O(1)
        """

        if current is None:
            return 0
        return self.get_height(cast(AVLTreeNode[_K, _I], current.right)) - self.get_height(cast(AVLTreeNode[_K, _I], current.left))

    def __insert_aux(self, current: TreeNode[_K, _I], key: _K, item: _I) -> AVLTreeNode[_K, _I]:
        """
        Attempts to insert an item into the tree, it uses the Key to insert
        it. After insertion, performs sub-tree rotation whenever it becomes
        unbalanced.
        returns the new root of the subtree.
        :complexity: O(log(N)), where N is the amount of nodes in the tree
        """
        if current is None:
            current = AVLTreeNode(key, item)
            self._length += 1
        elif key < current.key:
            current.left = self.__insert_aux(cast(AVLTreeNode[_K, _I], current.left), key, item)
        elif key != current.key and not key < current.key:
            cast(AVLTreeNode[_K, _I], current).right_count += 1
            current.right = self.__insert_aux(cast(AVLTreeNode[_K, _I], current.right), key, item)
        else:
            current.item = item

        cast(AVLTreeNode[_K, _I], current).height = 1 + max(self.get_height(cast(AVLTreeNode[_K, _I], current.left)), self.get_height(cast(AVLTreeNode[_K, _I], current.right)))

        return self.__rebalance(cast(AVLTreeNode[_K, _I], current))

    def __delete_aux(self, current: TreeNode[_K, _I], key: _K) -> TreeNode[_K, _I] | None:
        """
        Attempts to delete an item from the tree, it uses the Key to
        determine the node to delete. After deletion,
        performs sub-tree rotation whenever it becomes unbalanced.
        returns the new root of the subtree.
        :complexity worst: O(log(N)), where N is the amount of nodes in the tree
        :complexity best: O(1) due to early exit options, e.g. if the node to delete is the root node without anything to either the left or right
        """
        if current is None:
            raise ValueError("Deleting non-existent item")
        elif key < current.key:
            current.left = self.__delete_aux(cast(AVLTreeNode[_K, _I], current.left), key)
        elif key != current.key and not key < current.key:
            cast(AVLTreeNode[_K, _I], current).right_count -= 1
            current.right = self.__delete_aux(cast(AVLTreeNode[_K, _I], current.right), key)
        else:
            if self._is_leaf(current):
                self._length -= 1
                return None
            elif current.left is None:
                self._length -= 1
                return cast(AVLTreeNode[_K, _I], current).right
            elif current.right is None:
                self._length -= 1
                return cast(AVLTreeNode[_K, _I], current).left

            succ = self._get_successor(current)
            current.key = cast(AVLTreeNode[_K, _I], succ).key
            current.item = cast(AVLTreeNode[_K, _I], succ).item
            cast(AVLTreeNode[_K, _I], current).right_count -= 1
            current.right = self.__delete_aux(current.right, cast(AVLTreeNode[_K, _I], succ).key)

        cast(AVLTreeNode[_K, _I], current).height = 1 + max(self.get_height(cast(AVLTreeNode[_K, _I], current.left)), self.get_height(cast(AVLTreeNode[_K, _I], current.right)))

        return self.__rebalance(cast(AVLTreeNode[_K, _I], current))

    def __left_rotate(self, current: AVLTreeNode[_K, _I]) -> AVLTreeNode[_K, _I]:
        """
        Perform left rotation of the sub-tree.
        Right child of the current node, i.e. of the root of the target
        sub-tree, should become the new root of the sub-tree.
        returns the new root of the subtree.
        Example:

             current                                       child
            /       |                                      /    |
        l-tree     child           -------->        current     r-tree
                  /     |                           /     |
             center     r-tree                 l-tree     center

        :complexity: O(1)
        """
        child = cast(AVLTreeNode[_K, _I], current.right)
        center = child.left

        child.left = current
        current.right = center
        current.right_count = current.right_count - 1 - child.right_count

        current.height = 1 + max(self.get_height(cast(AVLTreeNode[_K, _I], current.left)), self.get_height(cast(AVLTreeNode[_K, _I], current.right)))
        child.height = 1 + max(self.get_height(child.left), self.get_height(cast(AVLTreeNode[_K, _I], child.right)))

        return child

    def __right_rotate(self, current: AVLTreeNode[_K, _I]) -> AVLTreeNode[_K, _I]:
        """
        Perform right rotation of the sub-tree.
        Left child of the current node, i.e. of the root of the target
        sub-tree, should become the new root of the sub-tree.
        returns the new root of the subtree.
        Example:

                   current                                child
                  /       |                              /     |
              child       r-tree     --------->     l-tree     current
             /     |                                           /     |
        l-tree     center                                 center     r-tree

        :complexity: O(1)
        """
        child = cast(AVLTreeNode[_K, _I], current.left)
        center = child.right

        child.right = current
        child.right_count = child.right_count + current.right_count + 1
        current.left = center

        current.height = 1 + max(self.get_height(cast(AVLTreeNode[_K, _I], current.left)), self.get_height(cast(AVLTreeNode[_K, _I], current.right)))
        child.height = 1 + max(self.get_height(cast(AVLTreeNode[_K, _I], child.left)), self.get_height(child.right))

        return child

    def __rebalance(self, current: AVLTreeNode[_K, _I]) -> AVLTreeNode[_K, _I]:
        """
        Compute the balance of the current node.
        Do rebalancing of the sub-tree of this node if necessary.
        Rebalancing should be done either by:
        - one left rotate
        - one right rotate
        - a combination of left + right rotate
        - a combination of right + left rotate
        returns the new root of the subtree.
        :complexity: O(1), all operations (including rotations) are all O(1).
        """
        if self.__get_balance(current) >= 2:
            child = cast(AVLTreeNode[_K, _I], current.right)
            if self.get_height(cast(AVLTreeNode[_K, _I], child.left)) > self.get_height(cast(AVLTreeNode[_K, _I], child.right)):
                current.right = self.__right_rotate(child)
            return self.__left_rotate(current)

        if self.__get_balance(current) <= -2:
            child = cast(AVLTreeNode[_K, _I], current.left)
            if self.get_height(cast(AVLTreeNode[_K, _I], child.right)) > self.get_height(cast(AVLTreeNode[_K, _I], child.left)):
                current.left = self.__left_rotate(child)
            return self.__right_rotate(current)

        return current

    def kth_largest(self, k: int) -> AVLTreeNode[_K, _I]:
        """
        Returns the kth largest element in the tree.
        k=1 would return the largest.
        :complexity: O(log(N)), where N is the amount of nodes in the tree
        """
        if k < 1 or k > len(self):
            raise ValueError("Invalid k value, has to satisfy 1 <= k <= length of tree")
        return self.__kth_largest_aux(cast(AVLTreeNode[_K, _I], self.root), k)

    def __kth_largest_aux(self, current: AVLTreeNode[_K, _I], k: int) -> AVLTreeNode[_K, _I]:
        """
        This method works by utilising the right_count attribtue that stores the amount of nodes to the right of the current subtree.
        The method utilises this attribute and modifyies the k value as you go in response to the right_count.
        Therefore each iteration will go either left or right, therefore achieving O(log(N)) complexity.

        Returns the kth largest element in the tree.
        k=1 would return the largest.
        :complexity: O(log(N)), where N is the amount of nodes in the tree
        """
        # base case where k == current.right_count + 1
        if current.right_count + 1 == k:
            return current

        # if there are more to the right than k we go right
        elif current.right_count + 1 > k:
            return self.__kth_largest_aux(cast(AVLTreeNode[_K, _I], current.right), k)

        # if there a less to the right than k, we go left and edit the k value
        # this way we are finding the (k-current.right_count-1)th largest in the left subtree as we know the kth largest are in the right
        else:  # current.right_count + 1 < k
            return self.__kth_largest_aux(cast(AVLTreeNode[_K, _I], current.left), k - current.right_count - 1)


def main():
    x: AVLTree[int, str] = AVLTree()
    x[1] = "a"
    x[2] = "b"
    x[3] = "c"
    x[4] = "d"


if __name__ == "__main__":
    main()
