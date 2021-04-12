from typing import List, Optional


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
