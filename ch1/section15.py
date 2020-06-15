from typing import TypeVar, Generic, List
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self, name: str = "") -> None:
        self._container: List[T] = []
        self.name = name

    def push(self, item:T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def getList(self) -> List:
        return self._container

    def __repr__(self) -> str:
        return repr(f"{self.name} {self._container}")

def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], n: int) -> None:
    if n == 1:
        end.push(begin.pop())
        # print("----")
        # print(begin)
        # print(temp)
        # print(end)
    else:
        hanoi(begin, temp, end, n-1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n-1)


def multi_hanoi(towers: List[Stack[int]], n: int) -> None:
    if n == 1:
        towers[1].push(towers[0].pop())

    else:
        #hanoi(begin, temp, end, n-1)
        mid_list = towers[2:]
        towers_rotate = towers[0:1] + mid_list + towers[1:2]
        multi_hanoi(towers_rotate, n-1)
        
        #hanoi(begin, end, temp, 1)
        multi_hanoi(towers, 1)

        #hanoi(temp, end, begin, n-1)
        towers_rotate = towers[2:3] + towers[1:2] + towers[3:] + towers[0:1]
        multi_hanoi(towers_rotate, n-1)

def test_hanoi():
    num_discs: int = 5
    tower_a: Stack[int] = Stack("A")
    tower_b: Stack[int] = Stack("B")
    tower_c: Stack[int] = Stack("C")
    for i in range(1, num_discs + 1):
        tower_a.push(i)
    hanoi(tower_a, tower_c, tower_b, num_discs)
    assert tower_c.getList() == [1,2,3,4,5]

def test_multi_hanoi_vs_old():
    num_discs: int = 5
    num_towers: int = 3
    list_towers: list = []
    for i in range(num_towers):
        tower: Stack[int] = Stack(str(i))
        list_towers.append(tower)
    for i in range(1, num_discs + 1):
        list_towers[0].push(i)
    multi_hanoi(list_towers, num_discs)
    assert list_towers[1].getList() == [1,2,3,4,5]

def test_multi_hanoi():
    num_discs: int = 15
    num_towers: int = 5
    list_towers: list = []
    for i in range(num_towers):
        tower: Stack[int] = Stack(str(i))
        list_towers.append(tower)
    for i in range(1, num_discs + 1):
        list_towers[0].push(i)
    multi_hanoi(list_towers, num_discs)
    assert list_towers[1].getList() == list(range(1,num_discs + 1))

def main() -> None:
    num_discs: int = 5
    tower_a: Stack[int] = Stack("A")
    tower_b: Stack[int] = Stack("B")
    tower_c: Stack[int] = Stack("C")
    for i in range(1, num_discs + 1):
        tower_a.push(i)
    print("====Start====")
    print(f"Tower A: {tower_a}")
    print(f"Tower B: {tower_b}")
    print(f"Tower C: {tower_c}")
    hanoi(tower_a, tower_c, tower_b, num_discs)
    print("====End====")
    print(f"Tower A: {tower_a}")
    print(f"Tower B: {tower_b}")
    print(f"Tower C: {tower_c}")


def test_Stack_push():
    items_to_push = [1,2]
    stack = Stack()
    assert stack.getList() == []
    stack.push(1)
    assert stack.getList() == [1]
    stack.push(2)
    assert stack.getList() == items_to_push

def test_Stack_pop():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    assert stack.getList() == [1]




if __name__ == "__main__":
    test_Stack_push()
    test_Stack_pop()
    test_hanoi()
    test_multi_hanoi_vs_old()
    test_multi_hanoi()
    main()