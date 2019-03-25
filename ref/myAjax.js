function data2str(data){
	
	//随机
	data.t = new Date().getTime();
	
	console.log(data)

	var res = [];
	for(var key in data){
		//在url中不能出现中文，需要转码
		//url中只能出现字母/数字/下划线/ASCII
		res.push(encodeURIComponent(key)+"="+encodeURIComponent(data[key])); //[t="xxx",userName=xjw,userPwd='123456']
	}

	res_str = res.join("&")
	console.log(res_str)
	return res_str; //将数组元素用&连接
}

function ajax(options){

    var xmlhttp;
	if(window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}
	else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
	
	if(options.type.toLowerCase() === "get"){
		//将对象data转换成字符串
		var str = data2str(options.data);
		// 2.设置请求方式和（后端的）请求地址
		xmlhttp.open(options.type,options.url+"?"+str,true);
		
		// 3.发送请求
		xmlhttp.send();
	}
	else{
		console.log("post")
		console.log(options.data)
		//str = data2str(options.data,false);
		// 2.设置请求方式和（后端的）请求地址
		xmlhttp.open(options.type,options.url,options.flag);
		
		// 设置HTTP头
		xmlhttp.setRequestHeader(options.headtype,JSON.stringify(options.data));
		
		// 3.发送请求，直接传参
		xmlhttp.send();
		
    }
    
    // 4.监听状态的变化
	xmlhttp.onreadystatechange = function(ev2){
		//判断请求是否完成（服务器有响应）
		if(xmlhttp.readyState==4){
			
			clearInterval(timer);
			
			//判断请求是否成功（服务器状态码）
			if(xmlhttp.status>=200 && xmlhttp.status<300 || xmlhttp.status==304){
				//5.处理返回的结果，获得服务器返回的数据
				//responseText 字符串形式的响应数据
				//responseXML XML形式
				
				options.success(xmlhttp);
			}
			else{
				options.error(xmlhttp);
			}    
		}
    }
    
    if(options.timeout){
		timer = setInterval(function(){
			//超时时执行的回调函数
			//中断异步对象的请求
			xmlhttp.abort();
			clearInterval(timer);
			
		},options.timeout);
	}
}