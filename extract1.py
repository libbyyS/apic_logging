



#removes data from specified point to a closed bracket
def sanitiseBracket(string, line):
    length = len(string)
    stringExt = string + ')'
    if line.find(string) > 0:
            while line.find(stringExt) <0:
                line = line[0:line.find(string)+length:] + line[line.find(string)+length+1::]
    return(line)

#removes all data from specified point to the end of the line
def sanitiseToEnd(string, line):
    length = len(string)
    if line.find(string) > 0:
            line = line[0:line.find(string) + length]
    return (line)
        

def sanitiseAndFindErrorType(file,index,errorDict):

    for l in file:
        line = file.readline()

    #sanitise
    #assuming first 33 characters are all not needed

        line = line[33:]
        if line.find("error") > 0:
        
            line = sanitiseBracket("idcred(",line)
            line = sanitiseBracket("apic-gw-service(",line)
            line = sanitiseBracket("action(",line)
            line = sanitiseBracket("tid(",line)
            line = sanitiseBracket("apigw(",line)
            line = sanitiseBracket("gtid(",line)
            line = sanitiseBracket("password-alias(",line)
            line = sanitiseBracket("assembly-invoke(",line)
            line = sanitiseBracket("api-ldap-reg(",line)

            line = sanitiseToEnd("tid()[error][172.18.0.1] gtid():",line)
            line = sanitiseToEnd("is interrupted:",line)
            line = sanitiseToEnd("gtid(): Assembly rule ",line)
            line = sanitiseToEnd("Error code",line)
            line = sanitiseToEnd("Configuration status: Failures",line)

     #append to list & count   
            if line not in errorDict:
                errorDict[line] = 1
            else:
                errorDict[line] += 1

    return errorDict

def sorting(errorDict):
    #sorting
    errorDict_Ordered = {}
    errorKeys_Ordered = sorted(errorDict, key = errorDict.get)
    print("Ascending or Descending? (A or D)")
    sort = str(input()).upper()

    while sort != "A" and sort != "D":
        print("Ascending or Descending? (A or D)")
        sort = str(input()).upper()
    if sort == "A":
        errorKeys_Ordered = sorted(errorDict, key = errorDict.get)
        

    elif sort == "D":
        errorKeys_Ordered = sorted(errorDict,key=errorDict.get, reverse = True)
        

    for i in errorKeys_Ordered:
            errorDict_Ordered[i] = errorDict[i]

    return errorDict_Ordered



print("How many files?")
numOfFiles = int(input())
errorListOfDict = []



for i in range (numOfFiles):
    errorListOfDict.append({})

textFile = []

for i in range(numOfFiles):
    print("Enter text file identifier")
    textFile.append(input() +".txt")
    file = open(textFile[i])
    errorListOfDict[i] = sanitiseAndFindErrorType(file,str(i),errorListOfDict[i])
    errorListOfDict[i] = sorting(errorListOfDict[i])
    file.close()

#print            
for item in range (len(errorListOfDict)):
    print("\033[1;32m FILE: ",textFile[item],"\033[00m" )
    print()
    for k,v in errorListOfDict[item].items():
        print(v , "  ", k)