//Variables
const overviewThisMonthButton = document.querySelector('#overviewThisMonth');
const overviewLastMonthButton = document.querySelector('#overviewLastMonth');
const trackForm = document.querySelector('#track-form');
const trackInputs = document.querySelectorAll('.track-input');

//Events
document.addEventListener('DOMContentLoaded', () => {
    request.open('POST', '/requestInformation');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = () => {
        const response = JSON.parse(request.responseText);

        //Total, Spent, Remaining, Track
        for (i in response) {

            //Total, Spent, Remaining
            if (i === 'total' || i === 'spent' || i === 'remaining') {
                document.querySelector(`#${i} > p`).innerHTML = `$${response[i]}`;
            }

            //Track

            //Show Users
            if (i === 'users') {
                for (i in response['users']) {
                    const newOption = document.createElement('option');
                    newOption.setAttribute('value', response['users'][i]);
                    newOption.innerHTML = response['users'][i];
                    document.querySelector('#track-user').appendChild(newOption);
                }
            }

            // Show Categories
            if (i === 'categories') {
                for (i in response['categories']) {
                    const newOption = document.createElement('option');
                    newOption.setAttribute('value', response['categories'][i]);
                    newOption.innerHTML = response['categories'][i];
                    document.querySelector('#track-category').appendChild(newOption);
                }
            }
        }

        //Progress Bar
        overviewThisMonth(response);

    }
    request.send()
})

overviewThisMonthButton.addEventListener('click', () => {
    request.open('POST', '/requestInformation');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = () => {
        const response = JSON.parse(request.responseText);
        overviewThisMonth(response);
    }
    request.send();
})

overviewLastMonthButton.addEventListener('click', () => {
    request.open('POST', '/requestInformation');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = () => {
        const response = JSON.parse(request.responseText);
        overviewLastMonth(response);
    }
    request.send();
})

trackForm.addEventListener('submit', () => {
    let newTransaction = {}

    const numOfFields = trackInputs.length - 1;
    let numOfValidFields = 0;

    trackInputs.forEach(element => {

        const type = element.getAttribute('data-track-input-type');
        const value = element.value;

        //Check for type
        if (type === 'type' && element.checked) {
            newTransaction[type] = value;
        }
        if (type === 'type' && !(element.checked)) {
            if (!(newTransaction[type])) {
                newTransaction[type] = '';
            }
        }
        if (type !== 'type') {
            newTransaction[type] = value;
        }
    })
    Track(newTransaction);
})

//Functions
function overviewThisMonth(response) {

    document.querySelector('#progress-bar').classList.remove('bg-success');
    document.querySelector('#progress-bar').classList.remove('bg-warning');
    document.querySelector('#progress-bar').classList.remove('bg-danger');
    document.querySelector('#progress-bar').classList.remove('bg-secondary');

    for (i in response) {
        if (i === 'total' || i === 'spent' || i === 'remaining') {
            document.querySelector(`#${i} > p`).innerHTML = `$${response[i]}`;
        }
    }


    if (response['total'] && response['spent']) {

        const percent = response['total'] / 100;
        const used = Math.round(response['spent'] / percent);

        if (used < 100) {
            document.querySelector('#progress-bar').style.width = `${used}%`;
            document.querySelector('#progress-bar').setAttribute('aria-valuenow', `${used}`);
            if (used <= 75) {
                document.querySelector('#progress-bar').classList.add('bg-success');
            }
            else {
                document.querySelector('#progress-bar').classList.add('bg-warning');
            }

            document.querySelector('#progress-bar').innerHTML = `${used}% ($${response['spent']}/$${response['remaining']})`;
        }

        else {
            document.querySelector('#progress-bar').style.width = '100%';
            document.querySelector('#progress-bar').setAttribute('aria-valuenow', '100');
            document.querySelector('#progress-bar').classList.add('bg-danger');
            document.querySelector('#progress-bar').innerHTML = `${used}% ($${response['remaining']})`;
        }
    }

    else {
        document.querySelector('#progress-bar').style.width = '100%';
        document.querySelector('#progress-bar').setAttribute('aria-valuenow', '100');
        document.querySelector('#progress-bar').classList.add('bg-secondary');
        document.querySelector('#progress-bar').innerHTML = '-';
    }
}

function overviewLastMonth(response) {

    document.querySelector('#progress-bar').classList.remove('bg-success');
    document.querySelector('#progress-bar').classList.remove('bg-warning');
    document.querySelector('#progress-bar').classList.remove('bg-danger');
    document.querySelector('#progress-bar').classList.remove('bg-secondary');

    for (i in response) {
        if (i === 'totalLastMonth') {
            document.querySelector('#total > p').innerHTML = `$${response[i]}`;
        }

        if (i === 'spentLastMonth') {
                document.querySelector('#spent > p').innerHTML = `$${response[i]}`;
        }

        if (i === 'remainingLastMonth') {
            document.querySelector('#remaining > p').innerHTML = `$${response[i]}`;
        }
    }

    if (response['totalLastMonth'] && response['spentLastMonth']) {

        const percent = response['totalLastMonth'] / 100;
        const used = Math.round(response['spentLastMonth'] / percent);

        if (used < 100) {
            document.querySelector('#progress-bar').style.width = `${used}%`;
            document.querySelector('#progress-bar').setAttribute('aria-valuenow', `${used}`);
            if (used <= 75) {
                document.querySelector('#progress-bar').classList.add('bg-success');
            }
            else {
                document.querySelector('#progress-bar').classList.add('bg-warning');
            }

            document.querySelector('#progress-bar').innerHTML = `${used}% ($${response['spentLastMonth']}/$${response['remainingLastMonth']})`;
        }

        else {
            document.querySelector('#progress-bar').style.width = '100%';
            document.querySelector('#progress-bar').setAttribute('aria-valuenow', '100');
            document.querySelector('#progress-bar').classList.add('bg-danger');
            document.querySelector('#progress-bar').innerHTML = `${used}% ($${response['remainingLastMonth']})`;
        }
    }

    else {
        document.querySelector('#progress-bar').style.width = '100%';
        document.querySelector('#progress-bar').setAttribute('aria-valuenow', '100');
        document.querySelector('#progress-bar').classList.add('bg-secondary');
        document.querySelector('#progress-bar').innerHTML = '-';
    }
}

function Track(transactionData) {
    request.open('POST', '/track');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = () => {
        const response = JSON.parse(request.responseText);
        if (response['status']) {
            location.reload();
        }
        else {
            document.querySelector('small[data-error-for-track]').innerHTML = response['error'];
        }
    }
    let data = new FormData();
    data.append('transactionData', JSON.stringify(transactionData));
    request.send(data);
}