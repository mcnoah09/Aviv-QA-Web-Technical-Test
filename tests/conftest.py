import allure
import pytest
from faker import Faker
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from structlog import get_logger
from webdriver_manager.chrome import ChromeDriverManager

from tests.helpers.utils import register_user

LOGGER = get_logger(module=__name__)


@pytest.fixture(scope="module", name="driver")
def webdriver_init():
    LOGGER.info("Initialising WebDriver")
    # Configure ChromeOptions
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-autofill")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--headless")
    options.add_argument("--start-maximized")

    # Initialise the Service object for handling the browser driver
    service = Service(ChromeDriverManager().install())

    # Create a new instance of the driver
    driver = webdriver.Chrome(service=service, options=options)
    LOGGER.info("Chrome WebDriver initialised!")

    LOGGER.info("Navigating to the homepage - https://demo.nopcommerce.com/")
    driver.get("https://demo.nopcommerce.com/")
    LOGGER.info("Successfully navigated to the homepage!")

    yield driver

    LOGGER.info("Quitting Chrome WebDriver")
    driver.quit()


@pytest.fixture(scope="module", name="wait")
def webdriver_wait(driver):
    """
    Initialise WebDriverWait
    :param driver: WebDriver instance
    :return: WebDriverWait instance
    """
    LOGGER.info("Initialising WebDriverWait")
    wait = WebDriverWait(driver, 5)
    LOGGER.info("WebDriverWait initialised")
    return wait


@pytest.fixture(scope="module")
def fake():
    return Faker()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Check if the test has the "driver" fixture
    if "driver" in item.fixturenames:
        # Get the "driver" fixture
        driver_fixture = item.funcargs["driver"]

        if rep.when == "call" and not rep.passed:
            # Attach screenshot to the Allure report
            screenshot_name = f"{item.name}_failure.png"
            allure.attach(
                driver_fixture.get_screenshot_as_png(),
                name=screenshot_name,
                attachment_type=allure.attachment_type.PNG,
            )


@pytest.fixture()
def auth(driver, wait, fake):
    # Register user for use in tests
    email, password = fake.email(), fake.password()
    register_user(
        driver=driver,
        wait=wait,
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=email,
        password=password,
        confirm_password=password,
        date_of_birth=fake.date_of_birth(),
    )
    return email, password
