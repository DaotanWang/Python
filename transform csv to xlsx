import openpyxl
import csv

def csv2xlsx():  # csv转为xlsx
    with open('D:\BATA.csv', 'r', encoding='utf-8') as f:
        read = csv.reader(f)

        wb = openpyxl.Workbook()
        ws = wb.active
        for line in read:
            ws.append(line)
        wb.save('D:\BATA.xlsx')


if __name__ == '__main__':
    csv2xlsx()
