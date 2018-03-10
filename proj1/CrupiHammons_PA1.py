"""
Created by Alex Crupi and Chase Hammons, 2/18/18, version 1
"""
import os

def useEnabled(): #Catch when a database isn't enabled
    if globalScopeDirectory is "":
        raise ValueError("!Failed to use table because no database is selected")

try: #This will check the CTRL D command, and the EOF
    
    globalScopeDirectory = "" #Create here for increased scope

    while(True): #exit loop at EOF or .EXIT
        
        command = raw_input("\n enter a command \n") #Read input from terminal
        
        if ";" in command:
            command = command[:-2] #Was running into weird chars at end of lines, so -1 gets rid of ; and -2 gets rid of those chars
        
        if "--" in command: #Pass comments
            pass

        elif "CREATE DATABASE" in command:
            try:
                directory = command.split("CREATE DATABASE ")[1] #Store the string after CREATE DATABASE
                if not os.path.exists(directory): #Only create if it doesn't exist
                    os.makedirs(directory)
                    print "Database " + directory + " created."
                else:
                    print "!Failed to create database " + directory + " because it already exists"
            except IndexError:
                print "!No database name specified"


        elif "DROP DATABASE" in command:
            try:
                directory = command.split("DROP DATABASE ")[1] #Store the string after DROP DATABASE
                if os.path.exists(directory): #Ensure database exists
                    for toRemove in os.listdir(directory): #Empty folder, then remove folder
                        os.remove(directory + "/" + toRemove)
                    os.rmdir(directory)
                    print "Database " + directory + " deleted."
                else:
                    print "!Failed to delete database " + directory + " because it does not exist"
            except IndexError:
                print "!No database name specified"

        elif "USE" in command:
            try:
                globalScopeDirectory = command.split("USE ")[1] #Store the string after USE (with 'global' scope)
                if os.path.exists(globalScopeDirectory):
                    print "Using database " + globalScopeDirectory + " ."
                else:
                    raise ValueError("!Failed to use database because it does not exist")
            except IndexError:
                print "!No database name specified"
            except ValueError as err:
                print err.args[0]

        elif "CREATE TABLE" in command:
            try:
                useEnabled() #Ensure database is selected
                subDirectory = command.split("CREATE TABLE ")[1] #Get string to use for table name
                subDirectory = subDirectory.split(" (")[0]
                workingDirectory = os.path.join(os.getcwd(),globalScopeDirectory)
                fileName = os.path.join(workingDirectory,subDirectory)
                if not os.path.isfile(fileName):
                    with open(fileName,"w") as table: #Create file to act as table
                        print "Table " + subDirectory + " created."
                        if "(" in command: #Check for start of argument section
                            out = [] #Create list for output to file
                            data = command.split("(",1)[1] #Remove (
                            data = data[:-1] #Remove )
                            loopCount = data.count(",") #Count the number of arguments
                            for x in range(loopCount+1):
                                out.append(data.split(",")[x]) #Import all arguments into list for printing and sorting later
                            table.write( ", ".join(out) ) #Output the array to a file

                else:
                    print "!Failed to create table " + subDirectory + " because it already exists"
            except IndexError:
                print "!Failed to remove Table because no table name is specified"
            except ValueError as err:
                print err.args[0]

        elif "DROP TABLE" in command:
            try:
                useEnabled() #Ensure database is selected
                subDirectory = command.split("DROP TABLE ")[1] #Get string to use for table name
                workingDirectory = os.path.join(os.getcwd(),globalScopeDirectory) #Format strings for file path
                filePath = os.path.join(workingDirectory,subDirectory) 
                if os.path.isfile(filePath):
                    os.remove(filePath)
                    print "Table " + subDirectory + " deleted."
                else:
                    print "!Failed to delete Table " + subDirectory + " because it does not exist"
            except IndexError:
                print "!Failed to remove Talbe because no table name is specified"
            except ValueError as err:
                print err.args[0]

        elif "SELECT *" in command:
            try:
                useEnabled() #Ensure database is selected
                tableName = command.split("FROM ")[1] #Get string to use for table name
                workingDirectory =  os.path.join(os.getcwd(),globalScopeDirectory)
                fileName = os.path.join(workingDirectory,tableName)
                if os.path.isfile(fileName):
                    with open(fileName,"r+") as table: #Since there should already be tables created, use r+
                        output = table.read()
                        print output
                else:
                    print "!Failed to query table " + tableName + " because it does not exist"
            except IndexError:
                print "!Failed to remove Talbe because no table name is specified"
            except ValueError as err:
                print err.args[0]

        elif "ALTER TABLE" in command:
            try:
                useEnabled() #Ensure database is selected
                tableName = command.split("ALTER TABLE ")[1]
                tableName = tableName.split(" ")[0]
                workingDirectory =  os.path.join(os.getcwd(),globalScopeDirectory)
                fileName = os.path.join(workingDirectory,tableName)
                if os.path.isfile(fileName):
                    if "ADD" in command: #Only checks for add at time of first project
                        with open(fileName,"a") as table: #Use A to append data to end of the file
                            additionalString = command.split("ADD ")[1]
                            table.write(", " + additionalString)
                            print "Table " + tableName + " modified."
                else:
                     print "!Failed to atler table " + tableName + " because it does not exist"
            except IndexError:
                print "!Failed to remove Talbe because no table name is specified"
            except ValueError as err:
                print err.args[0]
        
        elif ".EXIT" in command: #Exit if specified before EOF
            print "All done"
            exit()

except (EOFError, KeyboardInterrupt) as e: #Exit elegantly
    print "\nConnection to database terminated."


