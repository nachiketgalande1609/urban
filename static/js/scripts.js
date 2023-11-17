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