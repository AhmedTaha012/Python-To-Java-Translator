import nltk
import re
from checker import checkError
from tokenizer import JavaCodeTokenizer
class Translator:
    def __init__(self):
        self.listOfTokens=[] 
        self.pointer=0
        self.indentCounter=0
        self.indent='    '
        self.translatedText=[]
    def getTranslatedText(self):
        return "".join(self.translatedText)
    def getNextToken(self):
        self.pointer=self.pointer+1
        assert self.pointer<len(self.listOfTokens)
        return self.listOfTokens[self.pointer]
    def getToken(self):
        assert self.pointer>=0
        return self.listOfTokens[self.pointer]
    def prevToken(self):
        self.pointer=self.pointer-1
        assert self.pointer>0
        return self.listOfTokens[self.pointer]
    def setPointer(self, value):
        self.pointer=value
    def setListOfTokens(self,value):
        assert type(value)==list
        self.listOfTokens=value
    def checkLastToken(self):
        if self.pointer==len(self.listOfTokens)-1:
            return True
        else:
            return False   
    def getListOfTokens(self):
        return self.listOfTokens
    def runFor(self): 
        self.setPointer(self.pointer+1)
        if self.getToken()[0]=="(" :
            self.setPointer(self.pointer+1)
            if self.getToken()[1]=="identifier" or self.getToken()[1]=="type": # whether i=0 or int i=0
                if self.getToken()[1]=="type":
                    self.setPointer(self.pointer+1)
                id1=self.getToken()[0] 
                self.setPointer(self.pointer+1)
                if self.getToken()[0]=="=" :
                    self.setPointer(self.pointer+1)
                    if self.getToken()[1]=="digit":
                        id2=self.getToken()[0] 
                        self.setPointer(self.pointer+1)
                        if self.getToken()[0]==";":
                            self.setPointer(self.pointer+1)
                            if self.getToken()[1]=="identifier":
                                self.setPointer(self.pointer+1)
                                if self.getToken()[0]=="<" or self.getToken()[0]=='>':
                                    self.setPointer(self.pointer+1)
                                    if self.getToken()[1]=="digit" or self.getToken()[1]=="identifier":
                                        id3=self.getToken()[0] #for id1 in range(0,10
                                        self.setPointer(self.pointer+1)
                                        if self.getToken()[0]==";":
                                            self.setPointer(self.pointer+1)
                                            if self.getToken()[1]=="identifier":
                                                id4=1
                                                self.setPointer(self.pointer+1)
                                                if self.getToken()[0]=="++":  #if we get ++
                                                    id4=1  #for id1 in range(0,10,1)
                                                    self.getNextToken()
                                                elif self.getToken()[0]=="--": #if we get --
                                                    id4=-1 
                                                    self.getNextToken()
                                                elif self.getToken()[0]=="=": #if we get i=
                                                    self.setPointer(self.pointer+2)
                                                    #case =i+1
                                                    if self.getToken()[0]=='+':
                                                        self.setPointer(self.pointer+1)
                                                        id4=self.getToken()[0]
                                                    #case =i-1
                                                    elif self.getToken()[0]=='-':
                                                        self.setPointer(self.pointer+1)
                                                        id4='-'+self.getToken()[0]
                                                    self.getNextToken()
                                                if self.getToken()[0]==")":
                                                    self.translatedText.append(self.indent*self.indentCounter+"for "+id1+" in range("+str(id2)+","+str(id3)+","+str(id4)+"):\n")
                                                    self.getNextToken()
                                                    if self.getToken()[0]=="{":
                                                        self.indentCounter+=1
                                                        self.getNextToken()
                                            elif self.getToken()[0]==")":
                                                self.translatedText.append(self.indent*self.indentCounter+"for "+id1+" in range("+str(id2)+","+str(id3)+"):\n")
                                                self.getNextToken()
                                                if self.getToken()[0]=="{":
                                                    self.indentCounter+=1
                                                    self.getNextToken()
                                                
    def runIf(self):
        self.getNextToken() 
        bracketCounter=0
        outputString=''
        if self.getToken()[0]=="(" and self.getToken()[1]=="operator":
            outputString+=self.indent*self.indentCounter+'if '
            self.getNextToken()
            bracketCounter+=1
            while bracketCounter !=0:
                if self.getToken()[0]=='&&':
                    outputString+=' and '
                elif self.getToken()[0]=='||':
                    outputString+=' or '
                elif self.getToken()[1]=='operator' and self.getToken()[0]!='&&' and self.getToken()[0]!='||' and self.getToken()[0]!=')' and self.getToken()[0]!='(':
                    outputString+=self.getToken()[0]
                if self.getToken()[0]=='(':
                    bracketCounter+=1
                    if bracketCounter>1:
                        outputString+='('
                if self.getToken()[0]==')':
                    bracketCounter=bracketCounter-1
                    if bracketCounter!=0:
                        outputString+=') '
                if self.getToken()[1]=='identifier':
                    outputString+=self.getToken()[0]
                if self.getToken()[1]=='digit':
                    outputString+=self.getToken()[0]
                self.getNextToken()
            outputString+=':'
            if self.getToken()[0]=='{':
                self.indentCounter+=1
                outputString+='\n'
                self.getNextToken()
            self.translatedText.append(outputString)
    def runElseIf(self):
        self.getNextToken() 
        bracketCounter=0
        outputString=''
        if self.getToken()[0]=="(" and self.getToken()[1]=="operator":
            outputString+=self.indent*self.indentCounter+'elif '
            self.getNextToken()
            bracketCounter+=1
            while bracketCounter !=0:
                if self.getToken()[0]=='&&':
                    outputString+=' and '
                elif self.getToken()[0]=='||':
                    outputString+=' or '
                elif self.getToken()[1]=='operator' and self.getToken()[0]!='&&' and self.getToken()[0]!='||' and self.getToken()[0]!=')' and self.getToken()[0]!='(':
                    outputString+=self.getToken()[0]
                if self.getToken()[0]=='(':
                    bracketCounter+=1
                    if bracketCounter>1:
                        outputString+='('
                if self.getToken()[0]==')':
                    bracketCounter=bracketCounter-1
                    if bracketCounter!=0:
                        outputString+=') '
                if self.getToken()[1]=='identifier':
                    outputString+=self.getToken()[0]
                if self.getToken()[1]=='digit':
                    outputString+=self.getToken()[0]
                self.getNextToken()
            outputString+=':'
            if self.getToken()[0]=='{':
                self.indentCounter+=1
                outputString+='\n'
                self.getNextToken()
            self.translatedText.append(outputString)
    def runWhile(self):
        self.getNextToken()
        bracketCounter=0
        outputString=''
        if self.getToken()[0]=="(" and self.getToken()[1]=="operator":
            outputString+=self.indent*self.indentCounter+'while '
            self.getNextToken()
            bracketCounter+=1
            while bracketCounter !=0:
                if self.getToken()[0]=='&&':
                    outputString+=' and '
                elif self.getToken()[0]=='||':
                    outputString+=' or '
                elif self.getToken()[1]=='operator' and self.getToken()[0]!='&&' and self.getToken()[0]!='||' and self.getToken()[0]!=')' and self.getToken()[0]!='(':
                    outputString+=self.getToken()[0]
                if self.getToken()[0]=='(':
                    bracketCounter+=1
                    if bracketCounter>1:
                        outputString+='('
                if self.getToken()[0]==')':
                    bracketCounter=bracketCounter-1
                    if bracketCounter!=0:
                        outputString+=') '
                if self.getToken()[1]=='identifier':
                    outputString+=self.getToken()[0]
                if self.getToken()[1]=='digit':
                    outputString+=self.getToken()[0]
                self.getNextToken()
            outputString+=':'
            if self.getToken()[0]=='{':
                self.indentCounter+=1
                outputString+='\n'
                self.getNextToken()
            self.translatedText.append(outputString)
    def runElse(self):
        self.getNextToken()
        if self.getToken()[0]=="if":
            return self.runElseIf()
        outputString=''
        outputString+=self.indent*self.indentCounter+'else:'
        if self.getToken()[0]=='{':
            self.indentCounter+=1
            outputString+='\n'
            self.getNextToken()
        self.translatedText.append(outputString)
    def runAssignStmt(self):
            outputString=''                
            if self.getToken()[1]=="type":   
                savedType=self.getToken()[0]
                self.getNextToken()
            while True:
                if self.getToken()[0]!=";":
                    if self.getToken()[1]!="other":
                        outputString+=self.getToken()[0]
                    self.getNextToken()
                else:
                    break
            self.translatedText.append(self.indent*self.indentCounter+outputString+"\n")
            if self.checkLastToken()==False:
                self.getNextToken()
    def runCloseBraces(self):
        self.indentCounter-=1
        self.getNextToken()
    def runPrint(self):
        self.getNextToken()
        self.getNextToken()
        if self.getToken()[1]=="identifier":
            outputString=f"print({str(self.getToken()[0])})"
            self.getNextToken()
            self.getNextToken()
        else:
            self.getNextToken()
            outputString=f"print('{str(self.getToken()[0])}')"
            self.getNextToken()
            self.getNextToken()
            self.getNextToken()
        self.translatedText.append(self.indent*self.indentCounter+outputString+"\n")
        if self.checkLastToken()==False:
            self.getNextToken()
    def runTranslate(self):
        if self.getToken()[0]=="while" and self.getToken()[1]=="keyWord":
            self.runWhile()
            return self.run()
        elif self.getToken()[0]=="if"  and self.getToken()[1]=="keyWord":
            self.runIf()
            return self.run()
        elif self.getToken()[0]=="for"  and self.getToken()[1]=="keyWord":
            self.runFor()
            return self.run()
        elif self.getToken()[0]=="else" and self.getToken()[1]=="keyWord":
            self.runElse()
            return self.run()
        elif self.getToken()[0]=="System.out.println" or self.getToken()[0]=="System.out.print":
            self.runPrint()
            return self.run()
        elif self.getToken()[1]=="identifier" or self.getToken()[1]=="type":
            self.runAssignStmt()
            return self.run()
        elif self.getToken()[0]=="}" and self.getToken()[1]=="operator":
            self.runCloseBraces()
            return self.run()
        else:
            return
    def run(self):
        if self.checkLastToken()==True:
            return
        else:
            return self.runTranslate()
    def startTranslate(self,sentence=None,filepath=None,useTxt=False):
        tokenizer = JavaCodeTokenizer()
        if useTxt:
            tokinzedList=tokenizer.RunTokenizer(filepath=filepath,use_Txt=True)
        else:
            tokinzedList=tokenizer.RunTokenizer(code=sentence)
        self.setListOfTokens(tokinzedList)
        self.setPointer(0)
        self.run()
    def showTranslatedText(self):
        print(self.getTranslatedText())
    def saveFile(self,outputPath="output.txt"):
        with open(outputPath,'w') as f:
            f.write(self.getTranslatedText())




# if __name__ == "__main__":
#     t=Translator()
#     # tokens =["while","(","(","x","<","10",")","||","(","y","<","5",")",")","{",'if','(','(','f','<','80',")",')','{','var8','=','9',';',"}","i","=","10",";","var5","=","50",";","}",'while','(','gigi','>','18',')','{','int','f','=','18',';','}']
#     # tokens=["for","(","var1","=","50",';','i','<','200',';','i','=','i','+','2',')','{','while','(','False',')','{','int','c','=','c','+','1',';','}',"for","(","var6","=","50",';','i','<','200',';',')','{','j','=','100',';','}',"}"]
#     # sentence = """
#     #           while((var1&&var2)){                                            
#     #           for(int i=0;i<10;i++){                                                 
#     #             boolean state = True;
#     #             System.out.print("hello");
#     #           }
#     #           int x = 15;
#     # }"""  
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-f","--filepath", help="select txt file in folder",type=str)
#     args = parser.parse_args()
#     ce=checkError()
#     if ce.runCheckerOnFile(args.filepath)=="Clear":
#         print("Translated Succesfulyyy and saved in output.txt")
#         t.startTranslate(filepath=args.filepath,useTxt=True)
#         t.saveFile()
#     else:
#         print(ce.runCheckerOnFile(args.filepath))
#     # t.showTranslatedText()
    
    
    

    
    

    
