/**
 * Creates A web server and server
 */

// web server constants and dependencies
var webPort = 8080;
var serverUrl = "127.0.0.1";
var launchPath = "/index.html";
var http = require("http");
var url = require('url');
var path = require("path");
var fs = require("fs");


console.log("Starting web server at " + serverUrl + ":" + webPort);
http.createServer(function (req, res) {
    var urlObj = url.parse(req.url, true);
    var queryString = urlObj.query;
    
    if(Object.keys(queryString).length == 0)
    {
        var pathname = urlObj.pathname;
        var localPath = __dirname + (pathname == '/' ? launchPath : pathname || launchPath) ;
        console.log("Serving file: " + localPath);
        getFile(localPath, res, "html");
    }
    else
    {
        // let body = [];
        // request.on('data', (chunk) => {
        // body.push(chunk);
        // }).on('end', () => {
        // body = Buffer.concat(body).toString();
            
        // });

        res.setHeader('Content-Type', 'application/json');
        res.write(JSON.stringify({speed: 130.2}));
        res.end()
    }


}).listen(webPort, serverUrl);


function getFile(localPath, res, mimeType) {
    fs.readFile(localPath, function (err, contents) {
        if (!err) {
            res.setHeader("Content-Length", contents.length);
            if (mimeType != undefined) {
                res.setHeader("Content-Type", mimeType);
            }
            res.statusCode = 200;
            res.end(contents);
        } else {
            res.writeHead(500);
            res.end();
        }
    });
}

