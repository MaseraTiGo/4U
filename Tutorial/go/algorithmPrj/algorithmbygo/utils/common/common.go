// @File    : common
// @Project : go
// @Time    : 2021/5/13 15:21
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package common

func CompareSlice(s1 []int, s2 []int) bool {
	if len(s1) != len(s2) {
		//log.Fatal("failed! not enough nums!")
		return false
	}
	for i := 0; i < len(s1); i++ {
		if s1[i] != s2[i] {
			//log.Fatalf("failed: s1[%d]: %d != s2[%d]: %d", i, s1[i], i, s2[i])
			return false
		}
	}
	return true
}
