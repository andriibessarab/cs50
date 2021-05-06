//Variables
const historyTable = document.querySelector('#history-table');

const historyFilters = document.querySelectorAll('.history-filters');

document.querySelector('h2 > button').addEventListener('click', () => {
    turnOffAllFilters();
})

document.addEventListener('DOMContentLoaded', () => {
    request.open('POST', '/requestInformation');
    request.setRequestHeader('X-CSRFToken', csrf_token); 
    request.onload = () => {

        //Get response
        const response = JSON.parse(request.responseText);

        //Show all transactions
        for (transaction in response['transactions']) {
            const newRow = document.createElement('tr');
            for (col in response['transactions'][transaction]) {
                const newCol = document.createElement('td');
                if (col === 'amount') {
                    newCol.innerHTML=`$${response['transactions'][transaction][col]}`;
                }
                else {
                    newCol.innerHTML=response['transactions'][transaction][col];
                    if (newCol.innerHTML === '+') {
                        newRow.classList.add('bg-success');
                    }
                    if (newCol.innerHTML === '-') {
                        newRow.classList.add('bg-danger');
                    }
                }
                newRow.appendChild(newCol);
            }
            document.querySelector('#history-table > tbody').appendChild(newRow);
        }

        //Filters

        //  Show all users in filters
        for (user in response['users']) {
            const newOption = document.createElement('option');
            newOption.value = response['users'][user];
            newOption.innerHTML = response['users'][user];

            document.querySelector('select[data-history-filter-type=filterByUser]').appendChild(newOption);
        }

        //  Show all categories in filters
        for (category in response['categories']) {
            const newOption = document.createElement('option');
            newOption.value = response['categories'][category];
            newOption.innerHTML = response['categories'][category];

            document.querySelector('select[data-history-filter-type=filterByCategory]').appendChild(newOption);
        }
    }
    request.send();
})

historyFilters.forEach(element => {
    element.addEventListener('change', () => {
        const functionName = element.getAttribute('data-history-filter-type');
        historyFilters.forEach(element => {
            if (element.getAttribute('data-history-filter-type') !== functionName) {
                element.value = '';
                element.checked = false;
            }
        })
        this[functionName](element);
    })
})

function turnOffAllFilters() {

    document.querySelector('h3 > span').innerHTML = '';
    
    historyFilters.forEach(element => {element.value='';});

    for (let row = 1; row < historyTable.rows.length; row++) {
        historyTable.rows[row].style.display = 'table-row';
    }
}

function filterByType(element) {
    for (let row = 1; row < historyTable.rows.length; row++) {
        if (element.value === '') {
            historyTable.rows[row].style.display = 'table-row';
        }
        else {
            if (historyTable.rows[row].cells[0].innerHTML === element.value) {
                historyTable.rows[row].style.display = 'table-row';
            }
            else {
                historyTable.rows[row].style.display = 'none';
            }
        }
    }

    if (element.value) {
        document.querySelector('h3 > span').innerHTML = `(${element.value[0].toUpperCase()+element.value.slice(1)})`;
    }
    else {
        document.querySelector('h3 > span').innerHTML = '';
    }
}

function filterByUser(element) {

    for (let row = 1; row < historyTable.rows.length; row++) {
        if (element.value === '') {
            historyTable.rows[row].style.display = 'table-row';
        }
        else {
            if (historyTable.rows[row].cells[2].innerHTML === element.value) {
                historyTable.rows[row].style.display = 'table-row';
            }
            else {
                historyTable.rows[row].style.display = 'none';
            }
        }
    }

    if (element.value) {
        document.querySelector('h3 > span').innerHTML = `By ${element.value[0].toUpperCase()+element.value.slice(1)}`;
    }
    else {
        document.querySelector('h3 > span').innerHTML = '';
    }
}

function filterByCategory(element) {

    for (let row = 1; row < historyTable.rows.length; row++) {
        if (element.value === '') {
            historyTable.rows[row].style.display = 'table-row';
        }
        else {
            if (historyTable.rows[row].cells[1].innerHTML === element.value) {
                historyTable.rows[row].style.display = 'table-row';
            }
            else {
                historyTable.rows[row].style.display = 'none';
            }
        }
    }

    if (element.value) {
        document.querySelector('h3 > span').innerHTML = `In ${element.value[0].toUpperCase()+element.value.slice(1)}`;
    }
    else {
        document.querySelector('h3 > span').innerHTML = '';
    }
}

function filterByDate(element) {
    const filterDate = new Date (element.value);
    const filterDateFormatted = (filterDate.getUTCFullYear()) + '/' + (filterDate.getMonth() + 1)+ '/' + (filterDate.getUTCDate());
    for (let row = 1; row < historyTable.rows.length; row++) {
        if (element.value === '') {
            historyTable.rows[row].style.display = 'table-row';
        }
        else {
            const rowDate = new Date(historyTable.rows[row].cells[4].innerHTML.slice(0, 11));
            const rowDateFormatted = (rowDate.getUTCFullYear()) + '/' + (rowDate.getMonth() + 1)+ '/' + (rowDate.getUTCDate());
            if (filterDateFormatted === rowDateFormatted) {
                historyTable.rows[row].style.display = 'table-row';
            }
            else {
                historyTable.rows[row].style.display = 'none';
            }
        }
    }

    document.querySelector('h3 > span').innerHTML = `On ${filterDateFormatted}`;
}