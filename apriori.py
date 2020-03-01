import itertools


class Apriori:
    items = []
    transactions = []
    len_of_items = 0
    len_of_trans = 0
    item_set = []
    item_set_with_value = []
    larger_item_set = {}
    association_rules = {}

    support_threshold = 0.0
    confidence_threshold = 0.0

    def calculate(self, m_items, m_transactions, m_support, m_confidence):
        # init items, transactions, and len_of_trans
        self.items = sorted(m_items)
        self.transactions = m_transactions
        self.len_of_items = len(m_items)
        self.len_of_trans = len(m_transactions)
        self.support_threshold = m_support
        self.confidence_threshold = m_confidence

        # init item_set
        self.init_item_set()
        self._count_value_in_item_set()

        # find larger item set
        self._calculate_larger_item_set()

        # create rules
        self._association_rules()
        pass

    def info(self):
        print("items : " + str(self.items))
        print('support : ' + str(self.support_threshold))
        print('confidence : ' + str(self.confidence_threshold), end='\n\n')

        print("transactions : ")
        for m_trans in self.transactions:
            print('T' + str(self.transactions.index(m_trans) + 1) + ' : ' + str(m_trans))
        print(' ')

        print(str(len(self.larger_item_set)) + " larger item_set : ")
        for k_item, v_item in self.larger_item_set.items():
            print(str(k_item) + ' : ' + str(v_item[0]))
        print(' ')

        print(str(len(self.association_rules)) + " association rules : ")
        for k_rule, v_rule in self.association_rules.items():
            print(str(k_rule) + ' : ' + str(v_rule))
        print(' ')

    def dev(self):
        print(self.items)
        print(self.transactions)
        print(self.item_set)
        print(self.item_set_with_value)
        print(self.larger_item_set)
        print(self.association_rules)

    def init_item_set(self):
        self.item_set = [tuple(self.items)]
        for i in range(2, self.len_of_items):
            self.item_set.append(list(itertools.combinations(self.items, i)))

    @staticmethod
    def _count_item(m_item_set, m_transactions, index):
        dict_item_set_temp = {key: [0, index] for key in m_item_set}
        for t in m_transactions:
            # sorting item in transactions
            t.sort()
            for i in m_item_set:
                if index > 0:
                    temp_count = []
                    for sub_item in i:
                        temp_count.append(t.count(sub_item))
                    temp = min(temp_count)
                else:
                    temp = t.count(i)
                dict_item_set_temp[i][0] += temp
        return dict_item_set_temp

    def _count_value_in_item_set(self):
        for m_item in self.item_set:
            self.item_set_with_value.append(self._count_item(m_item, self.transactions, self.item_set.index(m_item)))

    def _calculate_larger_item_set(self):
        for m_item in self.item_set_with_value:
            for k, v in m_item.items():
                v_supp = v[0] / self.len_of_trans
                v_ind = v[1]
                if v_supp >= self.support_threshold:
                    self.larger_item_set[k] = [v_supp, v_ind]

    @staticmethod
    def pattern(item_set):
        n = len(item_set)
        temp_list = []
        for i in range(1, n):
            x = [x_ for x_ in range(i)]
            y = [y_ for y_ in range(i, n)]
            temp_list.append([x, y])
        return temp_list

    def pattern_to_item(self, item_set):
        def_list = []
        pattern = self.pattern(item_set)
        for m_pattern in pattern:
            x_item = []
            y_item = []
            for x in m_pattern[0]:
                x_item.append(item_set[x])
            for y in m_pattern[1]:
                y_item.append(item_set[y])
            def_list.append([x_item, y_item])
        return def_list

    def _create_pattern_of_item_set(self, m_item_set):
        list_temp = []
        list_permutation = list(itertools.permutations(m_item_set, len(m_item_set)))
        for m_item in list_permutation:
            list_temp.append(self.pattern_to_item(m_item))
        return list_temp

    def _create_rules(self, m_item_set):
        list_temp = []
        pattern_item_set = self._create_pattern_of_item_set(m_item_set)

        for m_item in pattern_item_set:
            for iterator in m_item:
                x = sorted(iterator[0])
                y = sorted(iterator[1])
                xy = sorted(iterator[0] + iterator[1])
                value = [self.larger_item_set[self.handling_tuple(xy)][0],
                         self.larger_item_set[self.handling_tuple(xy)][0] / self.larger_item_set[self.handling_tuple(x)][0]]
                list_temp.append([x, y, value])
        return list_temp

    def _association_rules(self):
        for k, v in self.larger_item_set.items():
            v_idx = v[1]
            if v_idx > 0:
                list_temp = self._create_rules(k)
                for item in list_temp:
                    key = self.handling_key(item[0], item[1])
                    value = item[2]
                    if value[0] >= self.support_threshold and value[1] >= self.confidence_threshold:
                        self.association_rules[key] = value

    @staticmethod
    def handling_key(x, y):
        return ', '.join(x) + ' => ' + ', '.join(y)

    @staticmethod
    def handling_tuple(input_list):
        if len(input_list) is 1:
            return tuple(input_list)[0]
        else:
            return tuple(input_list)
