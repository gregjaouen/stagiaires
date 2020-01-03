#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys

class ARGVParser:

    def __init__(self, pattern):
        ## TODO: throw exception for minial argv
        super().__init__()
        self.pattern = pattern
        self.rawArgs = sys.argv[1:]
        self.__parseRaw()

    def hasActions(self, *actions):
        for index in range(len(actions)):
            if actions[index] != self.parsed[index]:
                return False
        return True
    
    def getOptions(self):
        try:
            return self.parsed[-1]
        except (NameError, IndexError):
            return []

    def __parseFromLevel(self, index, patternLevel):
        if index < len(self.rawArgs):
            arg = self.rawArgs[index]
            if type(patternLevel) == dict:
                if arg in patternLevel:
                    self.parsed.append(arg)
                    self.__parseFromLevel(index+1, patternLevel[arg])
                else:
                    raise Exception("Unknown arg: {:s}".format(arg))
            elif type(patternLevel) == list:
                options = {}
                for i in range(len(patternLevel)):
                    options[patternLevel[i]] = self.rawArgs[index+i]
                self.parsed.append(options)
            else:
                # TODO: throw Exception for unknown pattern type
                pass

    def __parseRaw(self):
        self.parsed = []
        self.__parseFromLevel(0, self.pattern)
        print(self.parsed)

