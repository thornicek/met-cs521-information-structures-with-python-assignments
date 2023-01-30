#Tomas Hornicek, no collaborators, geeksforgeeks.org, no extension

#Problem 4
class Node:
    def __init__(self,value,prev,next):
        self.value = value
        self.prev = prev
        self.next = next

    def get_prev(self):
        return self.prev

    def get_next(self):
        return self.next

    def get_value(self):
        return self.value

    def set_prev(self,node):
        self.prev = node

    def set_next(self,node):
        self.next = node

    def set_value(self,val):
        self.value = val


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    #Function to add a node to the end of the DoubleLL
    def add_to_end(self,val):
        #Get reference to original tail
        current_tail = self.tail
        #Define new end node
        end_node = Node(val,current_tail,None)
        #Account for an empty Doubly LL
        if current_tail is None:
            self.head = end_node
            self.tail = end_node
            return
        #Set the pointer of the original end node to the new end node
        current_tail.next = end_node
        #Set the Double LL tail to the new end node
        self.tail = end_node

    def add_to_front(self,val):
        #Get reference to original head
        current_head = self.head
        #Define new head node
        first_node = Node(val,None,current_head)
        #Account for an empty Double LL
        if current_head is None:
            self.head = first_node
            self.tail = first_node
            return
        #Set the pointer of the new head node to the original head node
        current_head.prev = first_node
        #Set the Double LL head to the new head node
        self.head = first_node


    def delete(self, val):
        #Set current node to head node, this will serve as the beginning for iteration
        current_node = self.head
        #While loop that iterates through the length of the Double LL
        while current_node is not None:
            #Check if current node has given value
            if current_node.value == val:
                #Get preceding node
                previous_node = current_node.prev
                #Get following node
                next_node = current_node.next
                #Set the pointer of the deleted node to None for garbage collection
                current_node.prev = None
                current_node.next = None
                #Set the pointer of the preceding node to the following node
                previous_node.next = next_node
                #Set the pointer of the following node to the preceding node
                next_node.prev = previous_node
                #If node deleted then break out of the while loop
                break
            # Continue iteration
            else:
                current_node = current_node.next


    def reverse(self):
        current_head = self.head
        current_tail = self.tail
        current_node = self.head
        #Iterate through the Double LL and reverse the pointers
        while current_node is not None:
            previous_node = current_node.prev
            next_node = current_node.next
            current_node.next = previous_node
            current_node.prev = next_node
            current_node = next_node
        #Set the original head to be tail and vice versa
        self.head = current_tail
        self.tail = current_head

    def compare(self,lst):
        current_node = self.head
        i = 0
        #Iterate through the Double LL
        while current_node is not None:
            #Check if the size of the list is the same as Double LL
            if i >= len(lst):
                return False
            #Check if the value is in the list
            if current_node.value != lst[i]:
                return False
            else:
                #Continue iteration
                current_node = current_node.next
                i += 1
        return True

    def find(self,val):
        current_node = self.head
        i = 0
        #Iterate through Double LL
        while current_node is not None:
            #Check if the value is in the Double LL, if true return the index
            if val == current_node.value:
                return i
            i += 1
            current_node = current_node.next

#Problem 5

def merge_sort(lst):
    if len(lst) > 1:

        # Finding the midpoint of the list, use integer division to get integer as result
        mid = len(lst) // 2

        # Get left half of the list
        left_half = lst[:mid]

        # Get right half of the list
        right_half = lst[mid:]

        # Sorting the left half recursively
        merge_sort(left_half)

        # Sorting the right half recursively
        merge_sort(right_half)

        i = 0
        j = 0
        k = 0

        # Merge left and right halves of the list
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                lst[k] = left_half[i]
                i += 1
            else:
                lst[k] = right_half[j]
                j += 1
            k += 1

        # Account for odd length of the sub list
        while i < len(left_half):
            lst[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            lst[k] = right_half[j]
            j += 1
            k += 1
        return lst


def test_merge_sort():
    test_list = [34, 23, 1, 63, 45, 20, 2]
    result = merge_sort(test_list)
    print(result)
    print("Expected result: [1, 2, 20, 23, 34, 45, 63]")
test_merge_sort()

#Problem 6

def lst_to_dict(lst, start, end):
    """
    Given an unsorted list of integers, and two integers denoting a range - 'start' and 'end',
    create a dictionary whose keys are all the integers in the given range (inclusive) and whose values
    are the indices of those numbers if the numbers are in the list, or None otherwise.
    The proposed time complexity is O(n + nlog(n) + n + n), simplifying to O(nlog(n)).

    :param lst: list of unsorted integers
    :param start: integer denoting start of range
    :param end: integer denoting end of range
    :return: dict with numbers in range as keys and indices or None as values.
    """
    original_index_dict = {}
    result_dict = {}
    # Save original indices into dict - O(n)
    for index,value in enumerate(lst):
        original_index_dict[value] = index
    # Sort list - O(nlog(n))
    lst.sort()
    index = 0
    # iterate over whole list - O(n)
    while index < len(lst) - 1:
        current_element = lst[index]
        next_element = lst[index + 1]
        if current_element > end:
            break
        if current_element < start:
            if next_element > start:
                for k in range(start, next_element):
                    result_dict[k] = None
            index += 1
            continue
        result_dict[current_element] = index
        # iterate over 'gap' between current element and next element of the list.
        # for example if current element is 8 and next element is 12, iterate over 8 to 11.
        # this does not really depend on the size of the input list - O(1)
        for j in range(current_element + 1, next_element + 1):
            if j > end:
                break
            result_dict[j] = None
        # If we are on last iteration, and last element of list is less than end, we need to add None for
        # numbers between last element of list and end
        if index == len(lst) - 2:
            for j in range(next_element, end + 1):
                if j > end:
                    break
                result_dict[j] = None
            # if the last element in the list is less than end, add its index (previous for loop set it to None).
            if next_element <= end:
                result_dict[next_element] = index
        index += 1
    # 'translate' back to orignal indices, because indices were changed by sorting - O(n)
    for key in original_index_dict:
        if result_dict.get(key) is not None:
            result_dict[key] = original_index_dict[key]
    return result_dict

#Problem7

def target_sum(lst, target):
    """
    Given a list of integers and a target number, find whether there are two numbers in the list which
    add up to the given target number and return their indices.
    Proposed time complexity: O(n).
    :param lst: list of integers
    :param target: target number to which two numbers in the list should add up to
    :return: Two integer tuple with indices of the numbers which sum to target. Smaller index first.
    """
    lst_dict = {}
    # Put all numbers in list and their indices into dict
    for index, value in enumerate(lst):
        lst_dict[value] = index
    mid = target // 2
    # Loop over all numbers from 0 up to target / 2. The idea is to check the dict for all
    # possible combinations of numbers which add up to target. For example if target is 7,
    # we will check whether 0 and 7 are in the list on the first iteration, then 6 and 1 on the
    # second iteration, then 5 and 2 and so on.
    for i in range(mid + 1):
        small = i
        big = target - i
        small_index = lst_dict.get(small)
        big_index = lst_dict.get(big)
        if small_index is not None and big_index is not None:
            if small_index > big_index:
                return big_index, small_index
            else:
                return small_index, big_index

#Test the target_sum function
def target_sum_test():
    test_list = [1,2,3,5,9,15]
    target = 7
    result = target_sum(test_list,target)
    print(result)

target_sum_test()



