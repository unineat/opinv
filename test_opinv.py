# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 20:04:49 2024

@author: neat
"""

import unittest
from opinv import invert_conditions  


class TestConditionInverter(unittest.TestCase):

    def assert_code_equal(self, code1, code2):
        """Compare two code strings by normalizing whitespace and removing spaces in lists."""

        def normalize(code):
            # Remove all whitespace between list elements
            code = code.replace(", ", ",")
            # Normalize other whitespace
            return ' '.join(code.split())
        self.assertEqual(normalize(code1), normalize(code2))


    def test_basic_comparison_operators(self):
        """Test inversion of basic comparison operators."""

        test_cases = [
            ("if x > 0: pass",  "if x <= 0: pass", 1),
            ("if x < 0: pass",  "if x >= 0: pass", 1),
            ("if x == 0: pass", "if x != 0: pass", 1),
            ("if x >= 0: pass", "if x < 0: pass",  1),
            ("if x <= 0: pass", "if x > 0: pass",  1),
        ]
        
        for input_code, expected_code, expected_count in test_cases:
            modified_code, changes = invert_conditions(input_code)
            self.assert_code_equal(modified_code, expected_code)
            self.assertEqual(len(changes), expected_count)

    
    def test_is_operator(self):
        """Test handling of 'is' and 'is not' operators."""

        test_cases = [
            ("if x is None: pass",     "if x is not None: pass", 1),
            ("if x is not None: pass", "if x is None: pass",     1),
        ]
        
        for input_code, expected_code, expected_count in test_cases:
            modified_code, changes = invert_conditions(input_code)
            self.assert_code_equal(modified_code, expected_code)
            self.assertEqual(len(changes), expected_count)


    def test_in_operator(self):
        """Test handling of 'in' and 'not in' operators."""

        test_cases = [
            ("if x in [1,2,3]: pass", "if x not in [1,2,3]: pass", 1),
            ("if x not in [1,2,3]: pass", "if x in [1,2,3]: pass", 1),
        ]
        
        for input_code, expected_code, expected_count in test_cases:
            modified_code, changes = invert_conditions(input_code)
            self.assert_code_equal(modified_code, expected_code)
            self.assertEqual(len(changes), expected_count)

    
    def test_nested_if_statements(self):
        """Test handling of nested if statements."""

        input_code = """
if x > 0:
    if y < 0: pass
    else: pass
elif y > 0: pass
"""
        expected_code = """
if x <= 0:
    if y >= 0: pass
    else: pass
elif y <= 0: pass
"""
        modified_code, changes = invert_conditions(input_code)
        self.assert_code_equal(modified_code, expected_code)
        self.assertEqual(len(changes), 3)


    def test_comparisons_outside_if(self):
        """Test that comparisons outside if conditions are not modified."""

        input_code = """
result = x > 0
if x > 0:
    y = z < 10
    pass
"""
        expected_code = """
result = x > 0
if x <= 0:
    y = z < 10
    pass
"""
        modified_code, changes = invert_conditions(input_code)
        self.assert_code_equal(modified_code, expected_code)
        self.assertEqual(len(changes), 1)  # Only the if condition should be changed


    def test_elif_conditions(self):
        """Test handling of elif conditions."""

        input_code = """
if x > 0:
    pass
elif x < 0:
    pass
elif x == 0:
    pass
"""
        expected_code = """
if x <= 0:
    pass
elif x >= 0:
    pass
elif x != 0:
    pass
"""
        modified_code, changes = invert_conditions(input_code)
        self.assert_code_equal(modified_code, expected_code)
        self.assertEqual(len(changes), 3)


    def test_operator_positions(self):
        """Test that operator positions are correctly recorded."""

        input_code = "if x > 0: pass"
        _, changes = invert_conditions(input_code)
        self.assertEqual(len(changes), 1)
        change = changes[0]
        self.assertTrue('position' in change)
        self.assertTrue('original_op' in change)
        self.assertTrue('new_op' in change)
        self.assertEqual(change['original_op'], 'Gt')
        self.assertEqual(change['new_op'], 'LtE')



if __name__ == "__main__":
    unittest.main()

