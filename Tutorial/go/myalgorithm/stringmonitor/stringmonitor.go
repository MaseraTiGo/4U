// ===================================
// file_name     : stringmonitor.go
// file_author   : Johnathan.Strong
// create_time   : 2021/5/15 22:09
// ide_name      : GoLand
// project_name  : myalgorithm
// ===================================

//
//                                         /
//    __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
//
package stringmonitor

import (
	"fmt"
	"unicode/utf8"
)

func IterString(s string) {
	for len(s) != 0 {
		value, size := utf8.DecodeRuneInString(s)
		fmt.Print(string(value), "->")
		s = s[size:]
	}
}

