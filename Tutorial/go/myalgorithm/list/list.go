// @File    : list
// @Project : go
// @Time    : 2021/5/13 15:10
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package list

type ListNode struct {
	Val  int
	Next *ListNode
}

func GenerateListNode(nums []int) *ListNode {
	lNode := &ListNode{-1, nil}
	origin := lNode
	for _, num := range nums {
		lNode.Next = &ListNode{num, nil}
		lNode = lNode.Next
	}

	return origin.Next
}

func IterateListNode(l *ListNode) []int {
	var ans []int
	for l != nil {
		ans = append(ans, l.Val)
		l = l.Next
	}
	return ans
}
