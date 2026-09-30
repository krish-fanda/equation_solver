"""Module to solve a system of linear equations in 
as many variables as equations"""

from matrix import isListMatrix, ListMatrixWrapper, MatrixWrapper
from number_utilities import normalizeNumber
from copy import deepcopy


GAUSSIAN_EQN_MATRIX_ERROR=\
TypeError("Matrix for a Gaussian linear equation Matrix "+\
          "wrapper (row operations based) must be a Gaussian "+\
          "linear equation matrix (row operations based) "+\
          "which is a list and all its elements are list")


NO_SOLUTION="No solution"
INFINITE_SOLUTION="Infinite solution"
UNIQUE_SOLUTION="Unique solution"

def isGaussianEqnMatrix(value):
    """
    Checks whether value is a Gaussian linear equation matrix 
    (row operations based)

    A value is considered a Gaussian linear equation 
    (row operations based) matrix if and only if it is a list matrix.
    A value is considered a list matrix if and only if it is a matrix, value is a 
    list and all elements of value are list.
    
    Args: 
        value: a value of any data type to be checked whether it is a Gaussian 
        linear equation matrix (row operations based) or not

    Returns:
        a boolean which is True if value is a Gaussian linear equation matrix (row 
        operations based) and False otherwise
    """
    return isListMatrix(value) #and len(value)+1==len(value[0])


class GaussianEqnMatrixWrapper(ListMatrixWrapper):
  """A wrapper for a Gaussian linear equation matrix (row operations based)

  A value is considered a Gaussian linear equation matrix 
  (row operations based) if and only if it is a list matrix
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
    all elements as list.
    Each equation is a row of the matrix. The equation is specified in a form 
    such that each row contains coefficient of
    all variables, each appearing on left hand side followed by the constant 
    value appearing on the right hand side
    
    Args:
        data: A Gaussian Equation Matrix or a MatrixWrapper whose matrix is a 
        Gaussian Equation Matrix
    Returns:
        A pair (tuple) whose first element is a GaussianEqnMatrixWrapper containing
        the Row Reduced Echelon form of the matrix (except last columns) and second element 
        is the type of solution as a string (one of NO_SOLUTION,INFINITE_SOLUTION,UNIQUE_SOLUTION)
    """
    wrapper=GaussianEqnMatrixWrapper(data)
    rowCount,colCount=wrapper.getOrder()
    rowIndex,colIndex=1,1
    while rowIndex<=rowCount and colIndex<colCount:
        for i in range(rowIndex,rowCount+1):
            if wrapper.get(i,colIndex)!=0:
                if i!=rowIndex:
                    wrapper.swapRows(i,rowIndex)
                rowColVal=wrapper.get(rowIndex,colIndex)
                for j in range(1,rowCount+1):
                    if j==rowIndex:
                        continue
                    jColVal=wrapper.get(j,colIndex)
                    #wrapper.multiplyRow(j,rowColVal)
                    wrapper.addRowMultToAnother(j,rowIndex,-jColVal/rowColVal)
                wrapper.multiplyRow(rowIndex,1/rowColVal)
                rowIndex+=1
                break
        colIndex+=1

    for i in range(rowIndex,rowCount+1):
        if wrapper.get(i,colCount)!=0:
            return wrapper,NO_SOLUTION
    if rowIndex==colCount:
        return wrapper,UNIQUE_SOLUTION
    else:
        return wrapper,INFINITE_SOLUTION
    


  