// @File    : tree
// @Project : go
// @Time    : 2021/5/13 13:44
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package tree

import (
	"bytes"
	"math"
	"strconv"
	"strings"
)

type TreeNode struct {
	Val   int
	Left  *TreeNode
	Right *TreeNode
}

func GenerateTreeByArray(nums []int) *TreeNode {
	if len(nums) == 0 {
		return nil
	}
	if len(nums) == 1 {
		return &TreeNode{nums[0], nil, nil}
	}
	root := &TreeNode{nums[0], nil, nil}
	nodes := []*TreeNode{root}
	nums = append(nums[1:])
	for len(nums) != 0 {
		for _, node := range nodes {
			nodes = append(nodes[1:])
			if len(nums) != 0 {
				if nums[0] != -1 {
					node.Left = &TreeNode{nums[0], nil, nil}
				}
				nums = append(nums[1:])
				if node.Left != nil {
					nodes = append(nodes, node.Left)
				}
			}
			if len(nums) != 0 {
				if nums[0] != -1 {
					node.Right = &TreeNode{nums[0], nil, nil}
				}
				nums = append(nums[1:])
				if node.Right != nil {
					nodes = append(nodes, node.Right)
				}
			}

		}
	}
	return root
}

func helper(tree *TreeNode, res *[]int) {
	if tree != nil {
		helper(tree.Left, res)
		*res = append(*res, tree.Val)
		helper(tree.Right, res)
	}
}

func IterateTreeDFSInorder(tree *TreeNode) []int {
	var ans []int

	helper(tree, &ans)

	return ans
}

type Node struct {
	Val      int
	Children []*Node
}

func convertBinaryToDecimal(number int) int {
	decimal := 0
	counter := 0.0
	remainder := 0

	for number != 0 {
		remainder = number % 10
		decimal += remainder * int(math.Pow(2.0, counter))
		number = number / 10
		counter++
	}
	return decimal
}

// ---------------------------- 100. Same Tree ---------------------------------

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Same Tree.
// Memory Usage: 2.1 MB, less than 16.71% of Go online submissions for Same Tree.
func IsSameTree100(p *TreeNode, q *TreeNode) bool {
	var a, b bool
	if (p != nil && q == nil) || (p == nil && q != nil) {
		return false
	}
	if p == nil && q == nil {
		return true
	}
	if p.Val == q.Val {
		a = IsSameTree100(p.Left, q.Left)
		b = IsSameTree100(p.Right, q.Right)
	}
	return a && b
}

// ---------------------------- 100. Same Tree ---------------------------------

// ---------------------------- 104. Maximum Depth of Binary Tree -----------
// Runtime: 4 ms, faster than 93.06% of Go online submissions for Maximum Depth of Binary Tree.
//Memory Usage: 4.9 MB, less than 9.48% of Go online submissions for Maximum Depth of Binary Tree.
func helper104(root []*TreeNode, maxD *int) {
	var temp []*TreeNode
	for _, node := range root {
		if node.Left != nil {
			temp = append(temp, node.Left)
		}
		if node.Right != nil {
			temp = append(temp, node.Right)
		}
	}
	if len(temp) != 0 {
		*maxD++
		helper104(temp, maxD)
	}
}

func MaxDepth104(root *TreeNode) int {
	maxDepth := 0
	if root == nil {
		return maxDepth
	}

	helper104([]*TreeNode{root}, &maxDepth)
	return maxDepth + 1

}

// ---------------------------- 104. Maximum Depth of Binary Tree -----------

// ---------------------------- 108. Convert Sorted Array to Binary Search Tree -----------

// Runtime: 72 ms, faster than 67.05% of Go online submissions for Convert Sorted Array to Binary Search Tree.
//Memory Usage: 11.6 MB, less than 48.30% of Go online submissions for Convert Sorted Array to Binary Search Tree.

func helper108(nums []int) *TreeNode {
	if len(nums) <= 0 {
		return nil
	}
	mid := len(nums) / 2
	node := TreeNode{nums[mid], nil, nil}
	node.Left = helper108(nums[:mid])
	node.Right = helper108(nums[mid+1:])
	return &node
}

func SortedArrayToBST108(nums []int) *TreeNode {
	if nums == nil {
		return nil
	}
	root := helper108(nums)
	return root
}

// ---------------------------- 108. Convert Sorted Array to Binary Search Tree -----------

// --------------- 145. Binary Tree Postorder Traversal ------------------------

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Binary
// Tree Postorder Traversal.
//Memory Usage: 2.1 MB, less than 65.85% of Go online submissions for Binary
// Tree Postorder Traversal.
func helper145(root *TreeNode, res *[]int) {
	if root != nil {
		helper145(root.Left, res)
		helper145(root.Right, res)
		*res = append(*res, root.Val)
	}
}

func PostorderTraversal145(root *TreeNode) []int {

	var res []int

	if root == nil {
		return res
	}

	helper145(root, &res)
	return res
}

// --------------- 145. Binary Tree Postorder Traversal ------------------------

// ---------------------------- InorderTraversal94 --------------------------
// Runtime: 0 ms, faster than 100.00% of Go online submissions for Binary Tree Inorder Traversal.
// Memory Usage: 2 MB, less than 24.28% of Go online submissions for Binary Tree Inorder Traversal.

func helper94(node *TreeNode, ans *[]int) {
	if node != nil {
		helper94(node.Left, ans)
		*ans = append(*ans, node.Val)
		helper94(node.Right, ans)
	}
}

func InorderTraversal(root *TreeNode) []int {
	if root == nil {
		return nil
	}

	var ans []int
	helper94(root, &ans)
	return ans
}

// ---------------------------- InorderTraversal94 --------------------------

// ---------------------------- invertTree226 -------------------------------
// Runtime: 0 ms, faster than 100.00% of Go online submissions for Invert Binary Tree.
// Memory Usage: 2.2 MB, less than 6.62% of Go online submissions for Invert Binary Tree.
func InvertTree226(root *TreeNode) *TreeNode {
	if root == nil {
		return nil
	}

	temp := root.Left
	root.Left = root.Right
	root.Right = temp
	InvertTree226(root.Left)
	InvertTree226(root.Right)
	return root
}

// ---------------------------- invertTree226 -------------------------------

// ---------------------------- 257. Binary Tree Paths -------------------------

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Binary Tree Paths.
// Memory Usage: 2.4 MB, less than 56.69% of Go online submissions for Binary Tree Paths.
func helper257(node *TreeNode, ans *[]string, temp *[]string) {
	if node != nil {
		*temp = append(*temp, strconv.Itoa(node.Val))
		if node.Left == nil && node.Right == nil {
			*ans = append(*ans, strings.Join(*temp, "->"))
		}
		helper257(node.Left, ans, temp)
		helper257(node.Right, ans, temp)
		*temp = (*temp)[:len(*temp)-1]
	}
}

func BinaryTreePaths257(root *TreeNode) []string {
	var ans []string
	helper257(root, &ans, &[]string{})
	return ans
}

// ---------------------------- 257. Binary Tree Paths -------------------------

// ---------------------------- 530. Minimum Absolute Difference in BST --------

// Runtime: 8 ms, faster than 93.55% of Go online submissions for Minimum Absolute Difference in BST.
//Memory Usage: 7 MB, less than 12.90% of Go online submissions for Minimum Absolute Difference in BST.
func helper530(node *TreeNode, s *float64, e *float64, pivot *float64) float64 {
	if node != nil {
		helper530(node.Left, s, e, pivot)
		*e = float64(node.Val)
		*pivot = math.Min(math.Abs(*e-*s), *pivot)
		*s = *e
		helper530(node.Right, s, e, pivot)
	}
	return *pivot
}

func GetMinimumDifference530(root *TreeNode) int {
	//var ans []int
	//
	//helper530(root, &ans)
	//
	//pivot := math.Pow10(5) + 1
	//for i, v := range ans {
	//	if i == 0 {
	//		continue
	//	} else {
	//		pivot = math.Min(math.Abs(float64(v - ans[i-1])), pivot)
	//	}
	//}
	//return int(pivot)

	pivot := math.Pow10(5) + 1
	a, b := -pivot, 0.0
	return int(helper530(root, &a, &b, &pivot))
}

// ---------------------------- 530. Minimum Absolute Difference in BST --------

// ---------------------------- maxDepth559 ---------------------------------
// Runtime: 0 ms, faster than 100.00% of Go online submissions for Maximum Depth of N-ary Tree.
// Memory Usage: 3.5 MB, less than 28.95% of Go online submissions for Maximum Depth of N-ary Tree.
func maxDepth(root *Node) int {

	if root == nil {
		return 0
	}

	nodeArray := []*Node{root}
	depth := 0
	for len(nodeArray) != 0 {
		depth++
		var temp []*Node
		for _, node := range nodeArray {
			if len(node.Children) != 0 {
				temp = append(temp, node.Children...)
			}
		}
		nodeArray = temp
	}
	return depth
}

// ---------------------------- maxDepth559 ---------------------------------

// ---------------------------- 563. Binary Tree Tilt -----------------------

// Runtime: 20 ms, faster than 13.51% of Go online submissions for Binary Tree Tilt.
//Memory Usage: 6.5 MB, less than 10.81% of Go online submissions for Binary Tree Tilt.
//func helper563T(node *TreeNode) float64 {
//	if node == nil {
//		return 0.0
//	}
//	return float64(node.Val) + helper563T(node.Left) + helper563T(node.Right)
//}

func helper563(node *TreeNode, tilt *int) int  {
	if node == nil {
		return 0
	}
	left, right := helper563(node.Left, tilt), helper563(node.Right, tilt)
	*tilt += int(math.Abs(float64(left - right)))
	return node.Val + left + right

}

func FindTilt563(root *TreeNode) int {
	var ans int
	helper563(root, &ans)

	return ans
}

// ---------------------------- 563. Binary Tree Tilt -----------------------

// ---------------------------- Preorder589 ---------------------------------
func helper589(node *Node, ans *[]int) {
	if node != nil {
		*ans = append(*ans, node.Val)
		for _, n := range node.Children {
			helper589(n, ans)
		}
	}
}

// Runtime: 0 ms, faster than 100.00% of Go online submissions for N-ary Tree
// Preorder Traversal.
// Memory Usage: 4 MB, less than 31.50% of Go online submissions for N-ary
// Tree Preorder Traversal.
func Preorder589(root *Node) []int {
	if root == nil {
		return nil
	}
	var ans []int
	helper589(root, &ans)

	return ans
}

// ---------------------------- Preorder589 ---------------------------------

// ---------------------------- Postorder590 --------------------------------
func helper590(node *Node, ans *[]int) {
	if node != nil {
		for _, cNode := range node.Children {
			helper590(cNode, ans)
		}
		*ans = append(*ans, node.Val)
	}
}

// Runtime: 0 ms, faster than 100.00% of Go online submissions for N-ary Tree
// Postorder Traversal.
// Memory Usage: 4.3 MB, less than 40.00% of Go online submissions for N-ary
// Tree Postorder Traversal.
func Postorder(root *Node) []int {
	if root == nil {
		return nil
	}

	var ans []int
	helper590(root, &ans)
	return ans
}

// ---------------------------- Postorder590 --------------------------------

// ---------------------------- 606. Construct String from Binary Tree ---------

// Runtime: 8 ms, faster than 92.98% of Go online submissions for Construct String from Binary Tree.
//Memory Usage: 7.6 MB, less than 35.09% of Go online submissions for Construct String from Binary Tree.
func Tree2str606(root *TreeNode) string {
	var ans bytes.Buffer
	if root == nil {
		return ""
	}
	ans.WriteString(strconv.Itoa(root.Val))
	if root.Left != nil || root.Right != nil {
		ans.WriteString("(" + Tree2str606(root.Left) + ")")
	}
	if root.Right != nil {
		ans.WriteString("(" + Tree2str606(root.Right) + ")")
	}
	return ans.String()
}

// ---------------------------- 606. Construct String from Binary Tree ---------

// ---------------------------- MergeTrees617 -------------------------------
// Runtime: 24 ms, faster than 90.05% of Go online submissions for Merge Two
// Binary Trees.
// Memory Usage: 8.4 MB, less than 38.74% of Go online submissions for Merge
// Two Binary Trees.
func MergeTrees617(root1 *TreeNode, root2 *TreeNode) *TreeNode {
	var current *TreeNode
	if root1 != nil && root2 != nil {
		current = &TreeNode{root2.Val + root1.Val, nil, nil}
		current.Left = MergeTrees617(root1.Left, root2.Left)
		current.Right = MergeTrees617(root1.Right, root2.Right)
	}
	if root1 == nil && root2 != nil {
		current = root2
	}
	if root2 == nil && root1 != nil {
		current = root1
	}
	if root1 == nil && root2 == nil {
		return nil
	}
	return current
}

// ---------------------------- MergeTrees617 -------------------------------

// ---------------------------- AverageOfLevels637 --------------------------
// Runtime: 8 ms, faster than 88.00% of Go online submissions for Average of Levels in Binary Tree.
// Memory Usage: 6.2 MB, less than 90.00% of Go online submissions for Average of Levels in Binary Tree.
func AverageOfLevels637(root *TreeNode) []float64 {
	var ans []float64
	nodeList := []*TreeNode{root}
	for len(nodeList) != 0 {
		var temp []*TreeNode
		total := 0.0
		for _, node := range nodeList {
			total += float64(node.Val)
			if node.Left != nil {
				temp = append(temp, node.Left)
			}
			if node.Right != nil {
				temp = append(temp, node.Right)
			}
		}
		ans = append(ans, total/float64(len(nodeList)))
		nodeList = temp
	}
	return ans

}

// ---------------------------- AverageOfLevels637 --------------------------

// ---------------------------- 653. Two Sum IV - Input is a BST ---------------

//Runtime: 28 ms, faster than 46.73% of Go online submissions for Two Sum IV - Input is a BST.
//Memory Usage: 7.8 MB, less than 31.78% of Go online submissions for Two Sum IV - Input is a BST.
func inorder653(node *TreeNode, ans map[int]int) {
	if node != nil {
		inorder653(node.Left, ans)
		ans[node.Val] = node.Val
		inorder653(node.Right, ans)
	}
}

func FindTarget653(root *TreeNode, k int) bool {
	if root == nil {
		return false
	}

	ans := make(map[int]int)
	inorder653(root, ans)
	for _, value := range ans {
		rest := k - value
		_, err := ans[rest]
		if err == true && rest != value {
			return true
		}
	}
	return false
}

// ---------------------------- 653. Two Sum IV - Input is a BST ---------------

// ---------------------------- 872. Leaf-Similar Trees ---------------------
// Runtime: 0 ms, faster than 100.00% of Go online submissions for Leaf-Similar Trees.
//Memory Usage: 2.6 MB, less than 56.06% of Go online submissions for Leaf-Similar Trees.
func helper872(node *TreeNode, a *[]int) {
	if node.Left == nil && node.Right == nil {
		*a = append(*a, node.Val)
	}
	if node.Left != nil {
		helper872(node.Left, a)
	}

	if node.Right != nil {
		helper872(node.Right, a)
	}
}

func LeafSimilar872(root1 *TreeNode, root2 *TreeNode) bool {
	if root1 == nil && root2 == nil {
		return true
	}

	if root1 == nil && root2 != nil {
		return false
	}

	if root1 != nil && root2 == nil {
		return false
	}

	var a1, a2 []int

	helper872(root1, &a1)
	helper872(root2, &a2)

	if len(a1) != len(a2) {
		return false
	}

	for i, item := range a1 {
		if item != a2[i] {
			return false
		}
	}
	return true

}

// ---------------------------- 872. Leaf-Similar Trees ---------------------

// ---------------------------- IncreasingBST897 ----------------------------
func helper897(node *TreeNode, current *TreeNode) *TreeNode {
	if node == nil {
		return current
	}
	current = helper897(node.Left, current)
	node.Left = nil
	current.Right, current = node, node
	current = helper897(node.Right, current)
	return current
}

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Increasing
// Order Search Tree.
// Memory Usage: 2.5 MB, less than 54.55% of Go online submissions for
// Increasing Order Search Tree.
func IncreasingBST897(root *TreeNode) *TreeNode {
	head := &TreeNode{}
	current := head
	helper897(root, current)
	return head.Right
}

// ---------------------------- IncreasingBST897 ----------------------------

// ---------------------------- RangeSumBST938 ------------------------------
func helper938(node *TreeNode, ans *int, low int, high int) {
	if node != nil {
		if low <= node.Val && node.Val <= high {
			*ans += node.Val
		}
		helper938(node.Left, ans, low, high)
		helper938(node.Right, ans, low, high)
	}
}

// Runtime: 84 ms, faster than 91.67% of Go online submissions for Range
// Sum of BST.
//Memory Usage: 9 MB, less than 5.11% of Go online submissions for Range
// Sum of BST.
func RangeSumBST938(root *TreeNode, low int, high int) int {
	//ans := 0
	//nodeList := []*TreeNode{root}
	//
	//for len(nodeList) != 0 {
	//	var temp []*TreeNode
	//	for _, node := range nodeList {
	//		if low <= node.Val && node.Val <= high {
	//			ans += node.Val
	//		}
	//		if node.Left != nil {
	//			temp = append(temp, node.Left)
	//		}
	//		if node.Right != nil {
	//			temp = append(temp, node.Right)
	//		}
	//	}
	//	nodeList = temp
	//}
	//return ans
	ans := 0
	helper938(root, &ans, low, high)
	return ans
}

// ---------------------------- RangeSumBST938 ------------------------------

// ---------------------------- IsUnivalTree965 -----------------------------

func CoolDown() bool {
	ans := recover()
	if ans != nil {
		return false
	}
	return true
}

func helper965(node *TreeNode, flag *int) {
	defer CoolDown()
	if node != nil {
		if node.Val != *flag {
			*flag = -1
		} else {
			helper965(node.Left, flag)
			helper965(node.Right, flag)
		}
	}
}

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Univalued Binary Tree.
// Memory Usage: 2.3 MB, less than 100.00% of Go online submissions for Univalued Binary Tree.
func IsUnivalTree(root *TreeNode) bool {
	ans := root.Val
	helper965(root, &ans)
	if ans == -1 {
		return false
	}
	return true
}

// ---------------------------- IsUnivalTree965 -----------------------------

// ---------------------------- IterTreePathFromRoot1022 --------------------
// Runtime: 0 ms, faster than 100.00% of Go online submissions for Sum of Root To Leaf Binary Numbers.
// Memory Usage: 3.1 MB, less than 71.79% of Go online submissions for Sum of Root To Leaf Binary Numbers.
func IterTreePathFromRoot(root *TreeNode, Val int) int {
	if root != nil {
		Val = Val<<1 | root.Val
		if root.Left == nil && root.Right == nil {
			return Val
		}
		total := 0
		if root.Left != nil {
			total += IterTreePathFromRoot(root.Left, Val)
		}
		if root.Right != nil {
			total += IterTreePathFromRoot(root.Right, Val)
		}
		return total
	}
	return 0
}

// ---------------------------- IterTreePathFromRoot1022 --------------------

// ---------------------------- sumRootToLeaf1022 ---------------------------
func walk(node *TreeNode, sum int) int {
	if node == nil {
		return 0
	}

	sum = (sum << 1) | node.Val
	if node.Left == nil && node.Right == nil {
		return sum
	}

	return walk(node.Left, sum) + walk(node.Right, sum)
}

func sumRootToLeaf(root *TreeNode) int {
	return walk(root, 0)
}

// ---------------------------- sumRootToLeaf1022 ---------------------------
