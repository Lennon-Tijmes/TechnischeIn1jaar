import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8, sus=1):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()
        self.sus = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

        # ඞ Impostor among us :).. One cell lies :(
        safe_cells = [
            (i, j) for i in range(self.height)
            for j in range(self.width)
            if not self.board[i][j]
        ]
        self.impostor_cell = random.choice(safe_cells) # I LOVE THE RANDOM FUNCTION

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        # the result should be different if it is lying
        if cell == self.impostor_cell:
            return count + 1
            

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count, source=None):
        self.cells = set(cells)
        self.count = count
        self.source = source # More logic for the impostor cell, thank you jaqueline!

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count > 0:
            return set(self.cells)
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # Sus cells
        self.sus = set()

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Step 1 and 2
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Step 3 - Neighbours just like the filter for blur :) but different
        neighbours = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.safes and (i, j) not in self.mines:
                        neighbours.add((i, j))
                    elif (i, j) in self.mines:
                        count -= 1
        new_sentence = Sentence(neighbours, count, source=cell)
        self.knowledge.append(new_sentence)

        # Step 4 - safe = not boom
        self.update_knowledge()

        # Step 5 - not work in progress any longer hooray!
        self.infer_sentences()

        # Step 6 - throw everything through the window we got an impostor
        sus_cells = self.detect_contradictions()
        self.sus_update(sus_cells)

    def update_knowledge(self):
        """
        Updating the known safes and mines and marks them
        """
        changed = True
        while changed:
            changed = False

            # Fill an empty set for it
            safes = set()
            mines = set()

            for sentence in self.knowledge:
                safes = sentence.known_safes()
                mines = sentence.known_mines()
                if safes:
                    for cell in safes:
                        if cell not in self.safes:
                            self.mark_safe(cell)
                            changed = True
                if mines:
                    for cell in mines:
                        if cell not in self.mines:
                            self.mark_mine(cell)
                            changed = True

        # We should clean the sentences cause it may be emtpy...
        self.knowledge = [s for s in self.knowledge if s.cells]

    def infer_sentences(self):
        """
        Ngl I truly disliked this idk why but I had a hard time figuring this out.
        The goal is to infer new sentences based on existing knowledge with the subset method.
        """
        infer_sentences = []

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 == sentence2:
                    continue
                if sentence1.cells and sentence2.cells and sentence1.cells < sentence2.cells:
                    infer_cells = sentence2.cells - sentence1.cells
                    infer_count = sentence2.count - sentence1.count
                    infer_sentence = Sentence(infer_cells, infer_count)
                    if infer_sentence not in self.knowledge and infer_sentence not in infer_sentences:
                        infer_sentences.append(infer_sentence)

        if infer_sentences:
            self.knowledge.extend(infer_sentences)
            self.update_knowledge()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # I like random I WILL MAKE IT RANDOM!
        RANDOM = [
            (i, j)
            for i in range(self.height)
            for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]

        if RANDOM:
            return random.choice(RANDOM)  # This makes me happy
        return None
    
    def detect_contradictions(self):
        contradictions = set()

        for i in range(len(self.knowledge)):
            for j in range(i + 1, len(self.knowledge)):
                c1 = self.knowledge[i]
                c2 = self.knowledge[j]

                # Check if its a contradiction
                if c1.cells == c2.cells and c1.count != c2.count:
                    contradictions.add(c1.source)
                    contradictions.add(c2.source)
        
        return contradictions
    
    def sus_update(self, sus_cells):
        """
        It should update the AI with the knowledge that a cell can lie, it should be excluded if the AI finds them
        """
        for cell in sus_cells:
            self.sus.add(cell)

        self.knowledge = [s for s in self.knowledge if s.source not in self.sus]
