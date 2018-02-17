import os
import sys

print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

try:
    globalFolder = ""
    while(True):
        command = raw_input("enter a command \n")
        if ";" in command:
            command = command[:-2]
        print command
        if "--" in command:
            pass
        elif "CREATE DATABASE" in command:
            folder = command.split("CREATE DATABASE ")[1]
            if not os.path.exists(folder):
                os.makedirs(folder)
                print "Database " + folder + " created."
            else:
                print "!Failed to create database " + folder + " because it already exists."
        elif "DROP DATABASE" in command:
            folder = command.split("DROP DATABASE ")[1]
            if os.path.exists(folder):
                os.removedirs(folder)
                print "Database " + folder + " deleted."
            else:
                print "!Failed to delete database " + folder + " because it does not exist."
        elif "USE" in command:
            globalFolder = command.split("USE ")[1]
            print "using database" + globalFolder + "."
        elif "CREATE TABLE" in command:
            subFolder = command.split("CREATE TABLE ")[1]
            subFolder = subFolder.split(" (")[0]
            workFolder = os.path.join(os.getcwd(),globalFolder)
            fileName = os.path.join(workFolder,subFolder)
            if not os.path.isfile(fileName):
                with open(fileName,"w") as table:
                    print "Table " + subFolder + " Created"
                    if "(" in command:
                        data = command.split("(")[1]
                        loopCount = data.count(",")
                        for x in range(0,loopCount-1):
                            data[x] = command.split(",")[x]
                        table.write(data)

            else:
                print "!Failed to create table " + subFolder + " because it already exists"
        elif "DROP TABLE" in command:
            subFolder = command.split("DROP TABLE ")[1]
            workFolder = os.path.join(os.getcwd(),globalFolder)
            filePath = os.path.join(workFolder,subFolder)
            if os.path.isfile(filePath):
                os.remove(filePath)
                print "Table " + subFolder + " deleted."
            else:
                print "!Failed to delete Table " + subFolder + " because it does not exist."

        elif "SELECT *" in command:
            tableName = command.split("FROM ")[1]
            workFolder =  os.path.join(os.getcwd(),globalFolder)
            fileName = os.path.join(workFolder,tableName)
            if os.path.isfile(fileName):
                with open(fileName,"r+") as table:
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
                if "ADD" in command:
                    with open(fileName,"a") as table:
                        additonString = command.split("ADD ")[1]
                        table.write(", " + additonString)
                        print "Table " + tableName + " modified."
            else:
                 print "!Failed to atler table " + tableName + " because it does not exist."
        elif ".EXIT" in command:
            exit()
                    


except EOFError:
    print "exiting gracefully"
