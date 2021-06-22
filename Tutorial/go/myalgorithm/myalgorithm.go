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
	"jundong.dong/myalgorithm/tree"
	"net"
	"runtime"
	"strings"
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
	//fmt.Fprint(os.Stdout, "motherfucker!")
	//fuck, err := os.OpenFile("fuck.txt", os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0644)
	//if err != nil {
	//	fmt.Println("fucking err happened!", err)
	//}
	//
	//fmt.Fprint(fuck, "ai you fuck you!")
	//
	//ss := []string{"fuck you"}
	//var ii interface{}
	//ii = ss
	//fmt.Println(ii)
	//http.Client{}
	//testSlice := []int{1, 2, 3, 4}
	//testSlice = append(testSlice, 0)
	//x := copy(testSlice[1:], testSlice[:])
	//testSlice[0] = 0
	//fmt.Println("dong ----------------->", testSlice, x)
	//server, err := net.Listen("tcp", ":31046")
	//if err != nil {
	//	fmt.Printf("fail 2 start server, %s\n", err)
	//}
	//
	//fmt.Print("server is starting")
	//
	//for {
	//	conn, err := server.Accept()
	//	if err != nil{
	//		fmt.Printf("fail to connect, %s\n", err)
	//	}
	//	go connHandler(conn)
	//}

	//word1 := []string {"abc", "d", "defg"}
	//word2 := []string {"abcddefg"}
	//res := arrayStringsAreEqual(word1, word2)
	//fmt.Print("dong ---------------->", res)

	//// 1656
	//obj := list.Constructor(5)
	//res := obj.Insert(3, "ccccc")
	//fmt.Print("dong -------------->", res)
	//res = obj.Insert(1, "aaaaa")
	//fmt.Print("dong -------------->", res)
	//res = obj.Insert(2, "bbbbb")
	//fmt.Print("dong -------------->", res)
	//res = obj.Insert(5, "eeeee")
	//fmt.Print("dong -------------->", res)
	//res = obj.Insert(4, "ddddd")
	//fmt.Print("dong -------------->", res)
	//// 1656

	root := tree.GenerateTreeByArray([]int{})
	ans := tree.MaxDepth104(root)
	fmt.Println("dong ------------------>104", ans)

}
