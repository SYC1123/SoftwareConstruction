import copy

from test1.test import dealProgrammer, dealString, dealNumber

ReservedWords = []
TheOperator = {}
RangeFlag = {}
Number = {}
# 以下为空
Result = []
Identifier = []  # 标识符 字母A-Z,a-z,0-9,_
Constant = []  # 常数，定点小数
ReservedWordsList = []  # 保留字
TheOperatorList = []  # 运算符
RangeFlagList = []  # 界符


def addelement(tu, element):
    l = list(tu)
    l.append(element)
    tu = tuple(l)
    return tu


def findexist(j, Result):
    for part in Result:
        if j[1] == part[1]:
            return part


if __name__ == '__main__':
    f = open('ReservedWords.txt', 'r')
    for line in f.readlines():
        NewReservedWords = line.split(',')
        ReservedWords = copy.copy(NewReservedWords)
    f.close()
    f = open('TheOperator.txt', 'r')
    for line in f.readlines():
        TheOperatorlist = line.split(',')
        for i in TheOperatorlist:
            TheOperator[i] = 0
    f.close()
    f = open('RangeFlag.txt', 'r')
    for line in f.readlines():
        RangeFlaglist = line.split('-')
        for i in RangeFlaglist:
            RangeFlag[i] = 0
    f.close()
    f = open('Number.txt', 'r')
    for line in f.readlines():
        Numberlist = line.split(',')
        for i in Numberlist:
            Number[i] = 0
    f.close()
    builder = []
    builder = dealProgrammer('data.txt')
    dealNumber(builder)
    dealString(builder)
    f = open('Result.txt', 'w')
    for x in builder:
        ResultPart = []
        for j in x:
            if j[0] == 1:  # 标识符 字母A-Z,a-z,0-9,_
                if j[1] not in Identifier:
                    Identifier.append(j[1])
                    j = addelement(j, Identifier.index(j[1]))
                    Result.append(j)
                    ResultPart.append(j)
                else:
                    part = findexist(j, Result)
                    ResultPart.append(part)
            elif j[0] == 2:  # 常数，定点小数
                if j[1] not in Constant:
                    Constant.append(j[1])
                    j = addelement(j, Constant.index(j[1]))
                    Result.append(j)
                    ResultPart.append(j)
                else:
                    part = findexist(j, Result)
                    ResultPart.append(part)
            elif j[0] == 3:  # 保留字3
                if j[1] not in ReservedWordsList:
                    ReservedWordsList.append(j[1])
                    j = addelement(j, ReservedWords.index(j[1]))
                    Result.append(j)
                    ResultPart.append(j)
                else:
                    part = findexist(j, Result)
                    ResultPart.append(part)
            elif j[0] == 4:  # 运算符4
                if j[1] not in TheOperatorList:
                    TheOperatorList.append(j[1])
                    j = addelement(j, list(TheOperator).index(j[1]))
                    Result.append(j)
                    ResultPart.append(j)
                else:
                    part = findexist(j, Result)
                    ResultPart.append(part)
            else:  # 界符5
                if j[1] not in RangeFlagList:
                    RangeFlagList.append(j[1])
                    j = addelement(j, list(RangeFlag).index(j[1]))
                    Result.append(j)
                    ResultPart.append(j)
                else:
                    part = findexist(j, Result)
                    ResultPart.append(part)
        print(ResultPart)
        f.writelines(str(ResultPart))
        f.writelines('\n')
    print(Result)
    f.close()
    f = open('Identifier.txt', 'w')
    f.writelines(str(Identifier))
    f.close()
    f = open('Constant.txt', 'w')
    f.writelines(str(Constant))
    f.close()
