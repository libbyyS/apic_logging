
import re


#summary - removes all characters between the end of a string until the first instance of the specified character from a line
#parameters - (string where the removal will begin, line containing the string and series of characters to be removed, character where the removal should stop
#return - line with all relevant characters removed
def sanitiseUntilSpecified(string, line, char):
    length = len(string)
    previousLine = ""
    stringExt = string + char
    if line.find(string) > 0:
            while line.find(stringExt) <0:
                line = line[0:line.find(string)+length:] + line[line.find(string)+length+1::]
                if(previousLine == line): #ensures that if the specified character is not present in the string, the loop still breaks
                    stringExt = string
                previousLine = line
    return(line)


#summary - removes all data from specified point to the end of the line
#parameters - (string where the removal of characters will begin, line containing string that characters will be removed from)
#return - (the line with the relevant characters removed)
def sanitiseToEnd(string, line):
    length = len(string)
    if line.find(string) > 0:
            line = line[0:line.find(string) + length]
    return (line)


#summary - sorts a dictionary by either ascending or descending relative to the quantity of each error type
#parameters - (dictionary to be sorted)
#returns - the dictionary that is now ordered
def sorting(errorDict,sort):
    #sorting
    errorDict_Ordered = {}
    errorKeys_Ordered = sorted(errorDict, key = errorDict.get)
    
    if sort == "A":
        errorKeys_Ordered = sorted(errorDict, key = errorDict.get)
        
    elif sort == "D":
        errorKeys_Ordered = sorted(errorDict,key=errorDict.get, reverse = True)
        
    for i in errorKeys_Ordered:
            errorDict_Ordered[i] = errorDict[i]

    return errorDict_Ordered


#summary - removes data from the line given using the sanitise subroutines and regex
#parameters -(line to be sanatised)
#returns - the sanitised line
def sanitiseForAllLines (line):
    line = sanitiseUntilSpecified("audit [",line,']')
    line = sanitiseUntilSpecified("error [",line,']')
    line = sanitiseUntilSpecified("url=",line,')')
    line = sanitiseUntilSpecified("url\":",line,'}')

    line = sanitiseUntilSpecified("(id=",line,')')
    line = sanitiseUntilSpecified("POST ",line,')')
    line = sanitiseUntilSpecified("PATCH ",line,')')
    line = sanitiseUntilSpecified("GET ",line,')')
    line = sanitiseUntilSpecified("(key:",line,')')
    line = sanitiseUntilSpecified("(value:",line,')')
    line = sanitiseUntilSpecified(": {\"realm\":",line,'}')
    line = sanitiseUntilSpecified("certificate\\",line, "PEM")
    line = sanitiseUntilSpecified("/tmp",line," -text")
    line = sanitiseUntilSpecified("\"message\":[\"",line,']') 
    line = sanitiseUntilSpecified("The email value",line," is")   
    line = sanitiseUntilSpecified("post /",line,')')
    line = sanitiseUntilSpecified("patch /",line,')')
    line = sanitiseUntilSpecified("climbon:", line," ")
    line = sanitiseUntilSpecified("client_id\"",line,",")
    line = sanitiseUntilSpecified("first_name\"",line,",")
    line = sanitiseUntilSpecified("last_name\"",line,",")
    line = sanitiseUntilSpecified("\"name\"",line,",")
    line = sanitiseUntilSpecified("title\"",line,"}")
    line = sanitiseUntilSpecified("username\"",line,",")
    line = sanitiseUntilSpecified("\"password\":\"********\"}",line,":")
    line = sanitiseUntilSpecified(",\"email\":",line,",")
    line = sanitiseUntilSpecified("delete:/",line, ')')
    line = sanitiseUntilSpecified(" Event\"",line, "(U")
    line = sanitiseUntilSpecified("id:",line,')')

    line = sanitiseToEnd("put:/api",line)
    line = sanitiseToEnd("subscription with name=", line)
    line = sanitiseToEnd("Invitation]:",line)
    line = sanitiseToEnd("global-policy-error",line)
    line = sanitiseToEnd("global-policies",line)

    line = re.sub("\[.{32}\]","[]",line)
    line = re.sub("/user/","/",line)
    line = re.sub("[0-9]{15}"," num ",line)
    line = re.sub("components/schemas/Member","components/schemas/",line)
    line = re.sub("Invitation acceptance email '.+' does not match the email '.+' when","Invitation acceptance email [b] does not match the email [a] when",line)


    return line


##expects input to follow the printed format 'a' or 'd' follwed by the filenames
print("(A_or_D(ascending or descending) filename1 filename2 filename3 ...)")
userInput = input().split(' ')   ###expects filenames to contain no spaces.###
while(len(userInput[0]) != 1 or len(userInput) < 2):   #validation
    print("invalid syntax")
    print("(A_or_D(ascending or descending) filename1 filename2 filename3 ...)")
    userInput = input().split(' ')

sort = userInput[0].upper()
numOfFiles = len(userInput)-1
for i in range (numOfFiles):
    errorList=[]  
    errorDict= {}

    #iterates through every line
    file = open(userInput[1+i])
    for line in file:
        #filters out any line that does not contain "error"
        if(line.find("error") > 0):
            if(line.find("20") == 0):               ###ASSUMING ALL LOGS START WITH '20'
                line = line[24:]                    ###ASSUMING first 24 characters are not relevant
                line = sanitiseForAllLines(line)
                errorList.append(line)
            
            else:
                line = sanitiseForAllLines(line)
                a = re.search(r"\A    at ",line)   #checks to see if the line begins with '    at'. All these lines are part of the stack:
                if not a:
                    errorList[-1] += line
   

    for e in errorList:
        #filters out any line that does not contain "error"
        if(e.find("error")< 0):
            errorList.remove(e)
        else:
            #append to dictionary & count   
            if e not in errorDict:
                errorDict[e] = 1
            else:
                errorDict[e] += 1

    #sorts dictionary
    errorDict = sorting(errorDict,sort.upper())
    print("\033[1;96m File: ", userInput[1+i],"\033[00m") #prints file name in light blue for visibility
    for k,v in errorDict.items():
        k=k.strip()     #removes \n 
        print("\033[1;32m ",v,"\033[00m  ", k) #prints the quantity in bright green and the error message in white for visibility
    print()
    print(len(errorDict))


