var stripePublicKey = $('#id_stripe_public_key').text().slice(1,-1);
var clientSecret = $('#id_client_secret').text().slice(1,-1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var card = elements.create('card');
card.mount('#card-element');

// Handle form submission
var form = document.getElementById('checkout-form');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  $('#submit-button').attr('disabled', true);
  var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
  var postData = {
    'csrfmiddlewaretoken': csrfToken,
    'client_secret': clientSecret,
  };
  var url = '/checkout/cache_checkout_data/';
  $.post(url, postData).done(function () {
    stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
        billing_details: {
          name: $.trim(form.full_name.value),
        },
      },
    }).then(function(result) {
      if (result.error) {
        // Show error to the customer (e.g., insufficient funds)
        document.getElementById('card-errors').textContent = result.error.message;
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          // Payment succeeded
         // window.location.href = '{% url "success" %}';
         form.submit();

        }
      }
    });
  }).fail(function () {
    location.reload();
  });
});

