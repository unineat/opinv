# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 09:45:40 2024

@author: neat
"""

import sys
import ast
import astor
# from astpp import dump # nicer node print for debugging


class ConditionInverter(ast.NodeTransformer):
    def __init__(self):
        self.operator_positions = []
        self.in_if_test = False
        
    def get_operator_positions(self, node):
        """Get line and column numbers for operator nodes."""
        return (node.lineno, node.col_offset) if hasattr(node, 'lineno') else None
    
    def invert_operator(self, op):
        """Return the inverse of a comparison operator."""
        # op_map: dictionary of operator class to be inverted
        op_map = {
            ast.Eq: ast.NotEq,
            ast.NotEq: ast.Eq,
            ast.Lt: ast.GtE,
            ast.LtE: ast.Gt,
            ast.Gt: ast.LtE,
            ast.GtE: ast.Lt,
            ast.Is: ast.IsNot,
            ast.IsNot: ast.Is,
            ast.In: ast.NotIn,
            ast.NotIn: ast.In
        }
        # return inverted class if op type in op_map, or the original class otherwise
        return op_map.get(type(op), type(op))

    def visit_If(self, node):
        """Visit If nodes and process in_if_test state."""
        self.in_if_test = True
        node.test = self.visit(node.test)

        self.in_if_test = False
        node.body = [self.visit(stmt) for stmt in node.body]
        if node.orelse:
            node.orelse = [self.visit(stmt) for stmt in node.orelse]
        return node
    
    def visit_Compare(self, node):
        """Visit and transform comparison nodes only iside an if condition."""
        if not self.in_if_test:
            return node
            
        position = self.get_operator_positions(node)
        if position:
            self.operator_positions.append({
                'position': position,
                'original_op': type(node.ops[0]).__name__,
                'new_op': self.invert_operator(node.ops[0]).__name__
            })
        
        # Invert the operator
        node.ops = [self.invert_operator(op)() for op in node.ops]
        return node
    

def invert_conditions(source_code):
    """
    Invert conditional operators in if statements of the given Python source code.
    Returns the modified code and operator change information.
    """
    # Parse the source code into an AST
    tree = ast.parse(source_code)
    
    # Create and apply the transformer
    transformer = ConditionInverter()
    modified_tree = transformer.visit(tree)
    
    # Generate the modified source code
    modified_code = astor.to_source(modified_tree)
    
    return modified_code, transformer.operator_positions


def main():
    # Example input code
    sample_code = """
x = 10
y = 5

while x <= 0 and x < 0:
  x = x + 5
  print("x increased by 5")

if x >= y and x != 0:
  print("x is greater than y and x is not zero")
else:
  print("x is less than y or x is zero")


class MyClass:

  def __init__(self, a, b):
    self.a = a
    self.b = b

  def compare_values(self):
    if self.a > self.b:
      c = self.a < self.b
      print("a is greater than b")
    elif self.a == self.b:
      print("a is equal to b")
    else:
      print("a is less than b")

my_object = MyClass(7, 3)
my_object.compare_values()
"""
    
    # print("Original code:")
    # print(sample_code)
    # print("\nInverting conditions...\n")
    
    if len(sys.argv) > 1:
            with open(sys.argv[1]) as f:
                sample_code = f.read()
        
    modified_code, operator_changes = invert_conditions(sample_code)
    
    print("\n\nOperator changes:\n")
    for change in operator_changes:
        print(f"  {change['original_op']:5} → {change['new_op']:5}  ", end='')
        print(f"@  Line {change['position'][0]}, Column {change['position'][1]}")
    print(f"\n\nModified code:\n\n{modified_code}")


if __name__ == "__main__":
    main()