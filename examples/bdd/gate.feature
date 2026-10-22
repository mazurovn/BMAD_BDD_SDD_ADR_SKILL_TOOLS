Feature: Ready gate
  Scenario: A vague outcome is refused
    Given a vague outcome
    When the gate runs
    Then the result is refused
