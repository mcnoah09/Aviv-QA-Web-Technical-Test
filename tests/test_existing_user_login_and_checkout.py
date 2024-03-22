from typing import Tuple

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from tests.helpers.utils import (
    add_book_to_cart,
    checkout_from_cart,
    confirm_order,
    enter_billing_address,
    login_user,
    select_payment_method,
    select_shipping_method,
)


def test_existing_user_login_and_checkout(
    driver: webdriver, wait: WebDriverWait, fake: Faker, auth: Tuple[str, str]
):
    """
    Test existing user login and checkout

    :param driver: WebDriver instance
    :param wait: WebDriverWait instance
    :param fake: Faker instance
    :param auth: Tuple of email and password of an existing user

    :return: None
    """
    email, password = auth

    # 2. Login with the registered user
    login_user(driver=driver, wait=wait, email=email, password=password)

    # 3. Add a product to the shopping cart
    add_book_to_cart(driver=driver, wait=wait)

    # 4. Checkout
    checkout_from_cart(driver=driver, wait=wait)

    # 5. Enter billing address
    enter_billing_address(
        driver=driver,
        wait=wait,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=email,
        company=fake.company(),
        country="Angola",
        city=fake.city(),
        address1=fake.street_address(),
        zip_code=fake.postcode(),
        phone_number=fake.phone_number(),
        ship_to_same_address=True,
    )

    # 6. Select shipping method
    select_shipping_method(
        driver=driver,
        wait=wait,
        shipping_method="Next Day",
    )

    # 8. Select payment method
    select_payment_method(
        driver=driver,
        wait=wait,
        payment_method="cash",
    )

    # 9. Confirm order
    confirm_order(driver=driver, wait=wait), "Order was not confirmed successfully!"
