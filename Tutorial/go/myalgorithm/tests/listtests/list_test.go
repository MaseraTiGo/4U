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
package listtests

import (
	"fmt"
	"testing"
)
import "jundong.dong/myalgorithm/utils/common"
import "jundong.dong/myalgorithm/list"

func TestGenerateListNode(t *testing.T) {
	nums := []int{1, 2, 3, 4, 5, 6, 7}
	lNode := list.GenerateListNode(nums)
	ans := list.IterateListNode(lNode)
	flag := common.CompareSlice(nums, ans)
	if !flag {
		t.Fatal("failed... answer does not match expectation!")
	}

}

func TestTwoSum(t *testing.T) {
	nums := []int{1, 2, 3, 4, 9, 10, 8}
	target := 9
	ans := list.TwoSum(nums, target)
	if ans == nil {
		t.Fatal("no matching nums!")
	}
	fmt.Print("dong ----------------->ans:", ans)
}

func TestAddTwoNum(t *testing.T) {
	num1 := list.GenerateListNode([]int{9, 9, 9, 9, 9, 9, 9})
	num2 := list.GenerateListNode([]int{9, 9, 9, 9})
	num := list.AddTwoNums(num1, num2)
	ans := list.IterateListNode(num)
	expedition := []int{8, 9, 9, 9, 0, 0, 0, 1}
	flag := common.CompareSlice(ans, expedition)
	if !flag {
		t.Fatal("test is not passing......")
	}
}

func TestLongestSubstr(t *testing.T) {
	stings := []string{
		"tmmzuxt",
		"pwwkeow",
		" ",
		"bbbbbbbbbbb",
		"abcabcabc",
		"",
	}
	var res []int
	expectation := []int{5, 4, 1, 1, 3, 0}
	for _, s := range stings {
		res = append(res, list.LengthOfLongestSubstr(s))
	}
	flag := common.CompareSlice(res, expectation)
	if !flag {
		t.Fatal("test is not passing......", res)
	}

}

func TestMediaOfTwo(t *testing.T) {
	nums1 := []int{1, 2}
	nums2 := []int{3, 4}
	ans := list.FindMedianSortedArrays(nums1, nums2)
	fmt.Println("dong --------------->", ans == 2.5, ans)
}

func TestReverseSeven(t *testing.T) {
	testNums := []int{123, 321, 1, 10, 100, 333}
	expectation := []int{321, 123, 1, 1, 1, 333}
	var ans []int
	for _, value := range testNums {
		ans = append(ans, list.ReverseSeven(value))
	}
	if !common.CompareSlice(ans, expectation) {
		t.Fatal("test is not passing......", ans)
	}

}

// ---------------------- 14. Longest Common Prefix -------------------------

func TestLongestCommonPrefix14(t *testing.T) {
	strs := []string{"fuck", "iu", "fuck"}
	ans := list.LongestCommonPrefix(strs)
	fmt.Printf("dong----------------->14 ans: %#v\n", ans)

}

// ---------------------- 14. Longest Common Prefix -------------------------
