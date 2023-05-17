import re
from nltk.tokenize import word_tokenize

class JavaCodeTokenizer:
    def __init__(self):
        self.operators = ['+', '-', '*', '/', '%', '++', '--', '==', '!=', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '+=', '-=', '*=', '/=', '%=', '&=', '^=', '|=', '<<=', '>>=', '->', '::', '?', ':', '(', ')', '[', ']', '{', '}', ';', ':', ',', '=', '++']
        self.keywords = ['break', 'byte', 'case', 'catch', 'char', 'class', 'const', 'default', 'do', 'else', 'enum', 'extends', 'final', 'finally', 'for', 'if', 'implements', 'import', 'interface', 'native', 'new', 'package', 'private', 'protected', 'public', 'return', 'static', 'this', 'throw'
                         , 'throws', 'try', 'void', 'volatile', 'while','System.out.print','System.out.println,"else if']
        self.types = ['boolean', 'byte', 'char', 'double', 'float', 'short', 'long', 'int']

    def tokenize(self, code):
        tokens = self._split_tokens(word_tokenize(code))
        if "true" in tokens:
            tokens[tokens.index("true")]="True"
        if "false" in tokens:
            tokens[tokens.index("false")]="False"
        token_types = self._get_token_types(tokens)
        token_list = list(zip(tokens, token_types))
        return token_list

    def _split_tokens(self, tokens):
        split_tokens = []
        for token in tokens:
            if token.endswith('++') or token.endswith('--'):
                split_tokens.append(token[:-2])
                split_tokens.append(token[-2:])
            elif token=='&':
                if  split_tokens[-1]=='&':
                    split_tokens[-1]='&&'
                else:
                    split_tokens.append('&')
            elif token=='|':
                if  split_tokens[-1]=='|':
                    split_tokens[-1]='||'
                else:
                    split_tokens.append('||')
            elif '==' in token :
                parts = token.split('==')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('==')
            elif '=' in token :
                parts = token.split('=')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('=')
            elif '+=' in token :
                parts = token.split('+=')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('+=')
            elif '-=' in token :
                parts = token.split('-=')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('-=')
            elif '*=' in token :
                parts = token.split('*=')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('*=')
            elif '/=' in token :
                parts = token.split('/=')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('/=')
            elif '+' in token :
                parts = token.split('+')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('+')
            elif '-' in token :
                parts = token.split('-')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('-')
            elif '*' in token :
                parts = token.split('*')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('*')
            elif '/' in token :
                parts = token.split('/')
                for i, part in enumerate(parts):
                    split_tokens.append(part)
                    if i != len(parts) - 1:
                        split_tokens.append('/')
            else:
                split_tokens.append(token)
        return split_tokens
    def _get_token_types(self, tokens):
        token_types = []
        for token in tokens:
            token_type = self._classify_token(token)
            token_types.append(token_type)
        return token_types

    def _get_token_types(self, tokens):
        token_types = []
        for token in tokens:
            token_type = self._classify_token(token)
            token_types.append(token_type)
        return token_types
    def _classify_token(self, token):
        if token in self.operators:
            return 'OPERATOR'
        elif token in self.keywords:
            return 'KEYWORD'
        elif token in self.types:
            return 'TYPE'
        elif re.match(r'[A-Za-z]+\d*', token):
            return 'IDENTIFIER'
        elif re.match(r'\d+\.\d+|\d+',token):
            return 'DIGIT'
        else:
            return 'OTHER'
    def RunTokenizer(self,code=None,filepath=None,use_Txt=False):
        if use_Txt:
            assert filepath!=None
            with open(filepath, encoding='UTF8') as f:
                java_code = f.read()
        else:
            java_code=code
        token_list = self.tokenize(java_code)
       
        tokenized_list = []
        for token in token_list:
            if token[0] in self.keywords:
                tokenized_list.append((token[0], "keyWord"))
            elif token[0] in self.types:
                tokenized_list.append((token[0], "type"))
            elif re.match(r'\w+\+\w+', token[0]):  
                tokenized_list.append((token[0][0], "identifer"))
                tokenized_list.append(('+', "operator"))
                if re.match(r'\d+\.\d+|\d+',token[0][2]):
                    tokenized_list.append((token[0][2], "digit"))
                else:
                    tokenized_list.append((token[0][2], "identifer"))
            elif re.match(r'\w+\-\w+', token[0]):  
                tokenized_list.append((token[0][0], "identifer"))
                tokenized_list.append(('-', "operator"))
                if re.match(r'\d+\.\d+|\d+',token[0][2]):
                    tokenized_list.append((token[0][2], "digit"))
                else:
                    tokenized_list.append((token[0][2], "identifer"))
            elif re.match(r'\w+\*\w+', token[0]):  
                tokenized_list.append((token[0][0], "identifer"))
                tokenized_list.append(('*', "operator"))
                if re.match(r'\d+\.\d+|\d+',token[0][2]):
                    tokenized_list.append((token[0][2], "digit"))
                else:
                    tokenized_list.append((token[0][2], "identifer"))
            elif re.match(r'\w+\/\w+', token[0]):  
                tokenized_list.append((token[0][0], "identifer"))
                tokenized_list.append(('/', "operator"))
                if re.match(r'\d+\.\d+|\d+',token[0][2]):
                    tokenized_list.append((token[0][2], "digit"))
                else:
                    tokenized_list.append((token[0][2], "identifer"))
            elif re.match(r'[A-Za-z]+\d*', token[0]):
                tokenized_list.append((token[0], "identifier"))
            elif re.match(r'\d+\.?\d*', token[0]):
                tokenized_list.append((token[0], "digit"))
            elif token[0] in self.operators:
                tokenized_list.append((token[0], "operator"))
            else:
                tokenized_list.append((token, 'other'))
        return tokenized_list



    

