function sendData() {
    var items = {};
    items.product = document.querySelector('.product').value;
    items.color = document.querySelector('.color').value;
    items.size = document.querySelector('.size').value;
    items.category = document.querySelector('.category').value;
    items.name = document.querySelector('.name').value;
    items.email = document.querySelector('.email').value;
    items.phone = document.querySelector('.phone').value;
    items.address = document.querySelector('.address').value;
    items.city = document.querySelector('.city').value;
    items.state = document.querySelector('.state').value;
    items.zip = document.querySelector('.zip').value;
    items.credit_card_number = document.querySelector('.credit_card_number').value;
    items.cc_month = document.querySelector('.cc_month').value;
    items.cc_year = document.querySelector('.cc_year').value;
    items.cvv = document.querySelector('.cvv').value;
    var server = "http://127.0.0.1:5000"; 
    var appdir='/sum';
    alert("The Bot has processed your request and is inputting your information now. Thanks for using QuickCop!")
    $.ajax({
        type: "POST",
        url: server+appdir,
        data: JSON.stringify(items),
        dataType: 'json'
    }).done(function() {
        console.log("DONE");
    });
}

// var sub = document.querySelector('.submit');
// sub.onclick = sendData;

document.querySelector(".submit").addEventListener('click', sendData);


