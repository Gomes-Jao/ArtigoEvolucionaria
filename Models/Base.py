import random

'''
Representação das Bases:
    A base se dá por uma letra, representando um inimigo:
        G = Goblin
        W = Wolf
        T = Troll
        B = Bear
        _ = None

    Para termos de avaliação, atribuiremos um valor de dificuldade para cada inimigo:
        G = 2
        W = 5
        T = 10
        B = 35
        _ = 0

        (OBS: O valor atribuído neste caso, se dá pela quantidade de inimigos mais fracos
            que, teoricamente, se igualariam à dificulade de enfrentar um inimigo mais forte.
            Ou seja, se tivermos 2 wolves, eles teriam a mesma dificuldade de enfrentar um troll.)
'''

class Base:
    def __init__(self):
        self.letter = self.generate_base()
        self.difficulty = self.get_difficulty()

    def generate_base(self):
        random_number = random.randint(0, 100)
        if random_number < 50:
            return 'G'
        elif random_number < 80:
            return 'W'
        elif random_number < 95:
            return 'T'
        elif random_number < 100:
            return 'B'
        else:
            return '_'

    def get_difficulty(self):
        if self.letter == 'G':
            return 2
        elif self.letter == 'W':
            return 5
        elif self.letter == 'T':
            return 10
        elif self.letter == 'B':
            return 35
        elif self.letter == '_':
            return 0
        else:
            raise ValueError(f"Letra inválida: {self.letter}")

    def __str__(self):
        return self.letter

