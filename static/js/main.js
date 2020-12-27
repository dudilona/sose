// Admin panel section

// Users
let deletedUserId;

function deleteUser(userId) {
    deletedUserId = userId;
    let modal = new bootstrap.Modal(document.getElementById('deleteUserModal'), {keyboard: true});
    modal.show();
}

function confirmUserDeletion() {
    axios
        .delete('/admin/users', {
            data: {
                userId: deletedUserId
            }
        })
        .then(function () {
            window.location.reload(true);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function editUser(userId) {
    window.location.href = "/admin/users/edit?userId=" + userId;
}