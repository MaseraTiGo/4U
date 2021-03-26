# -*- coding: utf-8 -*-

# ===================================
# file_name     : trees.py
# python_version: python 3.7.4
# file_author   : Johnathan.Strong
# create_time   : 2021/3/13 10:08
# ide_name      : PyCharm
# project_name  : 4U
# ===================================

from typing import List, Optional


def dfs(tree):
    if tree:
        yield tree.val
        yield from dfs(tree.left)
        yield from dfs(tree.right)


def bfs(root):
    l = [root]
    while l:
        node = l.pop(0)
        print(node.val)
        if node.left:
            l.append(node.left)
        if node.right:
            l.append(node.right)


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class GenTree(object):
    def __init__(self, values):
        if not isinstance(values, (list, tuple)):
            raise Exception('give me fucking right type ok?')
        if not values:
            raise Exception('it is fucking empty')
        self.values = values

    @property
    def tree(self):
        root_ = TreeNode(self.values[0])
        start_counter = 1
        cur_nodes = [root_]
        while cur_nodes:
            level = len(cur_nodes)
            temp = self.values[start_counter: start_counter + (2 * level)]
            start_counter += len(temp)
            if not temp:
                break
            cur_values = [temp[2 * i: 2 * (i + 1)] for i in range(2 * level)]
            cur_values = [value for value in cur_values if value]
            new_list = []
            for node, values in zip(cur_nodes, cur_values):
                left, right = values
                if left is not None:
                    new_node = TreeNode(left)
                    node.left = new_node
                    new_list.append(new_node)
                if right is not None:
                    new_node = TreeNode(right)
                    node.right = new_node
                    new_list.append(new_node)
            cur_nodes = new_list
        return root_


# test_1 = [1, 2, 3, 4, 5, 6, 7]
# test_2 = [1, 7, 0, 7, -8, None, None]
# test_3 = [3, 5, 1, 6, 2, 0, 8, None, None, 7, 4]
# root = GenTree(test_3).tree
# bfs(root)


# root_single = TreeNode(1)
# root_common_1 = TreeNode(10, TreeNode(5, TreeNode(3), TreeNode(7)), TreeNode(15, right=TreeNode(18)))
# root_common_2 = TreeNode(10, TreeNode(5, TreeNode(3), TreeNode(7)), TreeNode(15, right=TreeNode(19)))


class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        self.children = children


node_1, node_2, node_3, node_4, node_5, node_6, node_7, node_8, node_9, node_10 = [Node(i) for i in range(1, 11)]
node_11, node_12, node_13, node_14 = [Node(i) for i in range(11, 15)]

node_1.children = [node_2, node_3, node_4, node_5]
node_3.children = [node_6, node_7]
node_4.children = [node_8]
node_5.children = [node_9, node_10]
node_7.children = [node_11]
node_8.children = [node_12]
node_9.children = [node_13]
node_11.children = [node_14]


# ================================================= 94. Binary Tree Inorder Traversal ==================================

class Solution94:
    def inorderTraversal(self, root: TreeNode) -> List[int]:
        if not root:
            return []

        temp = []

        def dfs_helper(node):
            if node:
                dfs_helper(node.left)
                temp.append(node.val)
                dfs_helper(node.right)

        dfs_helper(root)
        return temp


# ================================================= 94. Binary Tree Inorder Traversal ==================================


# ================================================= 100. Same Tree =====================================================
class Solution100:
    def isSameTree(self, p: TreeNode, q: TreeNode) -> bool:
        if not all([p, q]):
            return False

        def helper_bsf(root):
            yield root.val if root else None

            if root:
                yield from helper_bsf(root.left)
                yield from helper_bsf(root.right)

        pp = list(helper_bsf(p))
        qq = list(helper_bsf(q))
        return pp == qq


# print(Solution100().isSameTree(root_common_1, root_common_2))


# ================================================= 100. Same Tree =====================================================


# ================================================= 101. Symmetric Tree ================================================

class Solution101:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return False
        l = [root]
        placeholder = TreeNode(-101)
        while l:
            cur_list = [node.val for node in l]
            if cur_list != cur_list[::-1]:
                return False
            # temp = []
            # for node in l:
            #     if hasattr(node, 'stop'):
            #         continue
            #     for sub_node in (node.left, node.right):
            #         if not sub_node:
            #             temp.append(placeholder)
            #         else:
            #             temp.append(sub_node)
            l = [sub_node if sub_node else placeholder for node in l if node.val >= -100 for sub_node in
                 (node.left, node.right)]
            # l = temp
        return True


# root_101 = TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4)), TreeNode(2, TreeNode(4), TreeNode(3)))
# root_101_2 = TreeNode(1, TreeNode(2, TreeNode(3), TreeNode(4)), TreeNode(2, TreeNode(4), TreeNode(3)))
# [2,3,3,4,5,5,4,null,null,8,9,null,null,9,8]
# root_101_3 = TreeNode(2, TreeNode(3, TreeNode(4), TreeNode(5, TreeNode(8), TreeNode(9))),
#                       TreeNode(3, TreeNode(5), TreeNode(4, TreeNode(9), TreeNode(8))))
#
# print(Solution101().isSymmetric(root_101_2))


# ================================================= 101. Symmetric Tree ================================================


# ================================================= 110. Balanced Binary Tree ==========================================

class Solution110:
    def isBalanced(self, root: TreeNode) -> bool:
        # minus = []
        def counter(root):
            if not root:
                return 0

            left = counter(root.left)
            right = counter(root.right)
            diff = abs(left - right)
            if diff > 1:
                raise Exception('not balance')
            # minus.append(abs(left-right))
            return max(left, right) + 1

        try:
            counter(root)
        except Exception as _:
            return False
        # print(minus, gen)
        # for item in minus:
        #     if item > 1:
        #         return False
        return True


# root_110 = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4)), TreeNode(3)),
#                     TreeNode(2, TreeNode(3), TreeNode(3)))
# print(Solution110().isBalanced(root_110))


# ================================================= 110. Balanced Binary Tree ==========================================


# ================================================= 111. Minimum Depth of Binary Tree ==================================

class Solution111:
    def minDepth(self, root: TreeNode) -> int:
        if not root:
            return 0

        def bfs(node):
            l = [node]
            depth = 0
            out_flag = False
            while l:
                depth += 1
                for node in l:
                    if not node.right and not node.left:
                        out_flag = True
                        break
                if out_flag:
                    break
                l = [nd for node in l for nd in (node.left, node.right) if nd]
            return depth

        return bfs(root)


# root_111_1 = TreeNode(1)
# root_111_2 = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
#
# print(Solution111().minDepth(root_111_2))


# ================================================= 111. Minimum Depth of Binary Tree ==================================


# ================================================= 112. Path Sum ======================================================

class Solution112:
    def hasPathSum(self, root: TreeNode, targetSum: int) -> bool:
        if not root:
            return False
        temp = 0

        def dfs(node):
            nonlocal temp
            if node:
                temp += node.val
                if not node.left and not node.right:
                    yield temp
                yield from dfs(node.left)
                yield from dfs(node.right)
                temp -= node.val

        for item in dfs(root):
            if item == targetSum:
                return True
        return False
        # try:
        #     dfs(root)
        # except Exception:
        #     return True
        # else:
        #     return False


# root_112 = TreeNode(1, TreeNode(2), TreeNode(3))
# root_112_2 = TreeNode(5, TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))),
#                       TreeNode(8, TreeNode(13), TreeNode(4, right=TreeNode(1))))
# root_112_3 = TreeNode(1, TreeNode(-2, TreeNode(1, TreeNode(-1)), TreeNode(3)), TreeNode(-3, TreeNode(-2)))
# print(Solution112().hasPathSum(root_112_3, 3))


# ================================================= 112. Path Sum ======================================================


# ================================================= 235. Lowest Common Ancestor of a Binary Search Tree ================

class Solution235:

    def find_father(self, node, target):
        fathers = []
        while node:
            if node.val > target:
                fathers.append(node.val)
                node = node.left
            elif node.val < target:
                fathers.append(node.val)
                node = node.right
            else:
                break

        return fathers

    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode):
        if not all([root, p, q]):
            return None

        def helper(node, target):
            fathers = []
            while node:
                fathers.append(node)
                if node.val > target:
                    node = node.left
                elif node.val < target:
                    node = node.right
                else:
                    break

            return fathers

        p_fathers = helper(root, p.val)
        q_fathers = helper(root, q.val)
        fathers = p_fathers if len(p_fathers) < len(q_fathers) else q_fathers
        for i in range(len(fathers)):
            if p_fathers[i].val == q_fathers[i].val:
                continue
            return p_fathers[i - 1]
        else:
            return fathers[-1]


# root_235 = TreeNode(3, TreeNode(1, right=TreeNode(2)), TreeNode(4))
root_235 = TreeNode(6, TreeNode(2, TreeNode(0), TreeNode(4, TreeNode(3, TreeNode(5)))),
                    TreeNode(8, TreeNode(7), TreeNode(9)))


# print(Solution235().find_father(root_235, 2))


# print(Solution235().lowestCommonAncestor(root_235, TreeNode(7), TreeNode(5)).val)


# ================================================= 235. Lowest Common Ancestor of a Binary Search Tree ================


# ================================================= 257. Binary Tree Paths =============================================

class Solution257:
    def binaryTreePaths(self, root: TreeNode) -> list:
        if not root:
            return []

        def helper(node, temp=[]):
            temp.append(str(node.val))
            if not node.left and not node.right:
                yield '->'.join(temp)

            if node.left:
                yield from helper(node.left, temp)
                temp.pop()
            if node.right:
                yield from helper(node.right, temp)
                temp.pop()

        return list(helper(root))


# root_257 = TreeNode(1, TreeNode(2, right=TreeNode(5)), TreeNode(3))
#
# print(Solution257().binaryTreePaths(root_single))


# ================================================= 257. Binary Tree Paths =============================================


# ================================================= 404. Sum of Left Leaves ============================================

class Solution404:
    def sumOfLeftLeaves(self, root: TreeNode) -> int:
        if not root:
            return 0
        root.flag = False
        l = [root]
        total = 0
        while l:
            node = l.pop(0)
            if not node.left and not node.right and node.flag:
                total += node.val
            if node.left:
                node.left.flag = True
                l.append(node.left)
            if node.right:
                node.right.flag = False
                l.append(node.right)
        return total


# root_404 = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
#
# print(Solution404().sumOfLeftLeaves(root_404))


# ================================================= 404. Sum of Left Leaves ============================================


# ================================================= 429. N-ary Tree Level Order Traversal ==============================

class Solution429:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        if not root:
            return root
        temp = []
        l = [root]

        while l:
            temp.append([node.val for node in l])
            l = [leaf for node in l for leaf in node.children if leaf]
        return temp


# ================================================= 429. N-ary Tree Level Order Traversal ==============================


# ================================================= 501. Find Mode in Binary Search Tree ===============================

class Solution501:
    def findMode(self, root: TreeNode):
        if not root:
            return []

        def dfs(root):
            if root:
                yield from dfs(root.left)
                yield root
                yield from dfs(root.right)

        from collections import defaultdict
        temp_dict = defaultdict(int)
        for node in dfs(root):
            temp_dict[node.val] += 1
        temp_list = sorted(temp_dict, key=lambda x: temp_dict[x], reverse=True)
        first = temp_list[0]
        res_list = [first]
        most = temp_dict[first]
        for item in temp_list[1:]:
            if temp_dict[item] < most:
                break
            else:
                res_list.append(item)
        print(res_list)
        return res_list


# root_501 = TreeNode(1, TreeNode(2), TreeNode(2, TreeNode(2), TreeNode(3, TreeNode(3), TreeNode(3))))
#
# Solution501().findMode(root_501)


# ================================================= 501. Find Mode in Binary Search Tree ===============================


# ================================================= 530|783. Minimum Absolute Difference in BST ========================

class Solution530:
    def getMinimumDifference(self, root: TreeNode) -> int:
        if not root:
            return None

        def helper(root):
            temp.append(root.val)
            if root.left:
                helper(root.left)
            if root.right:
                helper(root.right)

        temp = []
        helper(root)
        temp = sorted(temp)
        minimum = float('inf')
        for i in range(len(temp) - 1):
            minimum = min((temp[i + 1] - temp[i]), minimum)
        return minimum


# root530 = TreeNode(1, right=TreeNode(8, TreeNode(3), TreeNode(11)))
# print(Solution530().getMinimumDifference(root530))


# ================================================= 530|783. Minimum Absolute Difference in BST ========================


# ================================================= 543. Diameter of Binary Tree =======================================

# todo: dong, not understand well
class Solution543:
    def diameterOfBinaryTree(self, root: TreeNode) -> int:
        diameter = 0

        def counter(root):
            nonlocal diameter
            if not root:
                return 0
            print(f'dong current node ---------> {root.val}')
            left = counter(root.left)
            print(f'dong current left : {root.val}: {left}')
            right = counter(root.right)
            print(f'dong current right : {root.val}: {right}')

            diameter = max(diameter, left + right)

            return max(left, right) + 1

        counter(root)
        return diameter


# root_543 = TreeNode(1, TreeNode(2, TreeNode(4), TreeNode(5)), TreeNode(3))
#
# print(Solution543().diameterOfBinaryTree(root_543))


# ================================================= 543. Diameter of Binary Tree =======================================


# ================================================= 559|104. Maximum Depth of N-ary Tree ===============================

class Solution559:
    def maxDepth(self, root: 'Node') -> int:
        if not root:
            return 0

        def helper(root, temp_res=0):
            if root:
                temp_res += 1
            if not root.right and not root.left:
                yield temp_res
                temp_res = 0
            # if root.children:
            #     for c in root.children:
            #         yield from helper(c, temp_res)
            if root.left:
                yield from helper(root.left, temp_res)
            if root.right:
                yield from helper(root.right, temp_res)

        return max(helper(root))


# print(Solution559().maxDepth(root_common))


# ================================================= 559. Maximum Depth of N-ary Tree ===================================


# ================================================= 563. Binary Tree Tilt ==============================================

class Solution563:
    cache_dict = {}

    def cal(self, node):
        if not node:
            return 0
        if node.val in self.cache_dict:
            return self.cache_dict[node.val]
        temp = []

        def total(node):
            temp.append(node.val)
            if node.left:
                total(node.left)
            if node.right:
                total(node.right)

        total(node)
        ss = sum(temp)
        self.cache_dict[node.val] = ss
        return ss

    def findTilt(self, root: TreeNode) -> int:
        if not root:
            return 0

        total_sum = []
        l = [root]
        while l:
            rr = l.pop(0)
            if not rr.right and not rr.left:
                continue
            total_sum.append(abs(self.cal(rr.right) - self.cal(rr.left)))
            if rr.left:
                l.append(rr.left)
            if rr.right:
                l.append(rr.right)
        return sum(total_sum)


# root_563_1 = TreeNode(1, TreeNode(2), TreeNode(3))
# root_563_2 = TreeNode(4, TreeNode(2, TreeNode(3), TreeNode(5)), TreeNode(9, right=TreeNode(7)))
#
# print(Solution563().findTilt(root_563_2))


# ================================================= 563. Binary Tree Tilt ==============================================


# ================================================= 572. Subtree of Another Tree =======================================

class Solution572:
    def helper(self, root):
        mid_s = []

        def dfs(root):
            if root:
                dfs(root.left)
                mid_s.append(root)
                dfs(root.right)

        dfs(root)
        return mid_s

    def isSubtree(self, s: TreeNode, t: TreeNode) -> bool:
        s_l = self.helper(s)
        t_l = ''.join([str(node.val) for node in self.helper(t)])
        mapping = {str(node.val): node for node in s_l}
        s_l_str = ''.join([str(key) for key in mapping.keys()])
        if t_l in s_l_str:
            if not mapping.get(t_l[0]).left and not mapping.get(t_l[-1]).right:
                return True
        return False


# root_572 = TreeNode(3, TreeNode(4, TreeNode(1), TreeNode(2, TreeNode(0))), TreeNode(5))
# root_572_1 = TreeNode(4, TreeNode(1), TreeNode(2))

# print(Solution572().isSubtree(root_572, root_572_1))


# ================================================= 572. Subtree of Another Tree =======================================


# ================================================= 589|590. N-ary Tree Preorder Traversal =============================


class Solution589:

    def __init__(self):
        self.res = []

    # def preorderBad(self, root: Node) -> list:
    #     if not root:
    #         return
    #
    #     if root.children:
    #         for children in root.children:
    #             self.preorder(children)
    #     self.res.append(root.val)
    #     return self.res

    def preorder(self, root: Node) -> list:
        if not root:
            return []

        def helper(root):
            if root.children:
                for c in root.children:
                    yield from helper(c)
            if root:
                yield root.val

        res = list(helper(root))
        # print(f'dong  ------------->{res}')
        return res


# Solution589().preorder(node_1)
# print(Solution589().preorderBad(node_1))

# ================================================= 589|590. N-ary Tree Preorder Traversal =============================

# ================================================= 606. Construct String from Binary Tree =============================

class Solution606:
    def tree2str(self, t: TreeNode) -> str:
        if not t:
            return ''

        def preorder(node, ans):
            if node:
                ans = ans + str(node.val)
                if node.left:
                    ans = preorder(node.left, ans + "(") + ")"
                if node.right:
                    if not node.left:
                        ans = ans + "()"
                    ans = preorder(node.right, ans + "(") + ")"

            return ans

        return preorder(t, "")


root606 = TreeNode(1, TreeNode(2, TreeNode(4, right=TreeNode(7))), TreeNode(3, right=TreeNode(6, TreeNode(5))))


# print(Solution606().tree2str(root606))


# ================================================= 606. Construct String from Binary Tree =============================


# ================================================= 637. Average of Levels in Binary Tree ==============================
class Solution637:
    def averageOfLevels(self, root: TreeNode) -> list:
        level = (root,)
        while level:
            yield round(sum(node.val for node in level) / len(level), 5)
            level = tuple(leaf for node in level for leaf in (node.left, node.right) if leaf)


# print(list(Solution637().averageOfLevels(root_common)))


# ================================================= 637. Average of Levels in Binary Tree ==============================


# ================================================= 653. Two Sum IV - Input is a BST ===================================

class Solution653:
    def findTarget(self, root: TreeNode, k: int) -> bool:
        if not root:
            return False

        def mid(root):
            if root.left:
                mid(root.left)
            sorted_list.append(root.val)
            if root.right:
                mid(root.right)

        sorted_list = []
        mid(root)
        s, e = 0, len(sorted_list) - 1
        while s != e:
            cur = sorted_list[s] + sorted_list[e]
            if cur == k:
                return True
            elif cur > k:
                e -= 1
            else:
                s += 1
        return False


# print(Solution653().findTarget(root_common_1, 33))


# ================================================= 653. Two Sum IV - Input is a BST ===================================


# ================================================= 654. Maximum Binary Tree ===========================================

class Solution654:
    def constructMaximumBinaryTree(self, nums: list):
        if not nums:
            return None

        root = None

        def form_2_tree(nums):
            nonlocal root
            cur_max = max(nums)
            cur_index = nums.index(cur_max)
            cur_node = TreeNode(cur_max)
            if not root:
                root = cur_node
            if nums[:cur_index]:
                cur_node.left = form_2_tree(nums[:cur_index])
            if nums[cur_index + 1:]:
                cur_node.right = form_2_tree(nums[cur_index + 1:])
            return cur_node

        form_2_tree(nums)

        return root


# root_654 = [3, 2, 1, 6, 0, 5]
#
# print(bfs(Solution654().constructMaximumBinaryTree(root_654)))


# ================================================= 654. Maximum Binary Tree ===========================================


# ================================================= 671. Second Minimum Node In a Binary Tree ==========================

class Solution671:
    def findSecondMinimumValue(self, root: TreeNode) -> int:
        if not root:
            return -1

        def dfs(node):
            if node:
                yield node.val
                yield from dfs(node.left)
                yield from dfs(node.right)

        values = sorted(set(dfs(root)))
        return values[1] if len(values) > 1 else -1


# root_671 = TreeNode(2, TreeNode(2), TreeNode(5, TreeNode(5), TreeNode(7)))
# root_671_2 = TreeNode(2, TreeNode(2), TreeNode(2))
#
# print(Solution671().findSecondMinimumValue(root_671_2))


# ================================================= 671. Second Minimum Node In a Binary Tree ==========================


# ================================================= 700. Search in a Binary Search Tree ================================
# 76 ms, faster than 52.91% ; Memory Usage: 15.3 MB, less than 100.00%

class Solution700:
    def searchBST(self, root: TreeNode, val: int) -> TreeNode:
        if not root:
            return None
        if root.val == val:
            return root
        elif root.val > val:
            root.right = None
            return self.searchBST(root.left, val)
        else:
            root.left = None
            return self.searchBST(root.right, val)


# result700 = Solution700().searchBST(root_common, 7)
# print(result700.val)


# ================================================= 700. Search in a Binary Search Tree ================================


# ================================================= 701. Insert into a Binary Search Tree ==============================

class Solution701:
    def insertIntoBST(self, root: TreeNode, val: int) -> TreeNode:
        insert_node = TreeNode(val)
        if not root:
            return insert_node

        def helper(node):
            if node.val < val:
                if not node.right:
                    node.right = insert_node
                    raise Exception('fuck it')
                helper(node.right)
            else:
                if not node.left:
                    node.left = insert_node
                    raise Exception('fuck it')
                helper(node.left)

        try:
            helper(root)
        except:
            pass
        return root


# root_701 = TreeNode(4, TreeNode(2, TreeNode(1), TreeNode(3)), TreeNode(7))
#
# root = Solution701().insertIntoBST(root_701, 5)
# bfs(root)


# ================================================= 701. Insert into a Binary Search Tree ==============================


# ================================================= 814. Binary Tree Pruning ===========================================

class Solution814:
    def pruneTree(self, root: TreeNode) -> TreeNode:
        if not root:
            return root
        root.left = self.pruneTree(root.left)
        root.right = self.pruneTree(root.right)
        if not root.left and not root.left and not root.val:
            root = None

        return root


# root_814 = TreeNode(0, TreeNode(0, TreeNode(0), TreeNode(0)))
# bfs(Solution814().pruneTree(root_814))


# ================================================= 814. Binary Tree Pruning ===========================================


# ================================================= 872. Leaf-Similar Trees ============================================

class Solution872:
    def leafSimilar(self, root1: TreeNode, root2: TreeNode) -> bool:
        if not root1 and not root2:
            return True
        if (not root1 and root2) or (not root2 and root1):
            return False

        def helper(root):
            if not root.left and not root.right:
                yield root.val
            if root.left:
                yield from helper(root.left)
            if root.right:
                yield from helper(root.right)

        r1, r2 = helper(root1), helper(root2)
        # return list(r1) == list(r2)
        e_flag_1 = e_flag_2 = False
        while 1:
            try:
                val_1 = next(r1)
            except StopIteration as _:
                e_flag_1 = True
            try:
                val_2 = next(r2)
            except StopIteration as _:
                if e_flag_1:
                    return True
                else:
                    return False
            else:
                if val_1 == val_2:
                    continue
                else:
                    return False


# print(Solution872().leafSimilar(root_common_1, root_common_2))


# ================================================= 872. Leaf-Similar Trees ============================================


# ================================================= 889. Construct Binary Tree from Preorder and Postorder Traversal ===

class Solution889:
    def constructFromPrePost(self, pre: list, post: list) -> TreeNode:
        pass


# ================================================= 889. Construct Binary Tree from Preorder and Postorder Traversal ===


# ================================================= 894. All Possible Full Binary Trees ================================

class Solution894:
    memo = {0: [], 1: [TreeNode(0)]}

    def allPossibleFBT(self, n: int):
        if n not in Solution894.memo:
            ans = []
            for x in range(1, n, 2):
                y = n - 1 - x
                for left in self.allPossibleFBT(x):
                    for right in self.allPossibleFBT(y):
                        bns = TreeNode(0)
                        bns.left = left
                        bns.right = right
                        ans.append(bns)
            print(f'dong------------->{n}', ans)
            Solution894.memo[n] = ans

        return Solution894.memo[n]


# print(Solution894().allPossibleFBT(7))


# ================================================= 894. All Possible Full Binary Trees ================================


# ================================================= 897. Increasing Order Search Tree ==================================
class Solution897:
    @staticmethod
    def increasingBSTBad(root: TreeNode) -> TreeNode:
        def helper(root_):
            if not root_:
                return root_
            if root_.left:
                yield from helper(root_.left)
            yield TreeNode(root_.val)
            if root_.right:
                yield from helper(root_.right)

        items = list(helper(root))
        for index, _ in enumerate(items):
            try:
                items[index].right = items[index + 1]
            except IndexError as _:
                break
        return items[0]

    def increasingBST(self, root: TreeNode) -> TreeNode:
        def inorder(node):
            if node:
                inorder(node.left)
                node.left = None
                self.cur.right = node
                self.cur = node
                inorder(node.right)

        ans = self.cur = TreeNode(-1)
        inorder(root)
        return ans.right


# node897 = Solution897().increasingBST(root)
# for item in dfs(node897):
#     print(f'dong -------------->', item)


# ================================================= 897. Increasing Order Search Tree ==================================


# ================================================= 617. Merge Two Binary Trees ========================================
class Solution617:
    def mergeTrees(self, root1: TreeNode, root2: TreeNode) -> TreeNode:
        if root1 is None and root2 is None:
            return None
        if root1 is None:
            res = root2
        elif root2 is None:
            res = root1
        else:
            res = TreeNode(root1.val + root2.val)
            res.left = self.mergeTrees(root1.left, root2.left)
            res.right = self.mergeTrees(root1.right, root2.right)

        return res


# ================================================= 617. Merge Two Binary Trees ========================================


# ================================================= 938. Range Sum of BST ==============================================
class Solution938:
    @staticmethod
    def range_sum_bst(root: TreeNode, low: int, high: int) -> int:
        sum_num = 0
        bs_list = [root]
        while bs_list:
            node = bs_list.pop(0)
            node.append_flag = True
            if low <= node.val <= high:
                sum_num += node.val
            if node.left:
                bs_list.append(node.left)
                if node.left.val <= low:
                    node.left.left = None
            if node.right:
                bs_list.append(node.right)
                if node.right.val >= high:
                    node.right.right = None
        return sum_num


# root = TreeNode(10, TreeNode(5, TreeNode(3), TreeNode(7)), TreeNode(15, right=TreeNode(18)))
# print(Solution938.range_sum_bst(root, low=7, high=15))
# ================================================= 938. Range Sum of BST ==============================================


# ================================================= 951. Flip Equivalent Binary Trees ==================================

# todo: dong---should exist a much better solution.


class Solution951:
    def flipEquiv(self, root1: TreeNode, root2: TreeNode) -> bool:
        if not root1 and not root2:
            return True
        if not all([root1, root2]):
            return False

        l = [(root1, root2)]

        while l:
            node1, node2 = l.pop(0)
            if node1.val != node2.val:
                return False
            else:
                node1_sons = [leaf for leaf in (node1.left, node1.right) if leaf]
                node2_sons = [leaf for leaf in (node2.left, node2.right) if leaf]
                value_1 = [leaf.val for leaf in node1_sons]
                value_2 = [leaf.val for leaf in node2_sons]

                if value_1 == value_2:
                    l.extend(list(zip(node1_sons, node2_sons)))
                elif value_1 == value_2[::-1]:
                    l.extend(list(zip(node1_sons, node2_sons[::-1])))
                else:
                    return False
        return True


# root1 = [1, 2, 3, 4, 5, 6, None, None, None, 7, 8]
# root2 = [1, 3, 2, None, 6, 4, 5, None, None, None, None, 8, 7]
root1 = [0, None, 1]
root2 = [0, 1, None]
root_951_1 = GenTree(root1).tree
root_951_2 = GenTree(root2).tree
print(Solution951().flipEquiv(root_951_1, root_951_2))


# ================================================= 951. Flip Equivalent Binary Trees ==================================


# ================================================= 965. Univalued Binary Tree =========================================

class Solution965:
    def isUnivalTree(self, root: TreeNode) -> bool:
        if not root:
            return False
        val = root.val

        root_list = [root]
        while root_list:
            node = root_list.pop(0)
            if val != node.val:
                return False
            if node.left:
                root_list.append(node.left)
            if node.right:
                root_list.append(node.right)

        return True


# root_965 = TreeNode(1, TreeNode(1, TreeNode(1)), TreeNode(1, TreeNode(1), TreeNode(1)))


# print(Solution965().isUnivalTree(root_965))


# ================================================= 965. Univalued Binary Tree =========================================


# ================================================= 979. Distribute Coins in Binary Tree ===============================

class Solution979:
    def distributeCoins(self, root: TreeNode) -> int:
        self.ans = 0

        def dfs(node):
            if not node:
                return 0
            L, R = dfs(node.left), dfs(node.right)
            print(f'dong current node: {node.val}--------------->{L}: {R}')
            self.ans += abs(L) + abs(R)
            return node.val + L + R - 1

        dfs(root)
        return self.ans


# root_979 = TreeNode(1, TreeNode(0, TreeNode(3)), TreeNode(0))
# print(Solution979().distributeCoins(root_979))


# ================================================= 979. Distribute Coins in Binary Tree ===============================


# ================================================= 993. Cousins in Binary Tree ========================================
class Solution993:
    def isCousins(self, root: TreeNode, x: int, y: int) -> bool:
        if not root:
            return False
        root.parent = 0
        l = [root]
        while l:
            temp = {node.val: node.parent for node in l}
            if x in temp and y in temp and temp[x] != temp[y]:
                return True
            temp = []
            for node in l:
                for leaf in (node.left, node.right):
                    if leaf:
                        leaf.parent = node
                        temp.append(leaf)
            l = temp
        return False


# root_993 = TreeNode(1, TreeNode(2, right=TreeNode(4)), TreeNode(3, right=TreeNode(5)))
#
# print(Solution993().isCousins(root_993, 2, 3))


# ================================================= 993. Cousins in Binary Tree ========================================


# ================================================= 1008. Construct Binary Search Tree from Preorder Traversal =========

class Solution1008:
    def bstFromPreorder(self, preorder: list):
        start = root = TreeNode(preorder.pop(0))

        while preorder:
            cur_num = preorder.pop(0)
            while root:
                if cur_num > root.val:
                    if not root.right:
                        root.right = TreeNode(cur_num)
                        break
                    root = root.right
                if cur_num < root.val:
                    if not root.left:
                        root.left = TreeNode(cur_num)
                        break
                    root = root.left
            root = start

        return start


# preorder = [8, 5, 1, 7, 10, 12]
# node = Solution1008().bstFromPreorder(preorder)
# print(list(dfs(node)))


# ================================================= 1008. Construct Binary Search Tree from Preorder Traversal =========


# ================================================= 1022. Sum of Root To Leaf Binary Numbers ===========================

class Solution1022:
    def sumRootToLeaf(self, root: TreeNode) -> int:
        if not root:
            return 0

        def helper(root, temp_str=''):
            if root:
                temp_str += str(root.val)
                if not root.left and not root.right:
                    yield int(temp_str, 2)
                yield from helper(root.left, temp_str)
                yield from helper(root.right, temp_str)

        return sum(helper(root))


# node_1022 = TreeNode(1, TreeNode(0, TreeNode(0), TreeNode(1)), TreeNode(1, TreeNode(0), TreeNode(1)))


# print(Solution1022().sumRootToLeaf(node_1022))
# ================================================= 1022. Sum of Root To Leaf Binary Numbers ===========================


# ================================================= 1026. Maximum Difference Between Node and Ancestor =================

class Solution1026:
    def maxAncestorDiff(self, root: TreeNode) -> int:
        if not root:
            return 0

        value = float('-inf')

        # def dfs_helper(node, parent):
        #     nonlocal value
        #     if node:
        #         value = max(abs(node.val - parent.val), value)
        #         if node.left:
        #             value = max(abs(parent.val - node.left.val), value)
        #             dfs_helper(node.left, node)
        #         if node.right:
        #             value = max(abs(parent.val - node.right.val), value)
        #             dfs_helper(node.right, node)
        #
        # dfs_helper(root, root)
        minimum, maximum = float('-inf'), float('inf')
        temp = []

        def dfs_helper(node):

            if node:
                temp.append(node.val)
                if not node.left and not node.right:
                    yield max(temp) - min(temp)
                yield from dfs_helper(node.left)
                yield from dfs_helper(node.right)
                temp.pop()

        return max(dfs_helper(root))


# root_1026 = TreeNode(1, right=TreeNode(2, right=TreeNode(0, TreeNode(3))))
# root_1026_2 = TreeNode(8, TreeNode(3, TreeNode(1), TreeNode(6, TreeNode(4), TreeNode(7))),
#                        TreeNode(10, right=TreeNode(14, TreeNode(13))))
#
# # [2,5,0,null,null,4,null,null,6,1,null,3]
# root_1026_3 = TreeNode(2, TreeNode(5), TreeNode(0, TreeNode(4, right=TreeNode(6, TreeNode(1, right=TreeNode(3))))))
#
# # [8,null,1,5,6,2,4,0,null,7,3]
# root_1026_4 = TreeNode(8, right=TreeNode(1, TreeNode(5, TreeNode(2, TreeNode(7), TreeNode(3)), TreeNode(4)),
#                                          TreeNode(6, TreeNode(0))))
# print(Solution1026().maxAncestorDiff(root_1026_3))


# ================================================= 1026. Maximum Difference Between Node and Ancestor =================


# ================================================= 1038. Binary Search Tree to Greater Sum Tree =======================

class Solution1038:
    def bstToGst(self, root: TreeNode) -> TreeNode:
        if not root:
            return None

        temp = []
        cur_sum = 0

        def dfs(node):
            nonlocal cur_sum
            if node:
                dfs(node.right)
                cur_sum += node.val
                node.val = cur_sum
                # temp.append(node.val)
                dfs(node.left)

        dfs(root)
        # node_l = [root]
        # place_holder = TreeNode(-1)
        # while node_l:
        #     ...

        # print(temp)


# root_1038 = TreeNode(4, TreeNode(1, TreeNode(0), TreeNode(2, right=TreeNode(3))),
#                      TreeNode(6, TreeNode(5), TreeNode(7, right=TreeNode(8))))
#
# Solution1038().bstToGst(root_1038)


# ================================================= 1038. Binary Search Tree to Greater Sum Tree =======================


# ================================================= 1104. Path In Zigzag Labelled Binary Tree ==========================

class Solution1104:
    def pathInZigZagTree(self, label: int) -> list:
        import math
        level, res = math.floor(math.log(label, 2)), [label]
        while level:
            value = (2 ** (level - 1)) + ((2 ** level) - res[0] // 2 - 1)
            print(f'dong ----------------> {level}==={value}')
            res.insert(0, value)
            level -= 1
        return res

        # gen_list = []
        # c = 1
        # while 1:
        #     temp = list(range(pow(2, c - 1), pow(2, c)))
        #     if not c % 2:
        #         temp.reverse()
        #     gen_list.append(temp)
        #     if label not in temp:
        #         c += 1
        #     else:
        #         break
        # path_list = []
        # pre_index = gen_list[-1].index(label)
        # for item in gen_list[::-1]:
        #     label = item[pre_index]
        #     path_list.append(label)
        #     pre_index = item.index(label) // 2
        # path_list.reverse()
        # return path_list


# print(Solution1104().pathInZigZagTree(14))


# ================================================= 1104. Path In Zigzag Labelled Binary Tree ==========================


# ================================================= 1110. Delete Nodes And Return Forest ===============================

class Solution1110:
    def delNodes(self, root: TreeNode, to_delete: list) -> list:
        if not TreeNode or not to_delete:
            return [root]
        ans = []
        if root.val not in to_delete:
            ans.append(root)

        def dfs_helper(node):
            if not node:
                return None

            node.left = dfs_helper(node.left)
            node.right = dfs_helper(node.right)
            if node.val in to_delete:
                if node.left:
                    ans.append(node.left)
                if node.right:
                    ans.append(node.right)

                return None
            return node

        dfs_helper(root)
        return ans

    # def delNodesOther(self, root: TreeNode, to_delete: list) -> list:
    #     res = []
    #     root_ = TreeNode(min(to_delete) - 1)
    #     root_.left = root
    #
    #     def recur(root, is_branch):
    #         if not root:
    #             return
    #
    #         if root.left:
    #             if root.left.val in to_delete:
    #                 tmp = root.left
    #                 root.left = None
    #                 recur(tmp, False)
    #             else:
    #                 if not is_branch:
    #                     res.append(root.left)
    #                 recur(root.left, True)
    #
    #         if root.right:
    #             if root.right.val in to_delete:
    #                 tmp = root.right
    #                 root.right = None
    #                 recur(tmp, False)
    #             else:
    #                 if not is_branch:
    #                     res.append(root.right)
    #                 recur(root.right, True)
    #
    #     recur(root_, False)
    #     return res


# root_1110 = GenTree([1, 3, 2, None, 5, 4, None]).tree
# print([node.val for node in Solution1110().delNodes(root_1110, [2])])


# ================================================= 1110. Delete Nodes And Return Forest ===============================


# ================================================= 1123 | 865. Lowest Common Ancestor of Deepest Leaves ===============

class Solution1123:
    def lcaDeepestLeaves(self, root: TreeNode) -> TreeNode:
        if not root:
            return root

        root.parent = root
        l_nodes = [root]
        while l_nodes:
            temp = []
            for node in l_nodes:
                for sub_node in (node.left, node.right):
                    if sub_node:
                        sub_node.parent = node
                        temp.append(sub_node)
            if not temp:
                break
            l_nodes = temp
        if len(l_nodes) == 1:
            return l_nodes[0]
        else:
            while len(l_nodes) > 1:
                if len(set([node.parent for node in l_nodes])) == 1:
                    return l_nodes[0].parent
                l_nodes = [node.parent for node in l_nodes]
            return root


# root_1123 = GenTree([1, 2, None, 3, 4, None, 6, None, 5]).tree
# print(Solution1123().lcaDeepestLeaves(root_1123).val)

# ================================================= 1123 | 865. Lowest Common Ancestor of Deepest Leaves ===============


# ================================================= 1161. Maximum Level Sum of a Binary Tree ===========================

class Solution1161:
    def maxLevelSum(self, root: TreeNode) -> int:
        if not root:
            return 0

        l_nodes = [root]
        temp = []

        while l_nodes:
            temp.append(sum([node.val for node in l_nodes]))

            l_nodes = [leaf for node in l_nodes for leaf in (node.left, node.right) if leaf]
        return temp.index(max(temp)) + 1


# root_1161 = TreeNode(1, TreeNode(7, TreeNode(7), TreeNode(-8)), TreeNode(0))
# print(Solution1161().maxLevelSum(root_1161))


# ================================================= 1161. Maximum Level Sum of a Binary Tree ===========================


# ================================================= 1261. Find Elements in a Contaminated Binary Tree ==================

class Solution1261:

    def __init__(self, root: TreeNode):
        self.mapping = {}
        root.val = 0

        def correct(node):
            if node:
                self.mapping[node.val] = 1
                if node.left:
                    node.left.val = 2 * node.val + 1
                    correct(node.left)
                if node.right:
                    node.right.val = 2 * node.val + 2
                    correct(node.right)

        correct(root)

    def find(self, target: int) -> bool:
        return True if self.mapping.get(target) else False


# root_1261 = TreeNode(-1, right=TreeNode(-1))
#
# obj = Solution1261(root_1261)
# print(obj.mapping)


# ================================================= 1261. Find Elements in a Contaminated Binary Tree ==================


# ================================================= 1130. Minimum Cost Tree From Leaf Values ===========================

class Solution1130:
    def mctFromLeafValues(self, arr: List[int]) -> int:
        sorted_arr = sorted(arr)
        counter = 0
        for index in range(len(sorted_arr) - 1):
            temp = sorted_arr[index] * sorted_arr[index + 1]
            counter += temp
        return counter


# print(Solution1130().mctFromLeafValues([6, 2, 4]))


# ================================================= 1130. Minimum Cost Tree From Leaf Values ===========================


# ================================================= 1305. All Elements in Two Binary Search Trees ======================

class Solution1305:
    def getAllElements(self, root1: TreeNode, root2: TreeNode):

        def dfs(node):
            if node:
                yield from dfs(node.left)
                yield node.val
                yield from dfs(node.right)

        # gen_1 = dfs(root1)
        # gen_2 = dfs(root2)
        #
        # flag_1 = flag_2 = False
        # res_list = []
        # while 1:
        #     print(res_list)
        #     val_1 = val_2 = None
        #     try:
        #         val_1 = next(gen_1)
        #     except StopIteration:
        #         flag_1 = True
        #     try:
        #         val_2 = next(gen_2)
        #     except StopIteration:
        #         flag_2 = True
        #     print(f'dong ------------> {val_1}: {val_2}')
        #     if not flag_1 and not flag_2:
        #         if val_1 != val_2:
        #             res_list.append(min(val_1, val_2))
        #         else:
        #             res_list.extend([val_1] * 2)
        #     else:
        #         res_list.extend([item for item in (val_1, val_2) if item is not None])
        #         break
        # if not flag_1:
        #     res_list.extend(list(gen_1))
        # if not flag_2:
        #     res_list.extend(list(gen_2))
        # return res_list

        l_one = list(dfs(root1))
        l_two = list(dfs(root2))

        res_list = []
        len_one, len_two = len(l_one), len(l_two)
        i = j = 0
        while i < len_one and j < len_two:
            if l_one[i] == l_two[j]:
                res_list.extend([l_one[i]] * 2)
                i += 1
                j += 1
            elif l_one[i] < l_two[j]:
                res_list.append(l_one[i])
                i += 1
            else:
                res_list.append(l_two[j])
                j += 1
        res_list.extend(l_one[i:])
        res_list.extend(l_two[j:])
        return res_list


# root_1305_1 = TreeNode(2, TreeNode(1), TreeNode(4))
# root_1305_2 = TreeNode(1, TreeNode(0), TreeNode(3))
#
# print(Solution1305().getAllElements(root_1305_1, root_1305_2))


# ================================================= 1305. All Elements in Two Binary Search Trees ======================


# ================================================= 1315. Sum of Nodes with Even-Valued Grandparent ====================

class Solution1315:
    def sumEvenGrandparent(self, root: TreeNode) -> int:
        if not root:
            return 0

        valid_values = []
        # total = 0
        node_l = [root]
        while node_l:
            # for node in node_l:
            #     if not node.val % 2:
            valid_values.extend(
                [leaf.val for node in node_l if not node.val % 2 for sub_node in (node.left, node.right) if sub_node for
                 leaf in
                 (sub_node.left, sub_node.right) if leaf])
            # for sub_node in (node.left, node.right):
            #     if sub_node:
            #         for leaf in (sub_node.left, sub_node.right):
            #             if leaf:
            #                 total += leaf.val
            node_l = [leaf for node in node_l for leaf in (node.left, node.right) if leaf]
        return sum(valid_values)
        # return total


# root_1315 = TreeNode(6, TreeNode(7, TreeNode(2, TreeNode(9)), TreeNode(7, TreeNode(1), TreeNode(4))),
#                      TreeNode(8, TreeNode(1), TreeNode(3, right=TreeNode(5))))
#
# print(Solution1315().sumEvenGrandparent(root_1315))

# ================================================= 1315. Sum of Nodes with Even-Valued Grandparent ====================


# ================================================= 1325. Delete Leaves With a Given Value =============================

class Solution1325:
    def removeLeafNodes(self, root: TreeNode, target: int) -> TreeNode:
        if not root:
            return root

        root.left = self.removeLeafNodes(root.left, target)
        root.right = self.removeLeafNodes(root.right, target)

        if not root.left and not root.right and root.val == target:
            root = None

        return root

        # def helper(node, parent=None, direct=0):
        #     nonlocal root
        #     if node:
        #         helper(node.left, node)
        #         helper(node.right, node, direct=1)
        #         if node.val == target and (not node.left) and (not node.right):
        #             if not parent:
        #                 root = None
        #             else:
        #                 if direct:
        #                     parent.right = None
        #                 else:
        #                     parent.left = None
        # helper(root)
        #
        # return root


# root_1325 = TreeNode(1, TreeNode(2), TreeNode(2, TreeNode(2, TreeNode(2))))
# rr = Solution1325().removeLeafNodes(root_1325, 2)
# bfs(rr)

# ================================================= 1325. Delete Leaves With a Given Value =============================


# ================================================= 1448. Count Good Nodes in Binary Tree ==============================

class Solution1448:
    def goodNodes(self, root: TreeNode) -> int:
        if not root:
            return 0

        counter = 0
        maximum = root.val
        members = [maximum]

        def dfs_helper(node):
            nonlocal counter, maximum
            if node:
                if node.val >= maximum:
                    counter += 1
                    maximum = node.val
                members.append(node.val)
                dfs_helper(node.left)
                dfs_helper(node.right)
                members.pop()
                maximum = max(members)

        dfs_helper(root)
        return counter


# root_1448 = TreeNode(3, TreeNode(1, TreeNode(3)), TreeNode(4, TreeNode(1), TreeNode(5)))
# root_1448_2 = TreeNode(3, TreeNode(3, TreeNode(4), TreeNode(2)))
# root_1448_3 = TreeNode(0)
# root_1448_4 = TreeNode(2, right=TreeNode(4, TreeNode(10), TreeNode(8, TreeNode(4))))
# root_1448_5 = TreeNode(2, TreeNode(4, TreeNode(4)),
#                        TreeNode(4, TreeNode(1, TreeNode(5, right=TreeNode(5, TreeNode(4), TreeNode(4)))), TreeNode(3)))
#
# print(Solution1448().goodNodes(root_1448_5))

# ================================================= 1448. Count Good Nodes in Binary Tree ==============================


# ================================================= 1457. Pseudo-Palindromic Paths in a Binary Tree ====================

class Solution1457:
    def pseudoPalindromicPaths(self, root: TreeNode) -> int:
        if not root:
            return 0

        temp = []

        def dfs_helper(node):
            temp.append(str(node.val))
            if not node.left and not node.right:
                yield ''.join(temp)
            if node.left:
                yield from dfs_helper(node.left)
                temp.pop()
            if node.right:
                yield from dfs_helper(node.right)
                temp.pop()

        counter = 0
        for item in dfs_helper(root):
            if self.can_be_palindromic(item):
                counter += 1
        return counter

    @staticmethod
    def can_be_palindromic(path):
        mapping = {}
        for item in path:
            if item not in mapping:
                mapping[item] = 1
            else:
                mapping[item] += 1
        if len(mapping) == 1:
            return True
        odd_nums = 0
        for value in mapping.values():
            if value % 2:
                odd_nums += 1
                if odd_nums > 1:
                    return False
        return True

# root_1457 = TreeNode(2, TreeNode(3, TreeNode(3), TreeNode(1)), TreeNode(1, right=TreeNode(1)))
# root_1457_2 = TreeNode(2, TreeNode(1, TreeNode(1), TreeNode(3, right=TreeNode(1))), TreeNode(1))
# print(Solution1457().pseudoPalindromicPaths(root_1457_2))
# ================================================= 1457. Pseudo-Palindromic Paths in a Binary Tree ====================
