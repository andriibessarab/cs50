//Unversal

const request = new XMLHttpRequest();
const csrf_token = document.querySelector('[name=csrf_token]').value;

//Modal

const modalTitle = document.querySelector('#modal-title');
const modalBody = document.querySelector('#modal-body');

//Colors

const red = 'rgb(252, 81, 81)';
const green = 'rgb(50, 168, 82)';
const blue = 'rgb(0, 208, 227)';

//Registration

const registration = `
    <form onsubmit="Register(); return false;">

        <div class="form-group">
            <input type="text" placeholder="Username" maxlength="15" class="registrationInput form-control" data-registration-data-type="username" aria-describedby="usernameError">
            <small id="usernameError" class="error-message text-muted" data-error-for-username>
            </small>
        </div>

        <div class="form-group">
            <input type="text" placeholder="Email" maxlength="320" class="registrationInput form-control" data-registration-data-type="email" aria-describedby="emailError">
            <small id="emailError" class="error-message text-muted" data-error-for-email>
            </small>
        </div>

        <div class="form-group">
            <input type="password" placeholder="Password" class="registrationInput form-control" data-registration-data-type="password" aria-describedby="passwordError">
            <small id="passwordError" class="error-message text-muted" data-error-for-password>
            </small>
        </div>

        <div class="form-group">
            <input type="text" placeholder="First Name" class="registrationInput form-control" data-registration-data-type="fname" aria-describedby="fnameError">
            <small id="fnameError" class="error-message text-muted" data-error-for-fname>
            </small>
        </div>

        <div class="form-group">
            <input type="text" placeholder="Last Name" class="registrationInput form-control" data-registration-data-type="lname" aria-describedby="lnameError">
            <small id="lnameError" class="error-message text-muted" data-error-for-lname>
            </small>
        </div>

        <div class="text-center">

            <button type="submit" class="btn btn-outline-warning text-center">Register</button>

        </div>

    </form>
`;