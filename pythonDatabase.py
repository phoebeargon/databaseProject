"""
Authors: Paul Marshall & Phoebe Aargon
Date: 2/17/18
History:
    2/14/18 - Started, basic database metadata commands work
    2/17/18 - Finished, basic table metadata commands work and outputs line up
Goal: Create a simple database application written in python
"""
import os
import sys

#Program is a basic script for now, might become a proper program in further assignments
#Will probably add a main in next assignment and clean up repeated code

try: #try catch for checking the cntl d command, and EOF
    
    globalFolder = ""
    while(True): #loops until EOF or .EXIT
        
        command = raw_input("\n enter a command \n") #reads input from terminal, even < from files
        
        if ";" in command: 
            command = command[:-2] #Was running into weird chars at end of lines, so -1 gets rid of ; and -2 gets rid of those chars
        
        if "--" in command: #Pass comments
            pass

        elif "CREATE DATABASE" in command:
            folder = command.split("CREATE DATABASE ")[1] #Gets string after CREATE DATABASE
            if not os.path.exists(folder):
                os.makedirs(folder)
                print "Database " + folder + " created."
            else:
                print "!Failed to create database " + folder + " because it already exists."

        elif "DROP DATABASE" in command:
            folder = command.split("DROP DATABASE ")[1] #Gets string after DROP DATABASE
            if os.path.exists(folder):
                os.removedirs(folder)
                print "Database " + folder + " deleted."
            else:
                print "!Failed to delete database " + folder + " because it does not exist."

        elif "USE" in command:
            globalFolder = command.split("USE ")[1] #sets a global, that lets us know which folder to use
            print "Using database " + globalFolder + " ."

        elif "CREATE TABLE" in command:
            subFolder = command.split("CREATE TABLE ")[1]
            subFolder = subFolder.split(" (")[0]
            workFolder = os.path.join(os.getcwd(),globalFolder)
            fileName = os.path.join(workFolder,subFolder)
            if not os.path.isfile(fileName):
                with open(fileName,"w") as table: #opens with W for file creation
                    print "Table " + subFolder + " Created"
                    if "(" in command: #looks for arguments
                        data = command.split("(",1)[1] #pulls everything after (
                        data = data[:-1] #gets rid of the ending )
                        loopCount = data.count(",") #Gets number of arguments
                        for x in range(0,loopCount-1): #Number of arguments minus 1 to put it in array counting format
                            data[x] = command.split(",")[x] #Put them all in an array for easier printing and sorting
                        table.write(data) #write array to file

            else:
                print "!Failed to create table " + subFolder + " because it already exists"

        elif "DROP TABLE" in command:
            subFolder = command.split("DROP TABLE ")[1] #subFolder
            workFolder = os.path.join(os.getcwd(),globalFolder) #Formats strings for file path
            filePath = os.path.join(workFolder,subFolder) 
            if os.path.isfile(filePath):
                os.remove(filePath)
                print "Table " + subFolder + " deleted."
            else:
                print "!Failed to delete Table " + subFolder + " because it does not exist."

        elif "SELECT *" in command:
            tableName = command.split("FROM ")[1] #Gets string after FROM
            workFolder =  os.path.join(os.getcwd(),globalFolder)
            fileName = os.path.join(workFolder,tableName)
            if os.path.isfile(fileName):
                with open(fileName,"r+") as table: #as the tables should already be created, we can use r+
                    output = table.read()
                    print output
            else:
                print "!Failed to query table " + tableName + " because it does not exist."

        elif "ALTER TABLE" in command:
            tableName = command.split("ALTER TABLE ")[1]
            tableName = tableName.split(" ")[0]
            workFolder =  os.path.join(os.getcwd(),globalFolder)
            fileName = os.path.join(workFolder,tableName)
            if os.path.isfile(fileName):
                if "ADD" in command: #Only checks for add at time of first project
                    with open(fileName,"a") as table: # we can use A to apend data to end of files
                        additonString = command.split("ADD ")[1]
                        table.write(", " + additonString)
                        print "Table " + tableName + " modified."
            else:
                 print "!Failed to atler table " + tableName + " because it does not exist."
        
        elif ".EXIT" in command: #If files specifies to exit before EOF
            print "All done"
            exit()
                    
except EOFError: #EOF checks for CNTL D escapes as well
    print "exiting gracefully"
