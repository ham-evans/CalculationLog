import os 
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def getDescriptions (path): 
    dirPath = os.path.dirname(path)
    directory = os.fsencode(dirPath)
    allDescriptions = {}
    for file in os.listdir(directory):
        file = file.decode('UTF-8')
        filename = os.fsdecode(file)
        if filename.endswith('.gjf') or filename.endswith('.com'):
            allDescriptions[filename] = (input(filename + ': '))

    return allDescriptions

def writeLog (file, allDescriptions, user, worksheetNum, path): 
    date, time, fileName, fileType, method, basisSet, specifications = parseInputFile (file, path)
    message = allDescriptions[file]
    
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('CalcLog.json', scope)
    client = gspread.authorize(creds)
    
    sheet = client.open('Calculation Log').get_worksheet(worksheetNum)
    sheet.append_row([user, date, time, fileName, fileType, method, basisSet, specifications, message])
    print('Added ' + file + ' to calculation log.')
    print()
        
def parseInputFile (file, path):
    file =open(path + file, 'r')
    basisSet = ''
    
    for line in file:
        if "%chk" in line: 
            fileName = line[5:-5]
            
        if '#' in line: 
            specifications = line[2:-1]
            split = line.index('/') + 1
            
            try:
                endBasis = len(line) - 1 - line[::-1].index(' ')
                basisSet = line[split:endBasis]
            except: 
                continue
            
            if basisSet == '': 
                basisSet = line[split:-1]
                
            method = line[:split -1]
            startMethod = len(method) - method[::-1].index(' ')
            method = method[startMethod:]
                
            if 'modredundant' in line: 
                fileType = 'Scan'
            elif 'opt' and 'freq' in line: 
                fileType = 'Opt + Freq'
            elif 'opt' in line: 
                fileType = 'Opt'
            elif 'freq' in line: 
                fileType = 'Freq'
            elif 'irc' in line: 
                fileType = 'IRC'
            else: 
                fileType = 'Energy'
                
    date = str(datetime.date(datetime.now()))
    time = str(datetime.time(datetime.now())).split('.')[0]
                
    return date, time, fileName, fileType, method, basisSet, specifications

def run (): 
    user = input('Input your name: ')
    
    if 'h' in user.lower(): 
        user = 'Ham'
        path = '/Users/VasiliouLab/Documents/HamCalc/Vanillin/WORKSTATION/'
        mvPath = '/Users/VasiliouLab/Documents/HamCalc/Vanillin/WORKSTATIONdump/'
        worksheetNum = 0
    elif 'j' in user.lower():
        user = 'Jane'
        path = '/Users/VasiliouLab/Documents/JaneCalc/run/'
        mvPath = '/Users/VasiliouLab/Documents/JaneCalc/process/'
        worksheetNum = 1
    elif 'p' in user.lower():
        user = 'Priya'
        path = '/Users/VasiliouLab/Documents/PriyaCalc/run/'
        mvPath = '/Users/VasiliouLab/Documents/PriyaCalc/process/'
        worksheetNum = 2
    
    print('Input File Descriptions: ')
    descriptions = getDescriptions(path)
    print()
    
    dirPath = os.path.dirname(path)
    directory = os.fsencode(dirPath)
    
    for file in os.listdir(directory):
        file = file.decode('UTF-8')
        filename = os.fsdecode(file)
        if filename.endswith('.gjf') or filename.endswith('.com'):
            writeLog(filename, descriptions, user, worksheetNum, path)
            print('Started Calculation ' + str(filename) + ' at ' + str(datetime.now())[:-7])
            os.system('g16 ' + path + str(filename))
            print('Finished Calculation ' + str(filename) + ' at ' + str(datetime.now())[:-7])
            print()
            os.system('mv ' + path + str(filename) + ' ' + mvPath) 
            try: 
                os.system('mv ' + path + str(filename)[:-3] + 'log ' + mvPath)
            except:
                continue
            
            try:
                os.system('mv ' + '/Users/VasiliouLab/Documents/RUNCALC/' + str(filename)[:-3] + 'chk ' + mvPath)
            except: 
                continue
            
            print('Files moved to process folder.')
            print()
        
run ()
