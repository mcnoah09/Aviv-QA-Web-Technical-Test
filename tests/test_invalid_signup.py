import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from structlog import get_logger

from tests.helpers.utils import register_user
from tests.pages.register import RegisterPage

LOGGER = get_logger(module=__name__)


@pytest.mark.parametrize(
    (
        "first_name, last_name, email, password, confirm_password, description,"
        " expected_error_message"
    ),
    [
        (
            "",
            "Larson",
            "brian@example.net",
            "password",
            "password",
            "First name field is empty",
            "First name is required.",
        ),
        (
            "Brian",
            "",
            "larson@example.net",
            "password",
            "password",
            "Last name field is empty",
            "Last name is required.",
        ),
        (
            "Brian",
            "Larson",
            "brian_larson.net",
            "password",
            "password",
            "Invalid email",
            "Wrong email",
        ),
        (
            "Brian",
            "Larson",
            "brianlarson1@example.net",
            "",
            "",
            "Password field is empty",
            "Password is required.",
        ),
        (
            "Brian",
            "Larson",
            "brianlarson2@example.net",
            "password",
            "",
            "Confirm password field is empty",
            "Password is required.",
        ),
        (
            "Brian",
            "Larson",
            "brianlarson3@example.net",
            "pass",
            "password",
            "Password is less than 6 characters",
            "Password must meet the following rules",
        ),
        (
            "Brian",
            "Larson",
            "brianlarson4@example.net",
            "password",
            "password1",
            "Passwords do not match",
            "The password and confirmation password do not match.",
        ),
    ],
)
def test_invalid_signup(
    driver: webdriver,
    wait: WebDriverWait,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    confirm_password: str,
    description: str,
    expected_error_message: str,
):
    """
    Test invalid user signup

    :param driver: WebDriver instance
    :param wait: WebDriverWait instance
    :param first_name: First name
    :param last_name: Last name
    :param email: Email
    :param password: Password
    :param confirm_password: Confirm password
    :param description: Test description
    :param expected_error_message: Expected error message

    :return: None
    """
    # 1. Register a new user with invalid data
    LOGGER.info(f"Registering a new user with invalid data where - {description}")
    register_user(
        driver=driver,
        wait=wait,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        confirm_password=confirm_password,
    )

    # 2. Validate that the error message is displayed
    LOGGER.info("Validating that the error message is displayed")
    field_validation_error = RegisterPage(
        driver=driver, wait=wait
    ).get_field_validation_error()

    assert expected_error_message in field_validation_error, (
        f"Expected error message: {expected_error_message} not in"
        f" {field_validation_error}"
    )

    LOGGER.info("Successfully validated that the expected error message is displayed")
