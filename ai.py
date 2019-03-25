import itertools


class Searcher(object):

    # 初始化
    def __init__(self, width, hight):
        self.col_num = width
        self.row_num = hight

    O = 'O'
    X = 'X'
    B = '-'  # 代表空白
    OX_LIST = [O, X]
    FIX_WRONG_01 = 'XXX'
    FIX_WRONG_02 = 'OOO'

    def show(self, note, data):
        print(note)
        for i in range(self.row_num):
            for j in range(self.col_num):
                print(data[i][j]+' ', end='')
            print()
        print()

    def reverse(self, char):
        if char == self.O:
            return self.X
        elif char == self.X:
            return self.O
        else:
            return self.B

    FIX_S01 = ('-XX-', 'OXXO')
    FIX_S02 = ('XX-', 'XXO')
    FIX_S03 = ('-XX', 'OXX')
    FIX_S04 = ('-OO-', 'XOOX')
    FIX_S05 = ('OO-', 'OOX')
    FIX_S06 = ('-OO', 'XOO')
    FIX_S07 = ('X-X', 'XOX')
    FIX_S08 = ('O-O', 'OXO')
    FIX_GS = (FIX_S01, FIX_S02, FIX_S03, FIX_S04, FIX_S05, FIX_S06, FIX_S07, FIX_S08)

    def _search_string(self, data):
        _fish_got = False
        # 最简单的直接替换
        for fix_s in self.FIX_GS:
            if data.find(fix_s[0]) != -1:
                _fish_got = True
                data = data.replace(fix_s[0], fix_s[1])
        if _fish_got:
            self._search_string(data)
        return data

    # 继续试错，规则是：如果指定一个空白处为X，导致后面的推论都错了，那必定是O，反之亦然
    # 如：- - O X O X X O X -
    # 第一个空白为X，都不能证明后面错，说明试错没用，继而使用O，也不能证明后面不行
    # 第二个也不行，但最后一个可以证明，如果是X，会导致三个O，说明不行，只能是O
    # 判断失败规则：1.不能三个重复 2.数量必须相等 3.有相同的行或列
    def _try_wrong_(self, data, width_or_hight, complete_list):
        blank_list = []
        i = 0
        data_init = data
        for s in data:
            if s == self.B:
                blank_list.append(i)
            i = i + 1
        blank_count = len(blank_list)
        all_ox = ''
        if blank_count >= 1:
            all_ox = self._combination_(blank_count-1)
        # print(all_ox)
        # print('blank_list:', blank_list)
        for idx in blank_list:
            blank_list2 = self._copy_blank_list(blank_list)
            blank_list2.remove(idx)
            data = self._try_one_blank_(data, idx, all_ox, blank_list2, width_or_hight, complete_list)
        if data_init != data:
            self._try_wrong_(data, width_or_hight, complete_list)
        return data

    def _copy_blank_list(self, blank_list):
        blank_list2 = []
        for blank in blank_list:
            blank_list2.append(blank)
        return blank_list2

    def _try_one_blank_(self, data, idx, all_ox, blank_list, num, complete_list):
        for try_char in self.OX_LIST:
            # print('try_char:', try_char)
            # print('data:', data)
            # print('idx:', idx)
            all_result_is_right = False
            cal_data = data
            for one_ox in all_ox:
                order_list = self._order_str_(blank_list, one_ox, idx, try_char)
                mix_data = self._mix_(cal_data, order_list)
                if self._validate_num_(mix_data, num) and not self._validata_same_(mix_data, complete_list):
                    all_result_is_right = True
                    break
            # 没有一个正确，需要反过来，试错成功
            if not all_result_is_right:
                return self._replace_char_(data, idx, self.reverse(try_char))
        return data

    # 返回顺序和字母的对应表
    def _order_str_(self, blank_list, one_ox, idx, try_char):
        order_list = []
        order_list.append([idx, try_char])
        i = 0
        for one in one_ox:
            order_list.append([blank_list[i], one])
            i = i + 1
        return order_list

    def _mix_(self, data, order_list):
        new_data = data
        for order in order_list:
            new_data = self._replace_char_(new_data, order[0], order[1])
        return new_data

    def _replace_char_(self, str, index, char):
        new_str = list(str)
        new_str[index] = char
        return ''.join(new_str)

    def _combination_(self, num):
        # print('num:', num)
        return list(itertools.product(self.OX_LIST, repeat=num))

    def _validate_num_(self, data, num):
        return data.find(self.FIX_WRONG_01) == -1 and data.find(self.FIX_WRONG_02) == -1 \
               and data.count(self.O) <= num/2 and data.count(self.X) <= num/2

    def _validata_same_(self, data, complete_list):
        for one in complete_list:
            if one == data:
                return True
        return False

    def _validate_ok_(self, arr_data):
        for i in range(self.row_num):
            str = ''
            str = str.join(arr_data[i])
            if str.count(self.B) > 0:
                return False
        return True

    def _complete_rows(self, arr_data):
        rows_list = []
        for i in range(self.row_num):
            str = ''
            str = str.join(arr_data[i])
            if str.find(self.B) == -1:
                rows_list.append(str)
        return rows_list

    def _complete_cols(self, arr_data):
        cols_list = []
        for i in range(self.col_num):
            str = ''
            for j in range(self.row_num):
                str = str + arr_data[j][i]
            if str.find(self.B) == -1:
                cols_list.append(str)
        return cols_list

    def _search_row(self, arr_data):
        fish_got = False
        for i in range(self.row_num):
            str = ''
            str = str.join(arr_data[i])
            str2 = str
            # print("1:", str)
            str = self._search_string(str)
            # print("2:", str)
            if str2 != str:
                fish_got = True
                k = 0
                for x in str:
                    arr_data[i][k] = x
                    k = k + 1
        if fish_got:
            self._search_col(arr_data)

    def _search_col(self, arr_data):
        fish_got = False
        for i in range(self.col_num):
            str = ''
            for j in range(self.row_num):
                str = str + arr_data[j][i]
            str2 = str
            # print("3:", str)
            str = self._search_string(str)
            # print("4:", str)
            if str2 != str:
                fish_got = True
                k = 0
                for x in str:
                    arr_data[k][i] = x
                    k = k + 1
        if fish_got:
            self._search_row(arr_data)

    def _search_row_update(self, arr_data):
        fish_got = False
        complete_list = self._complete_rows(arr_data)
        for i in range(self.row_num):
            str = ''
            str = str.join(arr_data[i])
            str2 = str
            # print("1:", str)
            str = self._try_wrong_(str, self.col_num, complete_list)
            # print("2:", str)
            if str2 != str:
                fish_got = True
                k = 0
                for x in str:
                    arr_data[i][k] = x
                    k = k + 1
        if fish_got:
            self._search_col_update(arr_data)

    def _search_col_update(self, arr_data):
        fish_got = False
        complete_list = self._complete_cols(arr_data)
        for i in range(self.col_num):
            str = ''
            for j in range(self.row_num):
                str = str + arr_data[j][i]
            str2 = str
            # print("3:", str)
            str = self._try_wrong_(str, self.row_num, complete_list)
            # print("4:", str)
            if str2 != str:
                fish_got = True
                k = 0
                for x in str:
                    arr_data[k][i] = x
                    k = k + 1
        if fish_got:
            self._search_row_update(arr_data)

    def search(self, arr_data):
        self.show('before:', arr_data)
        done = False
        for i in range(3):
            self._search_row(arr_data)
            self._search_col(arr_data)
            self._search_row_update(arr_data)
            self._search_col_update(arr_data)
            if self._validate_ok_(arr_data):
                print('循环次数：', i)
                self.show('done:', arr_data)
                done = True
                break
        if not done:
            self.show('fail:', arr_data)


if __name__ == '__main__':
    # data = '--OXOXXOX-'
    # data = '-XOXO--X'
    data = 'OXOX-O'
    #print('old:', data)
    searcher = Searcher(6, 6)
    # print('new:', searcher._try_wrong_(data, 6))
    print('order:', searcher._order_str_([1, 5, 6], 'XOX', 2, 'O'))

