import re
import time
import lxml.etree as et
import pylightxl as xl
import easygui

from settings import *

parser = et.XMLParser(remove_blank_text=False, strip_cdata=False)

lines_skipped = 0
ai_lines = 0
di_lines = 0
dout_lines = 0


class LocalData:
    def __init__(self, address):
        self.address = address
        self.l_char = self.address.strip().split(":")[0]
        self.l_index1 = self.address.strip().split(":")[1].split("/")[0]
        self.l_index2 = self.address.strip().split(":")[1].split("/")[1]


def replace_all_in_cdata(text_string: str, tag_name: str, rung_comment: str, tag_description: str, local: LocalData):
    string = text_string
    replacements = {
        "[*tag_name*]": tag_name,
        "[*rung_comment*]": rung_comment,
        "[*l_char*]": local.l_char,
        "[*l_index1*]": local.l_index1,
        "[*l_index2*]": local.l_index2,
        "[*tag_description*]": tag_description
    }

    for key in replacements.keys():
        string = string.replace(key, replacements[key])

    return string.strip()


def print_tags(controller: et.ElementBase):
    tags = controller.find("Tags")
    if len(tags.findall("Tag")) == 0:
        print(f"{controller.attrib} - NO TAGS FOUND")
    for tag in tags.findall("Tag"):
        print(tag.attrib)


def print_rungs(controller: et.ElementBase):
    rllcontent = controller.find("Programs").find("Program").find("Routines").findall("Routine")[1].find("RLLContent")
    if len(rllcontent.findall("Rung")) == 0:
        print(f"{controller.attrib} - NO RUNGS FOUND")
    for rung in rllcontent.findall("Rung"):
        print(rung.attrib)


def create_tag(tag_file, tag_name, tag_description, no):
    new_tag = et.parse(tag_file, parser=parser).getroot()
    new_tag.set("Name", tag_name)
    new_tag.find("Description").text = et.CDATA(tag_description)
    return new_tag


def create_rungs(rungs_file: str, tag_name: str, rung_comment: str, no: int, local: LocalData):
    new_rungs = et.parse(rungs_file, parser=parser).getroot().findall("Rung")
    for i, rung in enumerate(new_rungs):
        rung.set("Number", f"{3 * no + i}")

        try:
            new_comment = replace_all_in_cdata(text_string=rung.find("Comment").text, tag_name=tag_name,
                                               rung_comment=rung_comment, tag_description="???", local=local)
            rung.find("Comment").text = et.CDATA(new_comment)
        except:
            pass
        new_text = replace_all_in_cdata(text_string=rung.find("Text").text, tag_name=tag_name,
                                        rung_comment=rung_comment, tag_description="???", local=local)
        rung.find("Text").text = et.CDATA(new_text)

    return new_rungs


def add_tag(controller: et.ElementBase, ttype="", tag_name="", tag_description="", no=0):
    tags = controller.find("Tags")

    tag_file = None
    if ttype == "AI":
        tag_file = AI_TAG
    if ttype == "DI":
        tag_file = DI_TAG
    if ttype == "DOut":
        tag_file = DOUT_TAG

    new_tag = create_tag(tag_file=tag_file, tag_name=tag_name, tag_description=tag_description, no=no)
    tags.append(new_tag)
    print(f"{no}) Добавлен тег {row[ADDR]} {tag_name}")


def add_rungs(controller: et.ElementBase, routine: str, tag_name: str, rung_comment: str, no: int,
              local: LocalData):
    rllcontent = controller.find("Programs").find("Program").find("Routines").findall("Routine")[1].find("RLLContent")

    rungs_file = None
    if routine == "AI":
        rungs_file = AI_RUNGS
    if routine == "DI":
        rungs_file = DI_RUNGS
    if routine == "DOut":
        rungs_file = DOUT_RUNGS

    new_rungs = create_rungs(rungs_file=rungs_file, tag_name=tag_name, rung_comment=rung_comment, no=no, local=local)
    for new_rung in new_rungs:
        rllcontent.append(new_rung)
    print(f"{no}) Добавлена обработка {local.address} {tag_name} : {rung_comment}\n")


def get_excel_data(filename):
    data = xl.readxl(fn=filename)
    return data


if __name__ == "__main__":
    try:
        # Таблица EXCEL
        file = easygui.fileopenbox(msg="Выберите XLSX файл. Signal processing for InTA", default="./import/*.xlsx",
                                   filetypes=["*.xlsx"])
        data = get_excel_data(file)

        # Структура файла AI.L5X
        ai_tree: et = et.parse(source=AI_EMPTY_FILE, parser=parser)
        ai_root = ai_tree.getroot()
        ai_controller = ai_root[0]

        # Структура файла DI.L5X
        di_tree: et = et.parse(source=DI_EMPTY_FILE, parser=parser)
        di_root = di_tree.getroot()
        di_controller = di_root[0]

        # Структура файла DOut.L5X
        dout_tree: et = et.parse(source=DOUT_EMPTY_FILE, parser=parser)
        dout_root = dout_tree.getroot()
        dout_controller = dout_root[0]

        # Проверим что шаблоны не заполнены
        # for controller in (ai_controller, di_controller, dout_controller):
        #    print_tags(controller)
        #    print_rungs(controller)

        # Построчное считывание и добавление тегов и строк в структуры
        i = 0
        # проход по строкам xlsx файла
        for row in data.ws(ws="Sheet1").rows:
            routine = row[ROUTINE]
            address = row[ADDR]
            tag_name = row[TAG_NAME]

            # пропуск первой строки
            if routine == "ИМЯ ПО":
                continue

            # пропуск если строка адреса пустая
            if not address.strip():
                continue

            # блок выполняется только если ADDR записан верно
            elif re.match(r'^([I]|[Q]){1}[W]{0,1}[:][0-9]{1,2}[/][0-9]{2}$', address.strip()):

                # пропуск если стока имени тега пустая
                if not tag_name.strip():
                    print(f"Отсутствует имя тега у {address}, пропуск итерации\n")
                    lines_skipped += 1
                    continue

                tag_description = f"{row[DESCA]} {row[DESCB]} {row[DESCC]} {row[DESCD]} {row[DESCE]}".strip()

                try:
                    rung_comment = str(row[ROUT_DESC]).strip()
                except:
                    rung_comment = ""

                # Определение типа - AI/DI/DOut
                controller = None
                if "AI" in routine:
                    controller = ai_controller
                    routine = "AI"
                    i = ai_lines
                    ai_lines += 1
                elif "DI" in routine:
                    controller = di_controller
                    routine = "DI"
                    i = di_lines
                    di_lines += 1
                elif "DO" in routine:
                    controller = dout_controller
                    routine = "DOut"
                    i = dout_lines
                    dout_lines += 1
                else:
                    print(f"НЕВЕРНОЕ ИМЯ ПО ({routine}) У {address}, ЗАВЕРШЕНИЕ С ОШИБКОЙ\n")
                    raise Exception
                print(f"{routine} - {address} - {tag_name} - {tag_description}")

                # Добавление тега и строк в нужную рутину
                add_tag(
                    controller=controller,
                    ttype=routine,
                    tag_name=tag_name,
                    tag_description=tag_description,
                    no=int(i)
                )
                local = LocalData(address)
                add_rungs(
                    controller=controller,
                    routine=routine,
                    tag_name=tag_name,
                    rung_comment=rung_comment,
                    no=int(i),
                    local=local
                )
                # time.sleep(0.01)
            else:
                print(f"НЕВЕРНЫЙ LOCAL: {address}, ЗАВЕРШЕНИЕ С ОШИБКОЙ\n")
                raise Exception

        # Проверим что шаблоны ЗАПОЛНЕНЫ
        # for controller in (ai_controller, di_controller, dout_controller):
        #    print_tags(controller)
        #    print_rungs(controller)

        try:
            ai_tree.write(f"{controller_version}_{AI_OUTPUT}", encoding="UTF-8", xml_declaration=True, )
            di_tree.write(f"{controller_version}_{DI_OUTPUT}", encoding="UTF-8", xml_declaration=True)
            dout_tree.write(f"{controller_version}_{DOut_OUTPUT}", encoding="UTF-8", xml_declaration=True)
            print(f"Файлы {controller_version}_*.L5X успешно записаны!")
        except Exception as ex:
            print(ex)
            print("При записи файлов произошла ошибка. Возможно файлы не сохранены")

        print(
            f"УСПЕШНО ЗАВЕРШЕНО\nПропущено строк: {lines_skipped}\nОбработано строк: {ai_lines + di_lines + dout_lines}")
        input("нажмите ENTER для выхода")
    except Exception as ex:
        print(f"Ошибка выполнения\n{ex}")
        input("нажмите ENTER для выхода")
