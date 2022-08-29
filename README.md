## RSLogix генерация обработки сигналов из табличных данных - v20, v28.

---

## **Описание**
Скрипт получает на вход xlsx таблицу, в меню происходит выбор версии. На выходе генерирует обработку сигналов AI, DI и DOut в L5X формате

## **Содержание .env**
Файл конфигурации скрипта с информацией о порядке столбцов в таблице и имени выходных файлов

## **Содержание каталогов routine_file и template**
- Каталог routine_file содержит подкаталоги для различных версий. В них помещены L5X основы для вывода с пустым содержимым тегов \<Tags> и \<RLLContent>
- Каталог template содержит подкаталоги для версий. В них находятся XML файлы с шаблонами: *Tag.xml и *Rungs.xml. В файлах шаблонов для замены существует разметка:
  1. В `[*tag_name*]` подставляется имя тега
  2. В `[*tag_description*]` подставляется описание тега
  3. В `[*rung_comment*]` подставляется комментарий в рутине
  4. `[*l_index1*], [*l_char*], [*l_index2*]` - места для подставки символов из поля ADDR
- Подкаталоги для версий должны содержать в названии `версию` и `имя контроллера`, разделенные пробельным символом (прим: `v28_new PLC_LO1_IAT`). При добавлении новых шаблонов - требуется создать каталоги с файлами повторяя описанную выше разметку (в каталогах routine_file и template)

## **Содержание каталога import**
- В каталог import для удобства помещаются импортируемые файлы. Делать это не обязательно
- Поддерживаются **ТОЛЬКО** XLSX файлы (Excel 2007+)

## **Запуск интерпретатором / сборка скрипта в exe** 
- Требования: Python 3.10+ и система с его поддержкой
- Зависимости: *lxml, pylightxl, easygui, python-dotenv*
- Для установки зависимостей: ```pip install -r requirements.txt```
- Для сборки в exe требуется пакет pyinstaller: ```pyinstaller - F .\RSLogix_generator.py```. **Готовый exe находится в каталоге dist. ОБЯЗАТЕЛЬНО скопировать к нему каталоги import, routine_file, template и файл .env**
