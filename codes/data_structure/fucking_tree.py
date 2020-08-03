# -*- coding: utf-8 -*-
# file_name       : fucking_tree.py
# file_func       :
# file_author     : 'Johnathan.Wick'
# file_create_date: 2020/8/2 8:51


class MyNode(object):
    def __init__(self, value, l_node=None, r_node=None):
        self.value = value
        self.l_node = l_node
        self.r_node = r_node


my_tree = MyNode(1, MyNode(2, MyNode(4), MyNode(5)), MyNode(3, MyNode(6), MyNode(7)))


def df(node: MyNode):
    if node:
        yield from df(node.l_node)
        yield node.value
        yield from df(node.r_node)


def bf(node: MyNode):
    temp_list = [node]
    while temp_list:
        cur_n = temp_list.pop(0)
        yield cur_n.value if cur_n else 'Null'
        if not cur_n:
            continue
        if cur_n.l_node:
            temp_list.append(cur_n.l_node)
        if cur_n.l_node and not cur_n.r_node:
            temp_list.append(None)
        if not cur_n.l_node and cur_n.r_node:
            temp_list.append(None)
            temp_list.append(cur_n.r_node)
            continue
        if cur_n.l_node and cur_n.r_node:
            temp_list.append(cur_n.r_node)


class IterateMethod(object):
    DF = 'df'
    BF = 'bf'


def generate_binary_tree(data: list, method=IterateMethod.DF, order='left'):
    def get_node(cur_data):
        return MyNode(cur_data[len(cur_data) // 2]) if len(cur_data) else None

    def df_left(cur_root, df_data):
        if not df_data:
            return
        l_data = df_data[:len(df_data) // 2]
        r_data = df_data[len(df_data) // 2 + 1:]

        cur_root.l_node = get_node(l_data)
        df_left(cur_root.l_node, l_data)

        cur_root.r_node = get_node(r_data)
        df_left(cur_root.r_node, r_data)

    def df_right():
        pass

    def df_mid():
        pass

    def bf_inner():
        root = MyNode(data.pop(0))
        root_list = [root]
        while root_list:
            cur_root = root_list.pop(0)
            if not cur_root:
                continue
            if not data:
                break
            cur_value = data.pop(0)
            cur_root.l_node = MyNode(cur_value) if cur_value is not None else None
            root_list.append(cur_root.l_node)
            cur_value = data.pop(0)
            cur_root.r_node = MyNode(cur_value) if cur_value is not None else None
            root_list.append(cur_root.r_node)
        return root

    if not data:
        return None

    if method == 'df':

        if order == 'left':

            root_df_left = get_node(data)
            df_left(root_df_left, data)
            return root_df_left
        elif order == 'right':
            df_right()
        elif order == 'mid':
            df_mid()
        else:
            raise Exception(f"{method}: input method of ordering: {order} not support")
    else:
        return bf_inner()


tree_one = generate_binary_tree([4, 2, 5, 1, 6, 3, 7], method=IterateMethod.DF, order='left')
for i in bf(tree_one):
    print(i)
