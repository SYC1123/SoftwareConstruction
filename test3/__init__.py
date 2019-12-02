def go(old_first_size, new_first_size):
    for key in old_first_size:
        if old_first_size[key] != new_first_size[key]:
            # old=new
            exchange(old_first_size, new_first_size)
            return True
    return False


def exchange(old_first_size, new_first_size):
    for key in old_first_size:
        old_first_size[key] = new_first_size[key]


if __name__ == '__main__':
    grammar_rules = []  # 文法规则
    first = {}  # first集
    old_first_size = {}  # 旧的每个符号first集的大小
    new_first_size = {}  # 新的每个符号first集的大小
    follow = {}  # follow集
    init_set = {}  # 文法规则的初始集合
    temporary_set = {}  # 文法规则的初始集合的临时集合
    ε_set = []  # 能产生ε的符号
    f = open('grammer.txt')
    for line in f.readlines():
        line = line.strip('\n')
        grammar_rules.append(line)
    f.close()
    ''''
    该位置可以看文法规则
    '''
    # print(grammar_rules)
    # 初始化文法规则的初始集合
    for item in grammar_rules:
        if item[:item.index('-')] not in init_set.keys():
            init_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
            temporary_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
            old_first_size[item[:item.index('-')]] = 0
            new_first_size[item[:item.index('-')]] = 0
            first[item[:item.index('-')]] = []
        else:
            init_set[item[:item.index('-')]].append(item[item.index('>') + 1:])
            temporary_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
    # {'E': ['TA'], 'A': ['+TA', 'ε'], 'T': ['FB'], 'B': ['*FB', 'ε'], 'F': ['i', '(E)']}
    '''
    该位置可以看文法规则的初始集合
    '''
    # print(init_set)
    # 构造空集的临时表，用于计算后续的空集
    for item in init_set:
        if 'ε' in init_set[item]:
            ε_set.append(item)
            del temporary_set[item]
    '''
    该位置可以看文法规则的初始集合的临时集合，能产生ε的符号
    '''
    # print(temporary_set)
    # print(ε_set)
    # 计算能推出空集的符号集
    a = True
    while True:
        if a:
            a = False
            for item in ε_set:  # 产生空的符号
                for key in temporary_set.keys():  # 临时集的键
                    for i in range(0, len(temporary_set[key])):  # 遍历字典键值对应的value即为字符串
                        if item in temporary_set[key][i]:
                            temporary_set[key][i] = temporary_set[key][i].replace(item, '')  # 把该符号去掉
                            if temporary_set[key][i] == '':
                                a = True
                                ε_set.append(item)
                                # del temporary_set[key]
        else:
            break
    '''
    该位置可以看文法规则的初始集合
    '''
    # print(init_set)
    for key in init_set:
        for value in init_set[key]:
            if value[0].isupper():
                a = None
            else:
                first[key].append(value[0])
                new_first_size[key] = new_first_size[key] + 1
    # print(first)
    while go(old_first_size, new_first_size):
        # 下面操作new_first_size
        for key in init_set.keys():
            for value in init_set[key]:
                if value[0].isupper():
                    # 非终结符
                    if value[0] in ε_set:
                        # 开头的非终结符能推出空
                        first[key] = first[key] + first[value[0]]
                        first[key] = list(set(first[key]))
                        new_first_size[key] = len(first[key])
                        if len(value) == 1:
                            value = 'ε'
                        else:
                            value = value[1:]
                    else:
                        # 开头的非终结符不能推出空
                        first[key] = first[key] + first[value[0]]
                        first[key] = list(set(first[key]))
                        new_first_size[key] = len(first[key])
                else:
                    # 终结符
                    first[key].append(value[0])
                    first[key] = list(set(first[key]))
                    new_first_size[key] = len(first[key])
                # print(value, end=" ")
            # print()
    '''
    最终first集
    '''
    print(first)
