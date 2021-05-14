// @File    : tree_test
// @Project : go
// @Time    : 2021/5/13 16:01
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package tests

import "testing"
import "Johnathan.strong/algorithm/algorithmbygo/tree"

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
