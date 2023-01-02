from cloudia_challenge.telegram.views import process_input


def test_process_input_too_long():
    """Test input with more than 280 characters."""
    text_input = "9" * 281
    expected_output = "A entrada é muito longa. Por favor, insira até 280 caracteres."

    assert process_input(text_input) == expected_output


def test_process_input_non_integer():
    """Test input that is not an integer."""
    text_input = "abc"
    expected_output = "Por favor, insira um número inteiro."

    assert process_input(text_input) == expected_output


def test_process_input_fizzbuzz():
    """Tests input that is divisible by 3 and 5."""
    text_input = "15"
    expected_output = "FizzBuzz"

    assert process_input(text_input) == expected_output


def test_process_input_fizz():
    """Tests input that is divisible by 3 but not by 5."""
    text_input = "3"
    expected_output = "Fizz"

    assert process_input(text_input) == expected_output


def test_process_input_buzz():
    """Tests input that is divisible by 5 but not by 3."""
    text_input = "5"
    expected_output = "Buzz"

    assert process_input(text_input) == expected_output


def test_process_input_integer():
    """Tests input that is an integer but not divisible by 3 or 5."""
    text_input = "7"
    expected_output = 7

    assert process_input(text_input) == expected_output
