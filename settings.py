import os
import easygui

ROUTINE = 0
TAG_NAME = 12
ROUT_DESC = 13
ADDR = 1
DESCA = 4
DESCB = 5
DESCC = 6
DESCD = 7
DESCE = 8


AI_OUTPUT = "AI.L5X"
DI_OUTPUT = "DI.L5X"
DOut_OUTPUT = "DOut.L5X"


AI_TAG = "template/AITag.xml"
AI_RUNGS = "template/AIRungs.xml"
DI_TAG = "template/DITag.xml"
DI_RUNGS = "template/DIRungs.xml"
DOut_TAG = "template/DOutTag.xml"
DOut_RUNGS = "template/DOutRungs.xml"

controllers = os.listdir("./example_rout")
controllerversion = easygui.choicebox(msg='Выберите версию', title="Signal processing for InTA", choices=list(map(lambda x: x.split(" ")[0], controllers)))
controllerfolder = list(filter(lambda x: controllerversion in x, controllers))[0]
controllertype = controllerfolder.split(" ")[1]
AI_TEMPLATE = f"example_rout/{controllerfolder}/AI.L5X"
DI_TEMPLATE = f"example_rout/{controllerfolder}/DI.L5X"
DOut_TEMPLATE = f"example_rout/{controllerfolder}/DOut.L5X"

print(controllertype)