import re
#summary - removes data from specified point to the next instance of the specified character
#parameters - (string before the data being trimmed, line you are removing from, specified character where the removal should stop)
#return - line with desired bit removed (if it was present)


def sanitiseToChar(string, line,char):
    length = len(string)
    stringExt = string + char
    if line.find(string) > 0:
            while line.find(stringExt) <0:
                line = line[0:line.find(string)+length:] + line[line.find(string)+length+1::]
    return(line)

#summary - removes all data from specified point to the end of the line
#parameters - (string before the data being trimmed, line you are removing from)
#return - line with the all characters from the end of the specified point removed (if the specified point was present)
def sanitiseToEnd(string, line):
    length = len(string)
    if line.find(string) > 0:
            line = line[0:line.find(string) + length]
    return (line)
        

#summary - sanitises all lines in the file and adds it to a dictionary
#parameters - (text file, dictionary with key: log message and value: quantity of said log message)
#return - dictionary, now full
def sanitiseAndFindErrorType(file,errorDict):

    for l in file:
        line = file.readline()

    #sanitise
        #assuming first 33 characters are all not needed
        line = line[33:]
        if line.find("error") > 0:
        
            line = sanitiseToChar("idcred(",line,')')
            line = sanitiseToChar("apic-gw-service(",line,')')
            line = sanitiseToChar("action(",line,')')
            line = sanitiseToChar("tid(",line,')')
            line = sanitiseToChar("apigw(",line,')')
            line = sanitiseToChar("gtid(",line,')')
            line = sanitiseToChar("password-alias(",line,')')
            line = sanitiseToChar("assembly-invoke(",line,')')
            line = sanitiseToChar("api-ldap-reg(",line,')')

            line = sanitiseToEnd("tid()[error][172.18.0.1] gtid():",line)
            line = sanitiseToEnd("is interrupted:",line)
            line = sanitiseToEnd("gtid(): Assembly rule ",line)
            line = sanitiseToEnd("Error code",line)
            line = sanitiseToEnd("Configuration status: Failures",line)

            
            #removes ip addresses (assuming there is no other instances of 4 sets of numbers seperated by a '.')
            #is also not specific to max 3 numbers in each set meaning eg 12345.1.1.1 would also be removed
            ipString = "[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+"
            line = re.sub(ipString,'[]',line)
    
     #append to the log message to dictionary and iterate the value accordingly   

            if line not in errorDict:
                errorDict[line] = 1
            else:
                errorDict[line] += 1
        
    return errorDict


#summary - sorts the dictionary of errors to be either ascending or descending depending on user input
#parameters - (the dictionary of errors to be sorted)
#return - the now ordered dictionary of errors

def sorting(errorDict, sort):
    #sorting
    errorDict_Ordered = {}
    
    if sort == "A":
        errorKeys_Ordered = sorted(errorDict, key = errorDict.get)
    elif sort == "D":
        errorKeys_Ordered = sorted(errorDict,key=errorDict.get, reverse = True)
    else:
        print("invalid input")    

    for i in errorKeys_Ordered:
            errorDict_Ordered[i] = errorDict[i]

    return errorDict_Ordered


##expects input to follow the printed format 'a' or 'd' follwed by the filenames
###expects filenames to contain no spaces.###

print("(A_or_D(ascending or descending) filename1 filename2 filename3 ...)")
userInput = input().split(' ')
sort = userInput[0].upper()
numOfFiles = len(userInput)-1

#a list of dictionaries, one for each file
errorListOfDict = []

#a list of file names, one for each file 
textFile = []

#adds an empty dictionary to the list for every file
for i in range (numOfFiles):
    errorListOfDict.append({})


#for every file, opens the file, sanitises it, stores it, and sorts it
for i in range(numOfFiles):
    textFile.append(userInput[i+1])
    file = open(textFile[i])
    errorListOfDict[i] = sanitiseAndFindErrorType(file,errorListOfDict[i])
    errorListOfDict[i] = sorting(errorListOfDict[i],sort)
    file.close()


#prints every error type and its quantity for every file    
for item in range (len(errorListOfDict)):
    print("\033[1;32m FILE: ",textFile[item],"\033[00m" )    #prints in bright green
    for k,v in errorListOfDict[item].items():
        k = k.strip()       #removing \n 
        print(v , "  ", k)
