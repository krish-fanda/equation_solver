"""Module for matrix and related operations.

A value is considered a matrix if and only if it satifies all these conditions:-
  *is a non-empty list or tuple
  *all its elements are list or tuple whose elements in turn are int, float or
    complex only
  *all the elements of the matrix should have the same length and should be 
    non-empty
"""
from copy import deepcopy

LIST_MATRIX_ERROR=\
TypeError("Matrix for a List Matrix wrapper must be a list " + \
          "matrix which is a list and all its elements are list")
MULTIPLICATION_FACTOR_ERROR=\
TypeError("multiplicationFactor must be a number (int,float or complex)")

def isMatrix(value):
  """Checks whether value is a matrix

  Args: 
    value: a value of any data type to be checked whether it is a matrix or not

  Returns:
    a boolean which is True if value is a matrix and False otherwise
  """
  if type(value) not in (list,tuple):
    return False
  col_count=None
  if len(value)==0:
    return False
  for row in value:
    if type(row) not in (list,tuple):
      return False
    if col_count==None:
      col_count=len(row)
      if col_count==0:
        return False
    elif col_count!=len(row):
      return False
    for item in row:
      if type(item) not in (int,float,complex):
        return False
  return True

def isInnerListMatrix(value):
  """Checks whether value is an inner list matrix

  A value is considered an inner list matrix if and only if it is a matrix 
  and all its elements are list

  Args: 
    value: a value of any data type to be checked whether it is a inner list 
    matrix or not

  Returns:
    a boolean which is True if value is a inner list matrix and False otherwise
  """
  if not isMatrix(value):
    return False
  for row in value:
    if type(row) is not list:
      return False
  return True

def isListMatrix(value):
  """
  Checks whether value is a list matrix

  A value is considered a list matrix if and only if it is a matrix, value is a 
  list and all elements of value are list.
  
  Args: 
    value: a value of any data type to be checked 
    whether it is a list matrix or not

  Returns:
    a boolean which is True if value is a list matrix and False otherwise
  """
  return type(value) is list and isInnerListMatrix(value)


#rowIndex and colIndex counting starts from 1 instead of 0

class MatrixWrapper:
  """A wrapper for a matrix"""

  def __init__(self,data):
    """Initialize the Matrix Wrapper using the given matrix
    
    Args:
      data: the matrix (list/tuple of lists and tuples) to be used internally 
      by wrapper or another MatrixWrapper
    """
    if isinstance(data,MatrixWrapper):
      self.matrix=data.matrix
    elif not isMatrix(data):
      raise TypeError("Matrix for a Matrix wrapper must be a matrix.")
    else:
      self.matrix=data
    self.matrix=deepcopy(self.matrix)

  def get(self,rowIndex,colIndex):
    """Returns an element of matrix used by the Matrix Wrapper
  
    Args: 
      rowIndex: the integer index of the row (starting from 1 as in Maths) 
      1<=rowIndex<=len(self.matrix)
      colIndex: the integer index of the column (starting from 1 as in Maths) 
      1<=colIndex<=len(self.matrix[rowIndex-1])

    Returns:
      an int,float or complex corresponding to the element determined by 
      rowIndex, colIndex
    """
    return self.matrix[rowIndex-1][colIndex-1]
  
  def getOrder(self):
    """Returns the order of the matrix used by the Matrix Wrapper

    Returns:
      A tuple (m,n) where m is the no. of rows and n is the no. of columns
    """
    return (len(self.matrix),len(self.matrix[0]))

  def __str__(self):
    return str(self.matrix)

class ListMatrixWrapper(MatrixWrapper):
  """A wrapper for a list matrix

  A value is considered a list matrix if and only if it is a matrix, value is a 
  list and all elements of value are list.
  """

  def __init__(self,data):
    """Initialize the List Matrix Wrapper using the given matrix
    
    Args:
      data: the matrix (list of lists) to be used internally by wrapper or 
      another MatrixWrapper
    """
    if isinstance(data,MatrixWrapper):
      if not isListMatrix(data.matrix):
        raise LIST_MATRIX_ERROR
      self.matrix=data.matrix
    elif not isListMatrix(data):
      raise LIST_MATRIX_ERROR
    else:
      self.matrix=data
    self.matrix=deepcopy(self.matrix)

  #Elementary row operations

  def swapRows(self,rowIndex1,rowIndex2):
    """Swap two rows of the matrix used internally by the wrapper
    
    Args:
      rowIndex1: the integer index of one of the rows 
       (starting from 1 as in Maths) (1<=rowIndex1<=len(self.matrix))
      rowIndex2: the integer index of the other row 
       (starting from 1 as in Maths) (1<=rowIndex2<=len(self.matrix))
    """
    self.matrix[rowIndex1-1],self.matrix[rowIndex2-1]=\
      self.matrix[rowIndex2-1],self.matrix[rowIndex1-1]

  def multiplyRow(self,rowIndex,multiplicationFactor):
    """Multiply a particular row of the matrix by a scalar
    
    Args:
      rowIndex: the integer index of one of the rows 
       (starting from 1 as in Maths) (1<=rowIndex<=len(self.matrix))
      multiplicationFactor: the scalar by which the row is to be multiplied. 
       Must be an int, float or complex
    """
    if type(multiplicationFactor) not in (int,float,complex):
      raise MULTIPLICATION_FACTOR_ERROR
    row=self.matrix[rowIndex-1]
    for j in range(len(row)):
      row[j]*=multiplicationFactor

  def addRowMultToAnother(self,rowIndexTarget,rowIndexSource,
                          multiplicationFactor):
    """Add a multiple of a row of the matrix to another row
    
    Args:
      rowIndexTarget:
        the integer index of row to which addition has to be made 
        (starting from 1 as in Maths) (1<=rowIndexTarget<=len(self.matrix))
      rowIndexSource:
        the integer index of row whose multiple has to be added 
        (starting from 1 as in Maths) (1<=rowIndexSource<=len(self.matrix))
      multiplicationFactor: 
        the scalar by which the row to be added is to be multiplied before 
        adding. Must be an int, float or complex
    """
    if type(multiplicationFactor) not in (int,float,complex):
      raise MULTIPLICATION_FACTOR_ERROR
    targetRow=self.matrix[rowIndexTarget-1]
    sourceRow=self.matrix[rowIndexSource-1]
    for j in range(len(targetRow)):
      targetRow[j]+=sourceRow[j]*multiplicationFactor