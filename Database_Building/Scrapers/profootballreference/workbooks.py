import xlsxwriter

def generate_workbook(file):
    # initialize workbook
    workbook = xlsxwriter.Workbook(file)
    bold = workbook.add_format({'bold': True})
    worksheets = {
        "PLAYS": workbook.add_worksheet("PLAYS"),
        "PASS": workbook.add_worksheet("PASS"),
        "RUSH": workbook.add_worksheet("RUSH"),
        "DEF": workbook.add_worksheet("DEF"),
        "ST": workbook.add_worksheet("ST"),
        "PENALTY": workbook.add_worksheet("PENALTY")
    }

    # write play headers
    worksheets['PLAYS'].write(0,0, 'PLAY ID',bold)
    worksheets['PLAYS'].write(0,1, 'GAME ID',bold)
    worksheets['PLAYS'].write(0,2, 'QUARTER',bold)
    worksheets['PLAYS'].write(0,3, 'TIME REMAIN',bold)
    worksheets['PLAYS'].write(0,4, 'DOWN',bold)
    worksheets['PLAYS'].write(0,5, 'YDS TO GO',bold)
    worksheets['PLAYS'].write(0,6, 'LOCATION',bold)
    worksheets['PLAYS'].write(0,7, 'RESULT',bold)
    worksheets['PLAYS'].write(0,8, 'SCORE HOME',bold)
    worksheets['PLAYS'].write(0,9, 'SCORE AWAY',bold)
    worksheets['PLAYS'].write(0,10, 'EXPECTED POINTS BEFORE',bold)
    worksheets['PLAYS'].write(0,11, 'EXPECTED POINTS AFTER',bold)

    # write pass headers
    worksheets['PASS'].write(0,0, 'PLAY ID',bold)
    worksheets['PASS'].write(0,1, 'QB',bold)
    worksheets['PASS'].write(0,2, 'WR',bold)
    worksheets['PASS'].write(0,3, 'YARDS',bold)
    worksheets['PASS'].write(0,4, 'DEPTH',bold)
    worksheets['PASS'].write(0,5, 'LOCATION',bold)
    worksheets['PASS'].write(0,6, 'RESULT',bold)

    # write rush headers
    worksheets['RUSH'].write(0,0, 'PLAY ID',bold)
    worksheets['RUSH'].write(0,1, 'RB',bold)
    worksheets['RUSH'].write(0,2, 'YARDS',bold)
    worksheets['RUSH'].write(0,3, 'LOCATION',bold)
    worksheets['RUSH'].write(0,4, 'BOX_LOCATION',bold)
    worksheets['RUSH'].write(0,5, 'RESULT',bold)

    # write play headers
    worksheets['DEF'].write(0,0, 'PLAY ID',bold)
    worksheets['DEF'].write(0,1, 'TYPE',bold)
    worksheets['DEF'].write(0,2, 'STOPPAGE',bold)
    worksheets['DEF'].write(0,3, 'DEF1',bold)
    worksheets['DEF'].write(0,4, 'DEF2',bold)
    worksheets['DEF'].write(0,5, 'YARDS',bold)
    worksheets['DEF'].write(0,6, 'RTN YARDS',bold)
    worksheets['DEF'].write(0,7, 'OFF POINTS',bold)
    worksheets['DEF'].write(0,8, 'DEF POINTS',bold)

    # write special teams headers
    worksheets['ST'].write(0,0, 'PLAY ID',bold)
    worksheets['ST'].write(0,1, 'KICKER',bold)
    worksheets['ST'].write(0,2, 'TYPE',bold)
    worksheets['ST'].write(0,3, 'RETURNER',bold)
    worksheets['ST'].write(0,4, 'YARDS',bold)
    worksheets['ST'].write(0,5, 'RTN YARDS',bold)
    worksheets['ST'].write(0,6, 'RESULT',bold)

    # write penalty headers
    worksheets['PENALTY'].write(0,0, 'PLAY ID',bold)
    worksheets['PENALTY'].write(0,1, 'TEAM',bold)
    worksheets['PENALTY'].write(0,2, 'RESULT',bold)
    worksheets['PENALTY'].write(0,3, 'YARDS',bold)

    return workbook,worksheets
