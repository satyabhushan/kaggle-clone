window.onload = function () {
    competition_id = window.location.pathname.split('/')[2]
    url = window.location.origin + '/competition/' + competition_id + '/join-status'
    XMLHttpRequests('GET', handle_launch_status, url, null, null)
}

function handle_launch_status(data, element) {
    console.log(data)
    if (data.task_status == 'PENDING') {
        setTimeout(function () {
            competition_id = window.location.pathname.split('/')[2]
            url = window.location.origin + '/competition/' + competition_id + '/join-status'
            XMLHttpRequests('GET', handle_launch_status, url, null, null)
        }, 2000)
    } else if (data.task_status == 'SUCCESS'){
        document.querySelector('.task-status').innerHTML = '<h4>Jupyter notebook is launched successfully.</h4><a href="http://' + data.jupyter_path + '">Start Building your model.</p>'
    }
}
