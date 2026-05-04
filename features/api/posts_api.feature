Feature: Posts API
  As a QA engineer I want to validate the /posts REST endpoint

  @smoke @critical
  Scenario: GET /posts returns 200 with a list
    When I send GET "/posts"
    Then status code is 200
    And response is a non-empty list

  @smoke @critical
  Scenario: GET /posts/1 returns correct resource
    When I send GET "/posts/1"
    Then status code is 200
    And field "id" equals "1"

  @regression
  Scenario: POST /posts creates resource
    When I POST to "/posts" with body:
      """
      {"title": "CI Test", "body": "pipeline run", "userId": 1}
      """
    Then status code is 201
    And field "title" equals "CI Test"

  @regression
  Scenario: GET /posts/99999 returns 404
    When I send GET "/posts/99999"
    Then status code is 404

  @regression
  Scenario: GET /posts/1/comments returns list
    When I send GET "/posts/1/comments"
    Then status code is 200
    And response is a non-empty list

  @regression
  Scenario: PUT updates a post
    When I PUT to "/posts/1" with body:
      """
      {"id": 1, "title": "Updated Title", "body": "new body", "userId": 1}
      """
    Then status code is 200
    And field "title" equals "Updated Title"

  @regression
  Scenario: DELETE a post returns 200
    When I DELETE "/posts/1"
    Then status code is 200

  @regression
  Scenario: Response content-type is JSON
    When I send GET "/posts/1"
    Then status code is 200
    And content-type contains "application/json"
