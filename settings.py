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

# AI_TAG = os.environ.get("AI_TAG")
# AI_RUNGS = os.environ.get("AI_RUNGS")
# DI_TAG = os.environ.get("DI_TAG")
# DI_RUNGS = os.environ.get("DI_RUNGS")
# DOut_TAG = os.environ.get("DOUT_TAG")
# DOut_RUNGS = os.environ.get("DOUT_RUNGS")

controller_list = os.listdir("routine_file")
controller_version = easygui.choicebox(msg='Выберите версию', title="Signal processing for InTA",
                                       choices=list(map(lambda x: x.split(" ")[0], controller_list)))
controller_folder = list(filter(lambda x: controller_version in x, controller_list))[0]
controller_type = controller_folder.split(" ")[1]
AI_EMPTY_FILE = f"routine_file/{controller_folder}/AI.L5X"
DI_EMPTY_FILE = f"routine_file/{controller_folder}/DI.L5X"
DOUT_EMPTY_FILE = f"routine_file/{controller_folder}/DOut.L5X"

AI_TAG = f"template/{controller_folder}/AITag.xml"
AI_RUNGS = f"template/{controller_folder}/AIRungs.xml"
DI_TAG = f"template/{controller_folder}/DITag.xml"
DI_RUNGS = f"template/{controller_folder}/DIRungs.xml"
DOUT_TAG = f"template/{controller_folder}/DOutTag.xml"
DOUT_RUNGS = f"template/{controller_folder}/DOutRungs.xml"

print(controller_type)

# def create_replacement_dict():
#     replacement_dict = {}
#     replacement_dict.