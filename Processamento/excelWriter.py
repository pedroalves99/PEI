import xlsxwriter
from openpyxl import load_workbook
from copy import copy


def create_excel(filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    cell_format1 = workbook.add_format({ #blue
        'bold': True,
        'fg_color': '#20B2AA',
        'align': 'center',
        'border': 1,
        'valign': 'vcenter'})

    cell_format2 = workbook.add_format({ #green
        'bold': True,
        'fg_color': '#90EE90',
        'align': 'center',
        'border': 1,
        'valign': 'vcenter'})


    merge_format = workbook.add_format({ #laranja
        'bold': 1,
        'align': 'center',
        'border': 1,
        'valign': 'vcenter',
        'fg_color': '#FFA07A'})

    cell_format3 = workbook.add_format({  # rosa
        'bold': True,
        'fg_color': '#F0E68C',
        'align': 'center',
        'border': 1,
        'valign': 'vcenter'})

    cell_format4 = workbook.add_format({
        'bold': True,
        'fg_color':'#FFDAB9',
        'align': 'center',
        'border': 1,
        'valign': 'vcenter'})

    cell_format5 = workbook.add_format({
        'bold': True,
        'fg_color': '#808000',
        'align': 'center',
        'border': 1,
        'valign': 'vcenter'})

    cell_format6 = workbook.add_format({
        'bold': True,
        'fg_color': '#F5F5DC',
        'align': 'center',
        'border': 1,
        'valign': 'vcenter'})

    worksheet.set_row(0, 25)
    worksheet.set_column(0, 0, 60)
    worksheet.set_column(1, 1, 25)
    #cardinal columns
    for i in range(2,10):
        worksheet.set_column(i, i, 5)

    #cardinal columns
    for i in range(10,18):
        worksheet.set_column(i, i, 5)


    # area e perimeter columns
    for i in range(18, 26):
        worksheet.set_column(i, i, 5)

    for i in range(26, 30):
        worksheet.set_column(i, i, 10)


    worksheet.merge_range('C1:J1', 'Global Vectors Dislocation(mm)', merge_format) #global vector

    worksheet.merge_range('K1:R1', 'Center of Mass Dislocation(mm)', cell_format3) #centro de massa

    worksheet.merge_range('S1:Z1', 'Reference Contour Dislocation(mm)', cell_format4)  #reference contour

    worksheet.merge_range('AA1:AB1', 'Area(mm^2)', cell_format5)  # Area contour

    worksheet.merge_range('AC1:AD1', 'Perimeter(mm)', cell_format6)  # Area contour

    worksheet.write("A1", "Video Name", cell_format1 )
    worksheet.write("A2", "", cell_format1)

    worksheet.write("B1", "Evaluation Type", cell_format2)
    worksheet.write("B2", "", cell_format2)

    ## cardinal global vectors
    worksheet.write("C2", "N", merge_format)
    worksheet.write("D2", "NE", merge_format)
    worksheet.write("E2", "E", merge_format)
    worksheet.write("F2", "SE", merge_format)
    worksheet.write("G2", "S", merge_format)
    worksheet.write("H2", "SW", merge_format)
    worksheet.write("I2", "W", merge_format)
    worksheet.write("J2", "NW", merge_format)

    ## cardinal centro de massa
    worksheet.write("K2", "N", cell_format3)
    worksheet.write("L2", "NE", cell_format3)
    worksheet.write("M2", "E", cell_format3)
    worksheet.write("N2", "SE", cell_format3)
    worksheet.write("O2", "S", cell_format3)
    worksheet.write("P2", "SW", cell_format3)
    worksheet.write("Q2", "W", cell_format3)
    worksheet.write("R2", "NW", cell_format3)

    ## cardinal reference contour
    worksheet.write("S2", "N", cell_format4)
    worksheet.write("T2", "NE", cell_format4)
    worksheet.write("U2", "E", cell_format4)
    worksheet.write("V2", "SE", cell_format4)
    worksheet.write("W2", "S", cell_format4)
    worksheet.write("X2", "SW", cell_format4)
    worksheet.write("Y2", "W", cell_format4)
    worksheet.write("Z2", "NW", cell_format4)


    #perimeter and Area
    worksheet.write("AA2", "Initial", cell_format5)
    worksheet.write("AB2", "Final", cell_format5)

    worksheet.write("AC2", "Initial", cell_format6)
    worksheet.write("AD2", "Final", cell_format6)


    workbook.close()


def get_style(ws, index, y):
    if ws.cell(index - 1, y).has_style:
        print("ll")
        ws.cell(index, y)._style = copy(ws.cell(index - 1, y)._style)
    else: print("não encontrou o estilo")

def set_value(ws, index, p, value):
    get_style(ws, index, p)
    ws.cell(index, p).value = value



def add_data(filename, video_name, eval_type, global_dislocation, cm_dislocation, reference_dislocation, area_initial, area_final, perimeter_initial, perimeter_final):
    index = 1
    found = False
    workbook = load_workbook(filename)

    ws = workbook.worksheets[0]

    while not found:    #ve a proxima linha livre para escrever
        for j in range(1,26):
            if ws.cell(index, j).value:
                index += 1
                found = False
                break
            else: found = True

    print(index)
    # passa o style para a célula de baixo

    set_value(ws, index, 1, video_name)

    set_value(ws, index, 2, eval_type)

    p = 3

    if len(global_dislocation) == 8:
        for elem in global_dislocation:
            set_value(ws, index, p, round(elem, 3))
            p+=1

    else:
        max8 = p + 8
        for v in range (p, max8):
            set_value(ws, index, p, "")


    if len(cm_dislocation) == 8:
        for elem in cm_dislocation:
            set_value(ws, index, p, round(elem, 3))
            p += 1
    else:
        max8 = p + 8
        for v in range(p, max8):
            set_value(ws, index, p, "")

    if len(reference_dislocation) == 8:
        for elem in reference_dislocation:
            set_value(ws, index, p, round(elem, 3))
            p += 1
    else:
        max8 = p + 8
        for v in range(p, max8):
            set_value(ws, index, p, "")

    set_value(ws, index, p, area_initial)
    p += 1

    set_value(ws, index, p, area_final)
    p += 1

    set_value(ws, index, p, perimeter_initial)
    p += 1

    set_value(ws, index, p, perimeter_final)
    p += 1

    workbook.save(filename)


