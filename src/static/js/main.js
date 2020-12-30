// # Common

// Paste image file from input
function pasteImageFromInput(input, id) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(id).attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]); // convert to base64 string
    }
}

// ##########################################################################

// # Admin panel section

// ## Settings

// Favicon icon
$("#favicon_input").change(function () {
    pasteImageFromInput(this, "#favicon_img");
});

// Main image
$("#main_image_input").change(function () {
    pasteImageFromInput(this, "#main_image");
});
// ##########################################################################

// ## Users
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

// ##########################################################################

// ## Products

// Product image
$("#product_image_input").change(function () {
    pasteImageFromInput(this, "#product_image");
});


// Delete product
let deletedProductId;

function deleteProduct(productId) {
    deletedProductId = productId;
    let modal = new bootstrap.Modal(document.getElementById('deleteProductModal'), {keyboard: true});
    modal.show();
}

function confirmProductDeletion() {
    axios
        .delete('/admin/products', {
            data: {
                productId: deletedProductId
            }
        })
        .then(function () {
            window.location.reload(true);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function editProduct(productId) {
    window.location.href = "/admin/products/edit?productId=" + productId;
}

// ##########################################################################

// # Product
let piecesInput = document.querySelector("#piecesInput")

function leftBtnAction() {
    let pieces = parseInt(piecesInput.value);
    if (pieces > 0) {
        piecesInput.value = --pieces;
    }
}

function rightBtnAction() {
    let pieces = parseInt(piecesInput.value);
    piecesInput.value = ++pieces;
}

function buyBtnAction(product_id) {
    let pieces = parseInt(piecesInput.value);
    let price = parseInt(document.querySelector(".price span").textContent)
    let total = price * pieces;

    if (pieces > 0) {
        addProductToCart(product_id, pieces)

        let modal = new bootstrap.Modal(document.getElementById('buyModal'), {keyboard: true});
        document.getElementById('modal_pieces').innerText = pieces
        document.getElementById('modal_total').innerText = total

        modal.show();
    }

    piecesInput.value = 0
}

function addProductToCart(product_id, pieces) {
    axios
        .post('/cart', {
            product_id: product_id,
            pieces: pieces
        })
        .then(function () {
            updateCartCountIndicator(pieces)
        })
        .catch(function (error) {
            console.log(error);
        });
}

function deleteItemFromCart(item_id) {
    axios
        .delete('/cart', {
            data: {
                item_id: item_id
            }
        })
        .then(function () {
            window.location.reload(true);
        })
        .catch(function (error) {
            console.log(error);
        });
}

function updateCartCountIndicator(count) {
    let current_count = parseInt(document.getElementById('cart_count_indicator').innerText)
    document.getElementById('cart_count_indicator').innerText = current_count + count
}
