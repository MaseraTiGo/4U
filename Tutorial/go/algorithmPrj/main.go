// @File    : main
// @Project : go
// @Time    : 2021/5/13 14:20
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package main

import "fmt"
import "Johnathan.strong/algorithm/algorithmbygo/list"

func main() {
	fmt.Println("this is the fucking dream starts!")
	test := []int{1, 2, 3, 4}
	ll := list.GenerateListNode(test)
	ans := list.IterateListNode(ll)
	fmt.Println(ans)
}
