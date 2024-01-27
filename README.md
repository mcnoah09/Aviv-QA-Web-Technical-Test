# 🏗️ AVIV QA Web Technical Test

This repository contains the Aviv QA Web Technical Test.

--- 

## 🔧 Installation

To install the project dependencies, run:

```bash
poetry install --all-poetry
```

---

## Usage

To run all tests, run:

```bash
poetry run pytest
```

To run the tests locally and in a docker container, run:

```bash
docker build -t aviv-web-technical-test .
docker run --rm -it aviv-web-technical-test /bin/bash -c "poetry run pytest"
```

NB: Make sure Docker is installed and running on your machine.

## Overview

Welcome to the Aviv QA Web Technical Test! This challenge involves automating test scenarios for the [demo.nopcommerce.com](https://demo.nopcommerce.com/) website using your preferred programming language (TypeScript, JavaScript, Java, Python, or .NET) and your preferred test automation framework or library (Playwright, WebdriverIO, Cypress, TestCafe, or Selenium Webdriver). 

The focus is on implementing automation tests following the Page Object Model (POM) and Data-Driven Testing (DDT) principles for better maintainability and readability.

## Getting Started

1. Read and comprehend the test automation challenge requirements provided in this repository.
2. Fork the original repository to your GitHub account to submit pull requests.
3. Create a New Branch to work on your changes.
4. Implement test automation according to the challenge requirements. Follow best practices for writing clear, maintainable, and efficient code.
5. Commit your changes with clear and concise commit messages representing logical steps in your development process.
6. Push your branch to your forked repository on GitHub.
7. Navigate to your forked repository on GitHub and create a new pull request from your feature branch to the original repository's main branch.
8. In the PR description, explain the changes made, the approach taken, and any challenges faced. Be clear and concise.

## The Challenge

### Test Scenarios

#### Scenario 1: User Signup and Checkout

1. Navigate to the website.
2. Click on the "Register" link.
3. Fill in valid information for a new user.
4. Verify successful registration and redirection to the homepage.
5. Log in with the newly created user credentials.
6. Add a product to the shopping cart.
7. Proceed to the checkout process.
8. Verify the checkout process steps: Cart, Address, Shipping, Payment.
9. Fill in valid shipping information.
10. Choose a shipping method.
11. Select a payment method.
12. Complete the purchase.
13. Verify successful purchase and user confirmation.

#### Scenario 2: Invalid Signup Attempt

1. Navigate to the website.
2. Click on the "Register" link.
3. Fill in invalid information for a new user.
4. Verify the user is not registered, and an appropriate error message is displayed.

#### Scenario 3: Existing User Login and Checkout

1. Navigate to the website.
2. Log in with valid existing user credentials.
3. Add a product to the shopping cart.
4. Proceed to the checkout process.
5. Verify the checkout process steps: Cart, Address, Shipping, Payment.
6. Fill in valid shipping information.
7. Choose a shipping method.
8. Select a payment method.
9. Complete the purchase.
10. Verify successful purchase and user confirmation.

#### Scenario 4: Verify Cart Functionality

1. Navigate to the website.
2. Add multiple products to the shopping cart.
3. Verify correct products and quantities in the shopping cart.
4. Modify the quantity of a product.
5. Remove a product from the cart.
6. Verify the cart is updated accordingly.

### Continuous Integration

- The project should be integrated with (CircleCI, GitLab, Jenkins, or GitHub Actions) for continuous integration.
- The automation suite is triggered on each push or pull request to the repository.

### Test Reports

- Test reports should be generated after each test run and can be found in the `/reports` directory.

### Issues and Challenges

- Document any challenges faced during the automation process and how they were addressed.

### Future Improvements

- Highlight any improvements or optimizations considered for future iterations.

### Bonus Points

- You can earn bonus points for:
  - Implementing parameterized tests.
  - Using environmental configurations.
  - Demonstrating knowledge of parallel test execution.

## Good luck!

Best regards, 

Aviv Quality Team
