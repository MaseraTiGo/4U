// @File    : dynamic_programming
// @Project : myalgorithm
// @Time    : 2021/10/27 16:13
// ======================================================
//                                         /
//    __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package dp

// ------------------------------ 70. Climbing Stairs --------------------

func ClimbStairs70Old(n int) int {

	cacheMapping := make(map[int]int)
	cacheMapping[1] = 1
	cacheMapping[2] = 2
	value, ok := cacheMapping[n]
	if ok {
		return value
	}
	ans := ClimbStairs70(n-1) + ClimbStairs70(n-2)
	cacheMapping[n] = ans
	return ans
}

// Runtime: 0 ms, faster than 100.00% of Go online submissions for Climbing Stairs.
//Memory Usage: 1.9 MB, less than 80.86% of Go online submissions for Climbing Stairs.
func ClimbStairs70(n int) int {
	if n <= 2 {
		return n
	}
	if n <= 2 {
		return n
	}
	n1, n2 := 1, 2
	for i := 3; i <= n; i++ {
		tmp := n2
		n2 += n1
		n1 = tmp
	}
	return n2
}

// ------------------------------ 70. Climbing Stairs --------------------

// ------------------------------ 509. Fibonacci Number ------------------

func Fib509(n int) int {
	caching := []int{0, 1}
	if n < len(caching) {
		return caching[n]
	}
	ans := Fib509(n-1) + Fib509(n-2)
	caching = append(caching, ans)
	return ans
}

func Fib509Two(n int) int {
	if n <= 1 {
		return n
	}
	ans := Fib509Two(n-1) + Fib509Two(n-2)
	return ans
}

// ------------------------------ 509. Fibonacci Number ------------------

// ------------------------------ 1646. Get Maximum in Generated Array ---

//Runtime: 0 ms, faster than 100.00% of Go online submissions for Get Maximum in Generated Array.
//Memory Usage: 2.1 MB, less than 93.10% of Go online submissions for Get Maximum in Generated Array.
func GetMaximumGenerated1646(n int) int {
	cache := []int{0, 1}
	if n <= 1 {
		return cache[n]
	}
	maxValue := 1
	for i := 2; i <= n; i++ {
		if i%2 == 0 {
			tmp := cache[i/2]
			if tmp > maxValue {
				maxValue = tmp
			}
			cache = append(cache, tmp)
		} else {
			index := i / 2
			tmp := cache[index] + cache[index+1]
			if tmp > maxValue {
				maxValue = tmp
			}
			cache = append(cache, tmp)
		}
	}
	return maxValue
}

func GetMaximumGenerated1646NoUse(n int) int {
	if n <= 1 {
		return n
	}

	n0, n1, n2 := 1, 1, 1

	maxValue := 1
	for i := 2; i <= n; i++ {
		if i%2 == 0 {
			even := n1
			n2 = even
			println("dong ---------------->n : ", i)
			println("dong ---------------->even : ", even)
			println("dong ---------------->nums : ", n0, n1, n2)
			if even > maxValue {
				maxValue = even
			}
		} else {
			odd := n0 + n1
			println("dong ---------------->n : ", i)
			println("dong ---------------->odd : ", odd)
			n0 = n1
			n1 = n2
			n2 = odd
			println("dong ---------------->nums : ", n0, n1, n2)
			if odd > maxValue {
				maxValue = odd
			}
		}
	}
	return maxValue
}

// ------------------------------ 1646. Get Maximum in Generated Array ---
