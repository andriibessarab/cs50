//Variables

const addFamilyMemberButton = document.querySelector('#addFamilyMember');
const addNewCategoryButton = document.querySelector('#addNewCategory');

const addNewCategory = `
    <form id="createNewCategory" onsubmit="createNewCategory(); return false;">

        <div class="form-group">
            <input type="text" placeholder="Category's Name" maxlength="30" class="form-control" aria-describedby="categoryNameError">
            <small id="categoryNameError" class="text-muted">
            </small>
        </div>

        <div class="text-center">

            <button type="submit" class="btn btn-outline-warning text-center">Register</button>

        </div>

    </form>
`;

//Events

addFamilyMemberButton.addEventListener('click', () => { openModal('Add Family Member', registration, red) });


addNewCategoryButton.addEventListener('click', () => {
    openModal('Create Category', addNewCategory);
});

//Functions

function createNewCategory() {
    request.open('POST', '/createNewCategory');
    request.setRequestHeader('X-CSRFToken', csrf_token);
    request.onload = () => {
        const response = JSON.parse(request.responseText);
        if (response['status']) {
            location.reload();
        }
        else {
            document.querySelector('#categoryNameError').innerHTML = response['error'];
        }
    }
    let data = new FormData()
    data.append('name', document.querySelector('#createNewCategory input').value);
    request.send(data);
}