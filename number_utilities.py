"""Module for utility functions for numbers"""

def normalizeNumber(data):
  """Convert a number or string containing number to its 
  most appropriate numerical data type (int,float or complex)
  
  Args:
    data: the number or string to be converted
  Returns:
    An int,float or complex depending on which is 
    the most appropriate data type for the value
  Raises:
    ValueError: If it is not possible to convert data to any type of value
  """
  num=complex(data)
  if num.imag==0:
    num=num.real
    if num==int(num):
      num=int(num)
  return num

def wholeNumberToSubscript(integer):
  """Convert a whole number to a string 
  that displays it in subscript.
  
  Args:
    integer: the integer or the string representing 
    the whole number to be converted 
    (negative numbers and non integers are not accepted)
  Returns:
    A string with the whole number displayed in subscript
  """
  if type(integer) is str:
    integer=int(integer)
  if type(integer) is not int:
    raise TypeError("Only whole numbers (a subset of integers)"+\
                    " can be converted to subscript.")
  if integer<0:
    raise ValueError("Negative integers can't be converted to subscript.")
  integer_string=str(integer)
  result=""
  digit=None
  for char in integer_string:
    digit=int(char)
    result+=chr(8320+digit)
  return result