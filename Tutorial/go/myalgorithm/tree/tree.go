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