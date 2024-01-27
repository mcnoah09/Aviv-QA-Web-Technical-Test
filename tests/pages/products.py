from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ProductsCategoryPage:
    def __init__(self, driver, wait, url):
        self.driver = driver
        self.wait = wait
        self.url = url

        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight / 2);"
        )

        # Define web elements on the page
        self.product_item_button = (By.CSS_SELECTOR, ".product-item")
        self.add_to_cart_button = (By.CSS_SELECTOR, ".add-to-cart-button")
        self.product_added_to_cart_success_notification_bar = (
            By.CSS_SELECTOR,
            ".bar-notification.success p",
        )
        self.product_added_to_cart_message_close_button = (
            By.CSS_SELECTOR,
            ".bar-notification.success .close",
        )
        self.product_name = (By.CSS_SELECTOR, ".product-name h1")
        self.product_added_to_cart_message = (
            "The product has been added to your shopping cart"
        )

    def open(self):
        self.driver.get(self.url)

    def click_product_add_to_cart_message_close_button(self):
        self.wait.until(
            EC.visibility_of_element_located(
                self.product_added_to_cart_message_close_button
            )
        ).click()

    def get_product_added_to_cart_message(self):
        return self.wait.until(
            EC.visibility_of_element_located(
                self.product_added_to_cart_success_notification_bar
            )
        ).text

    def click_add_to_cart_button(self):
        self.wait.until(EC.element_to_be_clickable(self.add_to_cart_button)).click()

    def get_product_name(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.product_name)
        ).text


class DigitalDownloadsProductCategoryPage(ProductsCategoryPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait, "https://demo.nopcommerce.com/digital-downloads")


class BooksProductCategoryPage(ProductsCategoryPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait, "https://demo.nopcommerce.com/books")


class CellPhonesProductCategoryPage(ProductsCategoryPage):
    def __init__(self, driver, wait):
        super().__init__(driver, wait, "https://demo.nopcommerce.com/cell-phones")
