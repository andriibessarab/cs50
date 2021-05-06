//Buttons

const registerButton = document.querySelector('#register');
const logInButton = document.querySelector('#logIn')

const logIn = `
    <form onsubmit="LogIn(); return false;">

        <input type="text" placeholder="Username" data-logIn-data-type="username" class="logInInput form-control mx-auto my-2">

        <input type="password" placeholder="Password" data-logIn-data-type="password" class="logInInput form-control mx-auto my-2">

        <div class="text-center">

            <button type="submit" class="btn btn-outline-warning text-center">Log In</button>

        </div>

        <div class="text-center">

            <small class="text-muted" data-error-for-logIn></small>

        </div>

    </form>
`;

//Events

logInButton.addEventListener('click', () => {
    openModal('Log In', logIn);
});

registerButton.addEventListener('click', () => {
    openModal('Register', registration);
});

//Functions

function LogIn() {
    request.open('POST', '/logIn');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = () => {
        const response = JSON.parse(request.responseText);
        if (response['status']) {
            location.reload();
        }
        else {
            document.querySelector('[data-error-for-logIn]').innerHTML = response['error'];
        }
    }
    const allLogInFields = document.querySelectorAll('.logInInput');
    const collectedData = {};
    allLogInFields.forEach(field => {
        collectedData[field.getAttribute('data-logIn-data-type')] = String(field.value);
    })
    const data = new FormData();
    data.append('user', JSON.stringify(collectedData));
    request.send(data);
}