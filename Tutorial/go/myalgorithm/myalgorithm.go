// @File    : myalgorithm
// @Project : myalgorithm
// @Time    : 2021/5/13 17:09
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package main

import (
	"fmt"
	"net"
	"runtime"
	"strings"
	"jundong.dong/myalgorithm/list"
)

func a() {
	for i := 1; i < 10; i++ {
		runtime.Gosched()
		fmt.Println("A:", i)
	}
}

func b() {

	for i := 1; i < 10; i++ {
		runtime.Gosched()
		fmt.Println("B:", i)
	}
}

func connHandler(conn net.Conn) {
	if conn == nil {
		return
	}

	buf := make([]byte, 4096)
	for {
		cnt, err := conn.Read(buf)
		if err != nil || cnt == 0 {
			conn.Close()
			break
		}
		inStr := strings.TrimSpace(string(buf[0:cnt]))
		inputs := strings.Split(inStr, " ")
		fmt.Print("get msg------------->", inputs)
	}
}

func arrayStringsAreEqual(word1 []string, word2 []string) bool {
	return strings.Join(word1, "") == strings.Join(word2, "")
}



func main() {
	// go test example: go test ./... -v -test.run 104
	//fmt.Println(123%10)
	print(list.IsPalindrome(123321))

}
