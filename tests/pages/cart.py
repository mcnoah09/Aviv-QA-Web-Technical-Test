from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ShoppingCartPage:
    def __init__(self, driver, wait):
        self.driver = driver
        self.wait = wait

        # Define the page's URL
        self.url = "https://demo.nopcommerce.com/cart"

        # Define web elements on the page
        self.shopping_cart_page_button = (By.CSS_SELECTOR, ".ico-cart")
        self.checkout_button = (By.CSS_SELECTOR, ".checkout-button")
        self.terms_of_service_checkbox = (By.ID, "termsofservice")
        self.product_name = (By.CSS_SELECTOR, ".product-name")
        self.update_cart_button = (By.CSS_SELECTOR, ".update-cart-button")
        self.loading_image = (By.CSS_SELECTOR, ".loading-image")
        self.quantity_by_name_input = (By.XPATH, "..//..//..//td[5]//input")
        self.remove_product_by_name_button = (By.XPATH, "..//..//..//td[7]//button")

    def open(self):
        self.driver.get(self.url)

    def click_shopping_cart_page(self):
        self.wait.until(
            EC.element_to_be_clickable(self.shopping_cart_page_button)
        ).click()

    def click_terms_of_service(self):
        self.wait.until(
            EC.element_to_be_clickable(self.terms_of_service_checkbox)
        ).click()

    def click_checkout(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight / 2);"
        )
        self.wait.until(EC.element_to_be_clickable(self.checkout_button)).click()

    def list_products_in_cart(self):
        products = self.wait.until(
            EC.presence_of_all_elements_located(self.product_name)
        )
        return [product.text for product in products]

    def get_product_quantity(self, product_name):
        products = self.wait.until(
            EC.presence_of_all_elements_located(self.product_name)
        )
        for product in products:
            if product.text == product_name:
                return product.find_element(*self.quantity_by_name_input).get_attribute(
                    "value"
                )

    def remove_product_from_cart(self, product_name):
        products = self.wait.until(
            EC.presence_of_all_elements_located(self.product_name)
        )
        for product in products:
            if product.text == product_name:
                product.find_element(*self.remove_product_by_name_button).click()
                self.wait.until(
                    EC.element_to_be_clickable(self.update_cart_button)
                ).click()
                self.wait.until(EC.invisibility_of_element_located(self.loading_image))
                break

    def modify_product_quantity(self, product_name, quantity):
        products = self.wait.until(
            EC.presence_of_all_elements_located(self.product_name)
        )
        for product in products:
            if product.text == product_name:
                product.find_element(*self.quantity_by_name_input).clear()
                product.find_element(*self.quantity_by_name_input).send_keys(quantity)
                self.wait.until(
                    EC.element_to_be_clickable(self.update_cart_button)
                ).click()
                self.wait.until(EC.invisibility_of_element_located(self.loading_image))
                break
