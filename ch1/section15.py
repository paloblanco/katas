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
        print("----")
        print(begin)
        print(temp)
        print(end)
    else:
        hanoi(begin, temp, end, n-1)
        hanoi(begin, end, temp, 1)
        hanoi(temp, end, begin, n-1)

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
    main()