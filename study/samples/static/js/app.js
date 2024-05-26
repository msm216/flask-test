function loadContent(page) {
    fetch('/' + page)
        .then(response => response.text())
        .then(data => {
            document.getElementById('content').innerHTML = data;
        })
        .catch(error => console.error('Error loading content:', error));
}

function switchNav(navId) {
    var navs = document.querySelectorAll('.nav');
    navs.forEach(nav => nav.style.display = 'none');
    document.getElementById(navId).style.display = 'block';
}