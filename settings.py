import os
import easygui

ROUTINE = 0
TAG_NAME = 1
ADDR = 2
DESCA = 5
DESCB = 6
DESCC = 7
DESCD = 8
DESCE = 9


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
controllerfolder = easygui.choicebox(msg='Имя контроллера', title="RSLogix signal processing by Desunovu", choices=controllers)
controllertype = controllerfolder.split(" ")[0]
AI_TEMPLATE = f"example_rout/{controllerfolder}/AI.L5X"
DI_TEMPLATE = f"example_rout/{controllerfolder}/DI.L5X"
DOut_TEMPLATE = f"example_rout/{controllerfolder}/DOut.L5X"

print(controllertype)