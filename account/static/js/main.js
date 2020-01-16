function XMLHttpRequests(method, callback, url, data, element) {
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;

	xhr.addEventListener("readystatechange", function () {
		if (this.readyState === this.DONE) {
			response_data = JSON.parse(this.responseText)
			callback(response_data, element)
		} else {
			console.log(this.readyState)
		}
	});
	xhr.open(method, url);
    xhr.setRequestHeader("Content-Type", "application/json");
    console.log(data)
    if(data){
        xhr.send(data)
    }else{
            xhr.send()
    }
}


function fetch_upvote_data(data, element){
    console.log(data, element)
    if(data.action){
        if(data.action=='like'){
            child = element.firstElementChild
            UIkit.icon(child).svg.then(function(svg) { svg.querySelector('path').style.stoke = 'red'; })
            UIkit.icon(child).svg.then(function(svg) { svg.querySelector('path').style.fill = 'red'; })
            element.removeAttribute('unlike')
            element.setAttribute('like',' ')
            print(element)
            element.childNodes[1].nodeValue = parseInt(element.childNodes[1].nodeValue) +1  
        }else if(data.action=='unlike'){
            console.log(data.action)
            child = element.firstElementChild
            UIkit.icon(child).svg.then(function(svg) { svg.querySelector('path').style.stoke = '#000'; })
            UIkit.icon(child).svg.then(function(svg) { svg.querySelector('path').style.fill = '#fff'; })
            element.setAttribute('unlike', ' ')
            element.removeAttribute('like')
            element.childNodes[1].nodeValue = parseInt(element.childNodes[1].nodeValue) -1
        }
    }
    document.getElementById('flash-messages').innerHTML = ''
    document.getElementById('flash-messages').innerHTML ="<div class='uk-alert uk-alert-"+data.category+"'><a class='uk-alert-close' uk-close></a><p>"+data.message+"</p></div>"

}

function copy_to_clipboard(e) {
    var copyText = this.getAttribute("to_copy");
    copyText = window.location.origin+copyText

    var input = document.createElement('input');
    input.setAttribute('value', copyText);
    document.body.appendChild(input);
    input.select();

    result = document.execCommand("copy");
    document.getElementById('flash-messages').innerHTML = ''
    document.getElementById('flash-messages').innerHTML ="<div class='uk-alert uk-alert-success'><a class='uk-alert-close' uk-close></a><p>Link copied</p></div>"
    input.remove()
}

function upvote_answer(e){
    data = JSON.stringify({"upvote":true,"video_id":this.getAttribute('video-id'), "csrfmiddlewaretoken":document.querySelector('input[name=csrfmiddlewaretoken]').value});
    console.log(data)
    url = window.location.origin+'/upvote'
    XMLHttpRequests('POST', fetch_upvote_data, url, data, this)
    console.log(this)
}


window.onload = function(){
    upvote_buttons = document.getElementsByClassName('yt-upvote');
    for(upvote_button_index=0; upvote_button_index < upvote_buttons.length; upvote_button_index++){
        upvote_button = upvote_buttons[upvote_button_index]
        
        console.log(upvote_button)
        upvote_button.addEventListener('click', upvote_answer);
    }
    yt_upvotes = document.querySelectorAll('.yt-upvote[like]')
    for(yt_upvote_index=0; yt_upvote_index < yt_upvotes.length; yt_upvote_index++){
        yt_upvote = yt_upvotes[yt_upvote_index]
    
        console.log(yt_upvotes)
        yt_upvote_child = yt_upvote.firstElementChild
        // this.setTimeout
        UIkit.icon(yt_upvote_child).svg.then(function(svg) { svg.querySelector('path').style.fill = 'red'; })
    }

    to_copys = document.querySelectorAll('[to_copy]')
    for(to_copy_index=0; to_copy_index < to_copys.length; to_copy_index++){
        to_copy = to_copys[to_copy_index]
        
        to_copy.addEventListener('click', copy_to_clipboard)
    }

}