import os, sys

startStrings = ['XEW', 'XComGame'] # the strings that a valid Xcom folder must start with
connector = ' - ' # the connector between startString and mod name

launcherFolderName = '.XCOMLauncher'
launcherFolderPath = os.path.join(os.getcwd(), launcherFolderName)

dataFileName = 'folders'
dataFilePath = os.path.join(launcherFolderPath, dataFileName)

currentFolderFileName = 'current'
currentFolderFilePath = os.path.join(launcherFolderPath, currentFolderFileName)

EUDataFileName = 'folders_EU'
EUDataFilePath = os.path.join(launcherFolderPath, dataFileName)

EUCurrentFolderFileName = 'current_EU'
EUCurrentFolderFilePath = os.path.join(launcherFolderPath, currentFolderFileName)

currentMod = ''
modsList = []

EUCurrentMod = ''
EUModsList = []

def isXEW(name):
    '''
    Returns true if folder is a valid XEW folder, false otherwise
    '''
    if name[:len(startStrings[0])] == startStrings[0]:
        return True
    else:
        return False

def isXEU(name):
    '''
    Returns true if folder is a valid XEU folder, false otherwise
    '''
    if name[:len(startStrings[1])] == startStrings[1]:
        return True
    else:
        return False

def IsXcomFolder(name):
    '''
    Checks if the folder by the name is a valid Xcom folder (starts with XEW or XComGame)
    Returns true if it is a valid folder, false otherwise
    '''

    if name[:len(startStrings[0])] == startStrings[0] or name[:len(startStrings[1])] == startStrings[1]:
        return True
    else:
        return False

def scan():
    '''
    Scans the parent folder for directories which are Xcom directories and writes the directories to the data file.
    '''

    # filter out the folders into xcomDirectories
    dirObjs = os.listdir(os.getcwd())
    directories = filter(os.path.isdir, dirObjs)
    xcomDirectories = filter(IsXcomFolder, directories)

    # write to the data file in .XCOMLauncher
    if not os.path.exists(launcherFolderPath):
        os.makedirs(launcherFolderPath)

    with open(dataFilePath, 'w'), open(EUDataFilePath, 'w') as dataFile, EUDataFile:
        for xcomDir in xcomDirectories:
            # if the directory name is the default name for Enemy Within (the one launched by steam) ...
            if xcomDir == 'XEW':
                # then ask the user for the name of the mod. This will be written as the current mod
                modName = raw_input('Detected default directory for XCOM: Enemy Within, please enter mod name: ')
                xcomDir = startString + connector + modName

                with open(currentFolderFilePath, 'w') as currentFile:
                    currentFile.write(xcomDir)

            # if the directory name is the default name for Enemy Unknown (the one launched by steam) ...
            elif xcomDir == 'XComGame':
                # then ask the user for the name of the mod. This will be written as the current mod
                modName = raw_input('Detected default directory for XCOM: Enemy Unknown, please enter mod name: ')
                xcomDir = startString + connector + modName

                with open(EUCurrentFolderFilePath, 'w') as currentFile:
                    EUCurrentFile.write(xcomDir)

            if isXEW(xcomDir):
                dataFile.write(xcomDir + '\n')
            else:
                EUDataFile.write(xcomDir + '\n')

def loadFolders():
    '''
    load the current folders into a list, as well as the currently loaded mod.
    '''
    global modsList
    global currentMod

    global EUModsList
    global EUCurrentMod

    try:
        dataFile = open(dataFilePath, 'r')
    except IOError:
        scan()
        dataFile = open(dataFilePath, 'r')

    for line in dataFile:
        modsList += [line[:-1]] # stripping the last character (newline)
    print modsList

    dataFile.close()

    try:
        currentFile = open(currentFolderFilePath, 'r')
        for line in currentFile:
            currentMod = line
        currentFile.close()
    except IOError:
        currentMod = ''

    try:
        EUDataFile = open(EUDataFilePath, 'r')
    except IOError:
        scan()
        EUDataFile = open(EUDataFilePath, 'r')

    for line in EUDataFile:
        EUModsList += [line[:-1]] # stripping the last character (newline)
    print modsList

    EUDataFile.close()

    try:
        EUCurrentFile = open(EUCurrentFolderFilePath, 'r')
        for line in EUCurrentFile:
            EUCurrentMod = line
        EUCurrentFile.close()
    except IOError:
        EUCurrentMod = ''

    print EUCurrentMod

def PrettyFolderName(folderName):
    '''
    Returns a prettyified folderName.
    e.g., returns 'Long War' for 'XEW - Long War' if startString is 'XEW' and connector is ' - '
    '''
    if isXEW(folderName):
        return folderName[len(startStrings[0]) + len(connector):]
    else
        return foldername[len(startStrings[1]) + len(connector):]

def SwitchToMod(modName):
    '''
    Switches the folder layout of the parent folder to switch the default game folder (XEW) to match the mod named modName
    '''
    global currentMod
    global EUCurrent

    if modName == currentMod or modName == EUCurrentMod:
        return # already on modName, no need to do anything

    if isXEW(modName):
        if currentMod != '':
            os.rename('XEW', currentMod)

        os.rename(modName, 'XEW')
        currentMod = modName
        with open(currentFolderFilePath, 'w') as currentFile:
            currentFile.write(currentMod)

    elif isXEU(modName):
        if EUCurrentMod != '':
            os.rename('XComGame', EUCurrentMod)

        os.rename(modName, 'XComGame')
        EUCurrentMod = modName
        with open(EUCurrentFolderFilePath, 'w') as currentFile:
            currentFile.write(EUCurrentMod)
def main():
    loadFolders()

    print 'What mod do you want to make default?'
    for i, mod in zip(range(len(modsList)), modsList):
        print i, PrettyFolderName(mod)

    modIndex = input()
    if not isinstance(modIndex, (int, long)) or modIndex >= len(modsList) or modIndex < 0:
        print 'Invalid mod, exiting...'
        sys.exit()
    else:
        SwitchToMod(modsList[modIndex])

if __name__ == '__main__':
    main()
