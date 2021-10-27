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

// ------------------------------ 509. Fibonacci Number ------------------

func Fib509(n int) int {
	caching := []int{0, 1}
	if n < len(caching){
		return caching[n]
	}
	ans := Fib509(n-1) + Fib509(n-2)
	caching = append(caching, ans)
	return ans
}

func Fib509Two(n int) int {
	if n <=1 {
		return n
	}
	ans := Fib509Two(n-1) + Fib509Two(n-2)
	return ans
}
// ------------------------------ 509. Fibonacci Number ------------------
