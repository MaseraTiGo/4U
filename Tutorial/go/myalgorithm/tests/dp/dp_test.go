// @File    : dp_test
// @Project : myalgorithm
// @Time    : 2021/10/27 16:17
// ======================================================
//                                         /
//    __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package dp

import (
	"fmt"
	"jundong.dong/myalgorithm/dp"
	"testing"
)

func TestFib509(t *testing.T) {
	ans := dp.Fib509(5)
	println("dong ----------------------------->509: ", ans)
}

func TestClimbStairs70(t *testing.T) {
	ans := dp.ClimbStairs70(44)
	fmt.Println("dong -------------------->70: ", ans)
}

func TestGetMax1646(t *testing.T) {
	ans := dp.GetMaximumGenerated1646(7)
	fmt.Println("dong --------------------->1646: ", ans)
}

func TestParent(t *testing.T) {
	ans := dp.Parent(2)
	fmt.Println("dong ----------------------> parent: ", ans)
}