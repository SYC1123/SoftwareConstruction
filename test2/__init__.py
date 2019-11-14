from test1.test import dealProgrammer, dealString, dealNumber

ReservedWords = []
TheOperator = {}
RangeFlag = {}
Number = {}
Result = []
Identifier = []  # 标识符 字母A-Z,a-z,0-9,_
Constant = []  # 常数，定点小数


def init():
    f = open('ReservedWords.txt', 'r')
    for line in f.readlines():
        ReservedWords = line.split(',')
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


def addelement(tu, element):
    l = list(tu)
    l.append(element)
    tu = tuple(l)
    return tu


if __name__ == '__main__':
    init()
    builder = []
    builder = dealProgrammer('data.txt')
    dealNumber(builder)
    dealString(builder)
    for x in builder:
        for j in x:
            if j[0] == 1:  # 标识符 字母A-Z,a-z,0-9,_
                # print(1)
                if j[1] not in Identifier:
                    Identifier.append(j[1])
                    j=addelement(j, Identifier.index(j[1]))
                    Result.append(j)
            elif j[0] == 2:  # 常数，定点小数
                if j[1] not in Constant:
                    Constant.append(j[1])
                    addelement(j, Constant.index(j[1]))
                    Result.append(j)
                # print(2)
            elif j[0] == 3:  # 保留字3
                if j[1] not in Result:
                    addelement(j, ReservedWords.index(j[1]))
                    Result.append(j)
                # print(3)
            elif j[0] == 4:  # 运算符4
                if j[1] not in Result:
                    addelement(j, list(TheOperator).index(j[1]))
                    Result.append(j)
                # print(4)
            else:  # 界符5
                if j[1] not in Result:
                    addelement(j, list(RangeFlag).index(j[1]))
                    Result.append(j)
                # print(5)
        print(Result)
