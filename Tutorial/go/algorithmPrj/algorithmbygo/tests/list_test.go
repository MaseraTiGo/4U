// @File    : list_test
// @Project : go
// @Time    : 2021/5/13 16:00
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package tests

import "testing"
import "Johnathan.strong/algorithm/algorithmbygo/utils/common"
import "Johnathan.strong/algorithm/algorithmbygo/list"

func TestGenerateListNode(t *testing.T) {
	nums := []int{1, 2, 3, 4, 5, 6, 7}
	lNode := list.GenerateListNode(nums)
	ans := list.IterateListNode(lNode)
	flag := common.CompareSlice(nums, ans)
	if !flag {
		t.Fatal("failed... answer does not match expectation!")
	}

}

