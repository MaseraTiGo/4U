# binary search
from typing import List, Union


def binary_search(data: List[int], target: Union[int, float] = None) -> bool:
    if not data or target is None:
        return False

    mid = len(data) // 2
    mid_value = data[mid]
    if mid_value == target:
        return True
    if mid_value < target:
        return binary_search(data[mid + 1:], target=target)
    else:
        return binary_search(data[:mid], target=target)


def pop_sort(data: List[int]) -> List[int]:
    len_ = len(data)
    for i in range(len_-1):
        for j in range(i + 1, len_):
            if data[i] > data[j]:
                data[i], data[j] = data[j], data[i]

    print(data)
    return data


if __name__ == '__main__':
    # test_data = list(range(10))
    #
    # print(binary_search(test_data, target=9))

    # pop sort
    test_data = [3, 6, 1, 9, 3, 7, 5]
    # pop_sort(test_data)