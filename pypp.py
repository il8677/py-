variableTypes = ["int","string","char","double", "void"]
keywords = ["class","print","if","else","elif","return"]
reserved = variableTypes + keywords
operators = ["=","-","+","/","*"]
symbols = ["(",")","{","}",","]

variableNames = []

class variable:
    def __init__(self, type, value):
        self.type = type
        self.value = value

def scan(line):
    i = 0
    n=0
    chars = []

    splits="(){}"

    doReplaceSpace = True

    for char in line:
        chars.append(char)

    for char in line:
        if char in splits:
            chars.insert(i,";")
            chars.insert(i+2,";")
            i+=2
        elif char == " " and doReplaceSpace:
            chars[i] = ";"
        elif char == "\"" and doReplaceSpace:
            doReplaceSpace = False
        elif char == "\"" and not doReplaceSpace:
            doReplaceSpace = True

        i += 1
        n+=1

    final = ""

    for char in chars:
        final += char
    #final += "\n"
    return final

def parse(set):

    tokens = set.split(";")
    values="0 1 2 3 4 5 6 7 8 9".split(" ")
    values += ["true","false"]
    lexicon = []

    for token in tokens:
        if (token == ""):
            continue
        if token in variableTypes:
            lexicon.append(["type",token])
        elif token in keywords:
            lexicon.append(["keyword",token])
        elif token in operators:
            lexicon.append(["operator",token])
        elif token in symbols:
            lexicon.append(["symbol",token])
        elif token[0] == "\"" or token[0] in values:
            lexicon.append(["value", token])
        elif token != " " and token != "  " and token !="" and token !="\n":
            lexicon.append(["name",token])

    return lexicon

def compile(line):
    tokenType = 0
    tokenValue = 1
    cppLine=""

    isFirst = True
    doAddSemicolon=True
    isPrintLine = False
    isClass = False

    for t in line:
        if t[tokenType] == "type":
            cppLine+=t[tokenValue]

        elif t[tokenType] == "name":
            if(isFirst):

                i=0
                found = False

                for tt in line:
                    if tt[tokenType] == "value":
                        found = True
                        break

                    i+=1
                if found:
                    if line[i][tokenValue] in "0123456789":
                        cppLine+="int " + t[tokenValue]
                    elif line[i][tokenValue] in ["true","false"]:
                        cppLine+="bool " + t[tokenValue]
                    elif line[i][tokenValue][0] == "\"":
                        cppLine += "std::string " + t[tokenValue];
                    else:
                        cppLine+=t[tokenValue]
            else:
                variableNames.append(tokenValue)
                cppLine+=t[tokenValue]

        elif t[tokenType] == "symbol":
            cppLine+=t[tokenValue]
            doAddSemicolon = False

        elif t[tokenType] == "keyword":
            if(t[tokenValue] == "print"):
                cppLine+="std::cout<<"
                isPrintLine = True
            if(t[tokenValue] == "class"):
                cppLine += "class"
                isClass = True
            else:
                cppLine += t[tokenValue]

        elif t[tokenType] == "value":
            cppLine += t[tokenValue]
        elif t[tokenType] == "operator":
            cppLine += t[tokenValue]
        isFirst = False
        cppLine += " "

    if isPrintLine:
        cppLine += "<<std::endl"
    elif(isClass):
        cppLine+="public:"
    if doAddSemicolon:
        cppLine+=";"


    cppLine+="\n"
    return cppLine

code = open("main.pypp")

lex = []

for line in code.read().split("\n"):
    print(scan(line))
    lex.append(parse(scan(line)))

code.close()
draftCpp="#include<iostream>\n";
for l in lex:
    print(l)
    draftCpp+=compile(l)

finalCpp=""

print("\n\n\n\n")
i=0
for c in draftCpp.split("\n"):
    if not(c.__len__() == 1):
        finalCpp+=c+"\n"


print (finalCpp)

outputFile = open("output.cpp", "w")
outputFile.write(finalCpp)
outputFile.close()