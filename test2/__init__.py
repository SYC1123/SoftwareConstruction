from test1.test import dealProgrammer, dealString, dealNumber

ReservedWords = []
TheOperator = {}
RangeFlag = {}
Number = {}


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
        RangeFlaglist = line.split(',')
        for i in RangeFlaglist:
            RangeFlag[i] = 0
    f.close()
    f = open('Number.txt', 'r')
    for line in f.readlines():
        Numberlist = line.split(',')
        for i in Numberlist:
            Number[i] = 0
    f.close()


if __name__ == '__main__':
    init()
    builder = []
    builder = dealProgrammer('data.txt')
    dealNumber(builder)
    dealString(builder)
    for x in builder:
        for j in x:
            print(j, end=" ")
        print()
