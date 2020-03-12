import os
import sys
import JackTokenizer
import CompilationEngine

class JackAnalyzer:

    def main(self):
        input_file = sys.argv[1]
        if os.path.isfile(input_file):
            token_obj = JackTokenizer.JackTokenizer(input_file)
            output_file = input_file.split(".")[0] + ".xml"
            compilation_engine = CompilationEngine.CompilationEngine(token_obj, output_file)
            compilation_engine.compileClass()



        elif os.path.isdir(input_file):
            for file in os.listdir(input_file):
                if file.split(".")[1] == "jack":
                    token_obj = JackTokenizer.JackTokenizer(os.path.join(input_file, file))
                    output_file = os.path.join(input_file, file.split(".")[0]) + ".xml"
                    compilation_engine = CompilationEngine.CompilationEngine(token_obj, output_file)
                    compilation_engine.compileClass()


if __name__ == "__main__":
    analyzer =JackAnalyzer()
    analyzer.main()

