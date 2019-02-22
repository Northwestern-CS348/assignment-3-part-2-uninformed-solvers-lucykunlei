from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        ask1 = parse_input("fact: (on ?disk peg1)")
        ask2 = parse_input("fact: (on ?disk peg2)")
        ask3 = parse_input("fact: (on ?disk peg3)")

        peg1Bindings = self.kb.kb_ask(ask1)
        peg2Bindings = self.kb.kb_ask(ask2)
        peg3Bindings = self.kb.kb_ask(ask3)

        if peg1Bindings == False:
            disksOnPeg1 = []
        else:
            disksOnPeg1 = []
            for peg1binding in peg1Bindings:
                disksOnPeg1.append(int(str(peg1binding)[-1]))
                disksOnPeg1.sort()

        if peg2Bindings == False:
            disksOnPeg2 = []
        else:
            disksOnPeg2 = []
            for peg2binding in peg2Bindings:
                disksOnPeg2.append(int(str(peg2binding)[-1]))
                disksOnPeg2.sort()

        if peg3Bindings == False:
            disksOnPeg3 = []
        else:
            disksOnPeg3 = []
            for peg3binding in peg3Bindings:
                disksOnPeg3.append(int(str(peg3binding)[-1]))
                disksOnPeg3.sort()
        
        resultTuple = []
        resultTuple.append(tuple(disksOnPeg1))
        resultTuple.append(tuple(disksOnPeg2))
        resultTuple.append(tuple(disksOnPeg3))

        return tuple(resultTuple)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        retract_facts = []
        assert_facts = []
        
        sl = list(map(lambda x: str(x), movable_statement.terms))
        retract_facts.append(parse_input('fact: (on '+sl[0]+' '+sl[1]+')'))
        assert_facts.append(parse_input('fact: (on '+sl[0]+' '+sl[2]+')'))
        retract_facts.append(parse_input('fact: (topof '+sl[0]+' '+sl[1]+')'))
    
        answer = self.kb.kb_ask(parse_input('fact: (topof ?disk '+sl[2]+')'))
        if not answer: # there is no disk on the desination peg
            retract_facts.append(parse_input('fact: (empty '+sl[2]+')'))
            assert_facts.append(parse_input('fact: (topof '+sl[0]+' '+sl[2]+')'))
        else:
            retract_facts.append(parse_input('fact: (topof '+answer[0]['?disk']+' '+sl[2]+')'))
            assert_facts.append(parse_input('fact: (topof '+sl[0]+' '+sl[2]+')'))
            assert_facts.append(parse_input('fact: (ondisk '+sl[0]+' '+answer[0]['?disk']+')'))

        answer = self.kb.kb_ask(parse_input('fact: (ondisk '+sl[0]+' ?disk)'))
        if not answer:
            assert_facts.append(parse_input('fact: (empty '+sl[1]+')'))
        else:
            retract_facts.append(parse_input('fact: (ondisk '+sl[0]+' '+answer[0]['?disk']+')'))
            assert_facts.append(parse_input('fact: (topof '+answer[0]['?disk']+' '+sl[1]+')'))
                
        for fact in retract_facts:
            self.kb.kb_retract(fact)
        for fact in assert_facts:
            self.kb.kb_assert(fact)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        ask11 = parse_input("fact: (at ?tile pos1 pos1)")
        ask12 = parse_input("fact: (at ?tile pos1 pos2)")
        ask13 = parse_input("fact: (at ?tile pos1 pos3)")
        ask21 = parse_input("fact: (at ?tile pos2 pos1)")
        ask22 = parse_input("fact: (at ?tile pos2 pos2)")
        ask23 = parse_input("fact: (at ?tile pos2 pos3)")
        ask31 = parse_input("fact: (at ?tile pos3 pos1)")
        ask32 = parse_input("fact: (at ?tile pos3 pos2)")
        ask33 = parse_input("fact: (at ?tile pos3 pos3)")

        tileList = []
        tileList.append(self.kb.kb_ask(ask11)[0])
        #print(str(self.kb.kb_ask(ask21)))
        tileList.append(self.kb.kb_ask(ask21)[0])
        tileList.append(self.kb.kb_ask(ask31)[0])
        tileList.append(self.kb.kb_ask(ask12)[0])
        tileList.append(self.kb.kb_ask(ask22)[0])
        tileList.append(self.kb.kb_ask(ask32)[0])
        tileList.append(self.kb.kb_ask(ask13)[0])
        tileList.append(self.kb.kb_ask(ask23)[0])
        tileList.append(self.kb.kb_ask(ask33)[0])

        numList = []

        for tile in tileList:
          if str(tile)[-5:] == "empty":
            numList.append(-1)
          else: 
            #print(str(tile))
            numList.append(int(str(tile)[-1]))

        resultTuple = []
        resultTuple.append(tuple(numList[0:3]))
        resultTuple.append(tuple(numList[3:6]))
        resultTuple.append(tuple(numList[6:9]))

        return tuple(resultTuple)


        #resultTuple = tuple(tuple(numList[0:2]), tuple(numList[3:5]), tuple(numList[6:8]))
        
        #return resultTuple


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        ### Solved: How should I turn the movable statement into a list, or access the words in the movable statement?
        
        sl = movable_statement.terms

        moveTile = sl[0]
        initialX = sl[1]
        initialY = sl[2]
        targetX = sl[3]
        targetY = sl[4]

        ### get the tileName at (targetX, targetY)
        askOrigTileTarget = parse_input("fact: (at ?tile " + str(targetX) + " " + str(targetY) + ")")
        OrigTileTarget = str(self.kb.kb_ask(askOrigTileTarget)[0])[-5:]
        #print(OrigTileTarget)
        ### end get the tileName at (targetX, targetY)

        oldFactMT = parse_input("fact: (at " + str(moveTile) + " " + str(initialX) + " " + str(initialY) + ")")
        self.kb.kb_retract(oldFactMT)

        oldFactOTT = parse_input("fact: (at " + str(OrigTileTarget) + " " + str(targetX) + " " + str(targetY) + ")")
        self.kb.kb_retract(oldFactOTT)

        newFactMT = parse_input("fact: (at " + str(moveTile) + " " + str(targetX) + " " + str(targetY) + ")")
        self.kb.kb_assert(newFactMT)

        newFactOTT = parse_input("fact: (at " + str(OrigTileTarget) + " " + str(initialX) + " " + str(initialY) + ")")
        self.kb.kb_assert(newFactOTT)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
