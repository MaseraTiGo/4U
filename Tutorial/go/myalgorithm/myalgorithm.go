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
	"os"
	"runtime"
	"runtime/trace"
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

func main() {
	f, err := os.Create("trace.out")
	if err != nil {
		panic(err)
	}

	defer f.Close()

	//启动trace goroutine
	err = trace.Start(f)
	if err != nil {
		panic(err)
	}
	defer trace.Stop()

	//main
	fmt.Println("Hello World")
}
