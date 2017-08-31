from openpyxl import load_workbook, Workbook

def processSalary(fileName):

    # Load main sheet of file
    wb = load_workbook(filename=fileName)
    ws = wb.get_sheet_by_name(fileName)

    size = ws.get_highest_row()
    print size
