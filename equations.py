"""Module to solve a system of linear equations in 
as many variables as equations"""

from matrix import isListMatrix, ListMatrixWrapper, MatrixWrapper
from number_utilities import normalizeNumber
from copy import deepcopy

GAUSSIAN_EQN_MATRIX_ERROR=\
TypeError("Matrix for a Gaussian linear equation Matrix "+\
          "wrapper (row operations based) must be a Gaussian "+\
          "linear equation matrix (row operations based) "+\
          "which is a list and all its elements are list and "+\
          "no. of columns is 1 more than the no. of rows.")

def isGaussianEqnMatrix(value):
  """
  Checks whether value is a Gaussian linear equation matrix 
  (row operations based)

  A value is considered a Gaussian linear equation 
  (row operations based) matrix if and only if it is a list matrix and
  no. of columns is 1 more than the number of rows.
  A value is considered a list matrix if and only if it is a matrix, value is a 
  list and all elements of value are list.
  
  Args: 
    value: a value of any data type to be checked whether it is a Gaussian 
    linear equation matrix (row operations based) or not

  Returns:
    a boolean which is True if value is a Gaussian linear equation matrix (row 
    operations based) and False otherwise
  """
  return isListMatrix(value) and len(value)+1==len(value[0])


class GaussianEqnMatrixWrapper(ListMatrixWrapper):
  """A wrapper for a Gaussian linear equation matrix (row operations based)

  A value is considered a Gaussian linear equation matrix 
  (row operations based) if and only if it is a list matrix and
  no. of columns is 1 more than the number of rows
  A value is considered a list matrix if and only if it is a matrix, value is a 
  list and all elements of value are list.
  """

  def __init__(self,data):
    """Initialize the Gaussian linear equation Matrix Wrapper 
    (row operations based) using the given matrix
    
    Args:
      data: the matrix (list of lists) to be used internally by wrapper or 
      another MatrixWrapper
    """

    if isinstance(data,MatrixWrapper):
      if not isGaussianEqnMatrix(data.matrix):
        raise GAUSSIAN_EQN_MATRIX_ERROR
      self.matrix=data.matrix
    elif not isGaussianEqnMatrix(data):
      raise GAUSSIAN_EQN_MATRIX_ERROR
    else:
      self.matrix=data
    self.matrix=deepcopy(self.matrix)

def solveEquations(data):
  """Solve a system of linear equations specified as a Gaussian Linear Equation 
  Matrix or a Gaussian Equation Matrix Wrapper (row operations based)

  A Gaussian Linear Equation Matrix (row operations based) must be a list, have 
  all elements as list and have 1 more column than no. of rows
  Each equation is a row of the matrix. The equation is specified in a form 
  such that each row contains coefficient of
  all variables, each appearing on left hand side followed by the constant 
  value appearing on the right hand side
  
  Args:
    data: A Gaussian Equation Matrix or a MatrixWrapper whose matrix is a 
    Gaussian Equation Matrix
  Returns:
    A list containing the values of the variables in order if the equations can 
    be solved for a unique solution.
    None is returned if there is no solution or infinite solutions
  """
  wrapper=GaussianEqnMatrixWrapper(data)
  order=wrapper.getOrder()
  for i in range(1,order[0]+1):
    k=i+1
    while wrapper.get(i,i)==0 and k<=order[0]:
      wrapper.swapRows(i,k)
      k+=1
    if wrapper.get(i,i)==0:
      return None
    for l in range(i+1,order[0]+1):
      mFactor=-wrapper.get(l,i)/wrapper.get(i,i)
      wrapper.addRowMultToAnother(l,i,mFactor)
  
  for i in range(order[0],0,-1):
    for l in range(i-1,0,-1):
      mFactor=-wrapper.get(l,i)/wrapper.get(i,i)
      wrapper.addRowMultToAnother(l,i,mFactor)
  
  for i in range(1,order[0]+1):
    wrapper.multiplyRow(i,1/wrapper.get(i,i))
  result=[normalizeNumber(wrapper.get(i,order[1])) for i in range(1,order[0]+1)]
  return result