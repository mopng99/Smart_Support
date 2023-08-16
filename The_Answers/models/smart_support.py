# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


def backtrack(combination, open_count, close_count, n, result):
    # Base case: If the combination length reaches 2n, add it to the result
    if len(combination) == 2 * n:
        result.append(combination)
        return

    # If the open count is less than n, we can add an opening parenthesis
    if open_count < n:
        backtrack(combination + '(', open_count + 1, close_count, n, result)

    # If the close count is less than the open count, we can add a closing parenthesis
    if close_count < open_count:
        backtrack(combination + ')', open_count, close_count + 1, n, result)


class SmartSupport(models.Model):
    _name = 'smart.support'

    # 1. [Convert a Number to Hexadecimal](https://leetcode.com/problems/convert-a-number-to-hexadecimal/)
    def decimal_to_hexadecimal(number):
        hex_digits = "0123456789ABCDEF"
        if number == 0:
            return '0'
        hex_string = ''
        while number > 0:
            remainder = number % 16
            hex_string = hex_digits[remainder] + hex_string
            number //= 16

        if number < 0:
            number = number & 0xFFFFFFFF  # Convert to 32-bit signed integer

        hex_string = hex(number)[2:]  # Remove the '0x' prefix from the hexadecimal string
        hex_string = hex_string.rjust(8, '0')  # Pad with leading zeros to ensure 8 characters
        return hex_string

    # Example usage
    # decimal_number = 26
    decimal_number = -1
    hexadecimal_number = decimal_to_hexadecimal(decimal_number)
    print(f"The hexadecimal representation of {decimal_number} is {hexadecimal_number}")

    # 2. [Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
    def compute_max_profit(prices):

        min_price = prices[0]
        max_profit = 0
        day_min_price = 0
        day_max_profit = 0
        count = 0
        for price in prices:
            if price < min_price:
                min_price = price
                day_min_price = prices.index(price) + 1
                count = prices.index(price)
        for price in prices:
            if price > max_profit and prices.index(price) > count:
                max_profit = price
                day_max_profit = prices.index(price) + 1

        print("min price", min_price)
        print("day min price", day_min_price)
        print("max profit", max_profit)
        print("day max profit", day_max_profit)

    # prices = [7, 1, 5, 3, 6, 4]
    prices = [7, 6, 4, 3, 1]
    compute_max_profit(prices)

    # 3. [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)
    def generate_parentheses(n):
        result = []
        backtrack('', 0, 0, n, result)
        return result

    print(generate_parentheses(1))
