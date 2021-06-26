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
	"fmt"
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

// ---------------------------- 101. Symmetric Tree -------------------------

// Runtime: 4 ms, faster than 17.17% of Go online submissions for Symmetric Tree.
//Memory Usage: 4.2 MB, less than 7.16% of Go online submissions for Symmetric Tree.
//func IsSymmetric101(root *TreeNode) bool {
//	nodel := []*TreeNode{root}
//
//	for len(nodel) != 0{
//		var temp []*TreeNode
//		var valsOne, valsTwo string
//		count := 0
//		for _, node := range nodel {
//			if node == nil {
//				valsOne += "-101,"
//				valsTwo = "-101," + valsTwo
//				temp = append(temp, nil)
//				count ++
//			} else {
//				valsOne += fmt.Sprintf("%d,", node.Val)
//				valsTwo = fmt.Sprintf("%d,", node.Val) + valsTwo
//				temp = append(temp, node.Left)
//				temp = append(temp, node.Right)
//			}
//
//		}
//
//		if strings.TrimRight(valsOne, ",") != strings.TrimRight(valsTwo, ",") {
//			return false
//		}
//
//		if count == len(temp) {
//			break
//		}
//		nodel = temp
//	}
//
//
//	return true
//}

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Symmetric Tree.
//Memory Usage: 2.9 MB, less than 30.23% of Go online submissions for Symmetric Tree.
func IsSymmetric101(root *TreeNode) bool {
	return IsSameTree100(InvertTree226(root.Left), root.Right)
}

// ---------------------------- 101. Symmetric Tree -------------------------

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

// ---------------------------- 110. Balanced Binary Tree -------------------

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Balanced Binary Tree.
//Memory Usage: 5.9 MB, less than 16.67% of Go online submissions for Balanced Binary Tree.
func helper110(node *TreeNode) (int, bool) {
	if node == nil {
		return 0, true
	} else {
		left, bleft := helper110(node.Left)
		right, bright := helper110(node.Right)
		if math.Abs(float64(left-right)) > 1 {
			return -1, false
		}
		return int(math.Max(float64(left), float64(right)) + 1), bleft && bright
	}

}

func IsBalanced110(root *TreeNode) bool {
	if root == nil {
		return true
	}
	_, ans := helper110(root)
	return ans
}

//func helper110T()  {
//	recover()
//}
//
//func helper110(node *TreeNode, ans *bool) int{
//	defer helper110T()
//	if node == nil {
//		return 0
//	} else {
//		left := helper110(node.Left, ans)
//		//if err != nil {
//		//	return -1, errors.New("error")
//		//}
//		right := helper110(node.Right, ans)
//		//if err != nil {
//		//	return -1, errors.New("error")
//		//}
//		if math.Abs(float64(left-right)) > 1 {
//			//return -1, errors.New("error")
//			*ans = false
//			panic("")
//		}
//		return int(math.Max(float64(left), float64(right)) + 1)
//	}
//
//}
//
//func IsBalanced110(root *TreeNode) bool {
//	ans := true
//	if root == nil {
//		return ans
//	}
//	helper110(root, &ans)
//	return ans
//}

// ---------------------------- 110. Balanced Binary Tree -------------------

// ---------------------------- 112. Path Sum -------------------------------

//func helper112(node *TreeNode, target int) bool {
//	if node != nil {
//		target -= node.Val
//		fmt.Println("dong ------------------>", node.Val, target)
//		if node.Left == nil && node.Right == nil {
//			if target == 0 {
//				return true
//			} else {
//				target += node.Val
//			}
//		}
//		a := helper112(node.Left, target)
//		b := helper112(node.Right, target)
//		if a || b {
//			return true
//		}
//	}
//	return false
//}


// Runtime: 4 ms, faster than 94.75% of Go online submissions for Path Sum.
//Memory Usage: 4.7 MB, less than 63.89% of Go online submissions for Path Sum.
func HasPathSum112(root *TreeNode, targetSum int) bool {
	if root == nil {
		return false
	}
	//return helper112(root, targetSum)
	targetSum -= root.Val
	fmt.Println("dong ------------------>", root.Val, targetSum)
	if root.Left == nil && root.Right == nil {
		if targetSum == 0 {
			return true
		} else {
			targetSum += root.Val
		}
	}
	a := HasPathSum112(root.Left, targetSum)
	b := HasPathSum112(root.Right, targetSum)
	if a || b {
		return true
	} else {
		return false
	}

}

// ---------------------------- 112. Path Sum -------------------------------

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

// -------- 235. Lowest Common Ancestor of a Binary Search Tree -------------

// Runtime: 12 ms, faster than 100.00% of Go online submissions for Lowest Common Ancestor of a Binary Search Tree.
//Memory Usage: 7.1 MB, less than 48.82% of Go online submissions for Lowest Common Ancestor of a Binary Search Tree.
func helper235(node, target *TreeNode, nodePath *[]*TreeNode) {
	*nodePath = append(*nodePath, node)
	if node.Val > target.Val {
		helper235(node.Left, target, nodePath)
	} else if node.Val < target.Val {
		helper235(node.Right, target, nodePath)
	}
}

func LowestCommonAncestor235(root, p, q *TreeNode) *TreeNode {
	var pNodePath, qNodePath []*TreeNode
	helper235(root, p, &pNodePath)
	helper235(root, q, &qNodePath)

	ran := len(pNodePath)
	if len(pNodePath) > len(qNodePath) {
		ran = len(qNodePath)
	}
	num := 0
	for ; num < int(ran); num++ {
		if pNodePath[num].Val != qNodePath[num].Val {
			break
		}
	}

	return pNodePath[num-1]
}

// -------- 235. Lowest Common Ancestor of a Binary Search Tree -------------

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

// ---------------------------- 404. Sum of Left Leaves ---------------------

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Sum of Left Leaves.
//Memory Usage: 2.7 MB, less than 86.81% of Go online submissions for Sum of Left Leaves.
func helper404(node *TreeNode, source int, total *int) {
	if node != nil {
		if node.Left == nil && node.Right == nil && source == 1 {
			*total += node.Val
		}
		helper404(node.Left, 1, total)
		helper404(node.Right, 0, total)
	}

}

func SumOfLeftLeaves404(root *TreeNode) int {
	var ans int
	helper404(root, 0, &ans)
	return ans
}

// ---------------------------- 404. Sum of Left Leaves ---------------------

// ---------------------------- 501. Find Mode in Binary Search Tree --------

// Runtime: 12 ms, faster than 57.45% of Go online submissions for Find Mode in Binary Search Tree.
//Memory Usage: 6.5 MB, less than 34.04% of Go online submissions for Find Mode in Binary Search Tree.
//func FindMode501(root *TreeNode) []int {
//	var res []int
//	nodel := []*TreeNode{root}
//	ans := make(map[int]int)
//
//	maxNum := 1
//	for len(nodel) != 0 {
//		var temp []*TreeNode
//		for _, node := range nodel {
//			_, ok := ans[node.Val]
//			if ok {
//				ans[node.Val]++
//			} else {
//				ans[node.Val] = 1
//			}
//			if ans[node.Val] > maxNum {
//				maxNum = ans[node.Val]
//				res = []int{node.Val}
//			} else if ans[node.Val] == maxNum {
//				res = append(res, node.Val)
//			}
//			if node.Left != nil {
//				temp = append(temp, node.Left)
//			}
//			if node.Right != nil {
//				temp = append(temp, node.Right)
//			}
//		}
//		nodel = temp
//
//	}
//	//for k, v := range ans {
//	//	if v == maxNum {
//	//		res = append(res, k)
//	//	}
//	//}
//	return res
//}

func FindMode501(root *TreeNode) []int {
	var mode []int
	var stack []*TreeNode
	for max, cnt, prev := 0, 0, 0; root != nil || len(stack) > 0; root = root.Right {
		for ; root != nil; root = root.Left {
			stack = append(stack, root)
		}
		root = stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if root.Val == prev {
			cnt++
		} else {
			cnt, prev = 1, root.Val
		}
		if cnt > max {
			max = cnt
			mode = []int{prev}
		} else if cnt == max {
			mode = append(mode, prev)
		}
	}
	return mode
}

// ---------------------------- 501. Find Mode in Binary Search Tree --------

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

// ---------------------------- 543. Diameter of Binary Tree ----------------

// Runtime: 4 ms, faster than 94.74% of Go online submissions for Diameter of Binary Tree.
//Memory Usage: 4.5 MB, less than 89.85% of Go online submissions for Diameter of Binary Tree.
func helper543(node *TreeNode, max *float64) float64 {
	if node == nil {
		return 0
	}
	left := helper543(node.Left, max)
	right := helper543(node.Right, max)
	*max = math.Max(*max, left+right+1)
	return math.Max(left, right) + 1
}

func DiameterOfBinaryTree543(root *TreeNode) int {

	var max float64
	helper543(root, &max)
	return int(max) - 1
}

// ---------------------------- 543. Diameter of Binary Tree ----------------

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

func helper563(node *TreeNode, tilt *int) int {
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

// ---------------------------- 572. Subtree of Another Tree-----------------

// Runtime: 16 ms, faster than 78.69% of Go online submissions for Subtree of Another Tree.
//Memory Usage: 6.8 MB, less than 57.38% of Go online submissions for Subtree of Another Tree.
func IsSubtree572(root *TreeNode, subRoot *TreeNode) bool {
	if root == nil {
		return false
	}

	bRoot := IsSameTree100(root, subRoot)
	if bRoot {
		return bRoot
	} else {
		if IsSubtree572(root.Left, subRoot) || IsSubtree572(root.Right, subRoot) {
			return true
		}
	}

	return false
}

// ---------------------------- 572. Subtree of Another Tree-----------------

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

// ---------------------------- 993. Cousins in Binary Tree -----------------

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Cousins in Binary Tree.
//Memory Usage: 2.6 MB, less than 13.64% of Go online submissions for Cousins in Binary Tree.
type ExTreeNode struct {
	Node   *TreeNode
	Father *TreeNode
}

func IsCousins993(root *TreeNode, x int, y int) bool {
	nodeList := []*ExTreeNode{&ExTreeNode{root, nil}}

	var xFlag, yFlag *ExTreeNode

	for len(nodeList) != 0 {
		var temp []*ExTreeNode
		for _, node := range nodeList {
			if node.Node.Left != nil {
				temp = append(temp, &ExTreeNode{node.Node.Left, node.Node})
			}
			if node.Node.Right != nil {
				temp = append(temp, &ExTreeNode{node.Node.Right, node.Node})
			}
			if node.Node.Val == x {
				xFlag = node
			}
			if node.Node.Val == y {
				yFlag = node
			}
		}
		if xFlag != nil && yFlag != nil {
			if xFlag.Father.Val != yFlag.Father.Val {
				return true
			} else {
				return false
			}
		} else if xFlag == nil && yFlag == nil {
			nodeList = temp
		} else {
			return false
		}
	}
	return false
}

// ---------------------------- 993. Cousins in Binary Tree -----------------

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
