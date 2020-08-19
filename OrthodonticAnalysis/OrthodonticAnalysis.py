# -*- coding: cp1252 -*-
from __main__ import vtk, qt, ctk, slicer

class OrthodonticAnalysis:
  def __init__(self, parent):
    parent.title = "Orthodontic Analysis"
    parent.categories = ["Orthodontic Analysis"]
    parent.dependencies = []
    parent.contributors = ["João Vitor Lima Coimbra (Federal University of Espírito Santo",
                           "Vinicius Campos de Oliveira Batista (Federal University of Espírito Santo)",
                           "Rafhael Milanezi de Andrade (Federal University of Espírito Santo)",
                           "Pedro Lima Emmerich Oliveira (Federal University of Rio de Janeiro)",
                           "Lincoln Issamu Nojima (Federal University of Rio de Janeiro)"
                           ""
                          ] 
    parent.helpText = """
    Copy and paste the link into your browser to access the video lesson:  https://youtu.be/M78xGVvGJ_Y                 -                   
    In case of doubts, sent an e-mail to: pedroemmerich@hotmail.com"""
    
    parent.acknowledgementText = """
    The extension was developed to perform the most common dental analysis: model space discrepancies, Bolton and Peck and Peck. All point instructions for performing the analysis are available in Python interactor after study method points are selected. The Analysis button shows the result.
The model discrepancy calculates the difference between the required space and the present space. If the difference is positive, there is an excess of space available, if the difference is negative, it means that there is a space deficit.
The required upper and lower spaces are obtained from measurements of the mesiodistal diameters of the incisors, canines, and premolars. The present spaces are obtained in six straight line segments: from the mesial face of the first molar to the distal face of the canine, from the distal face of the canine to the mesial face of the canine and from the mesial face of the canine to the midline.
Bolton's analysis takes into account two proportional size ratios between the upper and lower arches. The first is based on the sums of mesiodistal diameters of the teeth from the first molars, including the same, totaling 12 teeth per arch. The second is based on the sums of mesiodistal diameters of the teeth from the canines, including the canines, totaling 6 teeth per arch.
The teeth evaluated in Peck and Peck analysis are the lower incisors. The measurements taken are the mesiodistal and buccolingual diameters. The value of the mesiodistal diameter is divided by the buccolingual diameter to obtain the proportion and make the evaluation.
"""
    self.parent = parent


class OrthodonticAnalysisWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
      self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):


    # Collapsible button - Space Analysis
    sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    sampleCollapsibleButton.text = "Space Analysis"
    self.layout.addWidget(sampleCollapsibleButton)

    # Layout within the sample collapsible button
    sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

    # Superior Space Analysis Button
    discrepanciasupButton = qt.QPushButton("Analysis - Superior")
    discrepanciasupButton.toolTip = "Print 'Analysis' in standard ouput."
    sampleFormLayout.addWidget(discrepanciasupButton)
    discrepanciasupButton.connect('clicked(bool)', self.onDiscrepanciasupButtonClicked)

    # Superior Space Button Help
    helpspacesupButton = qt.QPushButton("Points - Superior")
    helpspacesupButton.toolTip = "Print 'Points' in standard ouput."
    sampleFormLayout.addWidget(helpspacesupButton)
    helpspacesupButton.connect('clicked(bool)', self.onHelpSpacesupButtonClicked)

    # Inferior Space Analysis Button
    discrepanciainfButton = qt.QPushButton("Analysis - Inferior")
    discrepanciainfButton.toolTip = "Print 'Analysis' in standard ouput."
    sampleFormLayout.addWidget(discrepanciainfButton)
    discrepanciainfButton.connect('clicked(bool)', self.onDiscrepanciainfButtonClicked)

    # Space Button Help
    helpspaceinfButton = qt.QPushButton("Points - Inferior")
    helpspaceinfButton.toolTip = "Print 'Points' in standard ouput."
    sampleFormLayout.addWidget(helpspaceinfButton)
    helpspaceinfButton.connect('clicked(bool)', self.onHelpSpaceinfButtonClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.helpspacesupButton = helpspacesupButton

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.discrepanciasupButton = discrepanciasupButton

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.helpspaceinfButton = helpspaceinfButton

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.discrepanciainfButton = discrepanciainfButton


    # Collapsible button - Bolton Analysis
    sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    sampleCollapsibleButton.text = "Bolton Analysis"
    self.layout.addWidget(sampleCollapsibleButton)

    # Layout within the sample collapsible button
    sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

    # Bolton Button Help
    helpboltonButton = qt.QPushButton("Points")
    helpboltonButton.toolTip = "Print 'Points' in standard ouput."
    sampleFormLayout.addWidget(helpboltonButton)
    helpboltonButton.connect('clicked(bool)', self.onHelpBoltonButtonClicked)

    # Bolton Analysis Button
    boltonButton = qt.QPushButton("Analysis")
    boltonButton.toolTip = "Print 'Analysis' in standard ouput."
    sampleFormLayout.addWidget(boltonButton)
    boltonButton.connect('clicked(bool)', self.onBoltonButtonClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.helpboltonButton = helpboltonButton

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.boltonButton = boltonButton

    # Collapsible button - Peck & Peck Analysis
    sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    sampleCollapsibleButton.text = "Peck and Peck Analysis"
    self.layout.addWidget(sampleCollapsibleButton)

    # Layout within the sample collapsible button
    sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

    # Peck & Peck Button Help
    helppeckButton = qt.QPushButton("Points")
    helppeckButton.toolTip = "Print 'Points' in standard ouput."
    sampleFormLayout.addWidget(helppeckButton)
    helppeckButton.connect('clicked(bool)', self.onHelpPeckButtonClicked)

    # Peck & Peck Analysis Button
    peckPeckButton = qt.QPushButton("Analysis")
    peckPeckButton.toolTip = "Print 'Analysis' in standard ouput."
    sampleFormLayout.addWidget(peckPeckButton)
    peckPeckButton.connect('clicked(bool)', self.onPeckPeckButtonClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.helppeckButton = helppeckButton

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.peckPeckButton = peckPeckButton

    # Collapsible button - All Analysis
    sampleCollapsibleButton = ctk.ctkCollapsibleButton()
    sampleCollapsibleButton.text = "All Analysis"
    self.layout.addWidget(sampleCollapsibleButton)

    # Layout within the sample collapsible button
    sampleFormLayout = qt.QFormLayout(sampleCollapsibleButton)

    # All Analysis Button Help
    helpallButton = qt.QPushButton("Points")
    helpallButton.toolTip = "Print 'Points' in standard ouput."
    sampleFormLayout.addWidget(helpallButton)
    helpallButton.connect('clicked(bool)', self.onHelpAllButtonClicked)

    # All Analysis Button
    analisesButton = qt.QPushButton("Analysis")
    analisesButton.toolTip = "Print 'Analysis' in standard ouput."
    sampleFormLayout.addWidget(analisesButton)
    analisesButton.connect('clicked(bool)', self.onAnalisesButtonClicked)

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.helpallButton = helpallButton

    # Add vertical spacer
    self.layout.addStretch(1)

    # Set local var as instance attribute
    self.analisesButton = analisesButton


#---------------------------------------------------------------------------------------------------------
#Analysis Button
#---------------------------------------------------------------------------------------------------------

        
  def onPeckPeckButtonClicked(self):

    #PECK & PECK ANALYSIS

    #Points Matrix
                
    p = []
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    for i in range(numFids):
     linha = [0,0,0]
     ras = [0,0,0]
     fidList.GetNthFiducialPosition(i,ras)
     linha = [ras[0],ras[1],ras[2]]
     p.append(linha)

    #Distance code

    def diametro(ponto1, ponto2):
        d = ((p[ponto2][0] - p[ponto1][0])**2 + (p[ponto2][1] - p[ponto1][1])**2 + (p[ponto2][2] - p[ponto1][2])**2)**0.5
        return d

    dente32_md = diametro(0,1)
    dente32_fl = diametro(2,3)
    dente31_md = diametro(4,5)
    dente31_fl = diametro(6,7)
    dente41_md = diametro(8,9)
    dente41_fl = diametro(10,11)
    dente42_md = diametro(12,13)
    dente42_fl = diametro(14,15)

    indice_d42 = (dente42_md/dente42_fl)*100
    indice_d41 = (dente41_md/dente41_fl)*100
    indice_d31 = (dente31_md/dente31_fl)*100
    indice_d32 = (dente32_md/dente32_fl)*100

    print "-------------------------------"
    print "PECK & PECK ANALYSIS"
    print "-------------------------------"
    print " "
    print "Results (%)"
    print " "
    print "Tooth 42: ", round(indice_d42, 2)
    print "Normal: 90-95%"
    print "Tooth 41: ", round(indice_d41, 2)
    print "Normal: 88-92%"
    print "Tooth 31: ", round(indice_d31, 2)
    print "Normal: 88-92%"
    print "Tooth 32: ", round(indice_d32, 2)
    print "Normal: 90-95%"
    print " "
    print "-------------------------------"
    print " "
    print "Diameters (mm)"
    print " "
    print "Mesiodistal  Tooth 32: ", round(dente32_md, 2)
    print "Faciolingual Tooth 32: ", round(dente32_fl, 2)
    print "Mesiodistal  Tooth 31: ", round(dente31_md, 2)
    print "Faciolingual Tooth 31: ", round(dente31_fl, 2)
    print "Mesiodistal  Tooth 41: ", round(dente41_md, 2)
    print "Faciolingual Tooth 41: ", round(dente41_fl, 2)
    print "Mesiodistal  Tooth 42: ", round(dente42_md, 2)
    print "Faciolingual Tooth 42: ", round(dente42_fl, 2)
    print " "
    print "-------------------------------"

    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'PECK & PECK ANALYSIS', 'Open the Python Interactor to view the results')

    
  def onDiscrepanciainfButtonClicked(self):

    #INFERIOR SPACE ANALYSIS

    #Points Matrix

    p = []
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    for i in range(numFids):
     linha = [0,0,0]
     ras = [0,0,0]
     fidList.GetNthFiducialPosition(i,ras)
     linha = [ras[0],ras[1],ras[2]]
     p.append(linha)
 
    #Distance code

    def diametro(ponto1, ponto2):
        d = ((p[ponto2][0] - p[ponto1][0])**2 + (p[ponto2][1] - p[ponto1][1])**2 + (p[ponto2][2] - p[ponto1][2])**2)**0.5
        return d

    dente35 = diametro(0,1)
    dente34 = diametro(2,3)
    dente33 = diametro(4,5)
    dente32 = diametro(6,7)
    dente31 = diametro(8,9)
    dente41 = diametro(10,11)
    dente42 = diametro(12,13)
    dente43 = diametro(14,15)
    dente44 = diametro(16,17)
    dente45 = diametro(18,19)
  
    #Space code required
    esp_r_inf = dente35 + dente34 + dente33 + dente32 + dente31 + dente41 + dente42 + dente43 + dente44 + dente45
    
    #Rated space code superior and inferior
    esp_a_inf = diametro(20,21) + diametro(21,22) + diametro(22,23) + diametro(23,24) + diametro(24,25) + diametro(25,26)

    #Result code
    disc_inf = esp_a_inf - esp_r_inf

    print "-------------------------------"
    print "INFERIOR SPACE ANALYSIS"
    print "-------------------------------"
    print " "
    print "Spaces (mm)"
    print " "
    print "Inferior arch discrepancy: ", round(disc_inf, 2)
    print "Required Space: ", round(esp_r_inf, 2)
    print "Rated Space:  ", round(esp_a_inf, 2)
    print " "
    print "-------------------------------"
    print " "
    print "Diameters (mm)"
    print " "
    print "Diameter Tooth 35: ", round(dente35, 2)
    print "Diameter Tooth 34: ", round(dente34, 2)
    print "Diamater Tooth 33: ", round(dente33, 2)
    print "Diamater Tooth 32: ", round(dente32, 2)
    print "Diamater Tooth 31: ", round(dente31, 2)
    print "Diamater Tooth 41: ", round(dente41, 2)
    print "Diamater Tooth 42: ", round(dente42, 2)
    print "Diamater Tooth 43: ", round(dente43, 2)
    print "Diamater Tooth 44: ", round(dente44, 2)
    print "Diamater Tooth 45: ", round(dente45, 2)
    print " "
    print "-------------------------------"

    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'INFERIOR SPACE ANALYSIS', 'Open the Python Interactor to view the results')

    
  def onDiscrepanciasupButtonClicked(self):

    #SUPERIOR SPACE ANALYSIS

    #Points Matrix

    p = []
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    for i in range(numFids):
     linha = [0,0,0]
     ras = [0,0,0]
     fidList.GetNthFiducialPosition(i,ras)
     linha = [ras[0],ras[1],ras[2]]
     p.append(linha)
 
    #Distance code

    def diametro(ponto1, ponto2):
        d = ((p[ponto2][0] - p[ponto1][0])**2 + (p[ponto2][1] - p[ponto1][1])**2 + (p[ponto2][2] - p[ponto1][2])**2)**0.5
        return d

    dente15 = diametro(0,1)
    dente14 = diametro(2,3)
    dente13 = diametro(4,5)
    dente12 = diametro(6,7)
    dente11 = diametro(8,9)
    dente21 = diametro(10,11)
    dente22 = diametro(12,13)
    dente23 = diametro(14,15)
    dente24 = diametro(16,17)
    dente25 = diametro(18,19)
  
    #Space code required
    esp_r_sup = dente15 + dente14 + dente13 + dente12 + dente11 + dente21 + dente22 + dente23 + dente24 + dente25
    
    #Rated space code superior and inferior
    esp_a_sup = diametro(20,21) + diametro(21,22) + diametro(22,23) + diametro(23,24) + diametro(24,25) + diametro(25,26)
    
    #Result code
    disc_sup = esp_a_sup - esp_r_sup

    print "-------------------------------"
    print "SUPERIOR SPACE ANALYSIS"
    print "-------------------------------"
    print " "
    print "Spaces (mm)"
    print " "
    print "Superior arch discrepancy: ", round(disc_sup, 2)
    print "Required Space: ", round(esp_r_sup, 2)
    print "Rated Space:  ", round(esp_a_sup, 2)
    print " "
    print "-------------------------------"
    print " "
    print "Diameters (mm)"
    print " "
    print "Diameter Tooth 15: ", round(dente15, 2)
    print "Diameter Tooth 14: ", round(dente14, 2)
    print "Diamater Tooth 13: ", round(dente13, 2)
    print "Diamater Tooth 12: ", round(dente12, 2)
    print "Diamater Tooth 11: ", round(dente11, 2)
    print "Diamater Tooth 21: ", round(dente21, 2)
    print "Diamater Tooth 22: ", round(dente22, 2)
    print "Diamater Tooth 23: ", round(dente23, 2)
    print "Diamater Tooth 24: ", round(dente24, 2)
    print "Diamater Tooth 25: ", round(dente25, 2)
    print " "
    print "-------------------------------"

    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'SUPERIOR SPACE ANALYSIS', 'Open the Python Interactor to view the results')


  def onBoltonButtonClicked(self):

    #BOLTON ANALYSIS

    #POINTS MATRIX

    p = []
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    for i in range(numFids):
     linha = [0,0,0]
     ras = [0,0,0]
     fidList.GetNthFiducialPosition(i,ras)
     linha = [ras[0],ras[1],ras[2]]
     p.append(linha)

    #Distance code

    def diametro(ponto1, ponto2):
        d = ((p[ponto2][0] - p[ponto1][0])**2 + (p[ponto2][1] - p[ponto1][1])**2 + (p[ponto2][2] - p[ponto1][2])**2)**0.5
        return d
    
    dente16 = diametro(0,1)
    dente15 = diametro(2,3)
    dente14 = diametro(4,5)
    dente13 = diametro(6,7)
    dente12 = diametro(8,9)
    dente11 = diametro(10,11)
    dente21 = diametro(12,13)
    dente22 = diametro(14,15)
    dente23 = diametro(16,17)
    dente24 = diametro(18,19)
    dente25 = diametro(20,21)
    dente26 = diametro(22,23)
    dente36 = diametro(24,25)
    dente35 = diametro(26,27)
    dente34 = diametro(28,29)
    dente33 = diametro(30,31)
    dente32 = diametro(32,33)
    dente31 = diametro(34,35)
    dente41 = diametro(36,37)
    dente42 = diametro(38,39)
    dente43 = diametro(40,41)
    dente44 = diametro(42,43)
    dente45 = diametro(44,45)
    dente46 = diametro(46,47)

    #Arcs division code

    dist_12_sup = dente15 + dente14 + dente13 + dente12 + dente11 + dente21 + dente22 + dente23 + dente24 + dente25 + dente16 + dente26
    dist_12_inf = dente35 + dente34 + dente33 + dente32 + dente31 + dente41 + dente42 + dente43 + dente44 + dente45 + dente36 + dente46
 
    dist_6_sup = dente13 + dente12 + dente11 + dente21 + dente22 + dente23
    dist_6_inf = dente33 + dente32 + dente31 + dente41 + dente42 + dente43
    
    r_bolt_12 = (dist_12_inf/dist_12_sup)*100
    r_bolt_6 = (dist_6_inf/dist_6_sup)*100

    #Conditional code
    tab_bolt_12_sup = [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    tab_bolt_12_inf = [77.6, 78.5, 79.4, 80.3, 81.3, 82.1, 83.1, 84, 84.9, 85.8, 86.7, 87.6, 88.6, 89.5, 90.4, 91.3, 92.2, 93.1, 94, 95, 95.9, 96.8, 97.8, 98.6, 99.5, 100.4]
    tab_bolt_6_sup = [40, 40.5, 41, 41.5, 42, 42.5, 43, 43.5, 44, 44.5, 45, 45.5, 46, 46.5, 47, 47.5, 48, 48.5, 49, 49.5, 50, 50.5, 51, 51.5, 52, 52.5, 53, 53.5, 54, 54.5, 55]
    tab_bolt_6_inf = [30.9, 31.3, 31.7, 32, 32.4, 32.8, 33.2, 33.6, 34, 34.4, 34.7, 35.1, 35.5, 35.9, 36.3, 36.7, 37.1, 37.4, 37.8, 38.2, 38.6, 39, 39.4, 39.8, 40.1, 40.5, 40.9, 41.3, 41.7, 42.1, 42.5]

    #Upper arch excess
    if r_bolt_12 > 91.3:
        for i in range(25):
            if (tab_bolt_12_sup[i]-0.5)<=dist_12_sup<(tab_bolt_12_sup[i]+0.5):
                e12_inf = tab_bolt_12_inf[i] - dist_12_inf
                print "-------------------------------"
                print "BOLTON ANALYSIS"
                print "-------------------------------"
                print " "
                print "Total Bolton Analysis (mm):"
                print "-Excess on inferior arch: ", round(e12_inf, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_12_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_12_inf[i]
                print " "

    #Upper arch excess         
    else:
        for i in range(25):
            if (tab_bolt_12_inf[i]-0.5)<=dist_12_inf<(tab_bolt_12_inf[i]+0.5):
                e12_sup = tab_bolt_12_sup[i] - dist_12_sup
                print "-------------------------------"
                print "BOLTON ANALYSIS"
                print "-------------------------------"
                print " "
                print "Total Bolton Analysis (mm):"
                print "-Excess on superior arch: ", round(e12_sup, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_12_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_12_inf[i]
                print " "
                
    #Lower arch excess
    if r_bolt_6 > 77.2:
        for i in range(30):
            if (tab_bolt_6_sup[i]-0.25)<=dist_6_sup<(tab_bolt_6_sup[i]+0.25):
                e6_inf = tab_bolt_6_inf[i] - dist_6_inf
                print "Anterior Bolton Analysis (mm):"
                print "-Excess on inferior arch: ", round(e6_inf, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_6_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_6_inf[i]
                print " "
                print "-------------------------------"

    #Upper arch excess            
    else:
        for i in range(30):
            if (tab_bolt_6_inf[i]-0.2)<=dist_6_inf<(tab_bolt_6_inf[i]+0.2):
                e6_sup = tab_bolt_6_sup[i] - dist_6_sup
                print "Anterior Bolton Analysis (mm):"
                print "-Excess on superior arch: ", round(e6_sup, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_6_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_6_inf[i]
                print " "
                print "-------------------------------"

    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'BOLTON ANALYSIS', 'Open the Python Interactor to view the results')                
                

  def onAnalisesButtonClicked(self):

    #ALL ANALYSIS
    
    #Points Matrix

    p = []
    fidList = slicer.util.getNode('F')
    numFids = fidList.GetNumberOfFiducials()
    for i in range(numFids):
     linha = [0,0,0]
     ras = [0,0,0]
     fidList.GetNthFiducialPosition(i,ras)
     linha = [ras[0],ras[1],ras[2]]
     p.append(linha)
     
    #Distance code

    def diametro(ponto1, ponto2):
        d = ((p[ponto2][0] - p[ponto1][0])**2 + (p[ponto2][1] - p[ponto1][1])**2 + (p[ponto2][2] - p[ponto1][2])**2)**0.5
        return d

    dente16 = diametro(0,1)
    dente15 = diametro(2,3)
    dente14 = diametro(4,5)
    dente13 = diametro(6,7)
    dente12 = diametro(8,9)
    dente11 = diametro(10,11)
    dente21 = diametro(12,13)
    dente22 = diametro(14,15)
    dente23 = diametro(16,17)
    dente24 = diametro(18,19)
    dente25 = diametro(20,21)
    dente26 = diametro(22,23)
    dente36 = diametro(24,25)
    dente35 = diametro(26,27)
    dente34 = diametro(28,29)
    dente33 = diametro(30,31)
    dente32 = diametro(32,33)
    dente31 = diametro(34,35)
    dente41 = diametro(36,37)
    dente42 = diametro(38,39)
    dente43 = diametro(40,41)
    dente44 = diametro(42,43)
    dente45 = diametro(44,45)
    dente46 = diametro(46,47)

    print "-------------------------------"
    print " "
    print "Diameters (mm)"
    print " "
    print "Diameter Tooth 16: ", round(dente16, 2)
    print "Diameter Tooth 15: ", round(dente15, 2)
    print "Diameter Tooth 14: ", round(dente14, 2)
    print "Diamater Tooth 13: ", round(dente13, 2)
    print "Diamater Tooth 12: ", round(dente12, 2)
    print "Diamater Tooth 11: ", round(dente11, 2)
    print "Diamater Tooth 21: ", round(dente21, 2)
    print "Diamater Tooth 22: ", round(dente22, 2)
    print "Diamater Tooth 23: ", round(dente23, 2)
    print "Diamater Tooth 24: ", round(dente24, 2)
    print "Diamater Tooth 25: ", round(dente25, 2)
    print "Diamater Tooth 26: ", round(dente26, 2)
    print "Diamater Tooth 36: ", round(dente36, 2)
    print "Diameter Tooth 35: ", round(dente35, 2)
    print "Diameter Tooth 34: ", round(dente34, 2)
    print "Diamater Tooth 33: ", round(dente33, 2)
    print "Diamater Tooth 32: ", round(dente32, 2)
    print "Diamater Tooth 31: ", round(dente31, 2)
    print "Diamater Tooth 41: ", round(dente41, 2)
    print "Diamater Tooth 42: ", round(dente42, 2)
    print "Diamater Tooth 43: ", round(dente43, 2)
    print "Diamater Tooth 44: ", round(dente44, 2)
    print "Diamater Tooth 45: ", round(dente45, 2)
    print "Diamater Tooth 46: ", round(dente46, 2)
    print " "
    print "-------------------------------"
    
    
    #SPACE ANALYSIS

    #Space code required

    esp_r_sup = dente15 + dente14 + dente13 + dente12 + dente11 + dente21 + dente22 + dente23 + dente24 + dente25
    esp_r_inf = dente35 + dente34 + dente33 + dente32 + dente31 + dente41 + dente42 + dente43 + dente44 + dente45
        
    #Rated space code superior and inferior

    esp_a_sup = diametro(48,49) + diametro(49,50) + diametro(50,51) + diametro(51,52) + diametro(52,53) + diametro(53,54)
    esp_a_inf = diametro(55,56) + diametro(56,57) + diametro(57,58) + diametro(58,59) + diametro(59,60) + diametro(60,61)

    #Result code

    disc_sup = esp_a_sup - esp_r_sup
    disc_inf = esp_a_inf - esp_r_inf

    print "-------------------------------"
    print "SPACE ANALYSIS"
    print "-------------------------------"
    print " "
    print "Spaces (mm)"
    print " "
    print "Inferior arch discrepancy: ", round(disc_inf, 2)
    print "Superior arch discrepancy: ", round(disc_sup, 2)
    print " "
    print "-------------------------------"

    #BOLTON ANALYSIS

    #Arcs division code

    dist_12_sup = dente15 + dente14 + dente13 + dente12 + dente11 + dente21 + dente22 + dente23 + dente24 + dente25 + dente16 + dente26
    dist_12_inf = dente35 + dente34 + dente33 + dente32 + dente31 + dente41 + dente42 + dente43 + dente44 + dente45 + dente36 + dente46
 
    dist_6_sup = dente13 + dente12 + dente11 + dente21 + dente22 + dente23
    dist_6_inf = dente33 + dente32 + dente31 + dente41 + dente42 + dente43

    r_bolt_12 = (dist_12_inf/dist_12_sup)*100
    r_bolt_6 = (dist_6_inf/dist_6_sup)*100

    #Conditional code
    tab_bolt_12_sup = [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    tab_bolt_12_inf = [77.6, 78.5, 79.4, 80.3, 81.3, 82.1, 83.1, 84, 84.9, 85.8, 86.7, 87.6, 88.6, 89.5, 90.4, 91.3, 92.2, 93.1, 94, 95, 95.9, 96.8, 97.8, 98.6, 99.5, 100.4]
    tab_bolt_6_sup = [40, 40.5, 41, 41.5, 42, 42.5, 43, 43.5, 44, 44.5, 45, 45.5, 46, 46.5, 47, 47.5, 48, 48.5, 49, 49.5, 50, 50.5, 51, 51.5, 52, 52.5, 53, 53.5, 54, 54.5, 55]
    tab_bolt_6_inf = [30.9, 31.3, 31.7, 32, 32.4, 32.8, 33.2, 33.6, 34, 34.4, 34.7, 35.1, 35.5, 35.9, 36.3, 36.7, 37.1, 37.4, 37.8, 38.2, 38.6, 39, 39.4, 39.8, 40.1, 40.5, 40.9, 41.3, 41.7, 42.1, 42.5]

    #Lower arch excess
    if r_bolt_12 > 91.3:
        for i in range(25):
            if (tab_bolt_12_sup[i]-0.5)<=dist_12_sup<(tab_bolt_12_sup[i]+0.5):
                e12_inf = tab_bolt_12_inf[i] - dist_12_inf
                print "-------------------------------"
                print "BOLTON ANALYSIS"
                print "-------------------------------"
                print " "
                print "Total Bolton Analysis (mm):"
                print "-Excess on inferior arch: ", round(e12_inf, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_12_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_12_inf[i]
                print " "

    #Upper arch excess            
    else:
        for i in range(25):
            if (tab_bolt_12_inf[i]-0.5)<=dist_12_inf<(tab_bolt_12_inf[i]+0.5):
                e12_sup = tab_bolt_12_sup[i] - dist_12_sup
                print "-------------------------------"
                print "BOLTON ANALYSIS"
                print "-------------------------------"
                print " "
                print "Total Bolton Analysis (mm):"
                print "-Excess on superior arch: ", round(e12_sup, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_12_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_12_inf[i]
                print " "
                
    #Lower arch excess
    if r_bolt_6 > 77.2:
        for i in range(30):
            if (tab_bolt_6_sup[i]-0.25)<=dist_6_sup<(tab_bolt_6_sup[i]+0.25):
                e6_inf = tab_bolt_6_inf[i] - dist_6_inf
                print "Anterior Bolton Analysis (mm):"
                print "-Excess on inferior arch: ", round(e6_inf, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_6_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_6_inf[i]
                print " "
                print "-------------------------------"

    #Upper arch excess            
    else:
        for i in range(30):
            if (tab_bolt_6_inf[i]-0.2)<=dist_6_inf<(tab_bolt_6_inf[i]+0.2):
                e6_sup = tab_bolt_6_sup[i] - dist_6_sup
                print "Anterior Bolton Analysis (mm):"
                print "-Excess on superior arch: ", round(e6_sup, 2)
                print "-Ideal superior arch diameter:  ", tab_bolt_6_sup[i]
                print "-Ideal inferior arch diameter: ", tab_bolt_6_inf[i]
                print " "
                print "-------------------------------"
                

    #PECK & PECK ANALYSIS

    dente32_fl = diametro(62,63)
    dente31_fl = diametro(64,65)
    dente41_fl = diametro(66,67)
    dente42_fl = diametro(68,69)
  
    indice_d42 = (dente42/dente42_fl)*100
    indice_d41 = (dente41/dente41_fl)*100
    indice_d31 = (dente31/dente31_fl)*100
    indice_d32 = (dente32/dente32_fl)*100

    print "-------------------------------"
    print "PECK & PECK ANALYSIS"
    print "-------------------------------"
    print " "
    print "Results (%)"
    print " "
    print "Tooth 42: ", round(indice_d42, 2)
    print "Normal: 90-95%"
    print "Tooth 41: ", round(indice_d41, 2)
    print "Normal: 88-92%"
    print "Tooth 31: ", round(indice_d31, 2)
    print "Normal: 88-92%"
    print "Normal 32: ", round(indice_d32, 2)
    print "Normal: 90-95%"
    print " "
    print "-------------------------------"

    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'ALL ANALYSIS', 'Open the Python Interactor to view the results')


#---------------------------------------------------------------------------------------------------------
#HELP BUTTONS
#---------------------------------------------------------------------------------------------------------
    
  def onHelpSpaceinfButtonClicked(self):

    print " "
    print "-------------------------------------------------------------------------------------------------"
    print " "
    print "                                 INFERIOR SPACE ANALYSIS POINTS                                          "
    print " "
    print "Insert the points:"
    print " "
    print "Point 01: Distal point of the Tooth 35"
    print "Point 02: Mesial point of the Tooth 35"
    print "Point 03: Distal point of the Tooth 34"
    print "Point 04: Mesial point of the Tooth 34"
    print "Point 05: Distal point of the Tooth 33"
    print "Point 06: Mesial point of the Tooth 33"
    print "Point 07: Distal point of the Tooth 32"
    print "Point 08: Mesial point of the Tooth 32"
    print "Point 09: Distal point of the Tooth 31"
    print "Point 10: Mesial point of the Tooth 31"
    print "Point 11: Distal point of the Tooth 41"
    print "Point 12: Mesial point of the Tooth 41"
    print "Point 13: Distal point of the Tooth 42"
    print "Point 14: Mesial point of the Tooth 42"
    print "Point 15: Distal point of the Tooth 43"
    print "Point 16: Mesial point of the Tooth 43"
    print "Point 17: Distal point of the Tooth 44"
    print "Point 18: Mesial point of the Tooth 44"
    print "Point 19: Distal point of the Tooth 45"
    print "Point 20: Mesial point of the Tooth 45"
    print "Point 21: Distal point of Teeth segment 35-34"
    print "Point 22: Mesial point of Teeth segment 35-34 and Distal of the Tooth 33"
    print "Point 23: Mesial point of Tooth segment 33"
    print "Point 24: Inferior Arch Midpoint"
    print "Point 25: Mesial point of Tooth segment 43"
    print "Point 26: Mesial point of Teeth segment 45-44 and Distal of the Tooth 43"
    print "Point 27: Distal point of Teeth segment 45-44"
    
    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'Help Points Button', 'Open the Python Interactor to check the points that you must insert')

  def onHelpSpacesupButtonClicked(self):
    print " "
    print "-------------------------------------------------------------------------------------------------"
    print " "
    print "                                 SUPERIOR SPACE ANALYSIS POINTS                                          "
    print " "
    print "Insert the points:"
    print " "
    print "Point 01: Distal point of the Tooth 15"
    print "Point 02: Mesial point of the Tooth 15"
    print "Point 03: Distal point of the Tooth 14"
    print "Point 04: Mesial point of the Tooth 14"
    print "Point 05: Distal point of the Tooth 13"
    print "Point 06: Mesial point of the Tooth 13"
    print "Point 07: Distal point of the Tooth 12"
    print "Point 08: Mesial point of the Tooth 12"
    print "Point 09: Distal point of the Tooth 11"
    print "Point 10: Mesial point of the Tooth 11"
    print "Point 11: Distal point of the Tooth 21"
    print "Point 12: Mesial point of the Tooth 21"
    print "Point 13: Distal point of the Tooth 22"
    print "Point 14: Mesial point of the Tooth 22"
    print "Point 15: Distal point of the Tooth 23"
    print "Point 16: Mesial point of the Tooth 23"
    print "Point 17: Distal point of the Tooth 24"
    print "Point 18: Mesial point of the Tooth 24"
    print "Point 19: Distal point of the Tooth 25"
    print "Point 20: Mesial point of the Tooth 25"
    print "Point 21: Distal point of Teeth segment 15-14"
    print "Point 22: Mesial point of Teeth segment 15-14 and Distal of the Tooth 13"
    print "Point 23: Mesial point of Tooth segment 13"
    print "Point 24: Superior Arch Midpoint"
    print "Point 25: Mesial point of Tooth segment 23"
    print "Point 26: Mesial point of Teeth segment 25-24 and Distal of the Tooth 23"
    print "Point 27: Distal point of Teeth segment 25-24"
    
    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'Help Points Button', 'Open the Python Interactor to check the points that you must insert')


  def onHelpBoltonButtonClicked(self):

    print " "
    print "-------------------------------------------------------------------------------------------------"
    print " "
    print "                                 BOLTON ANALYSIS POINTS                                          "
    print " "
    print "Insert the points:"
    print " "
    print "Point 01: Distal point of the Tooth 16"
    print "Point 02: Mesial point of the Tooth 16"
    print "Point 03: Distal point of the Tooth 15"
    print "Point 04: Mesial point of the Tooth 15"
    print "Point 05: Distal point of the Tooth 14"
    print "Point 06: Mesial point of the Tooth 14"
    print "Point 07: Distal point of the Tooth 13"
    print "Point 08: Mesial point of the Tooth 13"
    print "Point 09: Distal point of the Tooth 12"
    print "Point 10: Mesial point of the Tooth 12"
    print "Point 11: Distal point of the Tooth 11"
    print "Point 12: Mesial point of the Tooth 11"
    print "Point 13: Distal point of the Tooth 21"
    print "Point 14: Mesial point of the Tooth 21"
    print "Point 15: Distal point of the Tooth 22"
    print "Point 16: Mesial point of the Tooth 22"
    print "Point 17: Distal point of the Tooth 23"
    print "Point 18: Mesial point of the Tooth 23"
    print "Point 19: Distal point of the Tooth 24"
    print "Point 20: Mesial point of the Tooth 24"
    print "Point 21: Distal point of the Tooth 25"
    print "Point 22: Mesial point of the Tooth 25"
    print "Point 23: Distal point of the Tooth 26"
    print "Point 24: Mesial point of the Tooth 26"
    print "Point 25: Distal point of the Tooth 36"
    print "Point 26: Mesial point of the Tooth 36"
    print "Point 27: Distal point of the Tooth 35"
    print "Point 28: Mesial point of the Tooth 35"
    print "Point 29: Distal point of the Tooth 34"
    print "Point 30: Mesial point of the Tooth 34"
    print "Point 31: Distal point of the Tooth 33"
    print "Point 32: Mesial point of the Tooth 33"
    print "Point 33: Distal point of the Tooth 32"
    print "Point 34: Mesial point of the Tooth 32"
    print "Point 35: Distal point of the Tooth 31"
    print "Point 36: Mesial point of the Tooth 31"
    print "Point 37: Distal point of the Tooth 41"
    print "Point 38: Mesial point of the Tooth 41"
    print "Point 39: Distal point of the Tooth 42"
    print "Point 40: Mesial point of the Tooth 42"
    print "Point 41: Distal point of the Tooth 43"
    print "Point 42: Mesial point of the Tooth 43"
    print "Point 43: Distal point of the Tooth 44"
    print "Point 44: Mesial point of the Tooth 44"
    print "Point 45: Distal point of the Tooth 45"
    print "Point 46: Mesial point of the Tooth 45"
    print "Point 47: Distal point of the Tooth 46"
    print "Point 48: Mesial point of the Tooth 46"
    
    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'Help Points Button', 'Open the Python Interactor to check the points that you must insert')

    
  def onHelpPeckButtonClicked(self):
    print " "
    print "-------------------------------------------------------------------------------------------------"
    print " "
    print "                              PECK AND PECK ANALYSIS POINTS                                      "
    print " "
    print "Insert the points:"
    print " "
    print "Point 01: Distal point of the Tooth 32"
    print "Point 02: Mesial point of the Tooth 32"
    print "Point 03: Vestibular point of the Tooth 32"
    print "Point 04: Lingual point of the Tooth 32"
    print "Point 05: Distal point of the Tooth 31"
    print "Point 06: Mesial point of the Tooth 31"
    print "Point 07: Vestibular point of the Tooth 31"
    print "Point 08: Lingual point of the Tooth 31"
    print "Point 09: Distal point of the Tooth 41"
    print "Point 10: Mesial point of the Tooth 41"
    print "Point 11: Vestibular point of the Tooth 41"
    print "Point 12: Lingual point of the Tooth 41"
    print "Point 13: Distal point of the Tooth 42"
    print "Point 14: Mesial point of the Tooth 42"
    print "Point 15: Vestibular point of the Tooth 42"
    print "Point 16: Lingual point of the Tooth 42"
    print " "
    
    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'Help Points Button', 'Open the Python Interactor to check the points that you must insert')


  def onHelpAllButtonClicked(self):
    print " "
    print "-------------------------------------------------------------------------------------------------"
    print " "
    print "                                    All ANALYSIS POINTS                                          "
    print " "
    print "Insert the points:"
    print " "
    print "Point 01: Distal point of the Tooth 16"
    print "Point 02: Mesial point of the Tooth 16"
    print "Point 03: Distal point of the Tooth 15"
    print "Point 04: Mesial point of the Tooth 15"
    print "Point 05: Distal point of the Tooth 14"
    print "Point 06: Mesial point of the Tooth 14"
    print "Point 07: Distal point of the Tooth 13"
    print "Point 08: Mesial point of the Tooth 13"
    print "Point 09: Distal point of the Tooth 12"
    print "Point 10: Mesial point of the Tooth 12"
    print "Point 11: Distal point of the Tooth 11"
    print "Point 12: Mesial point of the Tooth 11"
    print "Point 13: Distal point of the Tooth 21"
    print "Point 14: Mesial point of the Tooth 21"
    print "Point 15: Distal point of the Tooth 22"
    print "Point 16: Mesial point of the Tooth 22"
    print "Point 17: Distal point of the Tooth 23"
    print "Point 18: Mesial point of the Tooth 23"
    print "Point 19: Distal point of the Tooth 24"
    print "Point 20: Mesial point of the Tooth 24"
    print "Point 21: Distal point of the Tooth 25"
    print "Point 22: Mesial point of the Tooth 25"
    print "Point 23: Distal point of the Tooth 26"
    print "Point 24: Mesial point of the Tooth 26"
    print "Point 25: Distal point of the Tooth 36"
    print "Point 26: Mesial point of the Tooth 36"
    print "Point 27: Distal point of the Tooth 35"
    print "Point 28: Mesial point of the Tooth 35"
    print "Point 29: Distal point of the Tooth 34"
    print "Point 30: Mesial point of the Tooth 34"
    print "Point 31: Distal point of the Tooth 33"
    print "Point 32: Mesial point of the Tooth 33"
    print "Point 33: Distal point of the Tooth 32"
    print "Point 34: Mesial point of the Tooth 32"
    print "Point 35: Distal point of the Tooth 31"
    print "Point 36: Mesial point of the Tooth 31"
    print "Point 37: Distal point of the Tooth 41"
    print "Point 38: Mesial point of the Tooth 41"
    print "Point 39: Distal point of the Tooth 42"
    print "Point 40: Mesial point of the Tooth 42"
    print "Point 41: Distal point of the Tooth 43"
    print "Point 42: Mesial point of the Tooth 43"
    print "Point 43: Distal point of the Tooth 44"
    print "Point 44: Mesial point of the Tooth 44"
    print "Point 45: Distal point of the Tooth 45"
    print "Point 46: Mesial point of the Tooth 45"
    print "Point 47: Distal point of the Tooth 46"
    print "Point 48: Mesial point of the Tooth 46"
    print "Point 49: Distal point of Teeth segment 15-14"
    print "Point 50: Mesial point of Teeth segment 15-14 and Distal of the Tooth 13"
    print "Point 51: Mesial point of Tooth segment 13"
    print "Point 52: Superior Arch Midpoint"
    print "Point 53: Mesial point of Tooth segment 23"
    print "Point 54: Mesial point of Teeth segment 25-24 and Distal of the Tooth 23"
    print "Point 55: Distal point of Teeth segment 25-24"
    print "Point 56: Distal point of Teeth segment 35-34"
    print "Point 57: Mesial point of Teeth segment 35-34 and Distal of the Tooth 33"
    print "Point 58: Mesial point of Tooth segment 33"
    print "Point 59: Inferior Arch Midpoint"
    print "Point 60: Mesial point of Tooth segment 43"
    print "Point 61: Mesial point of Teeth segment 45-44 and Distal of the Tooth 43"
    print "Point 62: Distal point of Teeth segment 45-44"
    print "Point 63: Vestibular point of the Tooth 32"
    print "Point 64: Lingual point of the Tooth 32"
    print "Point 65: Vestibular point of the Tooth 31"
    print "Point 66: Lingual point of the Tooth 31"
    print "Point 67: Vestibular point of the Tooth 41"
    print "Point 68: Lingual point of the Tooth 41"
    print "Point 69: Vestibular point of the Tooth 42"
    print "Point 70: Lingual point of the Tooth 42"
    print " "
    
    qt.QMessageBox.information(
      	slicer.util.mainWindow(),
        'Help Points Button', 'Open the Python Interactor to check the points that you must insert')




      
