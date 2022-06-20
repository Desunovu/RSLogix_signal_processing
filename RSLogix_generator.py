import time
import xml.etree.ElementTree
import lxml.etree as ET
import pylightxl as xl

parser = ET.XMLParser(strip_cdata=False)

EXCELFILE = "data.xlsx"

format = 2
if __name__ == "__main__":
    format = input("[Введите число] Старый формат - 2, новый формат - 1: ")
if format == "2":
    AI_TEMPLATE = "example_rout/old/AI_old.L5X"
    DI_TEMPLATE = "example_rout/old/DI_old.L5X"
    DOut_TEMPLATE = "example_rout/old/DOut_old.L5X"
else:
    AI_TEMPLATE = "example_rout/new/AI.L5X"
    DI_TEMPLATE = "example_rout/new/DI.L5X"
    DOut_TEMPLATE = "example_rout/new/DOut.L5X"

AI_TAG = "template/AITag.xml"
AI_RUNGS = "template/AIRungs.xml"
DI_TAG = "template/DITag.xml"
DI_RUNGS = "template/DIRungs.xml"
DOut_TAG = "template/DOutTag.xml"
DOut_RUNGS = "template/DOutRungs.xml"

AI_OUTPUT = "AI.L5X"
DI_OUTPUT = "DI.L5X"
DOut_OUTPUT = "DOut.L5X"


def printTags(controller:xml.etree.ElementTree.Element):
    tags = controller.find("Tags")
    if len(tags.findall("Tag")) == 0:
        print(f"{controller.attrib} - NO TAGS FOUND")
    for tag in tags.findall("Tag"):
        print(tag.attrib)


def printRungs(controller:xml.etree.ElementTree.Element):
    rllcontent = controller.find("Programs").find("Program").find("Routines").findall("Routine")[1].find("RLLContent")
    if (len(rllcontent.findall("Rung"))==0):
        print(f"{controller.attrib} - NO RUNGS FOUND")
    for rung in rllcontent.findall("Rung"):
        print(rung.attrib)


def createAITag(tag_name, description, no):
    new_tag = ET.parse(AI_TAG, parser=parser).getroot()
    new_tag.set("Name", tag_name)
    new_tag.find("Description").text = ET.CDATA(description)
    return new_tag


def createDITag(tag_name, description, no):
    new_tag = ET.parse(DI_TAG, parser=parser).getroot()
    new_tag.set("Name", tag_name)
    new_tag.find("Description").text = ET.CDATA(description)
    return new_tag


def createDOutTag(tag_name, description, no):
    new_tag = ET.parse(DOut_TAG, parser=parser).getroot()
    new_tag.set("Name", tag_name)
    new_tag.find("Description").text = ET.CDATA(description)
    return new_tag


def createAIRungs(tag_name, comment, no, local):
    new_rungs = ET.parse(AI_RUNGS, parser=parser).getroot().findall("Rung")
    for i, rung in enumerate(new_rungs):
        rung.set("Number", f"{3*no + i}")

        if format == "1":
            local_str = f"Local:{local[0]}:I.Ch{local[2]}."
        else:
            local_str = f"Local:{local[0]}:I.Ch{int(local[2])}"

        if i == 0:
            rung.find("Comment").text = ET.CDATA(f"Обработка аналогового датчика: {comment}")
            rung.find("Text").text = ET.CDATA(f"XIO({tag_name}.Imit_Mode)MOV({local_str}Data,{tag_name}.In.In_Aut);")
        if i == 1:
            rung.find("Text").text = ET.CDATA(f"JSR(_AI,1,{tag_name},{tag_name});")
    return new_rungs


def createDIRungs(tag_name, comment, no, local):
    new_rungs = ET.parse(DI_RUNGS, parser=parser).getroot().findall("Rung")
    for i, rung in enumerate(new_rungs):
        rung.set("Number", f"{3*no + i}")

        if format == "1":
            local_str = f"Local:{local[0]}:I.Pt{local[2]}"
            local_end_str = ""
        else:
            local_str = f"Local:{local[0]}:I"
            local_end_str = f".{int(local[2])}"

        if i == 0:
            rung.find("Comment").text = ET.CDATA(f"Обработка дискретного входа: {comment}")
            rung.find("Text").text = ET.CDATA(f"[XIO({tag_name}.In.Imit_Mode) XIC({local_str}.Data{local_end_str}) ,XIC({tag_name}.In.Imit_Mode) XIC({tag_name}.In.In_Imit) ]OTE({tag_name}.In.In_Aut);")
        if i == 1:
            rung.find("Text").text = ET.CDATA(f"XIO({tag_name}.In.Imit_Mode)XIC({local_str}.Fault{local_end_str})OTE({tag_name}.In.Fault);")
        if i == 2:
            rung.find("Text").text = ET.CDATA(f"JSR(_DI,1,{tag_name},{tag_name});")
    return new_rungs


def createDOutRungs(tag_name, comment, no, local):
    new_rungs = ET.parse(DOut_RUNGS, parser=parser).getroot().findall("Rung")
    for i, rung in enumerate(new_rungs):
        rung.set("Number", f"{3*no + i}")

        if format == "1":
            local_str = f"Local:{local[0]}:I.Pt{local[2]}."
            local_sec_str = f"Local:{local[0]}:LETTER.Pt{local[2]}."
            local_end_str = ""
        else:
            local_str = f"Local:{local[0]}:I"
            local_sec_str = f"Local:{local[0]}:LETTER"
            local_end_str = f".{int(local[2])}"

        if i == 0:
            rung.find("Comment").text = ET.CDATA(f"Обработка дискретного выхода: {comment}")
            rung.find("Text").text = ET.CDATA(f"XIC({local_str}.Fault{local_end_str})OTE(DOSAMPLE.In.Fault);") # OTE(DO1_Alarm_Off.In.Fault)
        if i == 1:
            rung.find("Text").text = ET.CDATA(f"JSR(_DO,1,DOSAMPLE,DOSAMPLE);")
        if i == 2:
            rung.find("Text").text = ET.CDATA(f"XIC(DOSAMPLE.Out.Out)OTE({local_sec_str}.Data{local_end_str});")
    return new_rungs

def addTag(controller:xml.etree.ElementTree.Element, ttype="", tag_name="", description="", no=0):
    tags = controller.find("Tags")
    new_tag = None
    if ttype == "AI":
        new_tag = createAITag(tag_name=tag_name, description=description, no=no)
    if ttype == "DI":
        new_tag = createDITag(tag_name=tag_name, description=description, no=no)
    if ttype == "DOut":
        new_tag = createDOutTag(tag_name=tag_name, description=description, no=no)
    tags.append(new_tag)
    print(f"{no}) Добавлен тег {local[0]}/{local[2]} {tag_name}")


def addRungs(controller:xml.etree.ElementTree.Element, ttype="", tag_name="", comment="", no=0, local=("99", "I", "99")):
    rllcontent = controller.find("Programs").find("Program").find("Routines").findall("Routine")[1].find("RLLContent")
    new_rungs = None
    if ttype == "AI":
        new_rungs = createAIRungs(tag_name=tag_name, comment=comment, no=no, local=local)
    if ttype == "DI":
        new_rungs = createDIRungs(tag_name=tag_name, comment=comment, no=no, local=local)
    if ttype == "DOut":
        new_rungs = createDOutRungs(tag_name=tag_name, comment=comment, no=no, local=local)
    for new_rung in new_rungs:
        rllcontent.append(new_rung)
    print(f"{no}) Добавлена обработка {local[0]}/{local[2]} {tag_name} : {comment}\n")

def getexceldata(filename=EXCELFILE):
    data = xl.readxl(fn=filename)
    return data

if __name__ == "__main__":
    try:
        # Таблица EXCEL
        data = getexceldata()

        # Структура файла AI.L5X
        ai_tree = ET.parse(source=AI_TEMPLATE, parser=parser)
        ai_root = ai_tree.getroot()
        ai_controller = ai_root[0]

        # Структура файла DI.L5X
        di_tree = ET.parse(source=DI_TEMPLATE, parser=parser)
        di_root = di_tree.getroot()
        di_controller = di_root[0]

        # Структура файла DOut.L5X
        dout_tree = ET.parse(source=DOut_TEMPLATE, parser=parser)
        dout_root = dout_tree.getroot()
        dout_controller = dout_root[0]

        # Проверим что шаблоны не заполнены
        #for controller in (ai_controller, di_controller, dout_controller):
        #    printTags(controller)
        #    printRungs(controller)

        # Построчное считывание и добавление тегов и строк в структуры
        ai = 0
        di = 0
        do = 0
        i = 0
        for row in data.ws(ws="Sheet1").rows:
            if row[0] == "ИМЯ ПО":
                continue
            if row[2] != "":

                # Информация из строки EXEL - Имя тега, описание, local
                tag_name = row[1]
                tag_description = f"{row[5]} {row[6]} {row[7]} {row[8]}"
                rungs_comment = "ОПИСАНИЕ"
                letter = row[2].split(":")[0]
                index1 = row[2].split(":")[1].split("/")[0]
                index2 = row[2].split(":")[1].split("/")[1]
                local = (index1, letter, index2)

                # Определение типа - AI/DI/DOut
                controller = None
                ttype = ""
                if "AI" in row[0]:
                    print(f"AI - {tag_name} - {tag_description}")
                    controller = ai_controller
                    ttype = "AI"
                    i = ai
                    ai += 1
                if "DI" in row[0]:
                    print(f"DI - {tag_name} - {tag_description}")
                    controller = di_controller
                    ttype = "DI"
                    i = di
                    di += 1
                if "DO" in row[0]:
                    print(f"DOut - {tag_name} - {tag_description}")
                    controller = dout_controller
                    ttype = "DOut"
                    i = do
                    do += 1

                # Добавление тега и строк в нужную рутину
                addTag(
                    controller=controller,
                    ttype=ttype,
                    tag_name=tag_name,
                    description=tag_description,
                    no=int(i)
                )
                addRungs(
                    controller=controller,
                    ttype=ttype,
                    tag_name=tag_name,
                    comment=rungs_comment,
                    no=int(i),
                    local=local
                )
                #time.sleep(0.01)

        # Проверим что шаблоны ЗАПОЛНЕНЫ
        #for controller in (ai_controller, di_controller, dout_controller):
        #    printTags(controller)
        #    printRungs(controller)

        ai_tree.write(f"{format}_{AI_OUTPUT}", encoding="UTF-8", xml_declaration=True)
        di_tree.write(f"{format}_{DI_OUTPUT}", encoding="UTF-8", xml_declaration=True)
        dout_tree.write(f"{format}_{DOut_OUTPUT}", encoding="UTF-8", xml_declaration=True)



    except Exception as ex:
        print(f"Ошибка выполнения\n{ex}")
        input("нажмите ENTER для выхода")
    finally:
        input("нажмите ENTER для выхода")
