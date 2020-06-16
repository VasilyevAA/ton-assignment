import string
import pytest

"""
Необходимо реализовать функцию, которая принимает в качестве аргумента строку s, содержащую любые буквы латинского
алфавита а так-же скобки вида (){}[], и выдает в результате наибольшую возможную строку, такую что она является
подстрокой бесконечной строки вида sssssss... и скобочные символы в ней составляют правильную скобочную
последовательность. Если такая строка имеет бесконечную длину, вернуть строку "Infinite". Также необходимо
реализовать тесты.
"""

INFINITY_CONST = "Infinite"

OPPOSITE_BRACKET = {
    '{': '}',
    '(': ')',
    '[': ']',
    ']': '[',
    '}': '{',
    ')': '(',
}

OPEN_BRACKETS = '([{'
CLOSE_BRACKETS = ')]}'
ALL_BRACKETS = OPEN_BRACKETS + CLOSE_BRACKETS
SUPPORTED_SYMBOLS = string.ascii_letters + ALL_BRACKETS


# unfortunately it doesn't work, but if it fixed It should be work faster. Some problem in re pattern argument
# regex_for_balanced_brackets = '\w*(\(([^)(\]\[}{]+|\g<1>)*+\)|\[\g<2>*+\]|\{\g<2>*+\})\w*'


def grab_brackets(some_str):
    if not isinstance(some_str, str):
        raise Exception('Invalid input datatype. First arg should be string (str type)')
    processing_str = list(some_str)
    max_len_for_infinity = len(processing_str)

    max_str_result = list()
    open_brackets_buffer = list()
    current_str = [[]]

    for elem in processing_str + processing_str:

        if elem not in ALL_BRACKETS:
            if elem not in SUPPORTED_SYMBOLS:
                raise Exception(f'Use invalid symbol in input: "{elem}"')
            current_str[-1].append(elem)
            if len(current_str[-1]) > len(max_str_result):
                max_str_result = list(current_str[-1])

        if elem in OPEN_BRACKETS:
            open_brackets_buffer.append(elem)
            current_str[-1].append(elem)
            current_str.append([])

        if elem in CLOSE_BRACKETS:
            should_bracket = OPPOSITE_BRACKET[elem]
            if open_brackets_buffer and open_brackets_buffer[-1] == should_bracket:
                open_brackets_buffer.pop()
                current_str[-1].append(elem)
                if len(current_str) > 1:
                    current_str[-2].extend(current_str.pop())
                if len(current_str[-1]) > len(max_str_result):
                    max_str_result = list(current_str[-1])
            else:
                current_str = [[]]
                open_brackets_buffer = []

        if len(max_str_result) == max_len_for_infinity:
            return INFINITY_CONST

    return ''.join(max_str_result)


class TestGrabBrackets:

    def test_positive_check_all_symbols(self):
        symbs = string.ascii_letters
        test_str = f"({symbs[3:10]}){{{symbs[10:]}}}]][{symbs[:3]}]"
        assert grab_brackets(test_str) == f"[{symbs[:3]}]({symbs[3:10]}){{{symbs[10:]}}}"

    def test_positive_check_length_with_symbols_more_than_bracket_length(self):
        assert grab_brackets("[]()]][aaaaaaaa]][{}") == "[aaaaaaaa]"

    def test_positive_check_calculate_with_terminate_sequence(self):
        assert grab_brackets("[]()]{}") == "{}[]()"

    @pytest.mark.parametrize('infinity_str', ["{}", "[]", "()", "[][]", "a{}b", "[a]{}"])
    def test_positive_check_simple_infinity(self, infinity_str):
        assert grab_brackets(infinity_str) == INFINITY_CONST

    def test_positive_check_output_for_same_value(self):
        """
        undefined behavior
        """
        assert grab_brackets("[]()]][bbaacc]][{}") == "[bbaacc]"  # [](), [bbaacc], [{}[]()] -> return first max

    def test_positive_return_string_without_brackets_but_with_brackets_in_input(self):
        assert grab_brackets("[]{{assssdasd{{[]{{}}") == 'assssdasd'

    def test_positive_check_empty_string(self):
        assert grab_brackets("") == ""

    def test_negative_check_not_balanced_input_with_wrong_first_bracket(self):
        assert grab_brackets("{[]") == "[]"

    def test_negative_check_not_balanced_input_with_wrong_last_bracket(self):
        assert grab_brackets("()}") == "()"

    def test_negative_check_not_balanced_input_with_mixed_brackets(self):
        assert grab_brackets("{[}(])") == ""

    @pytest.mark.parametrize('invalid_input', ["{.}", "[]  {}", "!{}", "{5}", "[]3", "1{}"])
    def test_negative_check_invalid_input(self, invalid_input):
        with pytest.raises(Exception):
            grab_brackets(invalid_input)

    def test_negative_use_none_in_input(self):
        with pytest.raises(Exception):
            grab_brackets(None)
