from datetime import date
from random import randint
from typing import List, Optional

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from structlog import get_logger

from tests.pages.cart import ShoppingCartPage
from tests.pages.checkout import (
    BillingAddress,
    ConfirmOrder,
    PaymentMethod,
    ShippingAddress,
    ShippingMethod,
)
from tests.pages.login import LoginPage
from tests.pages.products import (
    BooksProductCategoryPage,
    CellPhonesProductCategoryPage,
    DigitalDownloadsProductCategoryPage,
)
from tests.pages.register import RegisterPage

LOGGER = get_logger(module=__name__)


def register_user(
    driver: webdriver,
    wait: WebDriverWait,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    confirm_password: str,
    gender: Optional[str] = None,
    date_of_birth: Optional[date] = None,
    company_name: Optional[str] = None,
    subscribe_newsletter: Optional[bool] = False,
):
    """
    Register a new user with the provided details.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address.
        password (str): User's password.
        confirm_password (str): Confirm the user's password.
        gender (Optional[str], optional): User's gender. Default is None.
        date_of_birth (Optional[date], optional): User's date of birth. Default is None.
        company_name (Optional[str], optional): User's company name. Default is None.
        subscribe_newsletter (Optional[bool], optional): Subscribe to newsletter. Default is False.

    Raises:
        AssertionError: If the user registration fails or redirection is not successful.
    """
    LOGGER.info("Register a new user")

    LOGGER.info("Navigate to the registration page")
    register_page = RegisterPage(driver, wait)
    register_page.click_register_page()
    LOGGER.info(
        f"Successfully navigated to the user registration page - {driver.current_url}"
    )

    LOGGER.info("Fill in the user registration form")
    register_page.enter_first_name(first_name)
    register_page.enter_last_name(last_name)
    register_page.enter_email(email)
    register_page.enter_password(password)
    register_page.enter_confirm_password(confirm_password)
    if gender:
        register_page.select_gender(gender)
    if date_of_birth:
        register_page.enter_date_of_birth(date_of_birth)
    if company_name:
        register_page.enter_company_name(company_name)
    if subscribe_newsletter:
        register_page.click_newsletter()

    LOGGER.info("Filled in the user registration form")

    LOGGER.info("Click the Register button")
    register_page.click_register()

    try:
        wait.until(
            EC.text_to_be_present_in_element(
                register_page.registration_success_message,
                "Your registration completed",
            )
        )

        # Validate that the user is redirected to the home page upon successful registration
        assert driver.current_url.startswith(register_page.url), (
            "User is not redirected to the registration page! Current URL:"
            f" {driver.current_url}"
        )

        LOGGER.info(f"New user with email: {email} registered successfully!")
        register_page.click_continue()
    except TimeoutException:
        LOGGER.error("User registration failed!")


def login_user(
    driver: webdriver,
    wait: WebDriverWait,
    email: str,
    password: str,
    remember_me: Optional[bool] = False,
):
    """
    Log in a user with the provided credentials.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        email (str): User's email address.
        password (str): User's password.
        remember_me (Optional[bool], optional): Remember the user. Default is False.

    Raises:
        AssertionError: If the user login fails.
    """
    LOGGER.info(f"Perform user login with email {email}")
    login_page = LoginPage(driver, wait)

    LOGGER.info(f"Navigate to the login page - {login_page.url}")
    login_page.open()

    LOGGER.info("Successfully navigated to the login page!")

    LOGGER.info("Fill in the email and password")
    login_page.enter_email(email)
    login_page.enter_password(password)
    if remember_me:
        login_page.click_remember_me()

    LOGGER.info("Click the Login button")
    login_page.click_login()

    # Wait for the logout button to be visible, indicating a successful login
    assert wait.until(
        EC.visibility_of_element_located(login_page.logout_button)
    ).is_displayed(), "User failed to login!"

    LOGGER.info("User logged in successfully!")


def enter_billing_address(
    driver: webdriver,
    wait: WebDriverWait,
    first_name: str,
    last_name: str,
    email: str,
    country: str,
    city: str,
    address1: str,
    zip_code: str,
    phone_number: str,
    company: Optional[str] = None,
    state: Optional[str] = None,
    address2: Optional[str] = None,
    fax_number: Optional[str] = None,
    ship_to_same_address: Optional[bool] = False,
):
    """
    Enter billing address details in a form.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address.
        country (str): User's country.
        city (str): User's city.
        address1 (str): User's address line 1.
        zip_code (str): User's ZIP or postal code.
        phone_number (str): User's phone number.
        company (Optional[str], optional): User's company name. Default is None.
        state (Optional[str], optional): User's state. Default is None.
        address2 (Optional[str], optional): User's address line 2. Default is None.
        fax_number (Optional[str], optional): User's fax number. Default is None.
        ship_to_same_address (Optional[bool], optional): Ship to the same address. Default is False.

    Raises:
        TimeoutException: If the continue button is still clickable after the form submission.
    """
    LOGGER.info("Enter billing address")
    billing_address = BillingAddress(driver, wait)

    # Choose whether to ship to the same address
    if ship_to_same_address:
        billing_address.click_ship_to_same_address()
    else:
        billing_address.uncheck_ship_to_same_address()

    # Fill in the billing address details
    billing_address.enter_first_name(first_name)
    billing_address.enter_last_name(last_name)
    billing_address.enter_email(email)
    billing_address.select_country(country)
    billing_address.enter_city(city)
    billing_address.enter_address1(address1)
    billing_address.enter_zip_postal_code(zip_code)
    billing_address.enter_phone_number(phone_number)

    # Fill in optional details
    if company:
        billing_address.enter_company(company)
    if state:
        billing_address.select_state(state)
    if address2:
        billing_address.enter_address2(address2)
    if fax_number:
        billing_address.enter_fax_number(fax_number)

    # Click Continue button and wait for it to become unclickable
    billing_address.click_continue()
    wait.until_not(EC.element_to_be_clickable(billing_address.continue_button))

    LOGGER.info("Billing address entered successfully")


def enter_shipping_address(
    driver: webdriver,
    wait: WebDriverWait,
    first_name: str,
    last_name: str,
    email: str,
    country: str,
    city: str,
    address1: str,
    zip_code: str,
    phone_number: str,
    add_new_address: bool = True,
    company: Optional[str] = None,
    state: Optional[str] = None,
    address2: Optional[str] = None,
    fax_number: Optional[str] = None,
):
    """
    Enter shipping address details in a form.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        first_name (str): User's first name.
        last_name (str): User's last name.
        email (str): User's email address.
        country (str): User's country.
        city (str): User's city.
        address1 (str): User's address line 1.
        zip_code (str): User's ZIP or postal code.
        phone_number (str): User's phone number.
        add_new_address (bool, optional): Add a new shipping address. Default is True.
        company (Optional[str], optional): User's company name. Default is None.
        state (Optional[str], optional): User's state. Default is None.
        address2 (Optional[str], optional): User's address line 2. Default is None.
        fax_number (Optional[str], optional): User's fax number. Default is None.

    Raises:
        TimeoutException: If the continue button is still clickable after the form submission.
    """

    LOGGER.info("Enter shipping address")
    shipping_address = ShippingAddress(driver, wait)

    if add_new_address:
        # Select to add a new shipping address
        shipping_address.select_new_shipping_address()
        shipping_address.enter_first_name(first_name)
        shipping_address.enter_last_name(last_name)
        shipping_address.enter_email(email)
        shipping_address.select_country(country)
        shipping_address.enter_city(city)
        shipping_address.enter_address1(address1)
        shipping_address.enter_zip_postal_code(zip_code)
        shipping_address.enter_phone_number(phone_number)

        # Fill in optional details for a new shipping address
        if company:
            shipping_address.enter_company(company)
        if state:
            shipping_address.select_state(state)
        if address2:
            shipping_address.enter_address2(address2)
        if fax_number:
            shipping_address.enter_fax_number(fax_number)
    else:
        # Select an existing billing address
        shipping_address.select_billing_address()

    # Click Continue button and wait for it to become unclickable
    shipping_address.click_continue()
    wait.until_not(EC.element_to_be_clickable(shipping_address.continue_button))

    LOGGER.info("Shipping address entered successfully")


def select_shipping_method(
    driver: webdriver,
    wait: WebDriverWait,
    shipping_method: str,
):
    """
    Select a shipping method on the shipping method page.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        shipping_method (str): The desired shipping method.

    Raises:
        ValueError: If an unexpected value for shipping_method is provided.
        TimeoutException: If the continue button is still clickable after the form submission.
    """
    LOGGER.info("Select shipping method")
    shipping_method_page = ShippingMethod(driver, wait)

    # Map the shipping method to the corresponding method on the ShippingMethodPage
    method_mapping = {
        "next day": shipping_method_page.select_next_day_air_shipping_method,
        "2nd day": shipping_method_page.select_second_day_air_shipping_method,
        "ground": shipping_method_page.select_ground_shipping_method,
    }

    # Select the shipping method using the provided method name
    selected_method = method_mapping.get(shipping_method.lower())
    if selected_method:
        selected_method()
    else:
        raise ValueError(f"Unexpected value for shipping method: {shipping_method}")

    # Click Continue button and wait for it to become unclickable
    shipping_method_page.click_continue()
    wait.until_not(
        EC.element_to_be_clickable(shipping_method_page.shipping_method_continue_button)
    )

    LOGGER.info("Shipping method selected successfully")


def select_payment_method(
    driver: webdriver,
    wait: WebDriverWait,
    payment_method: str,
    card_type: Optional[str] = None,
    card_holder_name: Optional[str] = None,
    card_number: Optional[str] = None,
    expiration_month: Optional[str] = None,
    expiration_year: Optional[str] = None,
    card_code: Optional[str] = None,
):
    """
    Select a payment method on the payment method page.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        payment_method (str): The desired payment method.
        card_type (Optional[str], optional): Card type for credit card payment. Default is None.
        card_holder_name (Optional[str], optional): Cardholder's name for credit card payment. Default is None.
        card_number (Optional[str], optional): Card number for credit card payment. Default is None.
        expiration_month (Optional[str], optional): Expiration month for credit card payment. Default is None.
        expiration_year (Optional[str], optional): Expiration year for credit card payment. Default is None.
        card_code (Optional[str], optional): Card code for credit card payment. Default is None.

    Raises:
        ValueError: If an unexpected value for payment_method is provided.
        TimeoutException: If the continue button is still clickable after the form submission.
    """
    LOGGER.info("Select payment method")
    payment_method_page = PaymentMethod(driver, wait)

    if payment_method.lower() == "card":
        payment_method_page.select_credit_card_payment_method()
        payment_method_page.select_card_type(card_type)
        payment_method_page.enter_card_holder_name(card_holder_name)

        # Ensure card number is not less or greater than 18 digits
        card_number = card_number.ljust(18, "0")[:18]
        payment_method_page.enter_card_number(card_number)

        payment_method_page.select_card_expiry_month(expiration_month)
        payment_method_page.select_card_expiry_year(expiration_year)

        # Ensure card code is not less or greater or less than 3 digits
        card_code = card_code.ljust(3, "0")[:3]
        payment_method_page.enter_card_code(card_code)

        payment_method_page.click_continue()

    elif payment_method.lower() in ("cheque", "cash"):
        payment_method_page.select_cheque_or_cash_on_payment_method()
        payment_method_page.click_continue()
        payment_method_page.click_continue_for_cheque_or_cash()
    else:
        raise ValueError(f"Unexpected value for payment method: {payment_method}")

    # Wait for the continue button to become unclickable after the form submission
    wait.until_not(
        EC.element_to_be_clickable(payment_method_page.payment_method_continue_button)
    )

    LOGGER.info("Payment method selected successfully")


def confirm_order(driver: webdriver, wait: WebDriverWait):
    """
    Confirm the order on the confirmation order page.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.

    Raises:
        AssertionError: If the order confirmation fails or the success message is not as expected.
        TimeoutException: If the continue button is still clickable after the form submission.
    """
    LOGGER.info("Confirm order")
    confirm_order_page = ConfirmOrder(driver, wait)
    confirm_order_page.click_confirm_order()

    # Verify the order success message
    order_success_message = confirm_order_page.get_success_message_text()
    expected_success_message = "Your order has been successfully processed!"
    assert order_success_message == expected_success_message, (
        "Order failed to confirm! "
        f"Expected success message: {expected_success_message}, "
        f"Actual success message: {order_success_message}"
    )

    # Click continue button and wait for it to become unclickable
    confirm_order_page.click_order_completed_continue()
    wait.until_not(
        EC.element_to_be_clickable(confirm_order_page.order_completed_continue_button)
    )

    LOGGER.info("Order confirmed successfully")


def add_book_to_cart(
    driver: webdriver,
    wait: WebDriverWait,
    return_product_name: bool = False,
) -> Optional[str]:
    """
    Navigate to the book product category page, select a random product,
    add it to the shopping cart, and optionally return the product name.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        return_product_name (bool, optional): Whether to return the added product's name. Default is False.

    Returns:
        Optional[str]: The product name if return_product_name is True, else None.

    Raises:
        AssertionError: If the user is not redirected to the cell phone product category page,
        or if the product is not added to the shopping cart.
    """

    books_page = BooksProductCategoryPage(driver, wait)

    LOGGER.info(f"Navigate to the Books product category page - {books_page.url}")
    books_page.open()
    assert driver.current_url == books_page.url, (
        "User is not redirected to the Books product category page!"
        f" Current URL: {driver.current_url}"
    )

    LOGGER.info("Successfully navigated to the Books product category page")

    # Click on a random product and add to cart
    products_elm = wait.until(
        EC.visibility_of_all_elements_located(books_page.product_item_button)
    )
    product_index = randint(0, len(products_elm) - 1)
    products_elm[product_index].click()
    books_page.click_add_to_cart_button()

    # Verify the product is added to the shopping cart
    assert (
        books_page.product_added_to_cart_message
        in books_page.get_product_added_to_cart_message()
    ), "Product was not added to the shopping cart!"
    books_page.click_product_add_to_cart_message_close_button()

    # Get the product name
    product_name = books_page.get_product_name()

    LOGGER.info(
        f"Product titled '{product_name}' successfully added to the shopping cart"
    )

    if return_product_name:
        return product_name


def add_digital_download_item_to_cart(
    driver: webdriver,
    wait: WebDriverWait,
    return_product_name: bool = False,
) -> Optional[str]:
    """
    Navigate to the digital download product category page, select a random product,
    add it to the shopping cart, and optionally return the product name.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        return_product_name (bool, optional): Whether to return the added product's name. Default is False.

    Returns:
        Optional[str]: The product name if return_product_name is True, else None.

    Raises:
        AssertionError: If the user is not redirected to the cell phone product category page,
        or if the product is not added to the shopping cart.
    """
    digital_download_product_page = DigitalDownloadsProductCategoryPage(driver, wait)

    LOGGER.info(
        "Navigate to the digital downloads product category page -"
        f" {digital_download_product_page.url}"
    )
    digital_download_product_page.open()
    assert driver.current_url == digital_download_product_page.url, (
        "User is not redirected to the digital downloads product category page!"
        f" Current URL: {driver.current_url}"
    )

    LOGGER.info("Navigated to the digital downloads product category page")

    LOGGER.info("Add a digital download item to the shopping cart")

    # Click on a random product and add to cart
    products_elm = wait.until(
        EC.visibility_of_all_elements_located(
            digital_download_product_page.product_item_button
        )
    )
    product_index = randint(0, len(products_elm) - 1)
    products_elm[product_index].click()
    digital_download_product_page.click_add_to_cart_button()

    # Verify the product is added to the shopping cart
    assert (
        digital_download_product_page.product_added_to_cart_message
        in digital_download_product_page.get_product_added_to_cart_message()
    ), "Product was not added to the shopping cart!"
    digital_download_product_page.click_product_add_to_cart_message_close_button()

    # Get the product name
    product_name = digital_download_product_page.get_product_name()

    LOGGER.info(
        f"Product titled '{product_name}' successfully added to the shopping cart"
    )

    if return_product_name:
        return product_name


def add_cellphone_item_to_cart(
    driver: webdriver, wait: WebDriverWait, return_product_name: bool = False
) -> Optional[str]:
    """
    Navigate to the cell phone product category page, select a random product,
    add it to the shopping cart, and optionally return the product name.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        return_product_name (bool, optional): Whether to return the added product's name. Default is False.

    Returns:
        Optional[str]: The product name if return_product_name is True, else None.

    Raises:
        AssertionError: If the user is not redirected to the cell phone product category page,
        or if the product is not added to the shopping cart.
    """

    cellphone_product_page = CellPhonesProductCategoryPage(driver, wait)

    LOGGER.info(
        "Navigate to the cell phone product category page -"
        f" {cellphone_product_page.url}"
    )
    cellphone_product_page.open()
    assert driver.current_url == cellphone_product_page.url, (
        "User is not redirected to the cell phone product category page!"
        f" Current URL: {driver.current_url}"
    )
    LOGGER.info("Successfully navigated to the cell phone product category page")

    LOGGER.info("Add a cell phone item to the shopping cart")

    # Click on a random product and add to cart
    products_elm = wait.until(
        EC.visibility_of_all_elements_located(
            cellphone_product_page.product_item_button
        )
    )
    product_index = randint(0, len(products_elm) - 1)
    products_elm[product_index].click()
    cellphone_product_page.click_add_to_cart_button()

    # Verify the product is added to the shopping cart
    assert (
        cellphone_product_page.product_added_to_cart_message
        in cellphone_product_page.get_product_added_to_cart_message()
    ), "Product was not added to the shopping cart!"
    cellphone_product_page.click_product_add_to_cart_message_close_button()

    # Get the product name
    product_name = cellphone_product_page.get_product_name()

    LOGGER.info(f"Product titled '{product_name}' added to the shopping cart")

    if return_product_name:
        return product_name


def open_cart(driver: webdriver, wait: WebDriverWait) -> ShoppingCartPage:
    """
    Open the shopping cart page and verify the navigation.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.

    Returns:
        ShoppingCartPage: An instance of the ShoppingCartPage.

    Raises:
        AssertionError: If the user is not redirected to the shopping cart page.
    """

    shopping_cart_page = ShoppingCartPage(driver, wait)
    shopping_cart_url = "https://demo.nopcommerce.com/cart"

    # Open the shopping cart page if the current URL is different
    if driver.current_url != shopping_cart_url:
        LOGGER.info(f"Navigate to the shopping cart page - {shopping_cart_page.url}")
        shopping_cart_page.open()

        assert driver.current_url == shopping_cart_page.url, (
            "User is not redirected to the shopping cart page!"
            f" Current URL: {driver.current_url}"
        )

        LOGGER.info("Successfully navigated to the shopping cart page!")
    else:
        # Verify the current URL matches the shopping cart URL
        assert driver.current_url == shopping_cart_page.url, (
            "User is not redirected to the shopping cart page!"
            f" Current URL: {driver.current_url}"
        )

    return shopping_cart_page


def list_products_in_cart(driver: webdriver, wait: WebDriverWait) -> List[str]:
    """
    List the products in the shopping cart.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.

    Returns:
        list: A list of product names in the shopping cart.
    """
    shopping_cart_page = open_cart(driver, wait)
    return shopping_cart_page.list_products_in_cart()


def get_product_quantity(driver: webdriver, wait: WebDriverWait, product_name: str):
    """
    Get the quantity of a product in the shopping cart.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        product_name (str): The name of the product to get the quantity of.

    Returns:
        int: The quantity of the product.
    """
    shopping_cart_page = open_cart(driver, wait)
    return shopping_cart_page.get_product_quantity(product_name)


def update_product_quantity_in_cart(
    driver: webdriver, wait: WebDriverWait, product_name: str, quantity: int
):
    """
    Update the quantity of a product in the shopping cart.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        product_name (str): The name of the product to update.
        quantity (int): The desired quantity of the product.

    Raises:
        TimeoutException: If the update cart button is still clickable after the form submission.
    """
    LOGGER.info(f"Update the quantity of product '{product_name}' in the shopping cart")
    shopping_cart_page = open_cart(driver, wait)
    shopping_cart_page.modify_product_quantity(product_name, quantity)

    # Verify the product quantity is updated
    assert shopping_cart_page.get_product_quantity(product_name) == str(
        quantity
    ), f"Product quantity was not updated to {quantity}!"

    LOGGER.info("Product quantity updated successfully")


def remove_product_from_cart(driver: webdriver, wait: WebDriverWait, product_name: str):
    """
    Remove a product from the shopping cart.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.
        product_name (str): The name of the product to remove.

    Raises:
        TimeoutException: If the update cart button is still clickable after the form submission.
    """
    LOGGER.info(f"Remove product '{product_name}' from the shopping cart")
    shopping_cart_page = open_cart(driver, wait)

    shopping_cart_page.remove_product_from_cart(product_name)

    # Verify the product is no longer in the shopping cart
    assert (
        product_name not in shopping_cart_page.list_products_in_cart()
    ), f"Product '{product_name}' was not removed from the shopping cart!"

    LOGGER.info("Product removed successfully")


def checkout_from_cart(driver: webdriver, wait: WebDriverWait):
    """
    Proceed to the checkout process from the shopping cart.

    Args:
        driver (WebDriver): The WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance.

    Raises:
        TimeoutException: If the checkout button is still clickable after the form submission.
    """
    LOGGER.info("Proceed to the checkout process")
    shopping_cart_page = open_cart(driver, wait)

    LOGGER.info("Check the agree to terms of service checkbox")
    shopping_cart_page.click_terms_of_service()

    LOGGER.info("Click the checkout button")
    shopping_cart_page.click_checkout()

    # Wait for the checkout button to become unclickable after the form submission
    wait.until_not(EC.element_to_be_clickable(shopping_cart_page.checkout_button))

    LOGGER.info("Proceeded to the checkout process")
