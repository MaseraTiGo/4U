var http = require('http')
http.createServer(function (request, response) {
    response.writeHead(200, {'Content-Type': 'text/plain'})
    response.end('hello my frist node.js')
}).listen(8888)

console.log('server now is running at 8888')