#非空链表相加，每位数字逆序存储。每个节点存储一位数字。

#请你将两个数相加，并以相同形式返回一个表示和的链表。
#你可以假设除了数字 0 之外，这两个数都不会以 0 开头。

#输入：l1 = [2,4,3], l2 = [5,6,4]
#输出：[7,0,8]
#解释：342 + 465 = 807.（逆序）

#2+5=7 6+4=0 carry 1 3+4+1（carry）=8

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        carry = 0
        root = ListNode(0)
        current = root
        
        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0
            
            sum_value = val1 + val2 + carry            
            
            carry = sum_value // 10
            sum_value = sum_value % 10
            
            current.next = ListNode(sum_value)
            current = current.next
            
            l1 = l1.next if l1 else None 
            l2 = l2.next if l2 else None    
            
        return root.next



# 这个算法的思路是:
# 1. 首先定义一个carry表示进位, root指向新的结果链表的头节点。
# 2. 然后遍历l1和l2两个链表,获取节点值相加,如果其中一个链表已经遍历完成则其值为0。
# 3. 计算val1 + val2 + carry,得到总和sum_value。
# 4. sum_value的进位carry为总和除10的商,个位数为总和%10。
# 5. 将个位数作为新节点的值,插入到结果链表中。
# 6. l1和l2后移,继续计算并插入新节点,直至两个链表都遍历完且进位为0。
# 7. 返回result的下一个节点,即结果链表的头节点。
