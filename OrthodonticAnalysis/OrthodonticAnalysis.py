import os
import unittest
import logging
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin

#
# OrthodonticAnalysis
#

class OrthodonticAnalysis(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Orthodontic Analysis"  # TODO: make this more human readable by adding spaces
    self.parent.categories = ["Orthodontics"]  # TODO: set categories (folders where the module shows up in the module selector)
    self.parent.dependencies = []  # TODO: add here list of module names that this module requires
    self.parent.contributors = ["João Vitor Coimbra (Federal University of Espírito Santo)",
      "Vinicius Batista (Federal University of Espírito Santo)",
      "Rafhael Milanezi (Federal University of Espírito Santo)",
      "Pedro Emmerich (Federal University of Rio de Janeiro)",
      "Lincoln Nojima (Federal University of Rio de Janeiro)"]
    self.parent.helpText = """The extension was developed to perform the most common dental analysis: model space discrepancies, Bolton and Peck and Peck.<br>
For instructions, see the <a href="https://github.com/OrthodonticAnalysis/SlicerOrthodonticAnalysis#orthodontic-analysis">extension documentation</a>.
In case of doubts, sent an e-mail to: pedroemmerich@hotmail.com<br>
"""
    # TODO: replace with organization, grant and thanks
    self.parent.acknowledgementText = """
"""

    # Additional initialization step after application startup is complete
    slicer.app.connect("startupCompleted()", registerSampleData)

#
# Register sample data sets in Sample Data module
#

def registerSampleData():
  """
  Add data sets to Sample Data module.
  """
  # It is always recommended to provide sample data for users to make it easy to try the module,
  # but if no sample data is available then this method (and associated startupCompeted signal connection) can be removed.

  import SampleData
  iconsPath = os.path.join(os.path.dirname(__file__), 'Resources/Icons')

  # To ensure that the source code repository remains small (can be downloaded and installed quickly)
  # it is recommended to store data sets that are larger than a few MB in a Github release.

  SampleData.SampleDataLogic.registerCustomSampleDataSource(
    # Category and sample name displayed in Sample Data module
    category='OrthodonticAnalysis',
    sampleName='TeethSurface',
    loadFileType='ModelFile',
    # Thumbnail should have size of approximately 260x280 pixels and stored in Resources/Icons folder.
    # It can be created by Screen Capture module, "Capture all views" option enabled, "Number of images" set to "Single".
    thumbnailFileName=os.path.join(iconsPath, 'TeethSurface.png'),
    # Download URL and target file name
    uris="https://github.com/lassoan/SlicerOrthodonticAnalysis/releases/download/TestingData/TeethSurface.vtp",
    fileNames='TeethSurface.vtp',
    # Checksum to ensure file integrity. Can be computed by this command:
    #  import hashlib; print(hashlib.sha256(open(filename, "rb").read()).hexdigest())
    checksums = 'SHA256:2f3d10acf0b378fd0ef0101fbe1171ed4d40efaba998608700b356613b967ae7',
    # This node name will be used when the data set is loaded
    nodeNames='TeethSurface'
  )

#
# OrthodonticAnalysisWidget
#

class OrthodonticAnalysisWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self.logic = None
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False
    self._inputPointsNode = None
    self._dockWidgetAdded = False

  def setup(self):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.setup(self)

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/OrthodonticAnalysis.ui'))
    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    # Set scene in MRML widgets. Make sure that in Qt designer the top-level qMRMLWidget's
    # "mrmlSceneChanged(vtkMRMLScene*)" signal in is connected to each MRML widget's.
    # "setMRMLScene(vtkMRMLScene*)" slot.
    uiWidget.setMRMLScene(slicer.mrmlScene)

    # Create logic class. Logic implements all computations that should be possible to run
    # in batch mode, without a graphical user interface.
    self.logic = OrthodonticAnalysisLogic()

    self.analysisButtonGroup = qt.QButtonGroup()
    self.analysisButtonGroup.setExclusive(True)
    self.analysisButtonGroup.addButton(self.ui.analysisSuperiorButton)
    self.analysisButtonGroup.addButton(self.ui.analysisInferiorButton)
    self.analysisButtonGroup.addButton(self.ui.analysisBoltonButton)
    self.analysisButtonGroup.addButton(self.ui.analysisPeckAndPeckButton)
    self.analysisButtonGroup.addButton(self.ui.analysisAllButton)

    # Point display dockable widget
    mainWindow = slicer.util.mainWindow()
    self.pointListDockWidget = qt.QDockWidget("Orthodontic Analysis Points", mainWindow)
    self.pointListDockWidget.setObjectName("OrthodonticAnalysisPoints")
    self.pointListDockWidget.setFeatures(qt.QDockWidget.DockWidgetClosable + qt.QDockWidget.DockWidgetMovable + qt.QDockWidget.DockWidgetFloatable)
    self.pointListTextBrowser = qt.QTextBrowser()
    self.pointListTextBrowser.lineWrapMode = qt.QTextBrowser.NoWrap
    self.pointListDockWidget.setWidget(self.pointListTextBrowser)
    slicer.w=self.pointListDockWidget
    slicer.t=self.pointListTextBrowser

    # Connections

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # These connections ensure that whenever user changes some settings on the GUI, that is saved in the MRML scene
    # (in the selected parameter node).
    self.analysisButtonGroup.connect("buttonClicked(QAbstractButton*)", self.updateParameterNodeFromGUI)
    self.ui.inputPointsSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.reportFolderPathLineEdit.connect("currentPathChanged(QString)", self.updateParameterNodeFromGUI)

    # Buttons
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Make sure parameter node is initialized (needed for module reload)
    self.initializeParameterNode()

  def showPointListWidget(self, show):
    if show:
      if self._dockWidgetAdded:
        self.pointListDockWidget.show()
      else:
        self._dockWidgetAdded = True
        slicer.util.mainWindow().addDockWidget(qt.Qt.RightDockWidgetArea, self.pointListDockWidget)
    else:
      if self.pointListDockWidget.parent():
        self.pointListDockWidget.close()

  def cleanup(self):
    """
    Called when the application closes and the module widget is destroyed.
    """
    slicer.util.mainWindow().removeDockWidget(self.pointListDockWidget)
    self.removeObservers()

  def enter(self):
    """
    Called each time the user opens this module.
    """
    # Make sure parameter node exists and observed
    self.initializeParameterNode()

  def exit(self):
    """
    Called each time the user opens a different module.
    """
    # Do not react to parameter node changes (GUI wlil be updated when the user enters into the module)
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self.showPointListWidget(False)

  def onSceneStartClose(self, caller, event):
    """
    Called just before the scene is closed.
    """
    # Parameter node will be reset, do not use it anymore
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    """
    Called just after the scene is closed.
    """
    # If this module is shown while the scene is closed then recreate a new parameter node immediately
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    """
    Ensure parameter node exists and observed.
    """
    # Parameter node stores all user choices in parameter values, node selections, etc.
    # so that when the scene is saved and reloaded, these settings are restored.

    self.setParameterNode(self.logic.getParameterNode())

    # Select default input nodes if nothing is selected yet to save a few clicks for the user
    if not self._parameterNode.GetNodeReference("InputPoints"):
      firstMarkupsFiducialNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLMarkupsFiducialNode")
      if firstMarkupsFiducialNode:
        self._parameterNode.SetNodeReferenceID("InputPoints", firstMarkupsFiducialNode.GetID())

  def setParameterNode(self, inputParameterNode):
    """
    Set and observe parameter node.
    Observation is needed because when the parameter node is changed then the GUI must be updated immediately.
    """

    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None:
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    # Initial GUI update
    self.updateGUIFromParameterNode()
    self.onInputPointsModified()

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True

    # Update widgets

    analysisType = self._parameterNode.GetParameter("AnalysisType")
    self.ui.analysisSuperiorButton.checked = analysisType=="Superior"
    self.ui.analysisInferiorButton.checked = analysisType=="Inferior"
    self.ui.analysisBoltonButton.checked = analysisType=="Bolton"
    self.ui.analysisPeckAndPeckButton.checked = analysisType=="PeckAndPeck"
    self.ui.analysisAllButton.checked = analysisType=="All"

    inputPointsNode = self._parameterNode.GetNodeReference("InputPoints") if self._parameterNode else None
    if self._inputPointsNode != inputPointsNode:
      if self._inputPointsNode is not None:
        self.removeObserver(self._inputPointsNode, slicer.vtkMRMLMarkupsNode.PointAddedEvent, self.onInputPointsModified)
        self.removeObserver(self._inputPointsNode, slicer.vtkMRMLMarkupsNode.PointRemovedEvent, self.onInputPointsModified)
        self.removeObserver(self._inputPointsNode, slicer.vtkMRMLMarkupsNode.PointPositionDefinedEvent, self.onInputPointsModified)
        self.removeObserver(self._inputPointsNode, slicer.vtkMRMLMarkupsNode.PointPositionUndefinedEvent, self.onInputPointsModified)
      self._inputPointsNode = inputPointsNode
      if inputPointsNode is not None:
        self.onInputPointsModified()
        self.addObserver(inputPointsNode, slicer.vtkMRMLMarkupsNode.PointAddedEvent, self.onInputPointsModified)
        self.addObserver(inputPointsNode, slicer.vtkMRMLMarkupsNode.PointRemovedEvent, self.onInputPointsModified)
        self.addObserver(inputPointsNode, slicer.vtkMRMLMarkupsNode.PointPositionDefinedEvent, self.onInputPointsModified)
        self.addObserver(inputPointsNode, slicer.vtkMRMLMarkupsNode.PointPositionUndefinedEvent, self.onInputPointsModified)

    self.ui.inputPointsSelector.setCurrentNode(self._parameterNode.GetNodeReference("InputPoints"))
    self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    self.ui.reportFolderPathLineEdit.currentPath = self._parameterNode.GetParameter("ReportFolder")

    # Update buttons states and tooltips
    if self._parameterNode.GetNodeReference("InputPoints") and self._parameterNode.GetParameter("ReportFolder"):
      self.ui.applyButton.toolTip = "Compute analysis results"
      self.ui.applyButton.enabled = True
    else:
      self.ui.applyButton.toolTip = "Select input markup points and select report folder"
      self.ui.applyButton.enabled = False

    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

    analysisType = "Superior"
    if self.ui.analysisSuperiorButton.checked:
      analysisType = "Superior"
    elif self.ui.analysisInferiorButton.checked:
      analysisType = "Inferior"
    elif self.ui.analysisBoltonButton.checked:
      analysisType = "Bolton"
    elif self.ui.analysisPeckAndPeckButton.checked:
      analysisType = "PeckAndPeck"
    elif self.ui.analysisAllButton.checked:
      analysisType = "All"
    if self._parameterNode.GetParameter("AnalysisType") != analysisType:
      self._parameterNode.SetParameter("AnalysisType", analysisType)
      self.onInputPointsModified()

    self._parameterNode.SetNodeReferenceID("InputPoints", self.ui.inputPointsSelector.currentNodeID)

    self._parameterNode.SetParameter("ReportFolder", self.ui.reportFolderPathLineEdit.currentPath)

    self._parameterNode.EndModify(wasModified)

  def onInputPointsModified(self, caller=None, event=None):
    analysisType = self._parameterNode.GetParameter("AnalysisType")
    inputPointsNode = self._parameterNode.GetNodeReference("InputPoints")
    if (not analysisType) or (not inputPointsNode):
      self.pointListTextBrowser.setPlainText("")
      self.showPointListWidget(False)
      return

    numberOfDefinedControlPoints = inputPointsNode.GetNumberOfDefinedControlPoints()
    numberOfControlPoints = inputPointsNode.GetNumberOfControlPoints()
    pointNames = self.logic.getPointNames(analysisType)

    # Only show all point labels when done with the marking
    # (labels would occlude the model, which is distracting while marking)
    showAllPointLabels = (numberOfDefinedControlPoints >= len(pointNames))

    pointDescription = "<html>\n<ol>\n"
    for pointIndex, [shortName, longName] in enumerate(pointNames):
      style = ""
      if pointIndex < numberOfDefinedControlPoints:  
        prefix = "&#x2611;"  # checked box (already placed)
      elif pointIndex == numberOfDefinedControlPoints:
        prefix = "&raquo;"  # double-arrow (being placed)
        style="font-weight: bold;"
      else:
        prefix = "&#x2610;"  # empty box (to be placed)
      pointDescription += '<li id="{0}"><div style="{1}">{2} {3} ({4})</div></li>\n'.format(shortName, style, prefix, longName, shortName)
      if pointIndex < numberOfControlPoints:
        # Only show label of the current point (unless markup is complete)
        label = shortName if (showAllPointLabels or (pointIndex == numberOfDefinedControlPoints)) else ""
        inputPointsNode.SetNthControlPointLabel(pointIndex, label)
    pointDescription += "</html>\n"
    self.pointListTextBrowser.setHtml(pointDescription)

    if numberOfDefinedControlPoints>=len(pointNames):
      # finished landmarking
      self.ui.MarkupsPlaceWidget.placeModeEnabled = False
      self.showPointListWidget(False)
    else:
      # landmarking is in progress
      self.showPointListWidget(True)
      topPointShownInList = max(numberOfDefinedControlPoints - 3, 0)
      self.pointListTextBrowser.scrollToAnchor(pointNames[topPointShownInList][0])

    wasModified = inputPointsNode.StartModify()
    while inputPointsNode.GetNumberOfControlPoints() > len(pointNames):
      inputPointsNode.RemoveNthControlPoint(inputPointsNode.GetNumberOfControlPoints()-1)
    inputPointsNode.EndModify(wasModified)

  def onApplyButton(self):
    """
    Run processing when user clicks "Generate" button.
    """
    try:
      self.ui.reportFolderPathLineEdit.addCurrentPathToHistory()

      analysisType = self._parameterNode.GetParameter("AnalysisType")
      inputPointsNode = self._parameterNode.GetNodeReference("InputPoints")
      reportFolder = self._parameterNode.GetParameter("ReportFolder")

      # Compute output
      reportFilename = self.logic.compute(analysisType, inputPointsNode, reportFolder)
      logging.info("Report generated: {0}".format(reportFilename))
      qt.QDesktopServices.openUrl(qt.QUrl().fromLocalFile(reportFilename))

    except Exception as e:
      slicer.util.errorDisplay("Failed to compute results: "+str(e))
      import traceback
      traceback.print_exc()


#
# OrthodonticAnalysisLogic
#

class OrthodonticAnalysisLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    """
    Called when the logic class is instantiated. Can be used for initializing member variables.
    """
    ScriptedLoadableModuleLogic.__init__(self)

    self.pointsPeckAndPeck = [
      ["32-D", "Distal point of Tooth 32"], ["32-M", "Mesial point of Tooth 32"], ["32-V", "Vestibular point of Tooth 32"], ["32-L", "Lingual point of Tooth 32"],
      ["31-D", "Distal point of Tooth 31"], ["31-M", "Mesial point of Tooth 31"], ["31-V", "Vestibular point of Tooth 31"], ["31-L", "Lingual point of Tooth 31"],
      ["41-D", "Distal point of Tooth 41"], ["41-M", "Mesial point of Tooth 41"], ["41-V", "Vestibular point of Tooth 41"], ["41-L", "Lingual point of Tooth 41"],
      ["42-D", "Distal point of Tooth 42"], ["42-M", "Mesial point of Tooth 42"], ["42-V", "Vestibular point of Tooth 42"], ["42-L", "Lingual point of Tooth 42"],
    ]

    self.pointsBolton = [
      ["16-D", "Distal point of Tooth 16"],  ["16-M", "Mesial point of Tooth 16"],
      ["15-D", "Distal point of Tooth 15"],  ["15-M", "Mesial point of Tooth 15"],
      ["14-D", "Distal point of Tooth 14"],  ["14-M", "Mesial point of Tooth 14"],
      ["13-D", "Distal point of Tooth 13"],  ["13-M", "Mesial point of Tooth 13"],
      ["12-D", "Distal point of Tooth 12"],  ["12-M", "Mesial point of Tooth 12"],
      ["11-D", "Distal point of Tooth 11"],  ["11-M", "Mesial point of Tooth 11"],
      ["21-M", "Mesial point of Tooth 21"],  ["21-D", "Distal point of Tooth 21"],
      ["22-M", "Mesial point of Tooth 22"],  ["22-D", "Distal point of Tooth 22"],
      ["23-M", "Mesial point of Tooth 23"],  ["23-D", "Distal point of Tooth 23"],
      ["24-M", "Mesial point of Tooth 24"],  ["24-D", "Distal point of Tooth 24"],
      ["25-M", "Mesial point of Tooth 25"],  ["25-D", "Distal point of Tooth 25"],
      ["26-M", "Mesial point of Tooth 26"],  ["26-D", "Distal point of Tooth 26"],
      ["36-D", "Distal point of Tooth 36"],  ["36-M", "Mesial point of Tooth 36"],
      ["35-D", "Distal point of Tooth 35"],  ["35-M", "Mesial point of Tooth 35"],
      ["34-D", "Distal point of Tooth 34"],  ["34-M", "Mesial point of Tooth 34"],
      ["33-D", "Distal point of Tooth 33"],  ["33-M", "Mesial point of Tooth 33"],
      ["32-D", "Distal point of Tooth 32"],  ["32-M", "Mesial point of Tooth 32"],
      ["31-D", "Distal point of Tooth 31"],  ["31-M", "Mesial point of Tooth 31"],
      ["41-M", "Mesial point of Tooth 41"],  ["41-D", "Distal point of Tooth 41"],
      ["42-M", "Mesial point of Tooth 42"],  ["42-D", "Distal point of Tooth 42"],
      ["43-M", "Mesial point of Tooth 43"],  ["43-D", "Distal point of Tooth 43"],
      ["44-M", "Mesial point of Tooth 44"],  ["44-D", "Distal point of Tooth 44"],
      ["45-M", "Mesial point of Tooth 45"],  ["45-D", "Distal point of Tooth 45"],
      ["46-M", "Mesial point of Tooth 46"],  ["46-D", "Distal point of Tooth 46"],
    ]

    pointsInferiorMid = [
      ["35-34-D", "Distal point of Teeth segment 35-34"],
      ["35-34-M-33-D", "Mesial point of Teeth segment 35-34 and Distal of Tooth 33"],
      ["33-MS", "Mesial point of Tooth segment 33"],
      ["IAM", "Inferior Arch Midpoint"],
      ["43-MS", "Mesial point of Tooth segment 43"],
      ["45-44-M-43-D", "Mesial point of Teeth segment 45-44 and Distal of Tooth 43"],
      ["45-44-D", "Distal point of Teeth segment 45-44"],
    ]

    self.pointsInferiorSpace = [
      ["35-D", "Distal point of Tooth 35"],  ["35-M", "Mesial point of Tooth 35"],
      ["34-D", "Distal point of Tooth 34"],  ["34-M", "Mesial point of Tooth 34"],
      ["33-D", "Distal point of Tooth 33"],  ["33-M", "Mesial point of Tooth 33"],
      ["32-D", "Distal point of Tooth 32"],  ["32-M", "Mesial point of Tooth 32"],
      ["31-D", "Distal point of Tooth 31"],  ["31-M", "Mesial point of Tooth 31"],
      ["41-M", "Mesial point of Tooth 41"],  ["41-D", "Distal point of Tooth 41"],
      ["42-M", "Mesial point of Tooth 42"],  ["42-D", "Distal point of Tooth 42"],
      ["43-M", "Mesial point of Tooth 43"],  ["43-D", "Distal point of Tooth 43"],
      ["44-M", "Mesial point of Tooth 44"],  ["44-D", "Distal point of Tooth 44"],
      ["45-M", "Mesial point of Tooth 45"],  ["45-D", "Distal point of Tooth 45"],
    ]
    self.pointsInferiorSpace.extend(pointsInferiorMid)

    pointsSuperiorMid = [
      ["15-14-D", "Distal point of Teeth segment 15-14"],
      ["15-14-M-13-D", "Mesial point of Teeth segment 15-14 and Distal of Tooth 13"],
      ["13-MS", "Mesial point of Tooth segment 13"],
      ["SAM", "Superior Arch Midpoint"],
      ["23-MS", "Mesial point of Tooth segment 23"],
      ["25-24-M-23-D", "Mesial point of Teeth segment 25-24 and Distal of Tooth 23"],
      ["25-24-D", "Distal point of Teeth segment 25-24"],
    ]

    self.pointsSuperiorSpace = [
      ["15-D", "Distal point of Tooth 15"],  ["15-M", "Mesial point of Tooth 15"],
      ["14-D", "Distal point of Tooth 14"],  ["14-M", "Mesial point of Tooth 14"],
      ["13-D", "Distal point of Tooth 13"],  ["13-M", "Mesial point of Tooth 13"],
      ["12-D", "Distal point of Tooth 12"],  ["12-M", "Mesial point of Tooth 12"],
      ["11-D", "Distal point of Tooth 11"],  ["11-M", "Mesial point of Tooth 11"],
      ["21-M", "Mesial point of Tooth 21"],  ["21-D", "Distal point of Tooth 21"],
      ["22-M", "Mesial point of Tooth 22"],  ["22-D", "Distal point of Tooth 22"],
      ["23-M", "Mesial point of Tooth 23"],  ["23-D", "Distal point of Tooth 23"],
      ["24-M", "Mesial point of Tooth 24"],  ["24-D", "Distal point of Tooth 24"],
      ["25-M", "Mesial point of Tooth 25"],  ["25-D", "Distal point of Tooth 25"],
    ]
    self.pointsSuperiorSpace.extend(pointsSuperiorMid)

    self.pointsAll = []
    self.pointsAll.extend(self.pointsBolton)
    self.pointsAll.extend(pointsSuperiorMid)
    self.pointsAll.extend(pointsInferiorMid)
    # Peck and Peck without medial-distal points
    self.pointsAll.extend([
      ["32-V", "Vestibular point of Tooth 32"], ["32-L", "Lingual point of Tooth 32"],
      ["31-V", "Vestibular point of Tooth 31"], ["31-L", "Lingual point of Tooth 31"],
      ["41-V", "Vestibular point of Tooth 41"], ["41-L", "Lingual point of Tooth 41"],
      ["42-V", "Vestibular point of Tooth 42"], ["42-L", "Lingual point of Tooth 42"],
    ])

  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter("AnalysisType"):
      parameterNode.SetParameter("AnalysisType", "Superior")
    if not parameterNode.GetParameter("ReportFolder"):
      parameterNode.SetParameter("ReportFolder", slicer.app.defaultScenePath)

  def getPointNames(self, analysisType):
    if analysisType == "Superior":
      pointList = self.pointsSuperiorSpace
    elif analysisType == "Inferior":
      pointList = self.pointsInferiorSpace
    elif analysisType == "Bolton":
      pointList = self.pointsBolton
    elif analysisType == "PeckAndPeck":
      pointList = self.pointsPeckAndPeck
    elif analysisType == "All":
      pointList = self.pointsAll
    else:
      raise ValueError("Invalid analysisType: {0}".format(analysisType))
    return pointList

  def getLabeledPoints(self, labels, markupsPointNode):
    """
    Return a map from "long point name" to "position"
    """
    pointPositions = slicer.util.arrayFromMarkupsControlPoints(markupsPointNode)
    labeledPoints = {}
    for index, [shortName, longName] in enumerate(labels):
      labeledPoints[longName] = pointPositions[index]
    return labeledPoints

  @staticmethod
  def distance(labeledPoints, label1, label2, errorIfMissing=True):
    import numpy as np
    if not errorIfMissing:
      if (label1 not in labeledPoints) or (label2 not in labeledPoints):
        return None
    return np.linalg.norm(labeledPoints[label1]-labeledPoints[label2])

  def compute(self, analysisType, inputPointsNode, reportFolder):
    from time import gmtime, strftime
    timestamp = strftime("%Y%m%d-%H%M%S", gmtime())
    reportFilename = "{0}/OrthodonticAnalysis-{1}-{2}.html".format(reportFolder, analysisType, timestamp)
    reportScreenshotFilenameName = "OrthodonticAnalysis-{0}-{1}.png".format(analysisType, timestamp)
    reportScreenshotFilename = "{0}/{1}".format(reportFolder, reportScreenshotFilenameName)

    if analysisType=="Superior":
      report = self.computeSuperiorSpaceAnalysis(inputPointsNode)
    elif analysisType=="Inferior":
      report = self.computeInferiorSpaceAnalysis(inputPointsNode)
    elif analysisType=="Bolton":
      report = self.computeBoltonAnalysis(inputPointsNode)
    elif analysisType=="PeckAndPeck":
      report = self.computePeckAndPeckAnalysis(inputPointsNode)
    elif analysisType=="All":
      report = self.computeAllAnalysis(inputPointsNode)
    else:
      raise ValueError("Invalid analysisType: {0}".format(analysisType))

    import ScreenCapture
    cap = ScreenCapture.ScreenCaptureLogic()
    cap.showViewControllers(False)
    cap.captureImageFromView(None, reportScreenshotFilename)
    cap.showViewControllers(True)

    screenshot = '<img src="{0}">'.format(reportScreenshotFilenameName)

    with open(reportFilename, 'w') as file_object:
      file_object.write("<html>\n{0}\n{1}\n</html>".format(report, screenshot))

    return reportFilename


  def computeSuperiorSpaceAnalysis(self, markupsPointNode=None, labeledPoints=None):

    if labeledPoints:
      p = labeledPoints
    else:
      p = self.getLabeledPoints(self.pointsSuperiorSpace, markupsPointNode)

    dente16 = self.distance(p, "Distal point of Tooth 16", "Mesial point of Tooth 16", False)
    dente15 = self.distance(p, "Distal point of Tooth 15", "Mesial point of Tooth 15")
    dente14 = self.distance(p, "Distal point of Tooth 14", "Mesial point of Tooth 14")
    dente13 = self.distance(p, "Distal point of Tooth 13", "Mesial point of Tooth 13")
    dente12 = self.distance(p, "Distal point of Tooth 12", "Mesial point of Tooth 12")
    dente11 = self.distance(p, "Distal point of Tooth 11", "Mesial point of Tooth 11")
    dente21 = self.distance(p, "Distal point of Tooth 21", "Mesial point of Tooth 21")
    dente22 = self.distance(p, "Distal point of Tooth 22", "Mesial point of Tooth 22")
    dente23 = self.distance(p, "Distal point of Tooth 23", "Mesial point of Tooth 23")
    dente24 = self.distance(p, "Distal point of Tooth 24", "Mesial point of Tooth 24")
    dente25 = self.distance(p, "Distal point of Tooth 25", "Mesial point of Tooth 25")
    dente26 = self.distance(p, "Distal point of Tooth 26", "Mesial point of Tooth 26", False)

    # Space code required
    esp_r_sup = dente15 + dente14 + dente13 + dente12 + dente11 + dente21 + dente22 + dente23 + dente24 + dente25
    
    # Rated space code superior and inferior
    esp_a_sup = (self.distance(p, "Distal point of Teeth segment 15-14", "Mesial point of Teeth segment 15-14 and Distal of Tooth 13")
      + self.distance(p, "Mesial point of Teeth segment 15-14 and Distal of Tooth 13", "Mesial point of Tooth segment 13")
      + self.distance(p, "Mesial point of Tooth segment 13", "Superior Arch Midpoint")
      + self.distance(p, "Superior Arch Midpoint", "Mesial point of Tooth segment 23")
      + self.distance(p, "Mesial point of Tooth segment 23", "Mesial point of Teeth segment 25-24 and Distal of Tooth 23")
      + self.distance(p, "Mesial point of Teeth segment 25-24 and Distal of Tooth 23", "Distal point of Teeth segment 25-24"))
    
    # Result code
    disc_sup = esp_a_sup - esp_r_sup

    htmlReport = """<h2>SUPERIOR SPACE ANALYSIS</h2>

<h3>Spaces</h3>
<ul>
  <li>Superior arch discrepancy: {0:.2f}mm</li>
  <li>Required Space: {1:.2f}mm</li>
  <li>Rated Space: {2:.2f}mm</li>
</ul>""".format(disc_sup, esp_r_sup, esp_a_sup)

    htmlReport +="""
<h3>Diameters</h3>
<ul>
"""
    if dente16 is not None:
      htmlReport += "  <li>Tooth 16: {0:.2f}mm</li>\n".format(dente16)
    htmlReport += """
  <li>Tooth 15: {0:.2f}mm</li>
  <li>Tooth 14: {1:.2f}mm</li>
  <li>Tooth 13: {2:.2f}mm</li>
  <li>Tooth 12: {3:.2f}mm</li>
  <li>Tooth 11: {4:.2f}mm</li>
  <li>Tooth 21: {5:.2f}mm</li>
  <li>Tooth 22: {6:.2f}mm</li>
  <li>Tooth 23: {7:.2f}mm</li>
  <li>Tooth 24: {8:.2f}mm</li>
  <li>Tooth 25: {9:.2f}mm</li>
""".format(dente15, dente14, dente13, dente12, dente11, dente21, dente22, dente23, dente24, dente25)
    if dente26 is not None:
      htmlReport += "  <li>Tooth 26: {0:.2f}mm</li>\n".format(dente26)

    htmlReport += "</ul>\n"

    return htmlReport


  def computeInferiorSpaceAnalysis(self, markupsPointNode=None, labeledPoints=None):

    if labeledPoints:
      p = labeledPoints
    else:
      p = self.getLabeledPoints(self.pointsInferiorSpace, markupsPointNode)

    dente36 = self.distance(p, "Distal point of Tooth 36", "Mesial point of Tooth 36", False)
    dente35 = self.distance(p, "Distal point of Tooth 35", "Mesial point of Tooth 35")
    dente34 = self.distance(p, "Distal point of Tooth 34", "Mesial point of Tooth 34")
    dente33 = self.distance(p, "Distal point of Tooth 33", "Mesial point of Tooth 33")
    dente32 = self.distance(p, "Distal point of Tooth 32", "Mesial point of Tooth 32")
    dente31 = self.distance(p, "Distal point of Tooth 31", "Mesial point of Tooth 31")
    dente41 = self.distance(p, "Distal point of Tooth 41", "Mesial point of Tooth 41")
    dente42 = self.distance(p, "Distal point of Tooth 42", "Mesial point of Tooth 42")
    dente43 = self.distance(p, "Distal point of Tooth 43", "Mesial point of Tooth 43")
    dente44 = self.distance(p, "Distal point of Tooth 44", "Mesial point of Tooth 44")
    dente45 = self.distance(p, "Distal point of Tooth 45", "Mesial point of Tooth 45")
    dente46 = self.distance(p, "Distal point of Tooth 46", "Mesial point of Tooth 46", False)

    # Space code required
    esp_r_inf = dente35 + dente34 + dente33 + dente32 + dente31 + dente41 + dente42 + dente43 + dente44 + dente45
    
    # Rated space code superior and inferior
    esp_a_inf = (self.distance(p, "Distal point of Teeth segment 35-34", "Mesial point of Teeth segment 35-34 and Distal of Tooth 33")
      + self.distance(p, "Mesial point of Teeth segment 35-34 and Distal of Tooth 33", "Mesial point of Tooth segment 33")
      + self.distance(p, "Mesial point of Tooth segment 33", "Inferior Arch Midpoint")
      + self.distance(p, "Inferior Arch Midpoint", "Mesial point of Tooth segment 43")
      + self.distance(p, "Mesial point of Tooth segment 43", "Mesial point of Teeth segment 45-44 and Distal of Tooth 43")
      + self.distance(p, "Mesial point of Teeth segment 45-44 and Distal of Tooth 43", "Distal point of Teeth segment 45-44"))

    # Result code
    disc_inf = esp_a_inf - esp_r_inf

    htmlReport = """<h2>INFERIOR SPACE ANALYSIS</h2>

<h3>Spaces</h3>
<ul>
  <li>Inferior arch discrepancy: {0:.2f}mm</li>
  <li>Required Space: {1:.2f}mm</li>
  <li>Rated Space: {2:.2f}mm</li>
</ul>""".format(disc_inf, esp_r_inf, esp_a_inf)

    htmlReport +="""
<h3>Diameters</h3>
<ul>
"""
    if dente36 is not None:
      htmlReport += "  <li>Tooth 36: {0:.2f}mm</li>\n".format(dente36)
    htmlReport += """
  <li>Tooth 35: {0:.2f}mm</li>
  <li>Tooth 34: {1:.2f}mm</li>
  <li>Tooth 33: {2:.2f}mm</li>
  <li>Tooth 32: {3:.2f}mm</li>
  <li>Tooth 31: {4:.2f}mm</li>
  <li>Tooth 41: {5:.2f}mm</li>
  <li>Tooth 42: {6:.2f}mm</li>
  <li>Tooth 43: {7:.2f}mm</li>
  <li>Tooth 44: {8:.2f}mm</li>
  <li>Tooth 45: {9:.2f}mm</li>
""".format(dente35, dente34, dente33, dente32, dente31, dente41, dente42, dente43, dente44, dente45)
    if dente46 is not None:
      htmlReport += "  <li>Tooth 46: {0:.2f}mm</li>\n".format(dente46)

    htmlReport += "</ul>\n"

    return htmlReport


  def computeBoltonAnalysis(self, markupsPointNode=None, labeledPoints=None):

    if labeledPoints:
      p = labeledPoints
    else:
      p = self.getLabeledPoints(self.pointsBolton, markupsPointNode)

    dente16 = self.distance(p, "Distal point of Tooth 16", "Mesial point of Tooth 16")
    dente15 = self.distance(p, "Distal point of Tooth 15", "Mesial point of Tooth 15")
    dente14 = self.distance(p, "Distal point of Tooth 14", "Mesial point of Tooth 14")
    dente13 = self.distance(p, "Distal point of Tooth 13", "Mesial point of Tooth 13")
    dente12 = self.distance(p, "Distal point of Tooth 12", "Mesial point of Tooth 12")
    dente11 = self.distance(p, "Distal point of Tooth 11", "Mesial point of Tooth 11")
    dente21 = self.distance(p, "Distal point of Tooth 21", "Mesial point of Tooth 21")
    dente22 = self.distance(p, "Distal point of Tooth 22", "Mesial point of Tooth 22")
    dente23 = self.distance(p, "Distal point of Tooth 23", "Mesial point of Tooth 23")
    dente24 = self.distance(p, "Distal point of Tooth 24", "Mesial point of Tooth 24")
    dente25 = self.distance(p, "Distal point of Tooth 25", "Mesial point of Tooth 25")
    dente26 = self.distance(p, "Distal point of Tooth 26", "Mesial point of Tooth 26")

    dente36 = self.distance(p, "Distal point of Tooth 36", "Mesial point of Tooth 36")
    dente35 = self.distance(p, "Distal point of Tooth 35", "Mesial point of Tooth 35")
    dente34 = self.distance(p, "Distal point of Tooth 34", "Mesial point of Tooth 34")
    dente33 = self.distance(p, "Distal point of Tooth 33", "Mesial point of Tooth 33")
    dente32 = self.distance(p, "Distal point of Tooth 32", "Mesial point of Tooth 32")
    dente31 = self.distance(p, "Distal point of Tooth 31", "Mesial point of Tooth 31")
    dente41 = self.distance(p, "Distal point of Tooth 41", "Mesial point of Tooth 41")
    dente42 = self.distance(p, "Distal point of Tooth 42", "Mesial point of Tooth 42")
    dente43 = self.distance(p, "Distal point of Tooth 43", "Mesial point of Tooth 43")
    dente44 = self.distance(p, "Distal point of Tooth 44", "Mesial point of Tooth 44")
    dente45 = self.distance(p, "Distal point of Tooth 45", "Mesial point of Tooth 45")
    dente46 = self.distance(p, "Distal point of Tooth 46", "Mesial point of Tooth 46")

    # Arcs division code
    dist_12_sup = dente16 + dente15 + dente14 + dente13 + dente12 + dente11 + dente21 + dente22 + dente23 + dente24 + dente25 + dente26
    dist_12_inf = dente36 + dente35 + dente34 + dente33 + dente32 + dente31 + dente41 + dente42 + dente43 + dente44 + dente45 + dente46
 
    dist_6_sup = dente13 + dente12 + dente11 + dente21 + dente22 + dente23
    dist_6_inf = dente33 + dente32 + dente31 + dente41 + dente42 + dente43
    
    r_bolt_12 = (dist_12_inf/dist_12_sup)*100
    r_bolt_6 = (dist_6_inf/dist_6_sup)*100

    htmlReport = "<h2>BOLTON ANALYSIS</h2>"

    # Total
    ideal_12_sup = None
    ideal_12_inf = None
    if r_bolt_12 > 91.3:
        # Excess on inferior arch (superior is used as ideal)
        excess_12_arch = "Inferior"
        ideal_12_sup = dist_12_sup
        ideal_12_inf = dist_12_sup * 0.913
        excess_12 = dist_12_inf - ideal_12_inf
    else:
        # Excess on superior arch (inferior is used as ideal)
        excess_12_arch = "Superior"
        ideal_12_sup = dist_12_inf / 0.913
        ideal_12_inf = dist_12_inf
        excess_12 = dist_12_sup - ideal_12_sup

    htmlReport+= """
<h3>Total Bolton Analysis</h3>
<ul>
<li>Excess on {0} arch: {1:.1f}mm</li>
<li>Ideal superior arch length: {2:.1f}mm</li>
<li>Ideal inferior arch length: {3:.1f}mm</li>
</ul>
""".format(excess_12_arch, excess_12, ideal_12_sup, ideal_12_inf)

    # Anterior
    ideal_6_sup = None
    ideal_6_inf = None
    if r_bolt_6 > 77.2:
        # Excess on inferior arch (superior is used as ideal)
        excess_6_arch = "Inferior"
        ideal_6_sup = dist_6_sup
        ideal_6_inf = dist_6_sup * 0.772
        excess_6 = dist_6_inf - ideal_6_inf
    else:
        # Excess on superior arch (inferior is used as ideal)
        excess_6_arch = "Superior"
        ideal_6_sup = dist_6_inf / 0.772
        ideal_6_inf = dist_6_inf
        excess_6 = dist_6_sup - ideal_6_sup

    htmlReport+= """
<h3>Anterior Bolton Analysis</h3>
<ul>
<li>Excess on {0} arch: {1:.1f}mm</li>
<li>Ideal superior arch length: {2:.1f}mm</li>
<li>Ideal inferior arch length: {3:.1f}mm</li>
</ul>
""".format(excess_6_arch, excess_6, ideal_6_sup, ideal_6_inf)

    return htmlReport


  def computePeckAndPeckAnalysis(self, markupsPointNode=None, labeledPoints=None):

    if labeledPoints:
      p = labeledPoints
    else:
      p = self.getLabeledPoints(self.pointsPeckAndPeck, markupsPointNode)

    dente32_md = self.distance(p, "Distal point of Tooth 32", "Mesial point of Tooth 32")
    dente32_fl = self.distance(p, "Vestibular point of Tooth 32", "Lingual point of Tooth 32")
    dente31_md = self.distance(p, "Distal point of Tooth 31", "Mesial point of Tooth 31")
    dente31_fl = self.distance(p, "Vestibular point of Tooth 31", "Lingual point of Tooth 31")
    dente41_md = self.distance(p, "Distal point of Tooth 41", "Mesial point of Tooth 41")
    dente41_fl = self.distance(p, "Vestibular point of Tooth 41", "Lingual point of Tooth 41")
    dente42_md = self.distance(p, "Distal point of Tooth 42", "Mesial point of Tooth 42")
    dente42_fl = self.distance(p, "Vestibular point of Tooth 42", "Lingual point of Tooth 42")

    indice_d42 = (dente42_md/dente42_fl)*100.0
    indice_d41 = (dente41_md/dente41_fl)*100.0
    indice_d31 = (dente31_md/dente31_fl)*100.0
    indice_d32 = (dente32_md/dente32_fl)*100.0

    results = [
      indice_d42, indice_d41, indice_d31, indice_d32,
      dente32_md, dente32_fl, dente31_md, dente31_fl, dente41_md, dente41_fl, dente42_md, dente42_fl]

    htmlReportTemplate = """<h2>PECK & PECK ANALYSIS</h2>

<h3>Results (%)</h3>

<table border="1">
  <tr> <th>Tooth</th>  <th>Result</th>    <th>Normal range</th>  </tr>
  <tr> <td>32</td>     <td>{3:.2f}%</td>  <td>90-95%</td>        </tr>
  <tr> <td>31</td>     <td>{2:.2f}%</td>  <td>88-92%</td>        </tr>
  <tr> <td>41</td>     <td>{1:.2f}%</td>  <td>88-92%</td>        </tr>
  <tr> <td>42</td>     <td>{0:.2f}%</td>  <td>90-95%</td>        </tr>
</table>

<h3>Diameters (mm)</h3>

<table border="1">
  <tr> <th>Tooth</th>  <th>Axis</th>          <th>Diameter</th>  </tr>
  <tr> <td>32</td>     <td>Mesiodistal</td>   <td>{4:.2f}mm</td>   </tr>
  <tr> <td>32</td>     <td>Faciolingual</td>  <td>{5:.2f}mm</td>   </tr>
  <tr> <td>31</td>     <td>Mesiodistal</td>   <td>{6:.2f}mm</td>   </tr>
  <tr> <td>31</td>     <td>Faciolingual</td>  <td>{7:.2f}mm</td>   </tr>
  <tr> <td>41</td>     <td>Mesiodistal</td>   <td>{8:.2f}mm</td>   </tr>
  <tr> <td>41</td>     <td>Faciolingual</td>  <td>{9:.2f}mm</td>   </tr>
  <tr> <td>42</td>     <td>Mesiodistal</td>   <td>{10:.2f}mm</td>   </tr>
  <tr> <td>42</td>     <td>Faciolingual</td>  <td>{11:.2f}mm</td>   </tr>
</table>
"""

    htmlReport = htmlReportTemplate.format(*results)
    return htmlReport


  def computeAllAnalysis(self, markupsPointNode=None, labeledPoints=None):

    if labeledPoints:
      p = labeledPoints
    else:
      p = self.getLabeledPoints(self.pointsAll, markupsPointNode)

    htmlReport = self.computeSuperiorSpaceAnalysis(labeledPoints=p)
    htmlReport += self.computeInferiorSpaceAnalysis(labeledPoints=p)
    htmlReport += self.computeBoltonAnalysis(labeledPoints=p)
    htmlReport += self.computePeckAndPeckAnalysis(labeledPoints=p)

    return htmlReport


#
# OrthodonticAnalysisTest
#

class OrthodonticAnalysisTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear()

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_OrthodonticAnalysis1()

  def test_OrthodonticAnalysis1(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests should exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")

    # Get/create input data

    import SampleData
    import numpy as np

    registerSampleData()
    inputModel = SampleData.downloadSample('TeethSurface')
    self.delayDisplay('Loaded test data set')

    boltonPoints = np.array([
        [ 22.08201981, -23.33771133,  20.25755501],
        [ 22.24702835, -31.33755684,  21.34285164],
        [ 21.05020905, -33.57769394,  20.82586288],
        [ 19.80578232, -38.49482346,  21.96247864],
        [ 18.11996651, -39.62874985,  20.58876419],
        [ 15.6773119 , -43.51329041,  20.84062958],
        [ 14.88829422, -45.93460083,  22.75982285],
        [ 13.19761467, -49.92071915,  24.98643875],
        [ 11.26348495, -51.92196655,  24.92158699],
        [  8.64679909, -54.30356979,  24.28428459],
        [  6.33776236, -56.0610466 ,  25.04037094],
        [  1.78006351, -56.95132446,  25.48031998],
        [ -2.16635013, -56.97172546,  25.0060463 ],
        [ -6.92025566, -56.07076645,  25.30604935],
        [ -9.60852814, -54.69460678,  22.86414337],
        [-12.39715576, -51.92007065,  24.64757919],
        [-13.62540627, -50.76442337,  22.39550209],
        [-16.08952713, -47.632267  ,  24.58095741],
        [-16.86974907, -44.14796448,  21.01618767],
        [-19.02500725, -40.79146957,  21.13197517],
        [-20.02264214, -38.30114746,  20.2833786 ],
        [-22.63177681, -33.98239517,  21.14200592],
        [-22.84235001, -32.13227844,  20.34781075],
        [-23.02272606, -23.87202072,  20.32165146],

        [-21.21748734,  28.36712456,  19.8465004 ],
        [-20.2088089 ,  35.91403961,  19.19993591],
        [-19.53867912,  39.61227798,  18.90285492],
        [-18.82330132,  42.92764664,  18.90742874],
        [-17.66699791,  45.53125   ,  19.33840942],
        [-14.75944424,  48.4083519 ,  18.84576416],
        [-13.24126625,  50.82159424,  17.86232758],
        [-10.98532295,  53.38891983,  19.96564484],
        [ -8.72065449,  55.52565384,  18.94808769],
        [ -7.38320017,  56.39972687,  18.83339882],
        [ -4.97158384,  57.34194565,  19.23067856],
        [ -1.77612793,  57.65716171,  19.53565407],
        [  1.08269632,  57.6644516 ,  18.88643074],
        [  3.59803629,  57.58930969,  18.73008728],
        [  6.15127277,  57.16143036,  18.54046822],
        [  9.16291714,  55.95013428,  19.57354355],
        [ 10.80373573,  54.19895172,  20.96066284],
        [ 13.1416111 ,  52.37386703,  20.06233978],
        [ 15.6479454 ,  49.06868744,  19.79941177],
        [ 16.05915833,  45.21175385,  19.17629242],
        [ 17.35715103,  43.17802811,  19.32717133],
        [ 18.95762825,  38.32523727,  19.18061638],
        [ 20.97534943,  36.32210541,  19.83763313],
        [ 21.8088131 ,  28.76040459,  20.85327911]
        ])

    inputPointsNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsFiducialNode", "P")
    slicer.util.updateMarkupsControlPointsFromArray(inputPointsNode, boltonPoints)

    # Test the module logic

    logic = OrthodonticAnalysisLogic()

    # Test algorithm with non-inverted threshold
    reportPath = logic.compute("Bolton", inputPointsNode, slicer.app.temporaryPath)
    self.assertIsNotNone(reportPath)

    self.delayDisplay('Test passed')
