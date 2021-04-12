from typing import List, Optional


# ================================================= common funcs =======================================================


# selection sort
def selection_sort(src_list):
    minimum = float('inf')
    for i in range(len(src_list) - 1):
        for item in src_list[i:]:
            minimum = min(minimum, item)
        j = src_list.index(minimum)
        src_list[i], src_list[j] = src_list[j], src_list[i]
        minimum = float('inf')
    return src_list


# insert sort
def insertion_sort(src_list):
    src_len = len(src_list)
    for i in range(src_len):
        current = src_list[i]
        animation_pos = i
        while animation_pos > 0 and src_list[animation_pos - 1] > current:
            src_list[animation_pos] = src_list[animation_pos - 1]
            animation_pos -= 1
        src_list[animation_pos] = current
    return src_list


print(insertion_sort([1, 4, 3, 5, 2, 7, 9, 6, 8]))


# ================================================= common funcs =======================================================


# ================================================= 1528. Shuffle String ===============================================

class Solution1528:
    def restoreString(self, s: str, indices: List[int]) -> str:
        ans = [''] * len(s)
        for i in range(len(s)):
            ans[indices[i]] = s[i]
        return ''.join(ans)

# s_src = "codeleet"
# indices_src = [4, 5, 6, 7, 0, 2, 1, 3]
# print(Solution1528().restoreString(s_src, indices_src))
# ================================================= 1528. Shuffle String ===============================================
