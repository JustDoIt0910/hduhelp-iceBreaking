function getOptions() {
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.addEventListener('load',() => {
        for(let i = 1; i <= 4; i++) {
            let op = document.getElementById('op' + i.toString())
            op.innerHTML = '';
            op.setAttribute('class', 'options font-style');
        }
        var res = xhr.response;
        for(let op in res) {
            var option = document.getElementById(op);
            option.innerHTML = res[op];
            option.addEventListener('click', (e) => validate(op))
            option.style.visibility = 'visible';
        }
        getPhoto();
    })
    xhr.open('get','http://localhost:5000/index/play/options',true);
    xhr.send(null);
}

function getPhoto() {
    var photo = document.getElementById('photo');
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'blob';
    xhr.addEventListener('load',() => {
        var blob = xhr.response;
        photo.src = window.URL.createObjectURL(blob);
        photo.style.visibility = 'visible'
    })
    xhr.open('get','http://localhost:5000/index/play/photo',true);
    xhr.send(null);
}

function validate(option) {
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'json';
    xhr.addEventListener('load', () => {
        //console.log(xhr.response)
        var res = xhr.response;
        var right = document.getElementById('op' + res.iscorrect.toString());
        right.setAttribute('class', 'font-style right');
        if(res.success === false) {
           var error = document.getElementById('op' + res.ans.toString());
           error.setAttribute('class', 'font-style error');
        }
    })
    xhr.open('get','http://localhost:5000/index/play/validate?select=' + option,true);
    xhr.send(null);
}

function userInfo(type) {
    var img = document.getElementById('avatar');
    var userinfo = document.getElementById('userinfo');
    var xhr = new XMLHttpRequest();
    xhr.responseType = type === 'avatar' ? 'blob' : 'json';
    xhr.addEventListener('load',() => {
    var redirect = xhr.getResponseHeader('redirect');
    if(redirect != null){
        window.location.href = 'http://localhost:5000' + redirect;
    }
    if(type === 'avatar') {
        var blob = xhr.response;
        img.src = window.URL.createObjectURL(blob);
    }
    else {
        var info = xhr.response;
        if(info['name'] !== undefined)
            userinfo.innerHTML = info['name'] + '  ' + info['stu_id'] + '  ' + info['department'];
    }
    })
    xhr.open('get','http://localhost:5000/userinfo/' + type,true);
    xhr.send(null);
}

window.onload = function () {
    var start = document.getElementById('start');
    start.addEventListener('click', () => {
        getOptions();
    });
    userInfo('avatar');
    userInfo('info')
}