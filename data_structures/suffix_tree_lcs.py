# Suffix Tree implementation to help solve the longest common substring problem.
# Date: 10-11-2022
# Author: Samir Gupta


from typing import Iterator


class SuffixTree:
    '''
    Representation of a suffix tree using a suffix array for all lower case alphabetic (and space) strings.
    '''

    class SuffixTreeNode:
        '''
        Node contained in the suffix tree.
        '''

        def __init__(self, string: str = '', children: list[int] | None = None, /, *, total_esc: int):
            '''
            Initialise the suffix tree node.
            - Input:
                - total_esc (int): The total amount of escaping characters present in the tree.
                - string (str, optional): The string represented by this node. Defaults to ''.
                - children (list[int] | None, optional): The list of indicies of child nodes of this node. Defaults to None.
            - Time Complexity: O(n), where n is the amount of escaping characters in the suffix tree.
            - Aux space complexity: O(n).
            '''
            self.string = string
            self.children = children or []  # initialise children
            self.marks = [''] * total_esc  # initialise marks array

    def __init__(self, *strings: str):
        '''
        Initialise the suffix tree.
        - Input:
            - *strings (str): Any number of strings to add to the suffix tree
        - Time Complexity: O(n*s^2), where n is the number of string and s is the sum of the lengths of the strings.
        - Aux space complexity: O(n*s^2).
        '''
        self.nodes = [self.SuffixTreeNode(total_esc=len(strings))]  # initialise head node in array
        self._strings = strings
        self._add_strings()  # add strings to tree O(n*s^2)
        self._mark_tree(self.nodes[0])  # mark the tree O(n*s)

    def _add_strings(self):
        '''
        Add the suffix tree's strings into the tree .
        - Time Complexity: O(n*s^2), where n is the number of string and s is the sum of the lengths of the strings.
        - Aux space complexity: O(n*s^2).
        '''
        for i, string in enumerate(self._strings):  # O(n*s^2)
            string += f'{i}'  # add null character unique to each string
            self.curr_suffixes = [string[i:] for i in range(len(string))]

            for suff_no, suffix in enumerate(self.curr_suffixes):  # O(s^2)
                self._add_string_suffix(suffix, suff_no)  # add each suffix

    def _add_string_suffix(self, suffix: str, suff_no: int):
        '''
        Add a string's suffix to the suffix tree.
        - Input:
            - suffix (str): The suffix to add.
            - suff_no (int): The index of the suffix in self.curr_suffixes.
        - Time Complexity: O(N), where N is the length of the suffix.
        - Aux space complexity: O(N).
        '''
        i = 0  # keep track of where we are in the string
        current_n = 0  # current node index
        while i < len(suffix):
            tree_pos = 0  # current position in the tree
            char = suffix[i]  # current character in suffix
            while True:
                children = self.nodes[current_n].children  # get the current children
                if tree_pos == len(children):  # no matching child, remainder of suffix becomes new node
                    new_n = len(self.nodes)  # get the new node index
                    self.nodes.append(self.SuffixTreeNode(self.curr_suffixes[suff_no + i], total_esc=len(self._strings)))  # add the rest of the suffix onto the nodde
                    self.nodes[current_n].children.append(new_n)  # add the new node as the child of the current one
                    return
                new_n = children[tree_pos]
                if self.nodes[new_n].string[0] == char:
                    break
                tree_pos = tree_pos + 1

            # find the common ground between the prefix of substring and child's suffix
            j = 0
            substring = self.nodes[new_n].string
            while j < len(substring):
                if suffix[i + j] != substring[j]:  # if we found the part in common
                    new_n, common_n = len(self.nodes), new_n
                    self.nodes.append(self.SuffixTreeNode(substring[:j], [common_n], total_esc=len(self._strings)))  # create the node
                    self.nodes[common_n].string = substring[j:]  # old node loses the part in common
                    self.nodes[current_n].children[tree_pos] = new_n
                    break
                j = j + 1

            i = i + j  # advance past part in common
            current_n = new_n  # continue down the tree

    def _mark_tree(self, curr: SuffixTreeNode) -> Iterator[bool]:
        '''
        Add markers to the nodes of the tree to indicate which string(s) the node's suffix belongs to.
        - Input:
            - curr (SuffixTreeNode): The current suffix node.
        - Returns (Generator[bool, None, None]): Generator of whether we have found a marker or not in curr or below.
        - Time Complexity: O(n*s), where n is the amount of strings in the tree and s is the sum of the lengths of those strings.
        - Aux space complexity: O(n*s).
        '''
        for child in curr.children:  # dfs approach
            found_gen = self._mark_tree(self.nodes[child])
            for i, found in enumerate(found_gen):  # if we have found a marker below
                if found:
                    curr.marks[i] = f'{i}'

        # return whether we have found a marker below of have a marker in curr for each marker
        return (bool(mark) or curr.string[-1] == f'{c}' for c, mark in enumerate(curr.marks))

    def longest_common_substring(self) -> str:
        '''
        Get the longest common substring between the strings in the suffix tree.
        - Returns (str): The longest common substring.
        - Time Complexity: O(s), where s is the sum of the lengths of strings inside the suffix tree.
        - Aux space complexity: O(s).
        '''
        solution = ['']  # store the lcs
        self._longest_common_substring_aux(self.nodes[0], solution)  # solve for it
        return solution[0]  # return it

    def _longest_common_substring_aux(self, curr: SuffixTreeNode, sol: list[str], curr_str: str = ''):
        '''
        Find the longest common substring by using a variation of DFS that checks the marks on each node. If a node has all markers it is a common substring so find the longest one.
        - Input:
            - curr (SuffixTreeNode): The current tree node.
            - sol (list[str]): The current solution state.
            - curr_str (str, optional): The current string formed when diving down the tree. Defaults to ''.
        - Time Complexity: O(s), where s is the sum of the lengths of strings inside the suffix tree.
        - Aux space complexity: O(s).
        '''
        for i in curr.children:
            child = self.nodes[i]
            self._longest_common_substring_aux(child, sol, curr_str + child.string)
            if all(child.marks):  # check if there is a common substring
                new_str = curr_str + child.string  # get the new common subtring
                if len(new_str) > len(sol[0]):  # update solution if this new common substring is the longer than the currently found one
                    sol[0] = new_str

    def __repr__(self) -> str:
        """
        Represent the suffix tree as a string.
        - Returns (str): The string representation of the string.
        - Time Complexity: O(n), where n is the amount of nodes in the tree.
        - Aux space complexity: O(n).
        """
        if len(self.nodes) == 0:
            return "<empty>"

        out = ['']

        def traverse(node_index: int, prefix: str):
            children = self.nodes[node_index].children
            if len(children) == 0:
                out[0] += f"-- {self.nodes[node_index].string}\n"
                return
            out[0] += f"+- {self.nodes[node_index].string}\n"
            for c in children[:-1]:
                out[0] += f"{prefix} +-"
                traverse(c, prefix + " |")
            out[0] += f"{prefix} +-"
            traverse(children[-1], prefix + "  ")

        traverse(0, "")
        return out[0]


def main():
    x = SuffixTree('banana')
    print(x)


if __name__ == '__main__':
    main()
