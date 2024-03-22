from random import choice

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from structlog import get_logger

from tests.helpers.utils import (
    add_book_to_cart,
    checkout_from_cart,
    confirm_order,
    enter_billing_address,
    enter_shipping_address,
    login_user,
    register_user,
    select_payment_method,
    select_shipping_method,
)

LOGGER = get_logger(module=__name__)


def test_user_signup_and_checkout(driver: webdriver, wait: WebDriverWait, fake: Faker):
    """
    Test user signup and checkout

    :param driver: WebDriver instance
    :param wait: WebDriverWait instance
    :param fake: Faker instance

    :return: None
    """
    # Define the homepage url
    homepage_url = "https://demo.nopcommerce.com/"

    # Generate random email and password
    email = fake.email()
    password = fake.password()

    # 1. Register a new user
    register_user(
        driver=driver,
        wait=wait,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=email,
        password=password,
        confirm_password=password,
        gender=choice(["Male", "Female"]),
        date_of_birth=fake.date_of_birth(),
        company_name=fake.company(),
        subscribe_newsletter=True,
    )

    # Validate that the user is redirected to the home page upon successful registration
    # Note: After successful registration, the user is not signed in automatically
    assert (
        driver.current_url == homepage_url
    ), f"User is not redirected to the home page! Current URL: {driver.current_url}"

    # 2. Validate the user is successfully registered by logging in
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
    )

    # 6. Enter shipping address
    enter_shipping_address(
        driver=driver,
        wait=wait,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=email,
        company=fake.company(),
        country="Armenia",
        city=fake.city(),
        address1=fake.street_address(),
        zip_code=fake.postcode(),
        phone_number=fake.phone_number(),
    )

    # 7. Select shipping method
    select_shipping_method(
        driver=driver,
        wait=wait,
        shipping_method="Next Day",
    )

    # 8. Select payment method
    select_payment_method(
        driver=driver,
        wait=wait,
        payment_method="Cheque",
    )

    # 9. Confirm order
    confirm_order(driver=driver, wait=wait), "Order was not confirmed successfully!"

    # Validate that the user is redirected to the home page upon successful order confirmation
    assert (
        driver.current_url == homepage_url
    ), f"User is not redirected to the home page! Current URL: {driver.current_url}"
