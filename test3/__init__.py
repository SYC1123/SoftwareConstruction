from copy import deepcopy

import xlrd as xlrd
import xlwt as xlwt


def continue_go(old_size, new_size):
    '''
    :param old_size: 旧的字典，字典内的键值对应的值是之前键值包含的次数（比如first（E）中的字符数量）
    :param new_size: 新的字典，字典内的键值对应的值是之后键值包含的次数（比如first（E）中的字符数量）
    :return: 如果两次字典内的字符集的个数不同，表示first集或者follow集没求完，返回True继续循环计算，否则返回False
    '''
    for key in old_size:
        if old_size[key] != new_size[key]:
            # old=new
            exchange(old_size, new_size)  # 自己写的函数，用于把new_size内容赋值到old_size内，即表示当前的新集合已经变成了下次计算的旧集合
            return True
    return False


def has_next(str, index):
    '''
    :param str:
    :param index:
    :return:
    '''
    try:
        a = str[index + 1]
        return True
    except:
        return False


def exchange(old_size, new_size):
    '''
    用于把new_size内容赋值到old_size内，即表示当前的新集合已经变成了下次计算的旧集合
    :param old_size: 旧集合
    :param new_size: 新集合
    :return:
    '''
    for key in old_size:
        old_size[key] = new_size[key]


def isnull(string):
    count = 0
    if string == 'ε':
        return True
    else:
        for var in string:
            if var.isupper() and var in ε_set:
                count = count + 1
        if count == len(string):
            return True
        else:
            return False


def getfirst(string):
    first_part = []
    if string == 'ε':
        return first_part
    else:
        for var in string:
            if var.isupper():
                if var in ε_set:
                    first_part = first_part + first[var]
                    first_part = list(set(first_part))
                else:
                    first_part = first_part + first[var]
                    first_part = list(set(first_part))
                    return first_part
            else:
                first_part.append(var)
                first_part = list(set(first_part))
                return first_part


def getendsymbol(original_set):
    end_symbol = []
    for key in original_set:
        for value in original_set[key]:
            for var in value:
                if var.isupper() or var == 'ε':
                    end_symbol = end_symbol + []
                else:
                    end_symbol.append(var)
    end_symbol = list(set(end_symbol))
    end_symbol.append('#')
    return end_symbol


if __name__ == '__main__':
    grammar_rules = []  # 文法规则
    first = {}  # first集
    old_first_size = {}  # 旧的每个符号first集的大小
    new_first_size = {}  # 新的每个符号first集的大小
    follow = {}  # follow集
    old_follow_size = {}  # 旧的每个符号的follow集的大小
    new_follow_size = {}  # 新的每个符号的follow集的大小
    select = {}  # select集
    init_set = {}  # 文法规则的初始集合
    temporary_set = {}  # 文法规则的初始集合的临时集合
    ε_set = []  # 能产生ε的符号
    '''
    从文件中把文法规则读出来
    '''
    f = open('grammer.txt')
    for line in f.readlines():
        line = line.strip('\n')
        grammar_rules.append(line)
        select[line] = []
    f.close()
    ''''
    该位置可以看文法规则
    '''
    # print(grammar_rules)
    '''
    初始化文法规则的初始集合，集合都是字典，含义是每个(字符:列表)
    '''
    for item in grammar_rules:
        # 对以上所有的集合进行初始化
        if item[:item.index('-')] not in init_set.keys():
            init_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
            temporary_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
            old_first_size[item[:item.index('-')]] = 0
            new_first_size[item[:item.index('-')]] = 0
            first[item[:item.index('-')]] = []
            old_follow_size[item[:item.index('-')]] = 0
            new_follow_size[item[:item.index('-')]] = 1
            follow[item[:item.index('-')]] = []
            if item[:item.index('-')] == 'E':  # 初始化follow集时，如果有起始符号E，则把#加进去
                follow['E'].append('#')
        else:
            init_set[item[:item.index('-')]].append(item[item.index('>') + 1:])
            temporary_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
    # {'E': ['TA'], 'A': ['+TA', 'ε'], 'T': ['FB'], 'B': ['*FB', 'ε'], 'F': ['i', '(E)']}
    '''
    该位置可以看文法规则的初始集合
    '''
    print(init_set)
    # 构造空集的临时表，用于计算后续的空集,遍历文法规则的初始集合，使用的是键值遍历,如果该键值的对应的文法有空，则把其添加到空集的临时表，
    # 但是该表不代表最终的空集符号集，比如C->AB,A,B都能推出空，但是临时表内没有C
    for item in init_set.keys():
        if 'ε' in init_set[item]:
            ε_set.append(item)  # 把能直接推出空的字符添加到空集中
            del temporary_set[item]  # 把能推出空的字符从temporary_set字典中移除
    '''
    该位置可以看文法规则的初始集合的临时集合，能产生ε的符号
    '''
    # print(temporary_set)
    # print(ε_set)
    '''
    计算能推出空集的符号集
    '''
    a = True
    while True:  # 做一个死循环，如果推出新的空集符号，则继续循环
        if a:
            a = False
            for item in ε_set:  # 遍历此时产生空的符号集
                for key in temporary_set.keys():  # 遍历临时空符号集的键
                    for i in range(0, len(temporary_set[key])):  # 遍历字典键值对应的value即为字符串（例如：A——>BC,遍历的是A键值下对应的BC字符串）
                        if item in temporary_set[key][i]:  # 如果此时空集里面的符号在该字符串内
                            temporary_set[key][i] = temporary_set[key][i].replace(item, '')  # 把该符号去掉
                            if temporary_set[key][i] == '':  # 经过遍历之后，如果该串经过去除推出空集的符号后，变成了空串，
                                # 则表示该串也能推出空，把键值添加到空集中（该方法处理的就是形如A->BC 这种产生式）
                                a = True
                                ε_set.append(item)
        else:
            break
    '''
    该位置可以看文法规则的初始集合
    '''
    # print(init_set)
    '''
    保存好文法规则的初始集合用于计算follow集、select集
    '''
    follow_init_set = {}
    follow_init_set = deepcopy(init_set)  # 调用深复制方法，复制一个一模一样的文法初始集合
    select_init_set = {}
    select_init_set = deepcopy(init_set)  # 调用深复制方法，复制一个一模一样的文法初始集合
    '''
    初始化第一次的first集
    '''
    for key in init_set.keys():
        for value in init_set[key]:
            if value[0].isupper():  # 如果开头是大写字符，即非终结符，则不处理
                a = None
            else:  # 如果开头是终极字符，则添加到该符号的first集中
                first[key].append(value[0])
                new_first_size[key] = new_first_size[key] + 1  # 用于统计每个符号first集中各个符号的个数
    # print(first)
    '''
    # 计算first集
    '''
    while continue_go(old_first_size, new_first_size):  # 上文中自己写的函，如果两次字典内的字符集的个数不同，即表示first集没求完，继续循环
        # 下面操作new_first_size
        for key in init_set.keys():  # 首先遍历文法集合的产生式左部
            for index in range(0, len(init_set[key])):  # 遍历每个左部推导的右部的内容，用一个index下标遍历每个字符串
                if init_set[key][index][0].isupper():
                    # 产生式右部开头是非终结符
                    if init_set[key][index][0] in ε_set:
                        # 产生式右部开头的非终结符能推出空
                        first[key] = first[key] + first[init_set[key][index][0]]  # 当前的first集要加上该非终结符的first集
                        first[key] = list(set(first[key]))  # 去重
                        new_first_size[key] = len(first[key])  # 更新first集个数
                        if len(init_set[key][index]) == 1:  # 如果产生式右部的字符串长度为一（比如A->B）
                            # 把该符号产生式右部变成'ε'，这么做的目的是下次循环遍历到该产生式时，直接添加'ε'，最后一去重，仍只有一个'ε'
                            # ，就不需要进到该判断式进行这么复杂的计算了
                            s = list(init_set[key][index])
                            s[0] = 'ε'
                            init_set[key][index] = ''.join(s)
                        else:
                            # 长度不为一，则把产生式右部第一个字符去掉
                            init_set[key][index] = init_set[key][index].lstrip(init_set[key][index][0])
                    else:
                        # 开头的非终结符不能推出空
                        first[key] = first[key] + first[init_set[key][index][0]]  # 当前的first集要加上该非终结符的first集
                        first[key] = list(set(first[key]))  # 去重
                        new_first_size[key] = len(first[key])  # 更新first集个数
                else:
                    # 产生式右部开头是终结符
                    first[key].append(init_set[key][index][0])  # 直接把该符号添加到first集中
                    first[key] = list(set(first[key]))  # 去重
                    new_first_size[key] = len(first[key])  # 更新first集个数
    '''
    最终first集
    '''
    print('--------------------------------------------------------------')
    # print('first集：', first)
    for key in first:
        print('first(%c)=' % key, first[key])
    print('--------------------------------------------------------------')
    '''
     计算follow集
    '''
    # print(follow_init_set)
    # print(follow)
    while continue_go(old_follow_size, new_follow_size):  # 上文中自己写的函，如果两次字典内的字符集的个数不同，即表示follow集没求完，继续循环
        for key in follow_init_set:  # 计算key的follow集
            for value in follow_init_set[key]:
                for k in follow_init_set:
                    for i in range(0, len(follow_init_set[k])):
                        index = follow_init_set[k][i].find(key)
                        if index != -1:
                            if has_next(follow_init_set[k][i], index):  # 查找的字符后面有follow
                                index = index + 1
                                var = follow_init_set[k][i][index]
                                if var.isupper():  # 非终结符
                                    follow[key] = follow[key] + first[var]
                                    follow[key] = list(set(follow[key]))
                                    new_follow_size[key] = len(follow[key])
                                    if var in ε_set and has_next(follow_init_set[k][i], index) == False:
                                        follow[key] = follow[key] + follow[k]
                                        follow[key] = list(set(follow[key]))
                                        new_follow_size[key] = len(follow[key])
                                    while var in ε_set and has_next(follow_init_set[k][i],
                                                                    index):  # 把后面非空的follow全加进去
                                        index = index + 1
                                        var = follow_init_set[k][i][index]
                                        follow[key] = follow[key] + first[var]
                                        follow[key] = list(set(follow[key]))
                                        new_follow_size[key] = len(follow[key])
                                        if var in ε_set and has_next(follow_init_set[k][i], index) == False:
                                            follow[key] = follow[key] + follow[k]
                                            follow[key] = list(set(follow[key]))
                                            new_follow_size[key] = len(follow[key])
                                else:  # 终结符
                                    if var not in follow[key]:
                                        follow[key].append(var)
                                        new_follow_size[key] = len(follow[key])
                            else:
                                follow[key] = follow[key] + follow[k]
                                follow[key] = list(set(follow[key]))
                                # print(key, k, follow[key], follow[k])
                                new_follow_size[key] = len(follow[key])
        # print(follow_init_set)
    for key in follow:
        for item in follow[key]:
            if 'ε' in item:
                follow[key].remove('ε')
    '''
    最终的follow集
    '''
    # print('follow集：', follow)
    for key in follow:
        print('follow(%c)=' % key, follow[key])
    print('--------------------------------------------------------------')
    '''
    计算select集
    '''
    # print(select)
    for key in select:
        if isnull(key[key.index('>') + 1:]):
            # 能推出空
            select[key] = getfirst(key[key.index('>') + 1:]) + follow[key[:key.index('-')]]
        else:
            # 推不出空
            select[key] = getfirst(key[key.index('>') + 1:])
    for key in select:
        if 'ε' in select[key]:
            select[key].remove('ε')
    for key in select:
        print('select(%s)=' % key, select[key])
    print('--------------------------------------------------------------')
    '''
    构造预测分析表
    '''
    writebook = xlwt.Workbook()
    test = writebook.add_sheet('预测分析表')
    end_symbol = getendsymbol(init_set)
    # print(end_symbol)
    for j in range(0, len(end_symbol)):
        test.write(0, j + 1, end_symbol[j])
    for i, key in zip(range(0, len(first)), first.keys()):
        test.write(i + 1, 0, str(key))
    writebook.save('grammerTable.xls')
    readbook = xlrd.open_workbook('grammerTable.xls')
    sheet = readbook.sheet_by_name('预测分析表')
    rows = sheet.row_values(0)  # 返回第1行，终结符
    cols = sheet.col_values(0)  # 返回第一列，非终结符
    for key in select.keys():
        var = key[:key.index('-')]
        row = cols.index(var)
        for value in select[key]:
            col = rows.index(value)
            test.write(row, col, key[key.index('>') + 1:])
    writebook.save('grammerTable.xls')
    print('预测分析表构建完成')
    print('--------------------------------------------------------------')
    remain_string = []  # 剩余字符串
    analysis_formula = []  # 分析式
    st = input("请输入表达式")
    # st = 'i+i*i'
    for var in st:
        remain_string.append(var)
    remain_string.append('#')
    analysis_formula.append('#')
    analysis_formula.append('E')
    remain = remain_string[0]
    analysis = analysis_formula[-1]
    f = open('Result.txt', 'w')
    # f.writelines('步骤\t\t' + '分析式\t\t\t\t' + '剩余输入串\t\t\t' + '所用产生式' + '\n')
    f.write("%-15s%-35s%-27s%-35s\n" % ('步骤', '分析式', '剩余输入串', '所用产生式'))
    count = 1
    while analysis.__eq__('#') + 1 != 2 or remain.__eq__('#') + 1 != 2:  # 都不是#
        readbook = xlrd.open_workbook('grammerTable.xls')
        sheet = readbook.sheet_by_name('预测分析表')
        if analysis.__eq__(remain):  # 相等
            # print('%c匹配' % analysis)
            tem = '%c匹配' % analysis
            f.write("%-15d%-35s%-35s%-35s\n" % (count, str(analysis_formula), str(remain_string), tem))
            count = count + 1
            analysis_formula.remove(analysis)
            remain_string.remove(remain)
            analysis = analysis_formula[-1]
            remain = remain_string[0]
        else:  # 不相等
            if analysis.__eq__('#'):
                print('错误')
                f.write("%-15d%-35s%-35s%-35s\n" % (count, str(analysis_formula), str(remain_string), '错误'))
                count = count + 1
                break
            else:
                j = rows.index(remain)
                i = cols.index(analysis)
                value = sheet.cell(i, j).value
                if value == '':
                    print('错误')
                    f.write("%-15d%-35s%-35s%-35s\n" % (count, str(analysis_formula), str(remain_string), '错误'))
                    count = count + 1
                    break
                tem_ana = analysis
                analysis_formula.remove(analysis)
                if value != 'ε':
                    value = value[::-1]
                    for item in value:
                        analysis_formula.append(item)
                value = value[::-1]
                value = tem_ana + '->' + value
                f.write("%-15d%-35s%-35s%-35s\n" % (count, str(analysis_formula), str(remain_string), value))
                count = count + 1
                analysis = analysis_formula[-1]
                remain = remain_string[0]
    if remain.__eq__('#') and analysis.__eq__('#'):
        f.write("%-15d%-35s%-35s%-35s\n" % (count, str(analysis_formula), str(remain_string), '接受'))
        print('接受')
    f.close()
    print('表达式分析完成')
    print('--------------------------------------------------------------')
