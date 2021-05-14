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
		return float64(total[mid] + total[mid-1]) / 2
	} else {
		return float64(total[int(lenTotal / 2)])
	}
}
