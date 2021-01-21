# Import the sorted calendar for get_calendar
from get_calendar import sortedCalendar as calendar
import gspread
import time
import datetime
from gspread_formatting import *

gc = gspread.service_account()
sheet = gc.open("Deadlines").sheet1

# Formatting the header
sheet.update('A1', 'Date Due')
sheet.update('B1', 'Assignment')
sheet.update('C1', 'Completed')
sheet.format('A1:C1', {
    "backgroundColor":{
        "red": 70,
        "green": 70,
        "blue": 70,
        "alpha": 1
    },
    "horizontalAlignment": "CENTER",
    "textFormat": {
        "fontSize": 14,
        "bold": True
    }
})

last_cell = len(calendar) + 1
sheet.format('A2:C' + str(last_cell), {
    "textFormat":{
        "fontSize": 13
    }
})

con_rule_false = ConditionalFormatRule(
    ranges=[GridRange(sheetId=0, startRowIndex=1, endRowIndex=last_cell, startColumnIndex=0, endColumnIndex=3)],
    booleanRule=BooleanRule(
        condition=BooleanCondition('CUSTOM_FORMULA', ['=$C2=FALSE']),
        format=CellFormat(
            backgroundColor=color(0.95686275, 0.78039217, 0.7647059)
        )
    )
)

con_rule_true = ConditionalFormatRule(
    ranges=[GridRange(sheetId=0, startRowIndex=1, endRowIndex=last_cell, startColumnIndex=0, endColumnIndex=3)],
    booleanRule=BooleanRule(
        condition=BooleanCondition('CUSTOM_FORMULA', ['=$C2=TRUE']),
        format=CellFormat(
            backgroundColor=color(0.7176471, 0.88235295, 0.8039216)
        )
    )
)

rules = get_conditional_format_rules(sheet)
rules.clear()
rules.append(con_rule_false)
rules.append(con_rule_true)
rules.save()


# setting cells to a checkbox
check_box = DataValidationRule(
    BooleanCondition('BOOLEAN', [])
)
set_data_validation_for_cell_range(sheet, 'C2:C' + str(last_cell), check_box)

for row in range(len(calendar)):
    assignment = str(calendar[row][0])
    date = datetime.date.strftime(calendar[row][1], "%m/%d/%Y")
    date = '=DATEVALUE("' + date + '")'
    sheet.update_cell(row + 2, 1, date)
    sheet.update_cell(row + 2, 2, assignment)
    time.sleep(2) # due to API write restrictions, must sleep. 1 write per second per user is allowed
    