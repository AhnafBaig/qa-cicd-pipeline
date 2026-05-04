Feature: User Authentication
  As a SauceDemo user I want to log in so I can access the catalogue

  @smoke @critical
  Scenario: Successful login with valid credentials
    Given I am on the login page
    When I login with username "standard_user" and password "secret_sauce"
    Then I should be on the inventory page

  @smoke
  Scenario: Locked out user sees error
    Given I am on the login page
    When I login with username "locked_out_user" and password "secret_sauce"
    Then I should see a login error message

  @regression
  Scenario: Invalid credentials shows error
    Given I am on the login page
    When I login with username "bad_user" and password "bad_pass"
    Then I should see a login error message

  @regression
  Scenario: Empty username shows error
    Given I am on the login page
    When I login with username "" and password "secret_sauce"
    Then I should see a login error message
