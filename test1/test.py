Identifier = 1  # 标识符 字母A-Z,a-z,0-9,_

Constant = 2  # 常数，定点小数

ReservedWords = ['int', 'long', 'short', 'float', 'double', 'char', 'unsigned', 'signed', 'const', 'void'
    , 'volatile'
    , 'enum', 'struct', 'union', 'if', 'else'
    , 'goto', 'switch', 'case', 'do', 'while', 'for'
    , 'continue', 'break', 'return'
    , 'default', 'typedef', 'auto', 'register', 'extern', 'static', 'sizeof']  # 保留字3

TheOperator = {'+': 0, '-': 0, '*': 0, '/': 0, '++': 0, '--': 0, '%': 0, '|': 0, '&': 0, '^': 0, '#': 0, '<': 0, '>': 0,
               '=': 0}  # 运算符4

RangeFlag = {'(': 0, ')': 0, '[': 0, ']': 0, '{': 0, '}': 0, '.': 0, ',': 0, ';': 0, '<': 0, '>': 0, "'": 0, '\\': 0,
             '\"': 0}  # 界符5

Number = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}  # 数字


def dealProgrammer(Path):
    builder = []
    f = open(Path, 'r')
    for line in f.readlines():
        lineBuilder = []
        line = line.strip('\n')
        line = line.strip(' ')
        line = line.split(' ')
        for item in line:  # 遍历每个字符串
            if item in ReservedWords:
                lineBuilder.append((3, item))
            elif item in RangeFlag.keys():
                lineBuilder.append((5, item))
            elif item in TheOperator.keys():
                lineBuilder.append((4, item))
            elif is_number(item):
                lineBuilder.append((2, item))
            else:
                nowPosition = -1  # 记录特殊符号位置
                beforPosition = -1  # 记录特殊符号位置
                for key in RangeFlag.keys():
                    RangeFlag[key] = 0
                for key in TheOperator.keys():
                    TheOperator[key] = 0
                for key in Number.keys():
                    Number[key] = 0
                for part in item:  # 遍历字符串的每一个字符
                    if part in TheOperator.keys():
                        beforPosition = nowPosition
                        nowPosition = item.find(part, TheOperator[part])  # 下标
                        TheOperator[part] = nowPosition + 1
                        addPart(nowPosition, beforPosition, lineBuilder, item)
                        lineBuilder.append((4, part))
                    elif part in RangeFlag.keys():
                        beforPosition = nowPosition
                        nowPosition = item.find(part, RangeFlag[part])
                        RangeFlag[part] = nowPosition + 1
                        addPart(nowPosition, beforPosition, lineBuilder, item)
                        lineBuilder.append((5, part))
                    elif part in Number.keys():
                        beforPosition = nowPosition
                        nowPosition = item.find(part, Number[part])
                        Number[part] = nowPosition + 1
                        addPart(nowPosition, beforPosition, lineBuilder, item)
                        lineBuilder.append((2, part))
                if nowPosition != (len(item) - 1):
                    lineBuilder.append((1, item[nowPosition + 1:]))
        builder.append(lineBuilder)
    f.close()
    return builder


def addPart(nowPosition, beforPosition, lineBuilder, item):
    if nowPosition == 0:
        beforPosition += 1
    if beforPosition != nowPosition:
        if beforPosition + 1 != nowPosition:
            if item[beforPosition + 1:nowPosition] in ReservedWords:  # 判断是否是保留字
                lineBuilder.append((3, item[beforPosition + 1:nowPosition]))
            else:
                lineBuilder.append((1, item[beforPosition + 1:nowPosition]))


def is_number(s):
    try:
        float(s)  # int, long and float
    except ValueError:
        try:
            complex(s)  # complex
        except ValueError:
            return False
    return True


def isNumber(index, data):
    if data[index][1].isdigit():
        return True
    elif data[index][1] == '.':
        if data[index + 1][1].isdigit():
            return True
    else:
        return False


def dealNumber(builder):
    for i in builder:
        string = ''
        deleteallindex = {}
        deleteindex = []  # 记录要删除的下标
        for a in range(len(i)):
            if isNumber(a, i):
                string += i[a][1]
                deleteindex.append(a)
            else:
                if string != '':
                    deleteallindex.update({str(deleteindex): string})
                    string = ''
                    deleteindex = []
        dellist = []
        for delallindex in deleteallindex.keys():
            p = eval(delallindex)
            if len(p) != 1:
                i[p[0]] = (1, deleteallindex[delallindex])
                dellist += p[1:]
        i = [i[x] for x in range(len(i)) if (x not in dellist)]
        dellist = []
        deleteallindex = {}


if __name__ == '__main__':
    builder = []
    builder = dealProgrammer('data.txt')
    # dealNumber(builder)
    for i in builder:
        # print(i)
        string = ''
        deleteallindex = {}
        deleteindex = []  # 记录要删除的下标
        for a in range(len(i)):
            if isNumber(a, i):
                string += i[a][1]
                deleteindex.append(a)
            else:
                if string != '':
                    deleteallindex.update({str(deleteindex): string})
                    string = ''
                    deleteindex = []
        dellist = []
        for delallindex in deleteallindex.keys():
            p = eval(delallindex)
            if len(p) != 1:
                i[p[0]] = (1, deleteallindex[delallindex])
                dellist += p[1:]
        print(i)
        i = [i[x] for x in range(len(i)) if (x not in dellist)]
        print(i)
        # dellist = []
        # deleteallindex = {}
    # for i in builder:
    #     for j in i:
    #         print(j, end="  ")
    #     print()
