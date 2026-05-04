Feature: Shopping Cart
  As a logged-in user I want to manage cart items

  Background:
    Given I am logged in as a standard user

  @smoke @critical
  Scenario: Add item to cart
    When I add "Sauce Labs Backpack" to the cart
    Then the cart count should be "1"

  @regression
  Scenario: Add multiple items
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then the cart count should be "2"

  @regression
  Scenario: Remove item from cart
    When I add "Sauce Labs Backpack" to the cart
    And I remove "Sauce Labs Backpack" from the cart
    Then the cart count should be "0"

  @regression
  Scenario: Cart retains items on navigation
    When I add "Sauce Labs Fleece Jacket" to the cart
    And I navigate to the cart page
    Then I should see "Sauce Labs Fleece Jacket" in the cart
