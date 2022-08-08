var stripe = Stripe('pk_test_51IV54zHy0YGrYC9hk45niKje0cKS5fpCLzQiF5wOE1ii2Sus7JLZCzt6OqkACdDRuFdbCSFBYOPH6fK1xWc0BhBc00lXpVGFS0');

var button = document.querySelector('#pay_bttn');
var button2 = document.querySelector('bttn');

var adultQuantity = document.getElementById("adultQuantity").value;
var childQuantity = document.getElementById("childQuantity").value;
var seniorQuantity = document.getElementById("seniorQuantity").value;

document.getElementById('cardNum').addEventListener('input', function (e) {
    e.target.value = e.target.value.replace(/[^\dA-Z]/g, '').replace(/(.{4})/g, '$1 ').trim();
  });