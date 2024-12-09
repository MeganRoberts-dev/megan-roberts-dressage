
    const stripe = Stripe('{{ stripe_public_key }}');
    const elements = stripe.elements();
    const card = elements.create('card');
    card.mount('#card-element');

    const form = document.getElementById('payment-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const { error, paymentMethod } = await stripe.createPaymentMethod({
            type: 'card',
            card: card,
        });

        if (error) {
            const errorsDiv = document.getElementById('card-errors');
            errorsDiv.textContent = error.message;
        } else {
            form.submit();
        }
    });
