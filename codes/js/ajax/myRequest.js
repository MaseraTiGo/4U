function myRequest(method, url, async)
{
	var xmlhttp;
	xmlhttp=new XMLHttpRequest();
	
	xmlhttp.onreadystatechange=function()
	{
		if (xmlhttp.readyState==4 && xmlhttp.status==200)
		{
            var res = xmlhttp.responseText
            console.log(res)
		}
    }

    xmlhttp.open(method, url, async)
    // xmlhttp.setRequestHeader('Content-Type', 'application/json')
    xmlhttp.send()
}

myRequest('GET', 'http://127.0.0.1:8000/fuck', true)
