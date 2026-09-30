"""Main file for equation solver program."""

from equations import isGaussianEqnMatrix,solveEquations
from number_utilities import normalizeNumber, wholeNumberToSubscript
from tkinter import BOTH, BOTTOM, HORIZONTAL, NW,  RIGHT, TOP, LEFT, \
  VERTICAL,X, Y, CENTER, Tk, PhotoImage, Canvas, BooleanVar, StringVar, \
  Entry as OldEntry
from tkinter.messagebox import showerror
from tkinter.ttk import Frame, Scrollbar, Button, Entry,Label, Checkbutton, \
  Combobox, Notebook
from tkinter.font import nametofont
from file_handling import EQN_COUNT, IMAGINARY_UNIT, MAX_HISTORY, \
  getSettings,updateSettings, getHistory, clearHistory, \
  addRecordToHistory, truncateHistory

NUMBER_VALIDITY_TEXT=" must be valid numbers (int,float,complex)."
COEFFICIENT_ERROR_MESSAGE="Coefficients for variables"+NUMBER_VALIDITY_TEXT
CONSTANT_RHS_ERROR_MESSAGE="Constant RHS"+NUMBER_VALIDITY_TEXT
COMPLEX_NUMBER_INFO_TEXT=\
  "Complex numbers must be input as a+bi, a-bi, bi or -bi"+\
  " where a,b are real numbers, b is non-negative and "+\
  "i (j also accepted) represents square root of -1\n"
NO_OR_INF_SOLUTIONS="No or infinite solutions"
NUMBER_TYPES=(int,float,complex)

settings=getSettings()
settingsDefaults={
  EQN_COUNT:"3",
  IMAGINARY_UNIT:"i",
  MAX_HISTORY: "5"
}
if MAX_HISTORY in settings:
  truncateHistory(int(settings[MAX_HISTORY]))
else:
  truncateHistory(int(settingsDefaults[MAX_HISTORY]))
history=getHistory()
root = Tk()
root.title("Equation Solver")
smallIcon=PhotoImage(file="icon-small.png")
largeIcon=PhotoImage(file="icon-large.png")
root.iconphoto(False,largeIcon,smallIcon)
defaultFont=nametofont("TkDefaultFont")
defaultFont.config(size=14)
root.option_add("*TCombobox*Listbox*Font",defaultFont)

def setEntry(entry, value):
  """Set the text of an Entry entry to value
  
  Args:
    entry: 
      The Entry whose text is to be set
    value: 
      The value with which the Entry's text is to be set
  """
  if not isinstance(entry,OldEntry):
    raise TypeError("First argument to setEntry must be an instance of"+
                    " tkinter.Entry")
  entry.delete(0,len(entry.get()))
  entry.insert(0,str(value))

def getInputChecker(types):
  """Create an input checker function which checks 
  whether the given string can be converted to one of the given types.
  
  Args:
    types: A sequence (list/tuple) of types, to one of which it
    should be possible to convert the string being checked 
    by the checker function
  Returns:
    A function of the signature checker(text) where text is 
    a string and return type bool which is True if text 
    can be converted to one of the types in types and False otherwise
  """
  def checker(text):
    for typ in types:
      try:
        if typ is complex:
          complex(text.replace("i","j"))
        else:
          typ(text)
      except:
        pass
      else:
        return True
    return False
  return checker

numberValidation=root.register(getInputChecker(NUMBER_TYPES))

def positiveIntegerChecker(text):
  """Check whether text, a str, represents a positive 
  integer and accordingly returns a bool."""
  try:
    num=int(text)
    return num>0
  except:
    return False

positiveIntegerCheckerValidation=root.register(positiveIntegerChecker)

def nonNegativeIntegerChecker(text):
  """Check whether text, a str, represents a non-negative integer
  and accordingly returns a bool."""
  try:
    num=int(text)
    return num>=0
  except:
    return False
  
nonNegativeIntegerCheckerValidation=root.register(nonNegativeIntegerChecker)

def getInvalidInputResetter(entry,message):
  """Create a resetter to reset a text of an entry to a 
  new value (on invalid input) and show appropriate error message
  Args:
    entry: An Entry for which the resetter has to be created
    message: A string which is to be shown as the message in messagebox on  
             invalid input before stating that the input value is invalid.
  Returns:
    A function of the signature resetter(invalidValue,
    newValue) where invalidValue is the invalid value input 
    by the user and the newValue is the value to which the 
    text of the entry is to be reset."""
  def resetter(invalidValue,newValue):
    showerror(title="Invalid input",message=str(message)+" "+
              str(invalidValue)+" is invalid.", parent=root)
    setEntry(entry,str(newValue))
    entry.focus()
  return resetter

def numberToText(number):
  """Converts a number to its most appropriate numerical representation 
  followed by conversion to its string form in required format
  Args:
    number:The int,float,complex of str representing number to converted
  Returns:
    The modified string form of the number with j substituted by the symbol 
    (i or j) specified by user for imaginary unit"""

  normalNum=normalizeNumber(number)
  return str(normalNum).replace("j",imaginaryUnitVariable.get())
  
def solutionToText(solution):
  """Converts solution of a system of equations to text form
  and returns the same
  Args:
    solution: None or list representing solution of system of linear 
    equations
  Returns:
    A string of the format "x₁=<value1>,..." or "No or infinite solutions" 
    representing the solution
  """
  #TODO: Interpret new format
  resultText=""
  """if solution is not None:
    if type(solution) is not list:
      raise TypeError("Argument solution to solutionToText function"+\
                      " must be None or list.")
    for element in solution:
      if type(element) not in NUMBER_TYPES:
        raise TypeError("Elements of argument solution to solutionToText"+\
                        " function must be numbers.")
    for i in range(1,len(solution)+1):
      numberString=numberToText(solution[i-1])
      resultText+=("x"+wholeNumberToSubscript(i)+"="+numberString+", ")
    resultText=resultText[:-2]
  else:
    resultText=NO_OR_INF_SOLUTIONS
  return resultText"""

topFrame=Frame(root)
topFrame.pack(fill=BOTH,expand=1)

topNotebook=Notebook(topFrame)
topNotebook.pack(side=LEFT,fill=BOTH,expand=1)

eqnSolverOuterFrame=Frame(topNotebook)
eqnSolverCanvas=Canvas(eqnSolverOuterFrame)
eqnSolverVerticalScrollbar=Scrollbar(eqnSolverOuterFrame,orient=VERTICAL,
                                     command=eqnSolverCanvas.yview)
eqnSolverVerticalScrollbar.pack(side=RIGHT,fill=Y)
eqnSolverHorizontalScrollbar=Scrollbar(eqnSolverOuterFrame,orient=HORIZONTAL,
                                       command=eqnSolverCanvas.xview)
eqnSolverHorizontalScrollbar.pack(side=BOTTOM,fill=X)
eqnSolverCanvas.config(yscrollcommand=eqnSolverVerticalScrollbar.set,
                       xscrollcommand=eqnSolverHorizontalScrollbar.set)
eqnSolverFrame=Frame(eqnSolverCanvas,padding=10)
eqnSolverCanvas.create_window(0,0,window=eqnSolverFrame,anchor=NW)
eqnSolverCanvas.pack(side=LEFT,fill=BOTH,expand=1)
topNotebook.add(eqnSolverOuterFrame,text="Equation Solver")

eqnSolverUpperConfigFrame=Frame(eqnSolverFrame,padding=3)
eqnSolverUpperConfigFrame.pack(side=TOP)
equationCountLabel=Label(eqnSolverUpperConfigFrame, 
                         text="Enter the no. of equations: ",
                         font=defaultFont)
equationCountLabel.pack(side=LEFT)
equationCountEntry=Entry(eqnSolverUpperConfigFrame, validate="focusout",
                         validatecommand=\
                         (positiveIntegerCheckerValidation, "%P"),
                         font=defaultFont)
equationCountEntry.pack(side=LEFT)
equationCountApplyButton=Button(eqnSolverUpperConfigFrame,text="Apply")
equationCountApplyButton.pack(side=LEFT)
equationCountSetDefaultButton=Button(eqnSolverUpperConfigFrame,
                                     text="Set As Default")
equationCountSetDefaultButton.pack(side=LEFT)
eqnSolverLowerConfigFrame=Frame(eqnSolverFrame)
eqnSolverLowerConfigFrame.pack(side=TOP)
dontResizeVariable=BooleanVar(value=False)
dontResizeCheckbutton=Checkbutton(eqnSolverLowerConfigFrame,
                                  text="Don't resize window "+
                                  "on clicking Apply button",
                                  variable=dontResizeVariable)
dontResizeCheckbutton.pack(side=LEFT)
complexNumberInfoLabel=Label(eqnSolverFrame,text=COMPLEX_NUMBER_INFO_TEXT,
                             font=defaultFont,justify=CENTER)
complexNumberInfoLabel.pack(side=TOP)
equationsFrame=Frame(eqnSolverFrame,padding=3)
equationsFrame.pack(side=TOP)

def onEqnSolverFrameConfigure(_):
  """Event handler for resizing of the eqnSolverFrame, the frame containing the
  widgets for the equation solver part of application
  
  Args:
    _: The event of resizing of eqnSolverFrame
  """
  #Code idea from https://coderslegacy.com/python/make-scrollable-frame-in-tkinter/ (for scrollable
  #frame implementation)
  complexNumberInfoLabel.config(text="")
  reqScrollWidth=eqnSolverFrame.winfo_reqwidth()
  if reqScrollWidth != eqnSolverCanvas.winfo_width():
    eqnSolverCanvas.config(width = reqScrollWidth)

  complexNumberInfoLabel.config(wraplength=min(500,reqScrollWidth),
                                text=COMPLEX_NUMBER_INFO_TEXT)

  reqScrollHeight=eqnSolverFrame.winfo_reqheight()
  if reqScrollHeight != eqnSolverCanvas.winfo_height():
    eqnSolverCanvas.config(height = reqScrollHeight)

  eqnSolverCanvas.config(scrollregion=(0,0,reqScrollWidth,reqScrollHeight))

eqnSolverFrame.bind("<Configure>",onEqnSolverFrameConfigure)

equationsFrameLHS=Frame(equationsFrame)
equationsFrameLHS.pack(side=LEFT)
equationsFrameRHS=Frame(equationsFrame)
equationsFrameRHS.pack(side=LEFT)

#equationsFrameLHSWidgets list consists of lists representing rows (equations)
#Each row in turn contains lists representing terms.
#Each term is of the form [entry,label] where entry is the textbox for
#the coefficient while label is the label for the variable and + sign if needed
equationsFrameLHSWidgets=[]

#equationsFrameRHSWidgets list consists of lists representing rows (equations)
#Each row contains [label,entry] where label is label for = sign while entry is
#textbox for RHS constant value.
equationsFrameRHSWidgets=[]

def resizeWindow():
  """Set the width and height of the root window according 
  to the required width of topFrame, the frame 
  containing most of the widgets used in the application and height of 
  eqnSolverFrame."""
  root.update_idletasks()
  reqWindowWidth=min(topFrame.winfo_reqwidth()+30,root.winfo_screenwidth()-200)
  reqWindowHeight=min(eqnSolverFrame.winfo_reqheight()+30, 
                      root.winfo_screenheight()-200)
  root.geometry(str(reqWindowWidth)+"x"+str(reqWindowHeight))

def resetInvalidEquationCountEntry():
  """Reset the equation count field on invalid input."""
  showerror(title="Invalid input",
            message="No. of equations must be a positive integer.",
            parent=root)
  setEntry(equationCountEntry,str(len(equationsFrameLHSWidgets)))
  equationCountEntry.focus()

equationCountEntry.config(invalidcommand=
                          (root.register(resetInvalidEquationCountEntry),))

def resetEquations():
  """Resets all the coefficients and constant terms in the 
  equations to 0 and also clears the solution label"""
  for row in equationsFrameLHSWidgets:
    for entry,_ in row:
      setEntry(entry,"0")
  for _,entry in equationsFrameRHSWidgets:
    setEntry(entry,"0")
  solutionLabel.config(text="\n")

solutionFrame=Frame(eqnSolverFrame,padding=3)
solutionFrame.pack(side=TOP)
eqnImaginaryUnitFrame=Frame(solutionFrame)
eqnImaginaryUnitFrame.pack(side=TOP)
eqnImaginaryUnitLabel=Label(eqnImaginaryUnitFrame,
                            text="Display imaginary unit as: ")
eqnImaginaryUnitLabel.pack(side=LEFT)
eqnImaginaryUnitCombobox=Combobox(eqnImaginaryUnitFrame,values=("i","j"),
                               font=defaultFont,state="readonly")
eqnImaginaryUnitCombobox.pack(side=LEFT)
solutionFrameButtonsFrame=Frame(solutionFrame)
solutionFrameButtonsFrame.pack(side=TOP)
solveButton=Button(solutionFrameButtonsFrame,text="Solve")
solveButton.pack(side=LEFT)
Label(solutionFrameButtonsFrame,text=" ").pack(side=LEFT)
resetButton=Button(solutionFrameButtonsFrame, text="Reset",
                   command=resetEquations)
resetButton.pack(side=LEFT)
solutionLabel=Label(solutionFrame, text="\n", font=defaultFont,padding=3,
                    wraplength=500)
solutionLabel.pack()

historyOuterFrame=Frame(topNotebook)
historyCanvas=Canvas(historyOuterFrame)
historyVerticalScrollbar=Scrollbar(historyOuterFrame,orient=VERTICAL,
                                     command=historyCanvas.yview)
historyVerticalScrollbar.pack(side=RIGHT,fill=Y)
historyHorizontalScrollbar=Scrollbar(historyOuterFrame,orient=HORIZONTAL,
                                       command=historyCanvas.xview)
historyHorizontalScrollbar.pack(side=BOTTOM,fill=X)
historyCanvas.config(yscrollcommand=historyVerticalScrollbar.set,
                     xscrollcommand=historyHorizontalScrollbar.set)
historyFrame=Frame(historyCanvas,padding=10)
historyCanvas.create_window(0,0,window=historyFrame,
                            anchor=NW)
historyCanvas.pack(side=LEFT,fill=BOTH,expand=1)
topNotebook.add(historyOuterFrame,text="History")

maxHistoryInfoLabel=Label(historyFrame,text="Maximum history refers to the "+\
                          "maximum number of systems of equations stored.",wraplength=500,
                          font=defaultFont)
maxHistoryInfoLabel.pack(side=TOP)
maxHistoryLabel=Label(historyFrame, 
                      text="Enter maximum history records"+\
                        " (0 or positive integer): ",
                      font=defaultFont)
maxHistoryLabel.pack(side=TOP)
historyConfigFrame=Frame(historyFrame,padding=3)
historyConfigFrame.pack(side=TOP)
maxHistoryEntry=Entry(historyConfigFrame, validate="focusout",
                         validatecommand=\
                          (nonNegativeIntegerCheckerValidation, "%P"),
                         font=defaultFont)
maxHistoryEntry.pack(side=LEFT)
maxHistoryApplyButton=Button(historyConfigFrame,text="Apply")
maxHistoryApplyButton.pack(side=LEFT)
clearHistoryButton=Button(historyFrame,text="Clear History")
clearHistoryButton.pack(side=TOP)

historyImaginaryUnitFrame=Frame(historyFrame)
historyImaginaryUnitFrame.pack(side=TOP)
historyImaginaryUnitLabel=Label(historyImaginaryUnitFrame,
                                text="Display imaginary unit as: ")
historyImaginaryUnitLabel.pack(side=LEFT)
historyImaginaryUnitCombobox=Combobox(historyImaginaryUnitFrame,
                                      values=("i","j"),
                                      font=defaultFont,state="readonly")
historyImaginaryUnitCombobox.pack(side=LEFT)

historyListFrame=Frame(historyFrame,padding=3)
historyListFrame.pack(side=TOP)
historyListButtons=[]

def onHistoryFrameConfigure(_):
  """Event handler for resizing of the historyFrame
  
  Args:
    _: The event of resizing of historyFrame
  """
  #Code idea from https://coderslegacy.com/python/make-scrollable-frame-in-tkinter/ (for scrollable
  #frame implementation)
  reqScrollWidth=historyFrame.winfo_reqwidth()
  if reqScrollWidth != historyCanvas.winfo_width():
    historyCanvas.config(width = reqScrollWidth)

  reqScrollHeight=historyFrame.winfo_reqheight()
  if reqScrollHeight != historyCanvas.winfo_height():
    historyCanvas.config(height = reqScrollHeight)
  historyCanvas.config(scrollregion=(0,0,reqScrollWidth,reqScrollHeight))

historyFrame.bind("<Configure>",onHistoryFrameConfigure)

def resetInvalidMaxHistoryEntry():
  """Reset the maximum history (no. of systems of equations stored) field
  on invalid input."""
  showerror(title="Invalid input",
            message="Maximum history (no. of systems of equations stored)"+\
              " must be a non-negative integer.",
            parent=root)
  setEntry(maxHistoryEntry,str(settings[MAX_HISTORY]))

maxHistoryEntry.config(invalidcommand=
                          (root.register(resetInvalidMaxHistoryEntry),))

def truncateHistoryButtons(maxRecords):
  """Removes oldest history record buttons so that the total no. of buttons is 
  not more than maxRecords (a non-negative integer).
  To clear all buttons, pass 0 as argument to maxRecords."""
  if type(maxRecords) is not int:
    raise TypeError("Argument maxRecords to truncateHistoryButtons"+\
                    " function must be an integer")
  if maxRecords<0:
    raise ValueError("Argument maxRecords to truncateHistoryButtons"+\
                    " function must be a non-negative integer")
  if len(historyListButtons)<=maxRecords:
    return
  surplus=len(historyListButtons)-maxRecords
  for i in range(0,surplus):
    recordButton=historyListButtons[i]
    recordButton.pack_forget()
  del historyListButtons[:surplus]
  del history[:surplus]

def loadEquations(equations):
  """Loads into the equation solver frame the equations passed and its solution
  Args:
    equations: A list (Gaussian Equation Matrix) representing the equations."""
  #TODO: Interpret solution correctly
  if not isGaussianEqnMatrix(equations):
    raise TypeError("First element of argument historyRecord to"+\
                    " loadHistoryRecord must be"+\
                    " a Gaussian Linear Equation Matrix (row operations"+\
                    " based) which is a list and all its elements are list"+\
                    " and no. of columns is 1 more than the no. of rows.")
  setEntry(equationCountEntry,str(len(equations)))
  renderEquationsWidgets()
  for i in range(1,len(equations)+1):
    for j in range(1,len(equations)+1):
      coeffEntry=equationsFrameLHSWidgets[i-1][j-1][0]
      setEntry(coeffEntry,equations[i-1][j-1])
    constantEntry=equationsFrameRHSWidgets[i-1][1]
    setEntry(constantEntry,equations[i-1][-1])
  solveAndShowSolution()
  topNotebook.select(eqnSolverOuterFrame)

def addHistoryRecordButton(historyRecord):
  """Creates a button corresponding to a history record historyRecord
  and adds it to the list historyListButtons and to historyListFrame
  Args:
    historyRecord: A tuple (list also allowed) corresponding to a record of 
    history. The tuple is of the form (equations,solution) representing the 
    equations (Gaussian Equation Matrix) and their solution (None or list)"""
  #TODO: Interpret solution correctly
  if type(historyRecord) not in (list,tuple):
    raise TypeError("Argument historyRecord to addHistoryRecordButton"+\
                    " must be tuple (or list).")
  if len(historyRecord)!=2:
    raise ValueError("Argument historyRecord (tuple/list) to "+\
                     "addHistoryRecordButton function must have "+\
                     "exactly 2 elements.")
  equations,solution=historyRecord
  if not isGaussianEqnMatrix(equations):
    raise TypeError("First element of argument historyRecord to"+\
                    " addHistoryRecordButton must be"+\
                    " a Gaussian Linear Equation Matrix (row operations"+\
                    " based) which is a list and all its elements are list"+\
                    " and no. of columns is 1 more than the no. of rows.")
  if solution is not None:
    if type(solution) is not list:
      raise TypeError("Second element of argument historyRecord to"+\
                    " addHistoryRecordButton must be a list.")
    if len(solution)!=len(equations):
      raise ValueError("Both elements of argument historyRecord"+\
                      " to addHistoryRecordButton function must have"+\
                      " same length.")
    for element in solution:
      if type(element) not in NUMBER_TYPES:
        raise TypeError("All elements of second element of argument"+\
                        " historyRecord to addHistoryRecordButton function"+\
                        " must be int,float or complex.")
  buttonText=""
  for row in equations:
    for j in range(1,len(row)):
      number=row[j-1]
      buttonText+=numberToText(number)+"x"+wholeNumberToSubscript(j)+" + "
    buttonText=buttonText[:-2]+"= "+numberToText(row[-1])+"\n"
  buttonText+="\n"
  solutionText=solutionToText(solution)
  wrapped=0
  i=0
  toBeWrapped=0
  while True:
    i=solutionText.find(", ",i)
    if i==-1:
      break
    toBeWrapped=i+2-wrapped
    if toBeWrapped>=30:
      solutionText=solutionText[:i+2]+"\n"+solutionText[i+2:]
      wrapped+=toBeWrapped+1
      i+=1
    i+=2
  buttonText+=solutionText
  recordButton=Button(historyListFrame,text=buttonText,
                      command=lambda:loadEquations(equations))
  recordButton.pack(side=BOTTOM,fill=BOTH)
  historyListButtons.append(recordButton)

def solveAndShowSolution():
  """Solve the equations and show the solution 
  in the solution label in eqnSolverFrame.
  Returns:
    A tuple of the form (equations,solution) representing the 
    equations (Gaussian Equation Matrix) and their solution (None or list)
  Raises:
    ValueError: 
      Raised if any of the coefficients/constant term is not a valid number """
  root.focus()
  matrix=[]
  equationsCount=len(equationsFrameLHSWidgets)
  for i in range(1,equationsCount+1):
    matrixRow=[]
    widgetsRow=equationsFrameLHSWidgets[i-1]
    for j in range(1,equationsCount+1):
      entry=widgetsRow[j-1][0]
      matrixRow.append(normalizeNumber(entry.get().replace("i","j")))
    constantEntry=equationsFrameRHSWidgets[i-1][1]
    matrixRow.append(normalizeNumber(constantEntry.get().replace("i","j")))
    matrix.append(matrixRow)
  solution=solveEquations(matrix)
  resultText=solutionToText(solution)
  solutionLabel.config(text=resultText)
  return (matrix,solution)
  
def onSolveButtonClick():
  """Event handler to be called when the Solve button in equationSolverFrame 
  is clicked. Solves the equations and show the solution in the solution label 
  in eqnSolverFrame and if equations have changed, adds the corresponding 
  record to history and displays button of that record in history tab."""
  #TODO: Interpret solution correctly
  try:
    equations,solution=solveAndShowSolution()
  except ValueError:
    return
  if MAX_HISTORY in settings:
    maxRecords=int(settings[MAX_HISTORY])
  else:
    maxRecords=5
  if len(history)>0:
    previousRecord=history[-1]
  else:
    previousRecord=None
  if previousRecord is None or previousRecord[0]!=equations:
    addRecordToHistory(equations,solution,maxRecords)
    historyRecord=(equations,solution)
    history.append(historyRecord)
    addHistoryRecordButton(historyRecord)
    truncateHistoryButtons(maxRecords)
  
solveButton.config(command=onSolveButtonClick)

def renderEquationsWidgets():
  """Creates/deletes necessary Entry widgets for the 
  coefficients and constant RHS of equations and Label 
  widgets for variables and + = before the mainloop is 
  called as well as when the no. of equations is changed."""
  root.focus()
  global equationsFrameLHSWidgets
  global equationsFrameRHSWidgets
  oldEquationsCount=len(equationsFrameLHSWidgets)
  try:
    newEquationsCount=int(equationCountEntry.get())
  except:
    newEquationsCount=int(settings.get(EQN_COUNT,3)) if oldEquationsCount==0 \
      else oldEquationsCount
  
  if newEquationsCount<=0:
    return
  if newEquationsCount>oldEquationsCount:
    for i in range(1,newEquationsCount+1):
      row=None
      if i>oldEquationsCount:
        row=[]
        equationsFrameLHSWidgets.append(row)
        constantEntry=Entry(equationsFrameRHS,
                            validate="focusout",
                            validatecommand=(numberValidation,"%P"),
                            font=defaultFont)
        constantEntry.insert(0,"0")
        constantEntryInvalidationFunction=\
          getInvalidInputResetter(constantEntry,CONSTANT_RHS_ERROR_MESSAGE)
        constantEntry.config(invalidcommand=
          (root.register(constantEntryInvalidationFunction),"%P","0"))
        constantEntry.grid(row=i-1,column=1)
        equalityLabel=Label(equationsFrameRHS,text=" = ",font=defaultFont)
        equalityLabel.grid(row=i-1,column=0)
        equationsFrameRHSWidgets.append([equalityLabel,constantEntry])
      else:
        row=equationsFrameLHSWidgets[i-1]
        lastLabel=row[-1][1]
        lastLabel.config(text=lastLabel.cget("text")+" + ")
      for j in range(oldEquationsCount+1 if i<=oldEquationsCount \
                     else 1,newEquationsCount+1):
        entry=Entry(equationsFrameLHS,validate="focusout",
                    validatecommand=(numberValidation,"%P"),
                    font=defaultFont)
        entry.insert(0,"0")
        entryInvalidationFunction=\
          getInvalidInputResetter(entry,COEFFICIENT_ERROR_MESSAGE)
        entry.config(invalidcommand=
                     (root.register(entryInvalidationFunction),"%P","0"))
        label=Label(equationsFrameLHS,text="x"+wholeNumberToSubscript(j)+
                    (" + "  if j!=newEquationsCount else ""),font=defaultFont)
        entry.grid(row=i-1,column=2*(j-1))
        label.grid(row=i-1,column=2*j-1)
        row.append([entry,label])
  elif newEquationsCount<oldEquationsCount:
    for i in range(1, oldEquationsCount+1):
      row=equationsFrameLHSWidgets[i-1]
      for j in range(1,oldEquationsCount+1):
          entry,label=row[j-1]
          if i>newEquationsCount or j>newEquationsCount:
            entry.grid_forget()
            label.grid_forget()
          elif j==newEquationsCount:
            label.config(text=label.cget("text").replace(" + ",""))
      if i>newEquationsCount:
        equalityLabel,constantEntry=equationsFrameRHSWidgets[i-1]
        equalityLabel.grid_forget()
        constantEntry.grid_forget()
      else:
        del row[newEquationsCount:oldEquationsCount]
    del equationsFrameLHSWidgets[newEquationsCount:oldEquationsCount]
    del equationsFrameRHSWidgets[newEquationsCount:oldEquationsCount]
  if newEquationsCount!=oldEquationsCount:
    solutionLabel.config(text="\n")
  if not dontResizeVariable.get():
    resizeWindow()

equationCountApplyButton.config(command=renderEquationsWidgets)

imaginaryUnitVariable=StringVar(value="i")

#Format followed below is {settingName:mapping} where mapping is
#a widget or value holder corresponding to settingName
settingsMappings={
  EQN_COUNT:equationCountEntry,
  IMAGINARY_UNIT:imaginaryUnitVariable,
  MAX_HISTORY:maxHistoryEntry
}

for settingName in settingsMappings:
  mapping=settingsMappings[settingName]
  default=settingsDefaults[settingName]
  value=settings.get(settingName,default)
  if isinstance(mapping,OldEntry):
    setEntry(mapping,value)
  elif isinstance(mapping,StringVar):
    mapping.set(value)
  settings[settingName]=value

def getSettingChanger(settingName):
  """Creates a function which sets the value of a setting (stored in 
  settings.csv and settings dictionary) to the value which can be retrieved 
  from the corresponding widget/value holder (referred to as a mapping)
  
  Args:
    settingName: A string corresponding to the setting to be set
  Returns:
    A function which sets the value corresponding to settingName to the value 
    retrieved from the mapping when called
  """
  if type(settingName) is not str:
    raise TypeError("Argument settingName to getSettingChanger function"+\
                    " must be a string.")
  mapping=settingsMappings[settingName]
  def settingChanger():
    value=mapping.get()
    updateSettings({settingName:value})
    settings[settingName]=str(value)
  return settingChanger

maxHistorySettingChanger=getSettingChanger(MAX_HISTORY)
imaginaryUnitVariableChanger=getSettingChanger(IMAGINARY_UNIT)

for record in history:
  addHistoryRecordButton(record)

def onMaxHistoryApply():
  """Event handler to be called when the Apply button is clicked 
  corresponding to the maximum history. The maximum history setting is changed 
  and oldest history records are deleted if necessary so that there are no more 
  records than maximum history. The corresponding buttons are also deleted."""
  maxHistorySettingChanger()
  maxRecords=int(settings[MAX_HISTORY])
  truncateHistoryButtons(maxRecords)
  truncateHistory(maxRecords)

def onClearHistoryButtonClick():
  """Event handler to be called when Clear History button is clicked. 
  All history records are deleted and so are the history buttons."""
  clearHistory()
  truncateHistoryButtons(0)

def correctImaginaryUnit(text):
  """Replaces all instances of i and j in text, a string, with value of 
  imaginaryUnitVariable and returns the new string."""
  if type(text) is not str:
    raise TypeError("Argument text to correctImaginaryUnitVariable"+\
                    " function must be str.")
  result=text.replace("i",imaginaryUnitVariable.get())\
    .replace("j",imaginaryUnitVariable.get())
  return result

def onImaginaryUnitVariableChange(_name,_index,_mode):
  """Event handler to be called when the value of imaginaryUnitVariable 
  is changed. The corresponding setting is updated and the solution label and
  history buttons are also updated."""
  imaginaryUnitVariableChanger()
  newSolutionLabelText=correctImaginaryUnit(solutionLabel.cget("text"))
  solutionLabel.config(text=newSolutionLabelText)
  for button in historyListButtons:
    oldButtonText=button.cget("text")
    newButtonText=correctImaginaryUnit(oldButtonText)
    button.config(text=newButtonText)

equationCountSetDefaultButton.config(command=getSettingChanger(EQN_COUNT))
eqnImaginaryUnitCombobox.config(textvariable=imaginaryUnitVariable)
historyImaginaryUnitCombobox.config(textvariable=imaginaryUnitVariable)
imaginaryUnitVariable.trace_add("write",onImaginaryUnitVariableChange)
maxHistoryApplyButton.config(command=onMaxHistoryApply)
clearHistoryButton.config(command=onClearHistoryButtonClick)

renderEquationsWidgets()
topNotebook.select(eqnSolverOuterFrame)
root.mainloop()