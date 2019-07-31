# -*- coding: utf-8 -*-
# file_func  :
# file_author: 'Johnathan.Wick'
# file_date  : '6/26/2019 8:44 AM'

# no.100

# Definition for a binary tree node.


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        def dfs(tree):
            if tree:
                yield tree.val
                if not tree.left and tree.right:
                    yield 'null'
                yield from dfs(tree.left)
                yield from dfs(tree.right)

        def bfs(tree):
            node_list = [tree]
            while node_list:
                layer = []
                layer_node = []
                for node in node_list:
                    # node = node_list.pop(0)
                    layer.append(node.val)
                    if node.left:
                        layer_node.append(node.left)
                    if node.right:
                        layer_node.append(node.right)
                    if not node.left and node.right:
                        layer.append('null')
                if layer != layer[-1::-1]:
                    return False
                node_list = layer_node
            return True

        # p_list = list(dfs(p))
        q_list = bfs(q)
        print(q_list)
        return q_list


a = TreeNode(1)
b_1 = TreeNode(2)
b_2 = TreeNode(3)
c_1 = TreeNode(4)
c_2 = TreeNode(5)
a.left = b_1
a.right = b_2
b_1.left = c_1
b_1.right = c_2

aa = TreeNode(1)
bb_1 = TreeNode(2)
bb_2 = TreeNode(2)
cc_1 = TreeNode(3)
cc_2 = TreeNode(4)
cc_3 = TreeNode(4)
cc_4 = TreeNode(3)
dd_1 = TreeNode(5)
dd_2 = TreeNode(6)
dd_3 = TreeNode(7)

aa.left = bb_1
aa.right = bb_2
bb_1.left = cc_1
bb_1.right = cc_2
bb_2.left = cc_3
bb_2.right = cc_4
cc_1.left = dd_2
cc_4.right = dd_1


# print(Solution().isSameTree(a, aa))

# no.104

class Solution104:
    def maxDepth(self, root: TreeNode) -> int:

        def dfs(root, c=0):
            if not root:
                c = c - 1
            if root:
                c = 1 + c
                yield c
                yield from dfs(root.left, c=c)
                yield from dfs(root.right, c=c)

        return sorted(list(dfs(root)))[-1]


# res = Solution104().maxDepth(a)
# print('104 res--------->', res)

# no.110
class Solution110:
    def isBalanced(self, root: TreeNode) -> bool:
        res = self.depth(root)
        print('final value is ', res)
        return res != -1

    def depth(self, root):
        if not root:
            return 0
        left = self.depth(root.left)
        if left == -1:
            return -1
        right = self.depth(root.right)
        if right == -1:
            return -1
        print(left, right, '--->', root.val)
        return max(left, right) + 1 if abs(left - right) < 2 else -1


# Solution110().isBalanced(aa)


# no.111
class Solution111:
    def minDepth(self, root: TreeNode) -> int:
        if not root:
            return 0
        g = self.helper(root)
        print(g)
        # l = list(g)
        # print('unsorted -------->', l)
        # l = sorted(l)
        # print('l----->', l)
        # return l[0]

    def helper(self, root, c=0):
        if not root:
            return c
        else:
            c += 1
            left = self.helper(root.left, c)
            right = self.helper(root.right, c)
            print(left, right, root.val)
            return min(left, right)


# print(Solution111().minDepth(aa))
#
# a111 = TreeNode(1)
# b111 = TreeNode(2)
# a111.left = b111
#
# print(Solution111().minDepth(a111))


# No.112

class Solution112:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        g = self.helper(root)
        for total in g:
            if sum == total:
                return True
        return False

    def helper(self, root, total=0):
        if not root:
            return 0
        if root:
            total += root.val
            if not root.left and not root.right:
                yield total
            yield from self.helper(root.left, total)
            yield from self.helper(root.right, total)


a = TreeNode(5)
b1 = TreeNode(4)
b2 = TreeNode(8)
c1 = TreeNode(11)
c2 = TreeNode(13)
c3 = TreeNode(4)
d1 = TreeNode(7)
d2 = TreeNode(2)
d3 = TreeNode(1)

a.left = b1
a.right = b2
b1.left = c1
b2.left = c2
b2.right = c3
c1.left = d1
c1.right = d2
c3.right = d3


# print(Solution112().hasPathSum(a, 22))


# No.257
class Solution257:
    def binaryTreePaths(self, root: TreeNode) -> list:
        res = []
        if not root:
            return res
        for g in self.helper(root):
            res.append('->'.join(g))
        return res

    def helper(self, root, temp=[]):
        if root:
            temp.append(str(root.val))
            if not root.left and not root.right:
                yield temp
            yield from self.helper(root.left, temp)
            yield from self.helper(root.right, temp)
            temp.pop()


print(Solution257().binaryTreePaths(a))
