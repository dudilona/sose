// Admin panel section

// Users
let deletedUserId;

function deleteUser(userId) {
    deletedUserId = userId;
    let modal = new bootstrap.Modal(document.getElementById('deleteUserModal'), {keyboard: true});
    modal.show()
}

function confirmUserDeletion() {
    axios
        .delete('/admin/users', {
            data: {
                userId: deletedUserId
            }
        })
        .then(function (response) {
            window.location.reload(true);
        })
        .catch(function (error) {
            console.log(error);
        });
}