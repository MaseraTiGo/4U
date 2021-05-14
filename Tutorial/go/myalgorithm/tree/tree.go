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

type Tree struct {
	Val   int
	left  *Tree
	right *Tree
}

func GenerateTreeByArray(nums []int) *Tree {
	if len(nums) == 0 {
		return nil
	}
	if len(nums) == 1 {
		return &Tree{nums[0], nil, nil}
	}
	root := &Tree{nums[0], nil, nil}
	nodes := []*Tree{root}
	nums = append(nums[1:])
	for len(nums) != 0 {
		for _, node := range nodes {
			nodes = append(nodes[1:])
			if len(nums) != 0 {
				node.left = &Tree{nums[0], nil, nil}
				nums = append(nums[1:])
				nodes = append(nodes, node.left)
			}
			if len(nums) != 0 {
				node.right = &Tree{nums[0], nil, nil}
				nums = append(nums[1:])
				nodes = append(nodes, node.right)
			}

		}
	}
	return root
}

func helper(tree *Tree, res *[]int) {
	if tree != nil {
		helper(tree.left, res)
		*res = append(*res, tree.Val)
		helper(tree.right, res)
	}
}

func IterateTreeDFSInorder(tree *Tree) []int {
	var ans []int

	helper(tree, &ans)

	return ans
}
