#Bruno de Castro Celestino  - 140576  
#Mauricio L. de Lorenzi  - 141269  


#     utilizado para consulta:  
#     http://pygments.org/docs/api/#module-pygments.lexer
#     http://pygments.org/docs/lexerdevelopment/
#     https://gist.github.com/eliben/5797351
#     http://jayconrod.com/posts/37/a-simple-interpreter-from-scratch-in-python-part-1


import re
import sys
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


class GUI:

    def browsefunc(self):
        filename = filedialog.askopenfilename()
        pathlabel.config(text=filename)

    def executelexer(self):
        f = open(pathlabel["text"], 'r')
        expreg = f.read().replace("\n", "").replace(" ", "")
        lx = Lexer(rules, skip_whitespace=True)
        lx.input(expreg)

        response = list()
        try:
            for tok in lx.tokens():
                response.append(tok.type)

        except LexerError as err:
            self.errormessage('Erro na posição: %s' % err.pos)

        if response.__len__() == 0:
            self.errormessage("Arquivo de codigo em branco!")
        else:
            self.successmessage(response)

    def errormessage(self, message):
        messagebox.showinfo("Erro", message)

    def successmessage(self, message):
        messagebox.showinfo("Sucesso", message)


class Token(object):

    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s' % self.type


class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    
    def __init__(self, rules, skip_whitespace=True):
        
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))
        self.skip_whitespace = skip_whitespace
        self.re_ws_skip = re.compile('\S')

    def input(self, buf):
        self.buf = buf
        self.pos = 0

    def token(self):
        
        if self.pos >= len(self.buf):
            return None
        else:
            if self.skip_whitespace:
                m = self.re_ws_skip.search(self.buf, self.pos)

                if m:
                    self.pos = m.start()
                else:
                    return None

            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = Token(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok
            raise LexerError(self.pos)

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None:
                break
            yield tok


if __name__ == '__main__':
    rules = [
        ('\d+',            'LITERAL'),
        ('and',            'AND'),
        ('or',             'OR'),
        ('\,',              'INICIO DE BLOCO'),
        ('\.',              'FIM DE BLOCO'),
        ('if',             'IF'),
        ('int',            'TIPO DE VARIÁVEL'),
        ('else',           'ELSE'),
        ('while',          'WHILE'),
        ('do',             'DO'),
        ('end',            'END'),
        ('[a-zA-Z_]*\w+',   'IDENTIFICADOR'),
        ('\+',             'OPERADOR DE ADIÇÃO'),
        ('\-',             'OPERADOR DE SUBTRAÇÃO'),
        ('\*',             'OPERADOR DE MULTIPLICAÇÃO'),
        ('\/',             'OPERADOR DE DIVISÃO'),
        ('\(',             'PARÊNTESES ESQUERDO'),
        ('\)',             'PARÊNTESES DIREITO'),
        ('\=',              'OPERADOR DE ATRIBUIÇÃO'),
        ('\==',             'OPERADOR DE EQUIVALÊNCIA'),
        ('\!=',             'OPERADOR DE DIFERENÇA'),
        ('\<=',             'OPERADOR MENOR IGUAL'),
        ('\>=',             'OPERADOR MAIOR IGUAL'),
        ('\>',              'OPERADOR MAIOR'),
        ('\<',              'OPERADOR MENOR'),
    ]

    interface = GUI()
    gui = tkinter.Tk()

    gui.title("Linguagens Formais e Automatos - Lexer ")
    gui.geometry("600x250")

    label_title = Label(gui, text="_______[LFA-6] - LEXER_______\nBruno de Castro Celestino - 140576\n"
                                  "Maurício L. de Lorenzi - 141269")
    label_title.pack()

    label = Label(gui, text="Escolha o arquivo de codigo que sera analisado")
    label.place(x=0, y=70)

    lbl_file_full_name = Label(gui, text="path: ")
    lbl_file_full_name.place(x=0, y=100)

    pathlabel = Label(gui)
    pathlabel.place(x=30, y=100)

    browsebutton = Button(gui, text="Browse", command=interface.browsefunc)
    browsebutton.place(x=520, y=100)

    okButton = Button(gui, text="OK", command=interface.executelexer, width="30")
    okButton.place(x=200, y=200)

    gui.mainloop()
