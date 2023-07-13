from typing import List

FRAME_PREFIX = "superDong ---------------->"


class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        mapping = {}
        for i in range(len(s)):
            reverse_mapping = {v: k for k, v in mapping.items()}
            if t[i] in reverse_mapping and reverse_mapping[t[i]] != s[i]:
                return False
            v = mapping.setdefault(s[i], t[i])
            if v != t[i]:
                return False

        return True


# print(Solution().isIsomorphic("egg", "add"))

class Solution392:
    def isSubsequence(self, s: str, t: str) -> bool:
        if not s:
            return True

        if s and not t:
            return False

        if len(s) > len(t):
            return False

        previous = 0
        for item in s:

            if item not in t[previous:]:
                return False

            index = t[previous:].index(item)
            previous += index + 1
        return True

# print(Solution392().isSubsequence('aaaaaa', 'bbaaaa'))

import heapq

def findKthLargest(nums, k):
    min_heap = []
    # [heapq.heappush(min_heap, nums[i]) for i in range(k)]
    # Add the first k elements to the min-heap
    # for i in range(k):
    #     heapq.heappush(min_heap, nums[i])

    # Compare remaining elements with the root of the min-heap
    # for i in range(k, len(nums)):
    #     if nums[i] > min_heap[0]:
    #         heapq.heapreplace(min_heap, nums[i])
    for i in range(len(nums)):
        if i <= k - 1:
            heapq.heappush(min_heap, nums[i])
        elif nums[i] > min_heap[0]:
            heapq.heapreplace(min_heap, nums[i])

    # [heapq.heapreplace(min_heap, nums[i]) for i in range(k, len(nums)) if nums[i] > min_heap[0]]
    # Return the root of the min-heap
    return min_heap[0]

print(findKthLargest([3,2,1,5,6,4], 2))