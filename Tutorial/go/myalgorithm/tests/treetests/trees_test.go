// @File    : trees_test
// @Project : go
// @Time    : 2021/5/13 16:07
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package treetests

import (
	"fmt"
	"testing"
)
import "jundong.dong/myalgorithm/tree"
import "jundong.dong/myalgorithm/utils/common"

func print(num int, ans interface{}) {
	fmt.Println("*******************************************")
	fmt.Println("dong-------------------------------------->", num, ans)
	fmt.Println("*******************************************")
}

func TestGenerateTreeByArray(t *testing.T) {
	nums := []int{1, 2, 3, 4, 5, 6, 7}
	expectedAns := []int{4, 2, 5, 1, 6, 3, 7}
	treeE := tree.GenerateTreeByArray(nums)
	ans := tree.IterateTreeDFSInorder(treeE)
	if len(expectedAns) != len(ans) {
		t.Fatal("failed! not enough nums!")
	}
	for i := 0; i < len(expectedAns); i++ {
		if expectedAns[i] != ans[i] {
			t.Fatalf("failed: expected_ans[%d]: %d != ans[%d]: %d", i, expectedAns[i], i, ans[i])
		}
	}
}

func TestRangeSumOfBST(t *testing.T) {
	//root := []int{10, 5, 15, 3, 7, -1, 18}
	root := tree.GenerateTreeByArray([]int{10, 5, 15, 3, 7, 13, 18, 1, -1, 6})
	ans := tree.RangeSumBST938(root, 6, 10)
	expectation := 23
	if ans != expectation {
		t.Fatal("test is not passing, fucking ans-------->", ans)
	}
}

func TestMergeTwoBinaryTree(t *testing.T) {
	tree1 := tree.GenerateTreeByArray([]int{1, 3, 2, 5})
	tree2 := tree.GenerateTreeByArray([]int{2, 1, 3, -1, 4, -1, 7})
	ta := tree.MergeTrees617(tree1, tree2)
	ans := tree.IterateTreeDFSInorder(ta)
	expectation := []int{5, 4, 4, 3, 5, 7}
	flag := common.JudgeTheResult(ans, expectation, 1)
	if !flag {
		t.Fatal("test is not passing ------------>", ans)
	}

}

func TestIncreasingOrderSearchTree(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{5, 3, 6, 2, 4, -1, 8, 1, -1, -1, -1, 7, 9})
	fmt.Println(tree.IterateTreeDFSInorder(root))
	root = tree.IncreasingBST897(root)
	ans := tree.IterateTreeDFSInorder(root)
	expectation := []int{1, 2, 3, 4, 5, 6, 7, 8, 9}
	flag := common.JudgeTheResult(expectation, ans, 1)
	fmt.Println("dong ------------------>", flag, ans)
}

func TestIterTreeFromRoot(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1, 1, 0, 0, 1, 1, 1})
	ans := tree.IterTreePathFromRoot(root, 0)
	fmt.Println("dong ------------->fucking paths is ------>", ans)
}

func TestIsUnivalTree(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1, 1, 1, 1, 1, 1, 1})
	ans := tree.IsUnivalTree(root)
	fmt.Println("dong -------------->ans", ans)
}

func TestInvertTree226(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{4, 2, 7, 1, 3, 6, 9})
	root = tree.InvertTree226(root)
	ans := tree.IterateTreeDFSInorder(root)
	fmt.Println("dong -------------->226", ans)
}

func TestAverageOfLevels(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{3, 9, 20, -1, 15, 7})
	ans := tree.AverageOfLevels637(root)
	fmt.Println("dong ------------------>637", ans)
}

func TestMaximumDepthOfBinaryTree104(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{3, 9, 20, -1, -1, 15, 7})
	ans := tree.MaxDepth104(root)
	fmt.Println("dong ------------------>104", ans)
}

func TestLeafSimilarTrees872(t *testing.T) {
	root1 := tree.GenerateTreeByArray([]int{3, 5, 1, 6, 2, 9, 8, -1, -1, 7, 4})
	root2 := tree.GenerateTreeByArray([]int{3, 5, 1, 6, 7, 4, 2, -1, -1, -1, -1, -1, -1, 9, 8})
	ans := tree.LeafSimilar872(root1, root2)
	fmt.Println("dong ------------------>872", ans)
}

func TestPostOrderTraversal145(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1, -1, 2})
	ans := tree.PostorderTraversal145(root)
	fmt.Println("dong ------------------->145", ans)
}

func TestFindTarget653(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{2, 1, 3})
	ans := tree.FindTarget653(root, 4)
	fmt.Println("dong ------------------>test 653", ans)
}

func TestTree2str606(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1, 2, 3, -1, 4})
	ans := tree.Tree2str606(root)
	fmt.Println("dong --------------->test 606", ans)
}

func TestGetMinimumDifference530(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{5, 1, 48, -1, -1, 12, 53})
	ans := tree.GetMinimumDifference530(root)
	fmt.Println("dong ---------------->test 530", ans)
}

func TestBinaryTreePath257(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1, 2, 3, -1, 5})
	ans := tree.BinaryTreePaths257(root)
	fmt.Println("dong ---------------->test 257", ans)
}

func TestIsSameTree100(t *testing.T) {
	p := tree.GenerateTreeByArray([]int{1, 2, 3})
	q := tree.GenerateTreeByArray([]int{1, 2, 3})
	ans := tree.IsSameTree100(p, q)
	fmt.Println("dong -------------->test 100", ans)
}

func TestFindTilt563(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{21, 7, 14, 1, 1, 2, 2, 3, 3})
	ans := tree.FindTilt563(root)
	fmt.Println("dong ------------------>test 563", ans)
}

func TestLowestCommonAncestor235(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{6, 2, 8, 0, 4, 7, 9, -1, -1, 3, 5})
	p := tree.GenerateTreeByArray([]int{7})
	q := tree.GenerateTreeByArray([]int{5})
	ans := tree.LowestCommonAncestor235(root, p, q)
	fmt.Println("dong ----------------> test 235", ans.Val)
}

func TestSumOfLeftLeaves404(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1})
	ans := tree.SumOfLeftLeaves404(root)
	fmt.Println("dong ----------------> test 404", ans)
}

func TestIsCousin993(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1, 2, 3, -1, 4})
	ans := tree.IsCousins993(root, 3, 2)
	fmt.Println("dong ----------------->test 993", ans)
}

func TestDiameterOfBinaryTree543(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1, 2, 3, 4})
	ans := tree.DiameterOfBinaryTree543(root)
	print(543, ans)
}

func TestIsSymmetric101(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{1,2,2,-1,3,-1,3})
	ans := tree.IsSymmetric101(root)
	print(101, ans)
}

func TestIsBalanced110(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{3,9,20,-1,-1,15,7})
	ans := tree.IsBalanced110(root)
	print(110, ans)
}

func TestIsSubtree572(t *testing.T) {
	root := tree.GenerateTreeByArray([]int{3})
	subRoot := tree.GenerateTreeByArray([]int{3})
	ans := tree.IsSubtree572(root, subRoot)
	print(572, ans)
}