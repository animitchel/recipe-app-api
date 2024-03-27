
from django.test import TestCase, SimpleTestCase
from .calc import calc_plus, calc_sub

class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        """Test that two numbers are added together"""
        result = calc_plus(num1=5, num2=5)
        self.assertEqual(result, 10)

class SubtractCalcTests(SimpleTestCase):
    def test_subtract_numbers(self):
        """Test that two numbers are subtracted from each other"""
        result = calc_sub(num1=10, num2=5)
        self.assertEqual(result, 5)
