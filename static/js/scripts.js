// Send form data using a POST request for signup
$("form[name=signup_form]").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "../user/signup",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/account/"
        },
        error: function(resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    
    e.preventDefault()
})

// Send form data using a POST request for login
$("form[name=login_form]").submit(function(e) {
    
    var $form = $(this);
    var $error = $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url: "../user/login",
        type: "POST",
        data: data,
        dataType: "json",
        success: function(resp) {
            window.location.href = "/account/"
        },
        error: function(resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    })
    
    e.preventDefault()
})

// Send form data using a POST request to add product to DB
$("form[name=add_product_form]").submit(function(e) {
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
        success: function(resp) {
            window.location.href = "/"
        },
        error: function(resp) {
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
});

// Add to cart
$(document).ready(function() {
    $('.add-to-cart-btn').on('click', function() {
        var product_id = $(this).data('product-id');
        $.ajax({
            url: '/user/get_user_id',
            method: 'GET',
            success: function(response) {
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
                    success: function(response) {
                        console.log('Successfully inserted item in cart');
                    },
                    error: function(error) {
                        console.log('Error in product insertion');
                    }
                });
            },
            error: function(error) {
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
        success: function(response) {
            console.log('Success');
            location.reload(); // Reload the page after successful removal
        },
        error: function(error) {
            console.log('Error');
        }
    });
}