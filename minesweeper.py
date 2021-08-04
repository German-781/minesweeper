import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

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

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return MinesweeperAI.mines

        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return MinesweeperAI.safes


        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        
        for sentence in self.knowledge:
            if cell in sentence:
                sentence.remove(cell)
                num_celdas = len(sentence) - 1
                if num_celdas == 0:
                    self.knowledge.remove(sentence)
                else:
                    sentence_celdas = []
                    celda1 = sentence[0]
                    if celda1 > 0:
                        celda1 = celda1 - 1
                        sentence[0] = celda1 

                    if num_celdas == celda1:
                        sentence_celdas = sentence[1:]
                        numero_celdas = len(sentence_celdas)


                        for celda in sentence_celdas:
                            if numero_celdas != 0:
                                if numero_celdas == 1:
                                    if sentence in self.knowledge:
                                        self.knowledge.remove(sentence)
                                    MinesweeperAI.mark_mine(self, celda)
                                else:
                                    MinesweeperAI.mark_mine(self, celda)
                                    numero_celdas = numero_celdas - 1
                    else:
                        if celda1 == 0:
                            sentence_celdas = sentence[1:]
                            numero_celdas = len(sentence_celdas)

                            for celda in sentence_celdas:
                                if numero_celdas != 0:
                                    if numero_celdas == 1:
                                        if sentence in self.knowledge:
                                            self.knowledge.remove(sentence)
                                        MinesweeperAI.mark_safe(self, celda)
                                    else:
                                        MinesweeperAI.mark_safe(self, celda)
                                        numero_celdas = numero_celdas - 1
        
        #raise NotImplementedError


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        for sentence in self.knowledge:
            if cell in sentence:

                num_celdas = len(sentence) - 1
                if num_celdas == 1:
                    self.knowledge.remove(sentence)
                else:
                    sentence.remove(cell)
                    num_celdas = len(sentence) - 1
                    celda1 = sentence[0] 

                    if num_celdas == celda1:
                        sentence_celdas = sentence[1:]
                        numero_celdas = len(sentence_celdas)

                        for celda in sentence_celdas:
                            if numero_celdas != 0:

                                if numero_celdas == 1:
                                    if sentence in self.knowledge:
                                        self.knowledge.remove(sentence)
                                        MinesweeperAI.mark_mine(self, celda)
                                else:
                                    MinesweeperAI.mark_mine(self, celda)
                                    numero_celdas = numero_celdas - 1
        
        #raise NotImplementedError


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

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            Sentence.mark_mine(self,cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        if cell not in(self.safes):

            self.safes.add(cell)
            for sentence in self.knowledge:
                Sentence.mark_safe(self,cell)


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
        
        self.moves_made.add(cell)

        if cell in self.safes:
            self.safes.remove(cell)

        MinesweeperAI.mark_safe(self, cell)
        """
        quita de celdas seguras las que están en movidas

        """
        seguras = set()
        for segura in self.safes:
            if segura in self.moves_made:
                seguras.add(segura)

        for jugadas in seguras:
            self.safes.remove(jugadas)


        numero_movidas = len(self.moves_made)

        if numero_movidas > 55:
            print("*** Felicitaciones gano el buscaminas ***")


        self.celdas = []

        i = cell[0]
        j = cell[1]

        if i == 0:
            menor_i = 0
        else:
            menor_i = i - 1

        if i == 7:
            mayor_i = 7 + 1
        else:
            mayor_i = i + 2 
    
        if j == 0:
            menor_j = 0
        else:
            menor_j = j - 1

        if j == 7:
            mayor_j = 7 + 1
        else:
            mayor_j = j + 2

        if count > 0:

            for i in range(menor_i, mayor_i):
                for j in range(menor_j, mayor_j):
                    celda = (i,j)
                    if celda not in self.moves_made:
                        self.celdas = self.celdas + [celda]

            if len(self.celdas) <= count:
                for celda in self.celdas:
                    MinesweeperAI.mark_mine(self, celda)
            elif len(self.celdas) == 1:                    
                MinesweeperAI.mark_safe(self, celda)
               
            else:
                self.celdas[:0] = [count]
                self.knowledge = self.knowledge + [self.celdas]
                sentence = self.celdas
                MinesweeperAI.revisa_oraciones(self)

        #raise NotImplementedError

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in range(self.height):
            for j in range(self.width):

                if (i,j) in self.moves_made:

                    continue
                else:
                    if (i,j) in self.mines:
                        continue
                    else:
                        if (i,j) in self.safes:
                            return (i,j)
        return None
        
        #raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        move_ok = False
        fin = False

        numero_movidas = len(self.moves_made)
        if numero_movidas == 56:
            fin = True
            move_ok = True
        else:
            move_ok = False


        while move_ok == False: 

            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i,j) in self.moves_made:
                continue
            else:
                if (i,j) in self.mines:
                    continue
                else: 
                    move_ok = True
        
        if fin == False:
            if move_ok:   
                return (i,j)
            else:
                return None
        else:
            return None
   
        #raise NotImplementedError

        
    def agrega_sentences(self, new_sentences):
        """
        Agrega nuevas sentences creadas por diferencia a knowledge
        
        """

        if len(new_sentences) >= 1:

            for new_sentence in new_sentences:
                contador = new_sentence[0]
                celdas = new_sentence[1:]
                num_celdas = len(celdas)
            
                if contador == 0:
                    for celda in celdas:
                        MinesweeperAI.mark_safe(self,celda)
                else:
                    if num_celdas <= contador:
                        for celda in celdas:

                            MinesweeperAI.mark_mine(self,celda)
                    else:
                        if len(new_sentence) > 1:
                            if new_sentence in self.knowledge:
                                continue
                            else:
                                self.knowledge = self.knowledge + [new_sentence]

    def revisa_oraciones(self):
        """
        Revisa si hay suficientes oraciones en knowledge
        para encontrar subconjuntos 
        
        """

        num_oraciones = len(self.knowledge)
        if num_oraciones > 3:
            for sentence in self.knowledge:
                MinesweeperAI.subconjuntos(self, sentence)

    def subconjuntos(self, sentence_e):
        """
        Revisa si una celda dada es subconjunto de alguna oracione en knowledge
       
        """
        subconjunto = False
        celdas_e = sentence_e[1:]
        contador_e = sentence_e[0]
        new_sentences = []

        largo_e = len(celdas_e)

        for sentence in self.knowledge:
            largo = len(sentence) - 1
            contador = sentence[0]
            contador_resta = contador_e - contador
            if contador_resta >= 0:

                if largo < largo_e:
                    celdas = sentence[1:]
                    for celda in celdas:
                        if celda in celdas_e:
                            subconjunto = True
                        else:
                            subconjunto = False
                            break

                    if subconjunto == True:
                        contador = sentence[0]
                        celdas_resta = []
                        celdas_resta_paso = []
                        new_sentence = []

                        celdas_resta_paso = set(celdas_e) - set(celdas)
                        for celda in celdas_resta_paso:
                            celdas_resta = celdas_resta + [celda]

                        if len(celdas_resta) != 0:
                            if len(celdas_resta) != len(celdas_e):
                                new_sentence[:0] = [contador_resta]

                            if len(celdas_resta) <= contador_resta:
                                for celda in celdas_resta:
                                    MinesweeperAI.mark_mine(self, celda)
                            else:
                                if len(celdas_resta) == 1:   
                                    for celda in celdas_resta:
                                        MinesweeperAI.mark_safe(self, celda)
               
                            new_sentence = new_sentence + celdas_resta
                            new_sentences = new_sentences + [new_sentence]

        if len(new_sentences) >= 1:
            MinesweeperAI.agrega_sentences(self, new_sentences)

        #raise NotImplementedError

