
class ParsetParser():

    __slots__ = ('parsetFile', 'parsetDict', 'comentsDict', 'params', 'lineNr')
    def __init__(self, parsetFile):
        self.parsetFile = parsetFile
        self.parsetDict = dict()
        self.comentsDict = dict()
        self.params = dict()
        self.lineNr = 0

    def parse(self):

        with open(self.parsetFile, "r") as parsetData:
            parsetLines = parsetData.readlines()

        for line in parsetLines:
            if  not line.startswith("#") and len(line) > 1:
                key = line.split("=")[0].strip()
                value = line.split("=")[1].replace(" ", "")
                if "#" in value:
                    value = value[0:value.index("#")]

                self.params[str(self.lineNr)] = key
                self.parsetDict[key] = value

            if "#" in line:
                if line.startswith("#"):
                    self.comentsDict[str(self.lineNr)] = [line[1:len(line)], "ALL"]
                else:
                    self.comentsDict[str(self.lineNr)] = [line[line.index("#"):len(line)], ""]

            self.lineNr += 1

    def getParams(self, param):
        return self.parsetDict[param]

    def setParam(self, param, value):
        self.parsetDict[param] = value

    def writeParset(self, parsetFile):
        with open(parsetFile, "w") as file:
            for l in range(0, self.lineNr):
                if str(l) in self.comentsDict.keys() and  str(l) in self.params.keys():
                    s1 = self.params[str(l)] + " = " + self.parsetDict[self.params[str(l)]]
                    s2 = "#" + self.comentsDict[str(l)][0] + "\n"
                    s = s1.ljust(99, " ") + s2
                    file.write(s)
                elif str(l) in self.comentsDict.keys():
                    file.write("# " + self.comentsDict[str(l)][0] + "\n")
                elif str(l) in self.params.keys():
                    file.write(self.params[str(l)] + " = " + self.parsetDict[self.params[str(l)]] + "\n")

