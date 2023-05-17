import subprocess
import os

class checkError:
    def check_java_syntax(self,java_code):
        try:
            # Create a temporary Java file
            with open("temp.java", 'w') as file:
                file.write(java_code)
                #file.read('temp.java')
            # Compile the Java file using javac
            compile_process = subprocess.Popen(["javac","temp.java"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            compile_output, compile_errors = compile_process.communicate()
            if compile_process.returncode == 0:
                # Compilation successful, syntax is correct
                return("Clear")
            else:
                return(compile_errors.decode())
        except Exception as e:
             return(str(e))
    def runChecker(self,code):
        startcode = '''class Test {public static void main(String[] args) { '''
        return self.check_java_syntax(startcode+code+'}'+'}')
    def runCheckerOnFile(self,filepath):
        with open(filepath, encoding='UTF8') as f:
            contents = f.read()
        return self.runChecker(code=contents)


