// @File    : arrays
// @Project : myalgorithm
// @Time    : 2021/5/14 10:44
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package list

import (
	"fmt"
	"math"
	"regexp"
	"strconv"
	"strings"
)

func TwoSum(nums []int, target int) []int {
	mapping := make(map[int]int)
	for i, num := range nums {
		minus := target - num
		if j, ok := mapping[minus]; ok {
			return []int{i, j}
		}
		mapping[num] = i
	}
	return nil
}

func AddTwoNums(l1 *ListNode, l2 *ListNode) *ListNode {
	if l1 == nil || l2 == nil {
		return nil
	}
	head := &ListNode{Val: 0, Next: nil}
	current := head
	flag := false
	for l1 != nil || l2 != nil {
		valOne := 0
		valTwo := 0
		if l1 != nil {
			valOne = l1.Val
		}
		if l2 != nil {
			valTwo = l2.Val
		}
		sum := valOne + valTwo
		if flag {
			sum += 1
		}
		if sum >= 10 {
			flag = true
			exValue := sum - 10
			current.Next = &ListNode{Val: exValue, Next: nil}
		} else {
			flag = false
			current.Next = &ListNode{Val: sum, Next: nil}
		}
		if l1 != nil {
			l1 = l1.Next
		}
		if l2 != nil {
			l2 = l2.Next
		}
		current = current.Next
	}

	if flag {
		current.Next = &ListNode{1, nil}
	}

	return head.Next

}

func LengthOfLongestSubstr(s string) int {
	if len(s) <= 1 {
		return len(s)
	}

	sPoint, ePoint := 0, 0
	max := 0
	cacheMapping := make(map[uint8]uint)
	for true {
		if ePoint == len(s) {
			break
		}

		if _, ok := cacheMapping[s[ePoint]]; ok {
			curMax := ePoint - sPoint
			if curMax > max {
				max = curMax
			}
			for true {
				if s[sPoint] == s[ePoint] {
					sPoint += 1
					break
				} else {
					delete(cacheMapping, s[sPoint])
				}
				sPoint += 1
			}

		} else {
			curMax := ePoint - sPoint + 1
			if curMax > max {
				max = curMax
			}

			cacheMapping[s[ePoint]] = 0
		}
		ePoint += 1
	}

	return max
}

func FindMedianSortedArrays(nums1 []int, nums2 []int) float64 {
	if len(nums1) == 0 && len(nums2) == 0 {
		return float64(0)
	}
	var total []int
	i := 0
	j := 0
	for true {
		if i == len(nums1) || j == len(nums2) {
			break
		}
		if nums1[i] < nums2[j] {
			total = append(total, nums1[i])
			i++
		} else if nums1[i] > nums2[j] {
			total = append(total, nums2[j])
			j++
		} else {
			total = append(total, nums1[i], nums2[j])
			i++
			j++
		}
	}
	if i < len(nums1) {
		total = append(total, nums1[i:]...)
	}
	if j < len(nums2) {
		total = append(total, nums2[j:]...)
	}
	lenTotal := len(total)
	if lenTotal%2 == 0 {
		mid := lenTotal / 2
		return float64(total[mid]+total[mid-1]) / 2
	} else {
		return float64(total[int(lenTotal/2)])
	}
}

func ReverseSeven(x int) int {
	ans := 0
	for x != 0 {
		ans = ans*10 + x%10
		x = x / 10
	}

	if ans < -(1<<31) || ans > 1<<31-1 {
		return 0
	}

	return ans
}

// ---------------------- 8. String to Integer (atoi) ----------------------

func MyAtoi8(s string) int {
	min := int(-math.Pow(2.0, 31))
	max := int(math.Pow(2.0, 31) - 1)
	newS := strings.TrimLeft(s, " ")
	reg, err := regexp.Compile(`^[-|+]?\d+`)
	if err != nil {
		return 0
	}
	if reg == nil {
		return 0
	}
	intStr := reg.FindString(newS)
	value, _ := strconv.Atoi(intStr)
	if value < min {
		return min
	}
	if value > max {
		return max
	}
	return value
}

// ---------------------- 8. String to Integer (atoi) ----------------------

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Longest Common Prefix.
// Memory Usage: 2.5 MB, less than 28.00% of Go online submissions for Longest Common Prefix.
// ---------------------- 14. Longest Common Prefix -------------------------

func LongestCommonPrefix(strs []string) string {
	n := 0
	breakFlag := false
	for i := 0; ; i++ {
		n = i
		var curValue uint8
		for _, s := range strs {
			if i >= len(s) {
				breakFlag = true
				break
			}
			if curValue == 0 {
				curValue = s[i]
				continue
			}
			if s[i] != curValue {
				breakFlag = true
				break
			}
		}
		if breakFlag {
			break
		}
	}
	return strs[0][:n]

}

// ---------------------- 14. Longest Common Prefix -------------------------

// ---------------------- 1656. Design an Ordered Stream --------------------

type OrderedStream struct {
	//size int
	val []string
	ptr int
}

func Constructor(n int) OrderedStream {
	return OrderedStream{make([]string, n), 1}
}

func (this *OrderedStream) Insert(idKey int, value string) []string {
	if idKey < 0 || idKey >= len(this.val) {
		panic("illegal idKey!")
	}

	this.val = append(this.val, "")
	copy(this.val[idKey:], this.val[idKey-1:])
	this.val[idKey] = value

	if idKey != this.ptr {
		return []string{}
	} else {
		this.ptr++
		end := idKey
		for idKey <= len(this.val) {
			if this.val[idKey] != "" {
				end++
			}
		}
		return this.val[idKey-1 : end]
	}

}

/**
 * Your OrderedStream object will be instantiated and called as such:
 * obj := Constructor(n);
 * param_1 := obj.Insert(idKey,value);
 */

// ---------------------- 1656. Design an Ordered Stream --------------------

// ---------------------- 9. Palindrome Number ------------------------------

func Helper9(x int) int {
	newX := 0
	for x != 0 {
		temp := x / 10
		tt := x % 10
		newX = newX*10 + tt
		x = temp
	}
	fmt.Println("dong ------------------>", newX)
	return newX
}

func hepler9X(x int) bool {
	value := strconv.Itoa(x)
	s, e := 0, len(value)-1
	for s <= e {
		if value[s] != value[e] {
			return false
		}
		s++
		e--
	}
	return true
}

// Runtime: 8 ms, faster than 91.85% of Go online submissions for Palindrome Number.
//Memory Usage: 5.2 MB, less than 55.13% of Go online submissions for Palindrome Number.
func IsPalindrome(x int) bool {
	if x < 0 {
		return false
	} else if x < 10 {
		return true
	} else {
		//return strconv.Itoa(x) == strconv.Itoa(Helper9(x))
		return hepler9X(x)
	}
}

// ---------------------- 9. Palindrome Number ------------------------------
