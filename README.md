# opinv -- Invert Operators

A Python program, which given an input Python code inverts the conditional operators of its if conditions, using the Python `ast` library.

The program outputs the operator changes, their positions, and the newly obtained code (with inverted operators).

**Use**:

- python opinv.py <py_file>

**Example input file**:

```py
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
```

***Resulting output***:

```py
Operator changes:

  GtE   → Lt     @  Line 9, Column 3
  NotEq → Eq     @  Line 9, Column 14
  Gt    → LtE    @  Line 22, Column 7
  Eq    → NotEq  @  Line 25, Column 9


Modified code:

x = 10
y = 5
while x <= 0 and x < 0:
    x = x + 5
    print('x increased by 5')
if x < y and x == 0:
    print('x is greater than y and x is not zero')
else:
    print('x is less than y or x is zero')


class MyClass:

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def compare_values(self):
        if self.a <= self.b:
            c = self.a < self.b
            print('a is greater than b')
        elif self.a != self.b:
            print('a is equal to b')
        else:
            print('a is less than b')


my_object = MyClass(7, 3)
my_object.compare_values()
```
