// Admin panel section

// Setings
// Favicon
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      $('#favicon_img').attr('src', e.target.result);
    }

    reader.readAsDataURL(input.files[0]); // convert to base64 string
  }
}

$("#favicon_input").change(function() {
  readURL(this);
});

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
