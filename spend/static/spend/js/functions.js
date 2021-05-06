function Register() {
    request.open('POST', '/register');
    request.setRequestHeader('X-CSRFToken', csrf_token); 
    request.onload = () => {
        const response = JSON.parse(request.responseText);
        if (response['status']) {
            location.reload();
        }
        else {
            for (i in response['errors']) {
                if (response['errors'][i] !== true) {
                    document.querySelector(`[data-error-for-${i}`).innerHTML = response['errors'][i];
                }
                else {
                    document.querySelector(`[data-error-for-${i}`).innerHTML = '';
                }
            }
        }
    }
    const allRegistrationFields = document.querySelectorAll('.registrationInput');
    const collectedData = {};
    allRegistrationFields.forEach(field => {
        collectedData[field.getAttribute('data-registration-data-type')] = String(field.value);
    })
    const data = new FormData();
    data.append('user', JSON.stringify(collectedData));
    request.send(data);
}

function openModal(title, body) {
    modalTitle.innerHTML = title;
    modalBody.innerHTML = body;
}