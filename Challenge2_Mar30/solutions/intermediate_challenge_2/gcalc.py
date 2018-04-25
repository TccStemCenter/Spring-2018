#!/usr/bin/env python3
# -*- coding: utf-8 -*-

r"""
                 _
  __ _  ___ __ _| | ___   _ __  _   _
 / _` |/ __/ _` | |/ __| | '_ \| | | |
| (_| | (_| (_| | | (__ _| |_) | |_| |
 \__, |\___\__,_|_|\___(_) .__/ \__, |
 |___/                   |_|    |___/

small graphing calculator in python using tkinter
"""

from enum import Enum
from math import e, pi
from math import log, sqrt, sin, cos, tan, asin, acos, atan
from random import random
from re import compile as recompile
from sys import stderr
import tkinter as tk


def main():
    c = Calc()
    c.get_rpn(input('y = '))
    c.eval_rpn()
    master = tk.Tk()
    c.graph(master)
    master.mainloop()


class Calc(tk.Frame):

    """
        Simple Graphing Calculator

            parses tokens and graphs
    """


    def __init__(self, **kwargs):
        """ initialize
                **kwargs:
                    width: width of graphing canvas (in pixels)
                    height: height of graphing canvas (in pixels)
                    xmin: minimum x-value for graph
                    xmax: maximum x-value for graph
                    ymin: minimum y-value for graph
                    ymax: maximum y-value for graph
                    master: tk.Tk() window (optional)
        """
        self.width  = kwargs.get('width', 800)
        self.height = kwargs.get('height', 800)
        self.xmin   = kwargs.get('xmin', -10)
        self.xmax   = kwargs.get('xmax', 10)
        self.ymin   = kwargs.get('ymin', -10)
        self.ymax   = kwargs.get('ymax', 10)
        self.master = kwargs.get('master', None)


    def graph(self, *args):
        """ graph the results stored into self.xpts and self.ypts
                *args:
                    0: tk.Tk() window for drawing graph
                        > THIS MUST BE PASSED IF NOT CREATED IN __init__()
        """

        if not self.master:
            if not args:
                print('No window for graphing. Please pass tk.Tk() to Calc.graph()')
                return
            self.master = args[0]

        self.master.geometry('{}x{}'.format(self.width, self.height))
        super().__init__(self.master)

        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height)
        self.canvas.configure(bg='white')
        self.canvas.pack()
        flag = True
        for x,y in zip(self.xpts, self.ypts):
            if flag:
                prevX = x
                prevY = y
                flag = False
                continue
            self.canvas.create_line(prevX, prevY, x, y)
            prevX = x
            prevY = y

        self.pack()


    def __parse_tokens__(self, s):
        tokens = []
        token = ""
        single_tokens = (
            '(', ')', '[', ']',
            '+', '-', '*', '/', '^',
        )
        for ch in s:
            if ch in single_tokens or ch == ' ':
                if token:
                    tokens.append(Token(token))
                if ch != ' ':
                    token = Token(ch)
                    if token.val in ('+', '-'):
                        if not tokens or tokens[-1].typ not in (TokenType.NUMBER, TokenType.X):
                            token.typ = TokenType.FUNCTION
                    tokens.append(token)
                token = ''
            else:
                if ch:
                    token += ch
        if token:
            token = Token(token)
            if token.val in ('+', '-'):
                if not tokens or tokens[-1].typ not in (TokenType.NUMBER, TokenType.X):
                    token.typ = TokenType.FUNCTION
            tokens.append(token)

        return tokens


    def get_rpn(self, s):
        opStack = []
        self.rpn = []

        for token in self.__parse_tokens__(s):
            if token.typ in (TokenType.NUMBER, TokenType.X):
                self.rpn.append(token)
            elif token.typ is TokenType.FUNCTION:
                opStack.append(token)
            elif token.typ is TokenType.OPERATOR:
                while opStack and\
                    (opStack[-1].typ is TokenType.FUNCTION or\
                    opStack[-1].precedence > token.precedence or\
                    (opStack[-1].precedence == token.precedence) and\
                    opStack[-1].typ is not TokenType.L_PAREN):
                    self.rpn.append(opStack.pop())
                opStack.append(token)
            elif token.typ is TokenType.L_PAREN:
                opStack.append(token)
            elif token.typ is TokenType.R_PAREN:
                while opStack and opStack[-1].typ is not TokenType.L_PAREN:
                    self.rpn.append(opStack.pop())
                if not opStack:
                    raise RuntimeError('Mismatched parentheses')
                opStack.pop()

        while opStack:
            if opStack[-1].typ is TokenType.L_PAREN or\
                opStack[-1].typ is TokenType.R_PAREN:
                raise RuntimeError('Mismatched parentheses')
            self.rpn.append(opStack.pop())

    def eval_rpn(self):
        self.xpts = []
        self.ypts = []
        dx = self.width / (self.xmax - self.xmin)
        dx = (self.xmax - self.xmin) / self.width
        for i in range(self.width):
            x = self.xmin + i * (self.xmax - self.xmin) / self.width
            result = []
            for token in self.rpn:
                if token.typ is TokenType.NUMBER:
                    result.append(token.val)
                elif token.typ is TokenType.X:
                    result.append(x)
                elif token.typ is TokenType.FUNCTION:
                    if token.val == 'ln':
                        result.append(log(result.pop()))
                    elif token.val == 'log':
                        result.append(log(result.pop()), 10)
                    elif token.val == 'sqrt':
                        result.append(sqrt(result.pop()))
                    elif token.val == 'sin':
                        result.append(sin(result.pop()))
                    elif token.val == 'cos':
                        result.append(cos(result.pop()))
                    elif token.val == 'tan':
                        result.append(tan(result.pop()))
                    elif token.val == 'asin':
                        result.append(asin(result.pop()))
                    elif token.val == 'acos':
                        result.append(acos(result.pop()))
                    elif token.val == 'atan':
                        result.append(atan(result.pop()))
                    elif token.val == '+':
                        pass
                    elif token.val == '-':
                        result.append(-result.pop())
                elif token.typ is TokenType.OPERATOR:
                    if token.val == '+':
                        result.append(result.pop() + result.pop())
                    elif token.val == '-':
                        result.append(-(result.pop() - result.pop()))
                    elif token.val == '*':
                        result.append(result.pop() * result.pop())
                    elif token.val == '/':
                        result.append(1/(result.pop() / result.pop()))
                    elif token.val == '^':
                        tmp = result.pop()
                        result.append(pow(result.pop(), tmp))
            self.xpts.append(i)
            self.ypts.append(-(self.ymin + result[0]) / (self.ymax - self.ymin) * self.height)
            i += 1


class Token():
    """ Token Class """

    l_parens = ('(', '[')
    r_parens = (')', ']')
    number = recompile(r'^-?(?!\.$)\d*\.?\d*$')
    constants = ('e', 'pi', 'tau', 'rand')
    functions = ('ln', 'log', 'sqrt', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan')
    operators = ('^', '+', '-', '*', '/', )

    def __init__(self, val):
        """ initialize a token """
        self.typ = self.__get_type__(val)
        self.precedence = -1

        if self.typ is TokenType.NUMBER:
            if val == 'e':
                self.val = e
            elif val == 'pi':
                self.val = pi
            elif val == 'tau':
                self.val = 2 * pi
            elif val == 'rand':
                self.val = random()
            else:
                if val[-1] == '.':
                    self.val = val[:-1]
                try:
                    self.val = int(val)
                except ValueError:
                    self.val = float(val)
        elif self.typ is TokenType.OPERATOR:
            if val == "^":
                pass
            self.val = val
        else:
            self.val = val


    def __get_type__(self, val):
        """ get TokenType for this Token
                based on:
                    - val: current token stored as string
        """
        if val in Token.l_parens:
            return TokenType.L_PAREN

        if val in Token.r_parens:
            return TokenType.R_PAREN

        if val in Token.operators:
            return TokenType.OPERATOR

        if self.check_re(Token.number.search(val)):
            return TokenType.NUMBER

        if val in Token.constants:
            return TokenType.NUMBER

        if val in Token.functions:
            return TokenType.FUNCTION

        if val == 'x':
            return TokenType.X

        return  TokenType.INVALID


    def check_re(self, regexp):
        if regexp is None:
            return False
        if regexp.end() == 0:
            return False
        return True


    def __repr__(self):
        return str(self.val) + ' (type: ' + str(self.typ) + ')'


class TokenType(Enum):
    """ TokenType Class """
    # x
    X = 0
    # sin,cos,tan,asin,acos,atan,max,min,round,int
    FUNCTION = 1
    # +,-,*,/ (LHS), ^ (RHS)
    OPERATOR = 2
    # [-1-9]+ or (e,pi,tau)
    NUMBER = 3
    # (,[
    L_PAREN = 4
    # ),]
    R_PAREN = 5
    # INVALID
    INVALID = -1


if __name__ == '__main__':
    main()
