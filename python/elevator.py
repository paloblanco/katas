"""
x 3

I bet you won't ever catch a Lift (a.k.a. elevator) again without thinking of this Kata !

Synopsis
A multi-floor building has a Lift in it.

People are queued on different floors waiting for the Lift.

Some people want to go up. Some people want to go down.

The floor they want to go to is represented by a number (i.e. when they enter the Lift this is the button they will press)

BEFORE (people waiting in queues)               AFTER (people at their destinations)
                   +--+                                          +--+ 
  /----------------|  |----------------\        /----------------|  |----------------\
10|                |  | 1,4,3,2        |      10|             10 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 9|                |  | 1,10,2         |       9|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 8|                |  |                |       8|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 7|                |  | 3,6,4,5,6      |       7|                |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 6|                |  |                |       6|          6,6,6 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 5|                |  |                |       5|            5,5 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 4|                |  | 0,0,0          |       4|          4,4,4 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 3|                |  |                |       3|            3,3 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 2|                |  | 4              |       2|          2,2,2 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 1|                |  | 6,5,2          |       1|            1,1 |  |                |
  |----------------|  |----------------|        |----------------|  |----------------|
 G|                |  |                |       G|          0,0,0 |  |                |
  |====================================|        |====================================|
Rules
Lift Rules
The Lift only goes up or down!
Each floor has both UP and DOWN Lift-call buttons (except top and ground floors which have only DOWN and UP respectively)
The Lift never changes direction until there are no more people wanting to get on/off in the direction it is already travelling
When empty the Lift tries to be smart. For example,
If it was going up then it may continue up to collect the highest floor person wanting to go down
If it was going down then it may continue down to collect the lowest floor person wanting to go up
The Lift has a maximum capacity of people
When called, the Lift will stop at a floor even if it is full, although unless somebody gets off nobody else can get on!
If the lift is empty, and no people are waiting, then it will return to the ground floor
People Rules
People are in "queues" that represent their order of arrival to wait for the Lift
All people can press the UP/DOWN Lift-call buttons
Only people going the same direction as the Lift may enter it
Entry is according to the "queue" order, but those unable to enter do not block those behind them that can
If a person is unable to enter a full Lift, they will press the UP/DOWN Lift-call button again after it has departed without them
Kata Task
Get all the people to the floors they want to go to while obeying the Lift rules and the People rules
Return a list of all floors that the Lift stopped at (in the order visited!)
NOTE: The Lift always starts on the ground floor (and people waiting on the ground floor may enter immediately)

I/O
Input
queues a list of queues of people for all floors of the building.
The height of the building varies
0 = the ground floor
Not all floors have queues
Queue index [0] is the "head" of the queue
Numbers indicate which floor the person wants go to
capacity maximum number of people allowed in the lift
Parameter validation - All input parameters can be assumed OK. No need to check for things like:

People wanting to go to floors that do not exist
People wanting to take the Lift to the floor they are already on
Buildings with < 2 floors
Basements
Output
A list of all floors that the Lift stopped at (in the order visited!)
Example
Refer to the example test cases.

Language Notes
Python : The object will be initialized for you in the tests
"""

from collections import deque

class Dinglemouse(object):

    def __init__(self, queues, capacity):
        self.cap = capacity
        self.floors = len(queues)
        self.answer = []
        self.current_floor = 0
        self.lift = [] # holds passengers
        self.building = []
        for i,floor in enumerate(queues):
            going_up = deque([each for each in floor if each > i])
            going_down = deque([each for each in floor if each < i])
            done = [each for each in floor if each == i]
            self.building.append([going_up,going_down,done])
        self.direction = "up"
        
    def theLift(self):
        self.answer.append(0) # ground floor start
        self._unload_and_load() # in case someone is waiting on 0
        while self.people_are_waiting or self.people_are_on_lift:
            # print(self)
            if self.direction == "up":
                next_floor = self._get_next_floor_up()
                if next_floor:
                    self.current_floor = next_floor
                    self._unload_and_load()
                    self.answer.append(self.current_floor)
                else:
                    self.direction = "down"
                    self._unload_and_load()
            elif self.direction == "down":
                next_floor = self._get_next_floor_down()
                if next_floor >= 0:
                    self.current_floor = next_floor
                    self._unload_and_load()
                    self.answer.append(self.current_floor)
                else:
                    self.direction = "up"
                    self._unload_and_load()
        if self.current_floor != 0:
            self.answer.append(0) # ground floor end
        return self.answer

    def repr(self):
        my_str = f"""\
======
Lift riders: {self.lift}
Direction: {self.direction}
Floor: {self.current_floor}
Answer: {self.answer}"""
        return my_str
    
    def __str__(self):
        return self.repr()

    def __repr__(self):
        return self.repr()

    def _unload_and_load(self):
        # unload passengers
        liftcopy = self.lift.copy()
        for p in liftcopy:
            if p == self.current_floor:
                self.lift.remove(p)
                self.building[p][2].append(p)
        # which queue will people load from?
        if self.direction == "up": 
            line = 0
        elif self.direction == "down":
            line = 1
        # load passengers
        while (len(self.lift) < self.cap) and (len(self.building[self.current_floor][line]) > 0):
            p = self.building[self.current_floor][line].popleft()
            self.lift.append(p)

    def _get_next_floor_down(self):
        next_floor = -1 # initial spoof value
        # check lift riders
        riders_going_down = [each for each in self.lift if each < self.current_floor]
        next_floor = max(riders_going_down + [next_floor])
        # check waiters who want to go down IF THERE IS ROOM
        # if len(self.lift) < self.cap:
        floors_with_people_going_down = [i for i in range(len(self.building)) if ((i < self.current_floor) and (len(self.building[i][1]) > 0))]
        next_floor = max(floors_with_people_going_down + [next_floor])
        # check the lowest floor with someone going up IF NOTHING ELSE
        if next_floor == -1:
            floors_with_people_going_up = [i for i in range(len(self.building)) if ((i < self.current_floor) and (len(self.building[i][0]) > 0))]
            if len(floors_with_people_going_up) > 0:
                highest_floor_up = min(floors_with_people_going_up)
                next_floor = max(highest_floor_up,next_floor)
        return next_floor
        
    def _get_next_floor_up(self):
        next_floor = self.floors # initial spoof value
        # check lift riders
        riders_going_up = [each for each in self.lift if each > self.current_floor]
        next_floor = min(riders_going_up + [next_floor])
        # check waiters who want to go up IF THERE IS ROOM
        # if len(self.lift) < self.cap:
        floors_with_people_going_up = [i for i in range(len(self.building)) if ((i > self.current_floor) and (len(self.building[i][0]) > 0))]
        next_floor = min(floors_with_people_going_up + [next_floor])
        # check the highest floor with someone going down IF NOTHING ELSE
        if next_floor == self.floors:
            floors_with_people_going_down = [i for i in range(len(self.building)) if ((i > self.current_floor) and (len(self.building[i][1]) > 0))]
            if len(floors_with_people_going_down) > 0:
                highest_floor_down = max(floors_with_people_going_down)
                next_floor = min(highest_floor_down,next_floor)
        if next_floor > self.floors-1: 
            return False
        else: 
            return next_floor

    @property
    def people_are_waiting(self):
        people = sum([len(each[0])+len(each[1]) for each in self.building])
        return people > 0

    @property
    def people_are_on_lift(self):
        return len(self.lift) > 0

if __name__ == "__main__":
    # Floors:    G     1      2        3     4      5      6         Answers:
    tests = [[ ( (),   (),    (5,5,5,5,5), (),   (),    (),    () ),     [0, 2, 5, 0]          ],
            [ ( (),   (),    (1,1),   (),   (),    (),    () ),     [0, 2, 1, 0]          ],
            [ ( (),   (3,),  (4,),    (),   (5,),  (),    () ),     [0, 1, 2, 3, 4, 5, 0] ],
            [ ( (),   (0,),  (),      (),   (2,),  (3,),  () ),     [0, 5, 4, 3, 2, 1, 0] ]]
    
    for queues, answer in tests:
        lift = Dinglemouse(queues, 5)
        aa = lift.theLift()
        assert aa == answer, f"{lift.theLift()} is not {answer}"
        print("Answer: ",aa)
    
    