// src/HiTrustHandler/app/static/js/app.js
new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    data: {
        username: '',
        password: '',
        source: '',
        loggedIn: false,
        loading: false,
        errorMessage: '',
        submitted: false,
        funds: [],
        selectedFunds: [],
        selectAll: false,
        logs: []
    },
    methods: {
        viewLog() {
            window.open('/get_log', '_blank')
        },
        login() {
            this.loading = true;
            this.errorMessage = '';
            fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({username: this.username, password: this.password})
            })
                .then(response => response.json())
                .then(data => {
                    this.loading = false;
                    if (data.status === 'success') {
                        this.loggedIn = true;
                    } else {
                        alert('Login failed. Please check your username and password.')
                    }
                })
                .catch(() => {
                    this.loading = false;
                    this.errorMessage = 'An unexpected error occurred. Please try again.';
                });
        },
        submitSource() {
            fetch('/submit_source', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({source: this.source})
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Source submitted successfully');
                        this.submitted = true;
                        this.logs.push(new Date().toLocaleString() + ": Start Processing...");
                    } else {
                        alert('Source submission failed')
                    }
                })
                .catch(() => {
                    this.errorMessage = 'An error occurred.';
                });
        },
        getCusip() {
            this.selectedFunds.forEach(fileName => {
                const fund = this.funds.find(f => f.source_file === fileName);
                if (fund) {
                    fund.loading = true;
                    this.logs.push(new Date().toLocaleString() + ": Searching Cusip and Investment Status for " + fund.fund_code + " in DMH");
                    fetch('/get_cusip', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            name: fund.fund_code,
                            ur: fund.ur_code,
                            data: fund.component_data,
                            ex_data: fund.ex_data,
                            dpu: fund.DPU
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === 'success') {
                                fund.cusip = data.cusip;
                                fund.investment_status = data.investment_status;
                                if (fund.cusip == 'Not Found') {
                                    this.logs.push(new Date().toLocaleString() + ": Can't find Cusip for " + fund.fund_code + " in DMH - Class Setup & Fund Setup");
                                } else {
                                    this.logs.push(new Date().toLocaleString() + ": Cusip received for  " + fund.fund_code);
                                }
                                if (fund.investment_status == 'Not Found') {
                                    this.logs.push(new Date().toLocaleString() + ": Can't find Investment Status for " + fund.fund_code + " in DMH - Fund Setup");
                                } else {
                                    this.logs.push(new Date().toLocaleString() + ": Investment Status received for  " + fund.fund_code);
                                }
                            } else {
                                this.logs.push(new Date().toLocaleString() + ": Failed to get Cusip and Investment Status for " + fund.fund_code);
                            }
                        })
                        .catch(error => {
                            this.logs.push(new Date().toLocaleString() + ": Error " + error + " occurred while getting Cusip and Investment Status for " + fund.fund_code);
                        })
                        .finally(() => {
                            fund.loading = false
                        })

                }
            });
        },
        importData() {
            this.selectedFunds.forEach(fundName => {
                const fund = this.funds.find(f => f.name === fundName);
                if (fund) {
                    fund.loading = true;
                    this.logs.push(new Date().toLocaleString() + ": Importing data for " + fund.name);
                    // Simulate API call to import data
                    setTimeout(() => {
                        fund.status = 'Imported'; // Mock status
                        fund.loading = false;
                        this.logs.push(new Date().toLocaleString() + ": Data imported for " + fund.name);
                    }, 2000);
                }
            });
        },
        toggleSelectAll() {
            this.selectedFunds = this.selectAll ? [] : this.funds.map(f => f.source_file);
        }
    }
});
