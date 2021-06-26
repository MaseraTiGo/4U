// ===================================
// file_name     : example.go
// file_author   : Johnathan.Strong
// create_time   : 2021/6/14 8:47
// ide_name      : GoLand
// project_name  : awesomeProjectIris
// ===================================

//
//                                         /
//    __.  , , , _  _   __ ______  _    __/  __ ____  _,
//   (_/|_(_(_/_</_/_)_(_)/ / / <_</_  (_/_ (_)/ / <_(_)_
//                                                    /|
//                                                   |/
//
package main

import (
	"fmt"
	"github.com/kataras/iris/v12"
)

func main() {
	app := iris.Default()
	fmt.Print(app)
	app.Use(myMiddleware)

	app.Handle("GET", "/ping", func(ctx iris.Context) {
		ctx.JSON(iris.Map{
			"mesage": "pong",
			"data": "fucker",
		})
	})
	app.Listen(":8000")
}

func myMiddleware(ctx iris.Context) {
	ctx.Application().Logger().Infof("runs before %s", ctx.Path())
	ctx.Next()
}
