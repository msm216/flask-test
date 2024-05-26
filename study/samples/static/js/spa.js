function loadContent(page) {
    var content = document.getElementById('content');
    switch(page) {
        case 'home':
            content.innerHTML = `
                <h1>Home</h1>
                <p>This is the home page content.</p>
            `;
            break;
        case 'about':
            content.innerHTML = `
                <h1>About</h1>
                <p>This is the about page content.</p>
            `;
            break;
        case 'contact':
            content.innerHTML = `
                <h1>Contact</h1>
                <p>This is the contact page content.</p>
            `;
            break;
        case 'profile':
            content.innerHTML = `
                <h1>Profile</h1>
                <p>This is the profile page content.</p>
            `;
            break;
        case 'settings':
            content.innerHTML = `
                <h1>Settings</h1>
                <p>This is the settings page content.</p>
            `;
            break;
        case 'help':
            content.innerHTML = `
                <h1>Help</h1>
                <p>This is the help page content.</p>
            `;
            break;
        case 'dashboard':
            content.innerHTML = `
                <h1>Dashboard</h1>
                <p>This is the dashboard page content.</p>
            `;
            break;
        case 'reports':
            content.innerHTML = `
                <h1>Reports</h1>
                <p>This is the reports page content.</p>
            `;
            break;
        case 'analytics':
            content.innerHTML = `
                <h1>Analytics</h1>
                <p>This is the analytics page content.</p>
            `;
            break;
    }
}

function switchNav(navId) {
    var navs = document.querySelectorAll('.nav');
    navs.forEach(nav => nav.style.display = 'none');
    document.getElementById(navId).style.display = 'block';
}