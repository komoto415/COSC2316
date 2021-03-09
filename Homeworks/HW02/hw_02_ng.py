from typing import List, Dict, NoReturn, Any
import unittest

# This class contains implementation of an array stack.


class EmptyStackError(Exception):
    """
    Exception raised when performing illegal operations on an empty stack
    """

    def __init__(self):
        super().__init__("Stack is Empty")


class Stack():

    def __init__(self):
        self.stack: List[Any] = []
        self.size: int = 0

    def push(self, item: Any) -> NoReturn:
        self.stack.append(item)
        self.size += 1

    def pop(self) -> Any:
        if (self.size <= 0):
            raise EmptyStackError
        else:
            self.size -= 1
            return self.stack.pop()

    def peek(self) -> Any:
        if (self.size == 0):
            raise EmptyStackError
        else:
            return self.stack[self.size-1]

    def get_size(self) -> int:
        return self.size

    def __str__(self) -> str:
        result: str = "["
        for i, e in enumerate(self.stack):
            result += f"{e}"
            if i != self.get_size() - 1:
                result += ", "
        return result + "]"


class ChangeMaker():

    def __init__(self, denom_list: List[int]):
        """
        Sets the denominations list for how we will make change

        :param denom_list: the desired monetary system
        :type denom_list: List[int]
        :raises AssertionError: if the denom_list contains a negative number
        """
        assert sum(
            n <= 0 for n in denom_list) == 0, f"Cannot have a list of denominations with negative numbers: {denom_list}"

        denom_list = list(set(denom_list))
        denom_list.sort(reverse=True)
        self.__denom_list: List[int] = denom_list

    @property
    def denom_list(self):
        return self.__denom_list

    def make_change(self, change_me: int) -> Dict[int, int]:
        """
        Takes in some integer and will make change with it based on the denominations instantiated with the class

        :param change_me: the desired amount we would like to make change with
        :type change_me: int
        :return: Dict[int, int]
        :raises AssertionError: if attemping to making change for a negative amount
        """
        assert change_me >= 0, f"Cannot make change with negative numbers: {change_me}"

        change: Dict[int, int] = {}
        for denom in self.denom_list:
            count: int = change_me // denom
            change[denom] = count
            change_me -= count * denom
        return change


OPEN_CLOSE_PAIRS: Dict[str, str] = {
    "(": ")",
    "{": "}",
    "[": "]"
}


def balance_check(string: str):
    """
    Takes some string off parentheses, curly brackets and square brackets and checks that every opener is closed by the correct closer

    :param string: some string composite of some amount of closing and/or opening brackets or parentheses
    :type string: str
    :return: bool
    """
    eval_stack: Stack = Stack()
    for char in string:
        if char in OPEN_CLOSE_PAIRS.values():
            try:
                look_behind: str = OPEN_CLOSE_PAIRS.get(eval_stack.peek())
                if char != look_behind:
                    return False
                else:
                    eval_stack.pop()
            except EmptyStackError:
                return False

        else:
            eval_stack.push(char)

    if eval_stack.get_size() == 0:
        return True
    else:
        return False


class AssignmentTest(unittest.TestCase):

    def test_us_change_system(self):
        denom_list: List[int] = [25, 10, 5, 1]
        change_maker: ChangeMaker = ChangeMaker(denom_list=denom_list)
        self.assertNotEqual(change_maker.make_change(10),
                            {25: 0, 10: 0, 5: 2, 1: 0})
        self.assertNotEqual(change_maker.make_change(10),
                            {25: 0, 10: 0, 5: 0, 1: 10})
        self.assertEqual(change_maker.make_change(10),
                         {25: 0, 10: 1, 5: 0, 1: 0})

        self.assertNotEqual(change_maker.make_change(118), {
            25: 0, 10: 11, 5: 1, 1: 3})
        self.assertEqual(change_maker.make_change(118),
                         {25: 4, 10: 1, 5: 1, 1: 3})

    def test_unoptimal_change_system_21_11_7_1(self):
        """
        15  ->  {21:00, 11:01, 07:00, 01:04} act
                    15      4      4      0
                {21:00, 11:00, 07:02, 01:01} opt
                    15      0      1      0    

        """
        denom_list: List[int] = [21, 11, 7, 1]
        change_maker: ChangeMaker = ChangeMaker(denom_list=denom_list)

        optimal: Dict[int, int] = {21: 0, 11: 0, 7: 2, 1: 1}
        actual: Dict[int, int] = change_maker.make_change(15)

        self.assertEqual(actual, {21: 0, 11: 1, 7: 0, 1: 4})

        optimal_count: int = sum(x for x in optimal.values())
        actual_count: int = sum(x for x in actual.values())

        self.assertTrue(optimal_count < actual_count)

    def test_unoptimal_change_system_56_23_11_1(self):
        """
        55  ->  {56:00, 23:02, 11:00, 01:09} act
                    55      9      9      0
            ->  {56:00, 23:00, 11:05, 01:00} opt
                    55     55      0      0
        """
        denom_list: List[int] = [56, 23, 11, 1]
        change_maker: ChangeMaker = ChangeMaker(denom_list=denom_list)

        optimal: Dict[int, int] = {56: 0, 23: 0, 11: 5, 1: 0}
        actual: Dict[int, int] = change_maker.make_change(55)

        self.assertEqual(actual, {56: 0, 23: 2, 11: 0, 1: 9})

        optimal_count: int = sum(x for x in optimal.values())
        actual_count: int = sum(x for x in actual.values())

        self.assertTrue(optimal_count < actual_count)

    def test_balance_check(self):
        self.assertTrue(balance_check("()()"))
        self.assertTrue(balance_check("(())"))
        self.assertTrue(balance_check("([])"))
        self.assertTrue(balance_check("([]{()}){[]}"))
        self.assertTrue(balance_check("({[][]{}})"))

        self.assertFalse(balance_check("())"))
        self.assertFalse(balance_check("((})"))
        self.assertFalse(balance_check("([{]})"))
        self.assertFalse(balance_check("([]()}){[]}"))
        self.assertFalse(balance_check("({[][]{})"))


if __name__ == '__main__':
    unittest.main()
