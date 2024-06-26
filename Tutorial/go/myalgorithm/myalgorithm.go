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
	"encoding/json"
	"fmt"
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

type Dante struct {
	Apple string `json:"apple"`
	Ball string `json:"ball"`
	Canada string `json:"canada"`
	Ing int `json:"ing"`
}


func main() {
	// go test example: go test ./... -v -test.run 104

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
	//
	//word1 := []string {"abc", "d", "defg"}
	//word2 := []string {"abcddefg"}
	//res := arrayStringsAreEqual(word1, word2)
	//fmt.Print("dong ---------------->", res)
	//
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
	//
	//root := tree.GenerateTreeByArray([]int{})
	//ans := tree.MaxDepth104(root)
	//fmt.Println("dong ------------------>104", ans)
	//
	//var res int
	//fmt.Println("dong -------------->", res)
	//
	//var a []int
	//fmt.Println("dong ------------>", a)
	//aa := make([]int, 2, 5)
	//fmt.Println("dong ------------>", aa, len(aa))
	//
	//aaa := make([]int, 5)
	//fmt.Println("dong ------------>", aaa)
	//
	//a := []int {1, 2, 3, 4}
	//b := []int {1, 2, 3}
	//fmt.Println("dong ---------------->", reflect.DeepEqual(a, b))

	//x := -123
	//
	//s := 0
	//for x != 0 {
	//	t := x % 10
	//	x = x / 10
	//	s = s*10 + t
	//}
	//println(s)

	//var a int = 2
	//fmt.Printf("dong ---------------->%T: %v\n", a, a)
	//aType := reflect.TypeOf(a)
	//aValue := reflect.ValueOf(&a)
	//fmt.Printf("dong ---------------->%T: %v\n", aType, aType)
	//fmt.Printf("dong ---------------->%T: %v\n", aValue, aValue)
	//aValue.Elem().SetInt(5)
	//fmt.Println("dong ---------------------->", a)

	testStr := "{\"apple\": \"aston\", \"ball\": \"martin\"}"
	var dante Dante
	_ = json.Unmarshal([]byte(testStr), &dante)
	fmt.Println(dante.Apple)
	fmt.Println(dante.Ball)
	//fmt.Println(dante.Canada)
	fmt.Printf("%#v", dante.Canada)
	fmt.Printf("%#v", dante.Ing)

	marshalStr, err := json.Marshal(testStr)
	if err != nil {
		fmt.Printf("%#v", marshalStr)
	}
	fmt.Printf("%#v", string(marshalStr))

}
