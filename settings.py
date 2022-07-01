import dotenv
import os
import easygui


dotenv.load_dotenv()


ROUTINE = int(os.environ.get("ROUTINE"))
TAG_NAME = int(os.environ.get("TAG_NAME"))
ROUT_DESC = int(os.environ.get("ROUT_DESC"))
ADDR = int(os.environ.get("ADDR"))
DESCA = int(os.environ.get("DESCA"))
DESCB = int(os.environ.get("DESCB"))
DESCC = int(os.environ.get("DESCC"))
DESCD = int(os.environ.get("DESCD"))
DESCE = int(os.environ.get("DESCE"))


AI_OUTPUT = os.environ.get("AI_OUTPUT")
DI_OUTPUT = os.environ.get("DI_OUTPUT")
DOut_OUTPUT = os.environ.get("DOUT_OUTPUT")


AI_TAG = os.environ.get("AI_TAG")
AI_RUNGS = os.environ.get("AI_RUNGS")
DI_TAG = os.environ.get("DI_TAG")
DI_RUNGS = os.environ.get("DI_RUNGS")
DOut_TAG = os.environ.get("DOUT_TAG")
DOut_RUNGS = os.environ.get("DOUT_RUNGS")

controllers = os.listdir("./example_rout")
controllerversion = easygui.choicebox(msg='Выберите версию', title="Signal processing for InTA", choices=list(map(lambda x: x.split(" ")[0], controllers)))
controllerfolder = list(filter(lambda x: controllerversion in x, controllers))[0]
controllertype = controllerfolder.split(" ")[1]
AI_TEMPLATE = f"example_rout/{controllerfolder}/AI.L5X"
DI_TEMPLATE = f"example_rout/{controllerfolder}/DI.L5X"
DOut_TEMPLATE = f"example_rout/{controllerfolder}/DOut.L5X"

print(controllertype)