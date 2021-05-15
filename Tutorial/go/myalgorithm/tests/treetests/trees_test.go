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
