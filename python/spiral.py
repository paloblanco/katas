class Spiral():
    def __init__(self, size):
        self.size = size
        self._build_spiral()
            
    def get(self):
        return self.spiral
    
    def _build_spiral(self):
        self.spiral = [[1 for _ in range(self.size)] for _ in range(self.size)]
        self._coords = {
        "row": 1,
        "column":0
        }
        self.spiral[self._coords["row"]][self._coords["column"]] = 0 #hard code first step
        self._delta_row = 0 #direction to move in y
        self._delta_column = 1 #direction to move in x
        self._done_spiral = False
        while not self._done_spiral:
            self._step_spiral()
    
    def _step_spiral(self):
        coords_next = {
            "row":self._coords["row"] + self._delta_row,
            "column":self._coords['column'] + self._delta_column
        }
        turn = True
        # have i finished?
        if self.spiral[coords_next["row"]][coords_next["column"]] == 0:
            self._done_spiral = True
        # do i need to turn?
        
        elif (-1 < coords_next["row"]+self._delta_row < self.size) and (-1 < coords_next["column"]+self._delta_column < self.size):
            if self.spiral[coords_next["row"]+self._delta_row][coords_next['column']+self._delta_column] == 1:
                turn = False
                self.spiral[coords_next['row']][coords_next['column']] = 0
                self._coords = coords_next
        if turn:
            if self._delta_row == 1:
                self._delta_row = 0
                self._delta_column = -1
            elif self._delta_row == -1:
                self._delta_row = 0
                self._delta_column = 1
            elif self._delta_column == 1:
                self._delta_row = 1
                self._delta_column = 0
            elif self._delta_column == -1:
                self._delta_row = -1
                self._delta_column = 0


def spiralize(size):
    spiral = Spiral(size)
    return spiral.get()
 

if __name__ == "__main__":
    assert spiralize(5) == [[1,1,1,1,1],
                            [0,0,0,0,1],
                            [1,1,1,0,1],
                            [1,0,0,0,1],
                            [1,1,1,1,1]]
    assert spiralize(8) == [[1,1,1,1,1,1,1,1],
                            [0,0,0,0,0,0,0,1],
                            [1,1,1,1,1,1,0,1],
                            [1,0,0,0,0,1,0,1],
                            [1,0,1,0,0,1,0,1],
                            [1,0,1,1,1,1,0,1],
                            [1,0,0,0,0,0,0,1],
                            [1,1,1,1,1,1,1,1]]