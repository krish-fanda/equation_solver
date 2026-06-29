"""Module to deal with data pertaining to Equation Solver application 
stored in files. This data includes:-
*History of the application stored in history.dat in the form of a 
list of tuples each containing Gaussian Equation Matrix and its 
solution(None or list of int,float,complex).
*User-specified settings in settings.csv in the format
Setting,Value"""

from equations import isGaussianEqnMatrix
from matrix import MatrixWrapper
from pickle import load,dump
from csv import reader,writer
from os import remove

HISTORY_FILE_NAME="history.dat"
SETTINGS_FILE_NAME="settings.csv"
HISTORY_TEMP_FILE_NAME="temp_history.dat"
SETTINGS_TEMP_FILE_NAME="temp_settings.csv"
SETTING,VALUE="Setting","Value"
SETTINGS_HEADERS=[SETTING,VALUE]

#Keys for settings file
EQN_COUNT="eqn_count"
IMAGINARY_UNIT="imaginary_unit"
MAX_HISTORY="max_history"

def writeCSVRecords(records,mainFilePath,tempFilePath=None):
  """Writes an iterable in CSV format first to a temp file (if its path is
    specified), then to the main file and finally deletes the temp file
  
  Args:
    records: The iterable to be written
    mainFilePath: The path of the main file (string)
    tempFilePath: The path of the temp file (string or None)"""
  try:
    for x in records:
      for _ in x:
        pass
  except TypeError:
    raise TypeError("Argument records to writeCSVRecords function must be an"+\
                    "iterable composed of iterables.")
  if type(mainFilePath) is not str:
    raise TypeError("Argument mainFilePath to writeCSVRecords function "+\
                    " must be a string")
  if tempFilePath is None:
    with open(mainFilePath,"w",newline="") as file:
      fWriter=writer(file)
      fWriter.writerows(records)
  elif type(tempFilePath) is str:
    writeCSVRecords(records,tempFilePath)
    writeCSVRecords(records,mainFilePath)
    remove(tempFilePath)
  else:
    raise TypeError("Argument tempFilePath to writeCSVRecords function"+\
                    " must be string or none.")

def getHistory():
  """Retrives the history of the application (list of tuples containing
  equations matrix and solution) from history.dat
  Returns:
    A list of records (a tuple of Gaussian Equation Matrix and its solution).
    An empty list is returned if the file doesn't exist or contains no data"""
  try:
    with open(HISTORY_FILE_NAME,"rb") as historyFileRead:
      return load(historyFileRead)
  except (FileNotFoundError,EOFError):
    return []
  
def addRecordToHistory(equations,solution,maxLimit=None):
  """
  Adds a record (a tuple of Gaussian Equation Matrix and its solution) to the 
  list of records in history.dat. Removes oldest record(s) if no. of records 
  exceeds maxLimit (if specified)
  Args:
    equations: A Gaussian Equation Matrix or a MatrixWrapper representing a 
    Gaussian Equation Matrix
    solution: A list representing the solution of the matrix or None 
    representing no/infinite solution
    maxLimit: An int representing the maximum no. of history records
    to be stored or None to represent no limit.
  """
  if isinstance(equations,MatrixWrapper):
    eqnsMatrix=equations.matrix
  else:
    eqnsMatrix=equations
  if not isGaussianEqnMatrix(eqnsMatrix):
    raise TypeError("Argument data to addRecordToHistory function"+\
                    " must be a Gaussian Equation Matrix or"+\
                    " a MatrixWrapper reprenting one.")
  if solution is not None and type(solution) is not list:
    raise TypeError("Argument solution to addGaussianMatrixToHistory"+\
                    " function must be a list.")
  if maxLimit is not None and type(maxLimit) is not int:
    raise TypeError("Argument maxLimit to addRecordToHistory function"+\
                    " must be a an int.")
  if type(maxLimit) is int and maxLimit<0:
    raise ValueError("Argument maxLimit to addRecordToHistory function"+\
                     " must be non-negative.")
  if solution is not None:
    for number in solution:
      if type(number) not in (int,float,complex):
        raise TypeError("List passed as argument to solution parameter of"+\
                        " addGaussianMatrixToHistory function must contain"+\
                        " int,float or complex only.")
    if len(solution)!=len(eqnsMatrix):
      raise ValueError("No. of equations in the Gaussian Matrix and the"+\
                       " no. of variables solved for don't match.")
    
  record=(eqnsMatrix,solution)
  history=getHistory()
  history.append(record)
  if maxLimit is not None and len(history)>maxLimit:
    del history[:len(history)-maxLimit]
  with open(HISTORY_TEMP_FILE_NAME,"wb") as tempFileWrite:
    dump(history,tempFileWrite)
  with open(HISTORY_FILE_NAME,"wb") as historyFileWrite:
    dump(history,historyFileWrite)
  remove(HISTORY_TEMP_FILE_NAME)

def clearHistory():
  """Deletes all the history records stored in history.dat i.e.
  only an empty list will be left in history.dat"""
  with open(HISTORY_FILE_NAME,"wb") as historyFileWrite:
    dump([],historyFileWrite)

def truncateHistory(maxRecords):
  """Clears oldest history records in history.dat if required so that the no. 
  of history records is no more than the maximum number specified
  
  Args:
    maxRecords: The maximum number of records to keep (non-negative integer) 
  """
  if type(maxRecords) is not int:
    raise TypeError("Argument maxRecords to truncateHistory function must be"+\
                    " an int.")
  if maxRecords<0:
    raise ValueError("Argument maxRecords to truncateHistory function must be"+\
                     " a non-negative integer.")
  history=getHistory()
  if len(history)<=maxRecords:
    return
  del history[:len(history)-maxRecords]
  with open(HISTORY_TEMP_FILE_NAME,"wb") as tempFileWrite:
    dump(history,tempFileWrite)
  with open(HISTORY_FILE_NAME,"wb") as historyFileWrite:
    dump(history,historyFileWrite)
  remove(HISTORY_TEMP_FILE_NAME)

def getSettings():
  """Get the current value of settings stored in settings.csv
  Returns:
    A dictionary of the format {setting:value} where setting and 
    value both are strings"""
  result={}
  try:
    with open(SETTINGS_FILE_NAME,"r",newline="") as settingsFileRead:
      settingsReader=reader(settingsFileRead)
      for record in settingsReader:
        if settingsReader.line_num==1:
          continue
        result[record[0]]=record[1]
  except FileNotFoundError:
    pass
  return result

def writeSettings(settings):
  """Writes a new set of settings to settings.csv. 
  All other settings are removed.
  Args:
    settings:A dictionary containing the new settings in the format 
    {setting:value} where setting is a string and value can have 
    any data type
  """
  if type(settings) is not dict:
    raise TypeError("Argument settings to writeSettings function"+\
                    " must be a dict.")
  records=[SETTINGS_HEADERS]
  for setting,value in settings.items():
    if type(setting) is not str:
      raise TypeError("Dict passed as argument to writeSettings function must"+\
                      " have only strings as keys.")
    records.append([setting,value])
  writeCSVRecords(records,SETTINGS_FILE_NAME,SETTINGS_TEMP_FILE_NAME)

def updateSettings(updations):
  """Updates the settings with a new set of settings in settings.csv. 
  Existing matching settings are overwritten but other settings 
  remain.
  Args:
    updations:A dictionary containing the new settings in the format 
    {setting:value} where setting is a string and value can have 
    any data type
  """
  if type(updations) is not dict:
    raise TypeError("Argument updations to updateSettings function must be"+\
                    " a dict.")
  for setting in updations:
    if type(setting) is not str:
      raise TypeError("Dict passed as argument to updateSettings function"+\
                      " must have only strings as keys.")
  settings=getSettings()
  settings.update(updations)
  writeSettings(settings)

def removeSetting(setting):
  """Removes a particular setting from settings.csv if it exists.
  Args:
    setting: A string specifying the setting to be removed.
  """
  if type(setting) is not str:
    raise TypeError("Argument to removeSetting function must be string.")
  result=[]
  try:
    with open(SETTINGS_FILE_NAME,"r",newline="") as settingsFileRead:
      settingsReader=reader(settingsFileRead)
      for record in settingsReader:
        if settingsReader.line_num==1 or record[0]!=setting:
          result.append(record)
  except FileNotFoundError:
    pass
  else:
    writeCSVRecords(result,SETTINGS_FILE_NAME,SETTINGS_TEMP_FILE_NAME)