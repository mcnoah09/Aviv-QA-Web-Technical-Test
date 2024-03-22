from random import randint
from typing import Tuple

from faker import Faker
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from tests.helpers.utils import (
    add_book_to_cart,
    add_cellphone_item_to_cart,
    add_digital_download_item_to_cart,
    get_product_quantity,
    list_products_in_cart,
    login_user,
    remove_product_from_cart,
    update_product_quantity_in_cart,
)


def test_cart_functionality(
    driver: webdriver, wait: WebDriverWait, fake: Faker, auth: Tuple[str, str]
) -> None:
    """
    Test cart functionality

    :param driver: WebDriver instance
    :param wait: WebDriverWait instance
    :param fake: Faker instance
    :param auth: Tuple of email and password of an existing user

    :return: None
    """
    email, password = auth

    # 1. Login with a registered user
    login_user(driver=driver, wait=wait, email=email, password=password)

    # 2. Add multiple products to the shopping cart
    digital_downloads_product_name = add_digital_download_item_to_cart(
        driver=driver, wait=wait, return_product_name=True
    )
    cellphone_product_name = add_cellphone_item_to_cart(
        driver=driver, wait=wait, return_product_name=True
    )
    book_product_name = add_book_to_cart(
        driver=driver, wait=wait, return_product_name=True
    )

    # 3. Open the cart and verify the items are added
    expected_items_in_cart = [
        digital_downloads_product_name,
        cellphone_product_name,
        book_product_name,
    ]
    actual_items_in_cart = list_products_in_cart(driver=driver, wait=wait)
    assert set(expected_items_in_cart) == set(actual_items_in_cart), (
        f"Expected items in cart: {expected_items_in_cart}\n"
        f"Actual items in cart: {actual_items_in_cart}"
    )

    # 4. Update the quantity of the book product
    book_product_quantity = randint(2, 10)
    update_product_quantity_in_cart(
        driver=driver,
        wait=wait,
        product_name=book_product_name,
        quantity=book_product_quantity,
    )

    # Verify the quantity of the book product is updated
    actual_book_product_quantity = get_product_quantity(
        driver=driver, wait=wait, product_name=book_product_name
    )
    assert actual_book_product_quantity == str(book_product_quantity), (
        f"Expected book product quantity: {book_product_quantity}\n"
        f"Actual book product quantity: {actual_book_product_quantity}"
    )

    # 5. Remove the digital downloads product from the cart
    remove_product_from_cart(
        driver=driver, wait=wait, product_name=digital_downloads_product_name
    )

    # Verify the digital downloads product is removed from the cart
    actual_items_in_cart = list_products_in_cart(driver=driver, wait=wait)
    assert digital_downloads_product_name not in actual_items_in_cart, (
        f"Expected items in cart: {expected_items_in_cart}\n"
        f"Actual items in cart: {actual_items_in_cart}"
    )
