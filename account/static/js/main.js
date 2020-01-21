function XMLHttpRequests(method, callback, url, data, element) {
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === this.DONE) {
            response_data = JSON.parse(this.responseText)
            console.log(response_data)
			callback(response_data, element)
		} else {
			console.log(this.readyState)
		}
	});
	xhr.open(method, url);
    // xhr.setRequestHeader("Content-Type", "application/json");
    // console.log(data)
    if(data){
        xhr.send(data)
    }else{
            xhr.send()
    }
}