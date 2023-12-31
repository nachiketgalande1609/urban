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
            window.location.href = "/"
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
            window.location.href = "/"
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
        var size = $('#sizeSelect').val();
        $.ajax({
            url: '/user/get_user_id',
            method: 'GET',
            success: function (response) {
                var user_id = response.user_id;
                $.ajax({
                    url: '../cart/add_to_cart',
                    method: 'POST',
                    data: {
                        product_id: product_id,
                        user_id: user_id,
                        size: size
                    },
                    success: function (response) {
                        $('.modal-background').addClass('show');
                        $('.modal-content').text('Item added to Cart');
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

// Add to cart
$(document).ready(function () {
    $('.add-to-wishlist-btn').on('click', function () {
        var product_id = $(this).data('product-id');
        var size = $('#sizeSelect').val();
        $.ajax({
            url: '/user/get_user_id',
            method: 'GET',
            success: function (response) {
                var user_id = response.user_id;
                $.ajax({
                    url: '/wishlist/add_to_wishlist',
                    method: 'POST',
                    data: {
                        product_id: product_id,
                        user_id: user_id,
                    },
                    success: function (response) {
                        $('.modal-background').addClass('show');
                        $('.modal-content').text('Item added to Wishlist');
                        $('.modal-content').fadeIn(); // Show the alert content
                        setTimeout(function () {
                            $('.modal-background').removeClass('show');
                            $('.modal-content').fadeOut('slow'); // Hide the alert content
                        }, 1000);
                        console.log('Successfully inserted item to wishlist');
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
    $.ajax({
        url: '../cart/remove_from_cart/' + itemId,
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

// remove item from wishlist
function removeFromWishlist(itemId) {
    $.ajax({
        url: '/wishlist/remove_from_wishlist/' + itemId,
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

// Navbar dropdown open on hover
$(document).ready(function () {
    function handleDropdownHover(dropdownClass) {
        $(dropdownClass).hover(function () {
            $(this).find('.dropdown-menu').stop(true, true).fadeIn(0);
        }, function () {
            $(this).find('.dropdown-menu').stop(true, true).fadeOut(0);
        });
        $(dropdownClass + ' .dropdown-menu').click(function (e) {
            e.stopPropagation();
        });
    }

    handleDropdownHover('.women-dropdown');
    handleDropdownHover('.men-dropdown');
    handleDropdownHover('.hamburg-dropdown');
});

// Show success notification on clicking Pay button
$(document).ready(function () {
    $('#payButton').on('click', function () {

        $('.modal-background').addClass('show');
        $('.modal-content').fadeIn(); // Show the alert content
        setTimeout(function () {
            $('.modal-background').removeClass('show');
            $('.modal-content').fadeOut('slow'); // Hide the alert content
        }, 2000);
    });
});

// Search function
$("form[name=search-form]").submit(function (e) {
    e.preventDefault(); // Prevent the default form submission
    var searchQuery = $(this).find('input[name=search_query]').val(); // Get the search query from the form input
    window.location.href = `/home?search=${searchQuery}`;
});

// Spinner animation
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        document.body.classList.add("loaded");
    }, 500); // 2 seconds delay before adding the 'loaded' class
});

// Toggle filter + -
$('.filter-heading').on('click', function () {
    $(this).find('.bi').toggleClass('bi-plus bi-dash');
});

// Sidebar filtering
$(document).ready(function(){
    const urlParams = new URLSearchParams(window.location.search);
    $('input[type=checkbox]').each(function(){
        const paramName = $(this).attr('name');
        if(urlParams.has(paramName) && urlParams.getAll(paramName).includes($(this).val())){
            $(this).prop('checked', true);
        }
    });
    
    $('form[name="filter-form"]').on('change', function(){
        $('#filter-form').submit(); // Submit the form when checkboxes change
    });
});

function showAddAddressPopup() {
    $('#addAddressModal').modal('show');
}