// src/HiTrustHandler/app/static/js/app.js
new Vue({
    el: '#app',
    data: {
        username: '',
        password: '',
        source: '',
        loggedIn: false
    },
    methods: {
        login() {
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username: this.username, password: this.password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    this.loggedIn = true;
                } else {
                    alert('Login failed');
                }
            });
        },
        submitSource() {
            fetch('/submit_source', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ source: this.source })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Source submitted successfully');
                } else {
                    alert('Source submission failed');
                }
            });
        }
    }
});
