import stripe
from rest_framework.reverse import reverse


def get_checkout_session(request, course):
    stripe_price = get_price(course)

    price_id = stripe_price.get('id')

    checkout_session = stripe.checkout.Session.create(
        success_url=request.build_absolute_uri(reverse('education:course-list')),
        line_items=[
            {
                'price': price_id,
                'quantity': 1
            },
        ],
        mode='payment'
    )

    return checkout_session


def get_price(course):
    stripe_price = stripe.Price.create(
        unit_amount=course.price * 100,
        currency='rub',
        product=course.product_id
    )

    return stripe_price
