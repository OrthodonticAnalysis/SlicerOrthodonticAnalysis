cmake_minimum_required(VERSION 3.5)

project(OrthodonticAnalysis)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://slicer.org/slicerWiki/index.php/Documentation/Nightly/Extensions/OrthodonticAnalysis")
set(EXTENSION_CATEGORY "Examples")
set(EXTENSION_CONTRIBUTORS "João Vitor Lima Coimbra (Federal University of Espírito Santo), Vinicius Campos de Oliveira Batista (Federal University of Espírito Santo), Rafhael Milanezi de Andrade (Federal University of Espírito Santo), Pedro Lima Emmerich Oliveira (Federal University of Rio de Janeiro), Lincoln Issamu Nojima (Federal University of Rio de Janeiro)")
set(EXTENSION_DESCRIPTION "The extension was developed to perform the most common dental analysis: model space discrepancies, Bolton and Peck and Peck. All point instructions for performing the analysis are available in Python interactor after study method points are selected. The Analysis button shows the result.
The model discrepancy calculates the difference between the required space and the present space. If the difference is positive, there is an excess of space available, if the difference is negative, it means that there is a space deficit.
The required upper and lower spaces are obtained from measurements of the mesiodistal diameters of the incisors, canines, and premolars. The present spaces are obtained in six straight line segments: from the mesial face of the first molar to the distal face of the canine, from the distal face of the canine to the mesial face of the canine and from the mesial face of the canine to the midline.
Bolton's analysis takes into account two proportional size ratios between the upper and lower arches. The first is based on the sums of mesiodistal diameters of the teeth from the first molars, including the same, totaling 12 teeth per arch. The second is based on the sums of mesiodistal diameters of the teeth from the canines, including the canines, totaling 6 teeth per arch.
The teeth evaluated in Peck and Peck analysis are the lower incisors. The measurements taken are the mesiodistal and buccolingual diameters. The value of the mesiodistal diameter is divided by the buccolingual diameter to obtain the proportion and make the evaluation.
")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/OrthodonticAnalysis.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/OrthodonticAnalysis/Screenshots/1.png")
set(EXTENSION_DEPENDS "NA") # Specified as a space separated string, a list or 'NA' if any

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(OrthodonticAnalysis)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_GENERATE_CONFIG})
include(${Slicer_EXTENSION_CPACK})
