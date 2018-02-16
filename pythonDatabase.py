import os
import sys

print "This is the name of the script: ", sys.argv[0]
print "Number of arguments: ", len(sys.argv)
print "The arguments are: " , str(sys.argv)

try:
    while(True):
        globalFolder = ""
        command = raw_input("enter a command \n")
        if "CREATE DATABASE" in command:
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
            subFolder = command.split(" (")[0]
            if not os.path.exists(globalFolder + "/" + subFolder):
                os.makedirs(globalFolder+"/"+subFolder)
                print "Table " + subFolder + " Created"
            else:
                print "Table " + subFolder + " already exists"
            if "(" in command:
                data = command.split("(")[1]
                loopCount = data.count(",")
                for x in range(0,loopCount-1):
                    data = command.split(",")[x]

                    
except EOFError:
    print "exiting gracefully"
