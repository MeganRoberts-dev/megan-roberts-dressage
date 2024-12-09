var stripe = Stripe('{{ stripe_public_key }}');
var elements = stripe.elements();
var card = elements.create('card');
card.mount('#card-element');

// Handle form submission
var form = document.querySelector('form');
form.addEventListener('submit', function(event) {
  event.preventDefault();

  stripe.confirmCardPayment('{{ client_secret }}', {
    payment_method: {
      card: card,
      billing_details: {
        name: '{{ order_form.name.value }}',
      },
    },
  }).then(function(result) {
    if (result.error) {
      // Show error to the customer (e.g., insufficient funds)
      document.getElementById('card-errors').textContent = result.error.message;
    } else {
      if (result.paymentIntent.status === 'succeeded') {
        // Payment succeeded
        window.location.href = '{% url "success" %}';
      }
    }
  });
});

