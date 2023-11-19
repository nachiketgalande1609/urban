// Send form data using a POST request for signup
$("form[name=signup_form]").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "../user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/account/"
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault()
})

// Send form data using a POST request for login
$("form[name=login_form]").submit(function (e) {

    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "../user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function (resp) {
            window.location.href = "/account/"
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })

    e.preventDefault()
})

// Send form data using a POST request to add product to DB
$("form[name=add_product_form]").submit(function (e) {
    e.preventDefault();

    var $form = $(this);
    var $error = $form.find(".error");
    var formData = new FormData(this);

    $.ajax({
        url: "../product/addproduct",
        type: "POST",
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,
        success: function (resp) {
            window.location.href = "/"
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
});

// Add to cart
$(document).ready(function () {
    $('.add-to-cart-btn').on('click', function () {
        var product_id = $(this).data('product-id');
        $.ajax({
            url: '/user/get_user_id',
            method: 'GET',
            success: function (response) {
                var user_id = response.user_id;
                console.log(product_id);
                console.log(user_id);

                $.ajax({
                    url: '../user/add_to_cart',
                    method: 'POST',
                    data: {
                        product_id: product_id,
                        user_id: user_id
                    },
                    success: function (response) {
                        $('.modal-background').addClass('show');
                        $('.modal-content').fadeIn(); // Show the alert content
                        setTimeout(function () {
                            $('.modal-background').removeClass('show');
                            $('.modal-content').fadeOut('slow'); // Hide the alert content
                        }, 1000);
                        console.log('Successfully inserted item in cart');
                    },
                    error: function (error) {
                        console.log('Error in product insertion');
                    }
                });
            },
            error: function (error) {
                // Handle error response here
            }
        });
    });
});

// remove item from cart
function removeFromCart(itemId) {
    console.log(itemId);
    $.ajax({
        url: '../user/remove_from_cart/' + itemId,
        method: 'POST',
        success: function (response) {
            console.log('Success');
            location.reload(); // Reload the page after successful removal
        },
        error: function (error) {
            console.log('Error');
        }
    });
}

// Render gender specific categories on AddProduct page
document.addEventListener('DOMContentLoaded', function () {
    const category = document.getElementById('category');
    const gender = document.getElementById('gender');
    const categoryOptions = Array.from(category.options);

    gender.addEventListener('change', function () {
        const selectedGender = document.getElementById('gender').value;

        categoryOptions.forEach(option => {
            const genderAttribute = option.getAttribute('data-gender');
            if (genderAttribute === selectedGender || genderAttribute === null) {
                option.style.display = 'block';
            } else {
                option.style.display = 'none';
            }
        });
    });
});

// Send form data using a POST request for password change
$("form[name=change_password]").submit(function (e) {
    e.preventDefault();
    var $form = $(this);
    var $error = $form.find(".error");

    var currentPassword = $form.find('input[name=currentPassword]').val();
    var newPassword = $form.find('input[name=newPassword]').val();

    // Create an object with the form data
    var formData = {
        currentPassword: currentPassword,
        newPassword: newPassword
    };

    $.ajax({
        url: "../user/change_password", // Update the URL to match your backend route for password change
        type: "POST",
        data: formData,
        dataType: "json",
        success: function (resp) {
            console.log('Password changed successfully');
            $error.addClass("error--hidden");
            $('.modal-background').addClass('show');
                        $('.modal-content').fadeIn(); // Show the alert content
                        setTimeout(function () {
                            $('.modal-background').removeClass('show');
                            $('.modal-content').fadeOut('slow'); // Hide the alert content
                        }, 1000);
        },
        error: function (resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
});