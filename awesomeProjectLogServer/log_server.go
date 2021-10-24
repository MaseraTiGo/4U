// @File    : log_server
// @Project : awesomeGoLogServer
// @Time    : 2021/8/6 12:00
// ======================================================
//                                        /
//   __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
// ======================================================
package main

import (
	"database/sql"
	"encoding/json"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	//"logserver/log_struct"
	"net"
	"time"
)

type LogStruct interface {
	formatDataToSqlStr() string
}

type OperateLog struct {
	User    string `json:"user"`
	Details string `json:"details"`
	Ip      string `json:"ip"`
	Flag    int    `json:"flag"`
	Status  int    `json:"status"`
}

type Classify struct {
	Classify int `json:"classify"`
}

func (o OperateLog) formatDataToSqlStr() string {

	return fmt.Sprintf("(\"%s\", \"%s\", \"%s\", %d, %d),", o.User, o.Details, o.Ip, o.Flag, o.Status)

}

var LogMapping = map[int]LogStruct{
	0: &OperateLog{},
}

func initDB() *sql.DB {
	path := "root:123918@tcp(127.0.0.1:3306)/localuse?autocommit=true"
	DB, _ := sql.Open("mysql", path)
	DB.SetConnMaxLifetime(100)
	DB.SetMaxIdleConns(10)
	if err := DB.Ping(); err != nil {
		fmt.Println("open database fail!")
		return nil
	} else {
		fmt.Println("open database successfully.")
	}
	return DB

}

func execString(jsonStr string) string {
	var kind Classify
	_ = json.Unmarshal([]byte(jsonStr), &kind)
	curLogStruct, _ := LogMapping[kind.Classify]
	_ = json.Unmarshal([]byte(jsonStr), curLogStruct)
	//fmt.Println(curLogStruct.formatDataToSqlStr())
	return curLogStruct.formatDataToSqlStr()
}

func UDPServer() {
	udpHandle, err := net.ListenUDP("udp", &net.UDPAddr{
		IP: net.IPv4(0, 0, 0, 0), Port: 50816, Zone: "0",
	})

	if err != nil {
		fmt.Println("create udp server failed!")
		return
	}
	defer udpHandle.Close()

	for {
		time.Sleep(time.Second)
		//var data [1024]byte
		//n, _, err := udpHandle.ReadFromUDP(data[:])
		//if err != nil {
		//	fmt.Println("read data error", err)
		//}
		//fmt.Println("received data is:", string(data[:n]))
		//var fucker log_struct.FuckingTest
		//json.Unmarshal(data[:n], &fucker)
		//print("dong --------------->", fucker.LogInfo.User)
	}
}

func client() {
	listen, err := net.DialUDP("udp", nil, &net.UDPAddr{
		IP:   net.IPv4(0, 0, 0, 0),
		Port: 50816,
	})
	if err != nil {
		fmt.Printf("listen udp server error:%v\n", err)
	}
	defer listen.Close()

	for i := 0; i < 10; i++ {
		print("gonna send data")
		sendData := []byte(`{"classify": 0, "logInfo": {"user": "aston_martin", "details": "stupid asshole", "ip": "127.0.0.1", "flag": 1, "status": 0}}`)
		_, err = listen.Write(sendData) // 发送数据
		if err != nil {
			fmt.Println("发送数据失败，err:", err)
			return
		}
		time.Sleep(time.Second)
	}

}

func main() {
	//testStr := `{"classify": 0, "logInfo": {"user": "aston_martin", "details": "stupid asshole", "ip": "127.0.0.1", "flag": 1, "status": 0}}`

	//operate, ok := curLogStruct.(*OperateLog)
	//if ok {
	//	fmt.Println("ok -------------------->")
	//	fmt.Println(operate.logMapping().Details)
	//} else {
	//	fmt.Println("not ok------------------->")
	//}
	//print(curLogStruct.getInfo().Details)

	//testStr := `{"classify": 0, "user": "aston_martin", "details": "stupid asshole", "ip": "127.0.0.1", "flag": 1, "status": 0}`
	//sqlPrefix := "insert into fuckingtest(user, details, ip, flag, status) values "
	//conn := initDB()
	//counter := 0
	//data := ""
	//sTime := time.Now().UnixNano()
	//for i := 0; i < 50000; i++ {
	//	counter++
	//	data += execString(testStr)
	//
	//	if counter == 1000 {
	//		fuck := sqlPrefix + data
	//		fuck = strings.TrimRight(fuck, ",")
	//		res, err := conn.Exec(fuck)
	//		if err != nil {
	//			fmt.Println("fuck====================>", err, res)
	//		}
	//		counter = 0
	//		data = ""
	//	}
	//}
	//eTime := time.Now().UnixNano()
	//println("fucking cost -------------------->", float64((eTime-sTime)/1e6))
	//go UDPServer()
	//go client()
	//for {
	//	time.Sleep(time.Second * 3)
	//}

	//test := "insert into fuckingtest(user, details, ip, flag, status) values (\"aston_martin\", \"stupid asshole\", \"127.0.0.1\", 1, 0),(\"aston_martin\", \"stupid asshole\", \"127.0.0.1\", 1, 0),(\"aston_martin\", \"stupid asshole\", \"127.0.0.1\", 1, 0),(\"aston_martin\", \"stupid asshole\", \"127.0.0.1\", 1, 0),(\"aston_martin\", \"stupid asshole\", \"127.0.0.1\", 1, 0),"
	//strings.TrimRight(test, ",")

	testStr := "fuck you"
	println("dong -------------->", string(testStr[11]))

}
