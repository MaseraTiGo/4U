# conding: utf-8

def product_model(prefix_list, suffix_list):
    result_list = []
    for prefix in prefix_list:
        for suffix in suffix_list:
            result_list.append(prefix + suffix)
    return result_list
temp = []
prefix_list = ['a', 'b', 'c', 'd']
suffix_list = ['A', 'B', 'C', 'D']
[[prefix+suffix for suffix in suffix_list] for prefix in prefix_list]
