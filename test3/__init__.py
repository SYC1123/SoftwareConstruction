def go(old_first_size, new_first_size):
    for key in old_first_size:
        if old_first_size[key] != new_first_size[key]:
            return True
    return False


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
    # print(grammar_rules)
    # 初始化文法规则的初始集合
    for item in grammar_rules:
        if item[:item.index('-')] not in init_set.keys():
            init_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
            temporary_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
            old_first_size[item[:item.index('-')]] = 0
            new_first_size[item[:item.index('-')]] = 0
        else:
            init_set[item[:item.index('-')]].append(item[item.index('>') + 1:])
            temporary_set[item[:item.index('-')]] = [item[item.index('>') + 1:]]
    # {'E': ['TA'], 'A': ['+TA', 'ε'], 'T': ['FB'], 'B': ['*FB', 'ε'], 'F': ['i', '(E)']}
    # print(init_set)
    # 构造空集的临时表，用于计算后续的空集
    for item in init_set:
        if 'ε' in init_set[item]:
            ε_set.append(item)
            del temporary_set[item]
    # print(temporary_set)
    # print(ε_set)
    # 计算能推出空集的符号集
    a = True
    while True:
        if a:
            a = False
            for item in ε_set:  # 产生空的符号
                for key in temporary_set:  # 临时集的键
                    for i in range(0, len(temporary_set[key])):  # 遍历字典键值对应的value即为字符串
                        if item in temporary_set[key][i]:
                            temporary_set[key][i] = temporary_set[key][i].replace(item, '')
                            if temporary_set[key][i] == '':
                                a = True
                                ε_set.append(item)
                                del temporary_set[item]
        else:
            break
    print(init_set)
    # while go(old_first_size, new_first_size):
    for key in init_set.keys():
        for value in init_set[key]:
            print(value, end=" ")
        print()
