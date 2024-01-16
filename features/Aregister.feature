Feature: Регистрация

  Scenario: Регистрация
    Given Я открыл страницу "Регистрации"
    When Я ввожу текст "task@gmail.com" в поле "email"
    And Я ввожу логин "taskmaster" в поле "username"
    And Я ввожу пароль "taskmaster1" в поле "password"
    And Я жму кнопку Зарегистрироваться
    And Я жду сек 7
    Then Я должен вернутся главную страницу

