'''
Created by Alex Crupi and Chase Hammons, 3/8/18, version 2
'''
import os

def useEnabled(): #Catch when a database isn't enabled
    if globalScopeDirectory is "":
        raise ValueError("!Failed to use table because no database is selected")

try: #This will check the CTRL D command, and the EOF
    
    globalScopeDirectory = "" #Create here for increased scope

    while(True): #exit loop at EOF or .EXIT

        command = ""
        while not ";" in command and not "--" in command:
            command += raw_input("\n enter a command \n") #Read input from terminal

        if "--" in command: #Pass comments
            pass
        command = command[:-1] #Remove ; from command
        commandUp = str(command) #Normalize input
        commandUp = commandUp.upper()
        #print "c: ", command, "\n cU: ", commandUp
        if "CREATE DATABASE" in commandUp:
            try:
                directory = command.split("CREATE DATABASE ")[1] #Store the string after CREATE DATABASE
                if not os.path.exists(directory): #Only create if it doesn't exist
                    os.makedirs(directory)
                    print "Database " + directory + " created."
                else:
                    print "!Failed to create database " + directory + " because it already exists"
            except IndexError:
                print "!No database name specified"


        elif "DROP DATABASE" in commandUp:
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

        elif "CREATE TABLE" in commandUp:
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
                                out.append(data.split(", ")[x]) #Import all arguments into list for printing and sorting later
                            table.write( " | ".join(out) ) #Output the array to a file

                else:
                    print "!Failed to create table " + subDirectory + " because it already exists"
            except IndexError:
                print "!Failed to remove Table because no table name is specified"
            except ValueError as err:
                print err.args[0]

        elif "DROP TABLE" in commandUp:
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

        elif "SELECT *" in commandUp:
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

        elif "ALTER TABLE" in commandUp:
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
                            table.write(" | " + additionalString)
                            print "Table " + tableName + " modified."
                else:
                     print "!Failed to alter table " + tableName + " because it does not exist"
            except IndexError:
                print "!Failed to remove Table because no table name is specified"
            except ValueError as err:
                print err.args[0]

        elif "INSERT INTO" in commandUp:
            try:
                useEnabled() #Ensure database is selected
                tableName = command.split(" ")[2] #Get string to use for table name
                workingDirectory = os.path.join(os.getcwd(),globalScopeDirectory)
                fileName = os.path.join(workingDirectory,tableName)
                if os.path.isfile(fileName):
                    if "values" in command: #Check for start of argument section
                        with open(fileName,"a") as table: #OPen file to insert into
                            out = [] #Create list for output to file
                            data = command.split("(",1)[1] #Remove (
                            data = data[:-1] #Remove )
                            loopCount = data.count(",") #Count the number of arguments
                            for x in range(loopCount+1):
                                out.append(data.split(", ")[x]) #Import all arguments into list for printing and sorting later
                                if "\"" == out[x][0] or "\'" == out[x][0]:
                                    out[x] = out[x][1:-1]
                            table.write("\n")
                            table.write( " | ".join(out) ) #Output the array to a file
                            print "1 new record created."
                    else:
                        print "!Failed to insert into " + tableName + " beacause no arguments were given"
                else:
                     print "!Failed to alter table " + tableName + " because it does not exist"
            except IndexError:
                print "!Failed to insert into Table because no table name is specified"
            except ValueError as err:
                print err.args[0]

        elif "DELETE FROM" in commandUp:
            try:
                useEnabled() #Ensure database is selected
                mainCount = 0
                tableName = command.split("DELETE FROM ")[1] #Get string to use for table name
                tableName = tableName.split(" ")[0]
                workingDirectory = os.path.join(os.getcwd(),globalScopeDirectory)
                fileName = os.path.join(workingDirectory,tableName)
                if os.path.isfile(fileName):
                    with open(fileName,"r+") as table:
                        data = table.readlines()
                        out = list(data) #Can't modify data of for loop below
                        colIndex = data[0].split(" | ")
                        for x in range( len(colIndex) ):
                            colIndex[x] = colIndex[x].split(" ")[0]
                        itemToDelete = command.split("WHERE ")[1]
                        if "=" in itemToDelete: #Figure out the operator for splitting command
                            relColumn = itemToDelete.split(" =")[0]
                            itemToDelete = itemToDelete.split("= ")[1]
                            if "\"" in itemToDelete or "\'" in itemToDelete: #Cleanup var
                                itemToDelete = itemToDelete[1:-1]
                            for line in data: #Check each row
                                lineCheck = line.split(" | ")
                                for x in range( len(lineCheck) ): #Check each column item
                                    lineCheck[x] = lineCheck[x].split(" ")[0]
                                if itemToDelete in lineCheck:
                                    colIndex = colIndex.index(relColumn)
                                    lineCheck = lineCheck.index(itemToDelete)
                                    if lineCheck == colIndex: #Check for proper column
                                        del out[out.index(line)] #Remove matched field
                                        mainCount += 1
                                        #print "DEBUG out: ", out
                        elif ">" in itemToDelete: #Figure out the operator for splitting command
                            relColumn = itemToDelete.split(" >")[0]
                            itemToDelete = itemToDelete.split("> ")[1]
                            for line in data: #Check each row
                                lineCheck = line.split(" | ")
                                for x in range( len(lineCheck) ): #Check each column item
                                    lineCheck[x] = lineCheck[x].split(" ")[0]
                                    try:
                                        lineCheck[x] = float(lineCheck[x]) #Only check numeric fields
                                        #lineCheck[x] = int(lineCheck[x])
                                        if lineCheck[x] > float(itemToDelete): #Match query
                                            tempColIndex = colIndex.index(relColumn)
                                            #print "x: ", x, " colIndex: ", colIndex, " mainIndex: ", data.index(line)
                                            if x == tempColIndex: #Check for proper column
                                                del out[out.index(line)] #Remove matched field
                                                mainCount += 1
                                    except ValueError:
                                        continue

                        #elif "<" in itemToDelete: # Future implementation #
                            #relColumn = itemToDelete.split("<")[0]
                            #itemToDelete = itemToDelete.split("< ")[1]
                        table.seek(0)
                        table.truncate()
                        for line in out:
                            table.write(line)
                        if mainCount == 1:
                            print "1 record deleted."
                        elif mainCount > 1:
                            print mainCount, " records deleted."
                        else:
                            print "No records deleted."
                else:
                     print "!Failed to alter table " + tableName + " because it does not exist"

            except IndexError:
                print "!Failed to alter Table because no table name is specified"
            except ValueError as err:
                print err.args[0]

        elif ".EXIT" in command: #Exit if specified before EOF
            print "All done"
            exit()

except (EOFError, KeyboardInterrupt) as e: #Exit elegantly
    print "\nConnection to database terminated."


