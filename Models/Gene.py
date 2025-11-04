import random
from Models.Base import Base

'''
Representação das Bases:
    A base se dá por uma letra, representando um inimigo:
        G = Goblin
        W = Wolf
        T = Troll
        B = Bear
        _ = None (representa a base inóqua)

    Para termos de avaliação, atribuiremos um valor de dificuldade para cada inimigo:
        G = 2
        W = 5
        T = 10
        B = 35
        _ = 0 (representa a base inóqua)

        (OBS: O valor atribuído neste caso, se dá pela quantidade de inimigos mais fracos
            que, teoricamente, se igualariam à dificulade de enfrentar um inimigo mais forte.
            Ou seja, se tivermos 2 wolves, eles teriam a mesma dificuldade de enfrentar um troll.)

========================================================================================================
Dificuldade Máxima: 60
Dificuldade Mínima: 3

Representação do gene:
    Cada gene representa uma sala, como uma lista dos inimigos presentes na sala:
    Gene: [G, W, B, T, T]

    - AFG (Axiomas de Formação de Genes):
        1.: O gene gerado não pode ser vazio
        2.: O gene gerado deve ter pelo menos três inimigos
        3.: O gene gerado pode ter apenas um inimigo do tipo B
        4*.: O gene gerado deve ter no máximo 8 inimigos do tipo G
        5*.: O gene gerado deve ter no máximo 6 inimigos do tipo W
        6**.: O gene inóquo é representado por '_' e seu valor 0 não altera o fitness do gene

    Considerando o AFG 2 e os valores de dificuldade atribuídos às bases, temos que:
        1.: Dificuldade máxima de um conjunto mínimo de inimigos de um gene é representada pelo conjunto {B, T, T} = 35 + 10 + 10 = 55
        2.: Dificuldade mínima de um gene é representada pelo conjunto {G, G, G} = 1 + 1 + 1 = 3
 
    Considerando as afirmações acima, iremos arbitrariamente definir um valor para dificuldade máxima de um gene:
        Considerando a dificuldade máxima de um conjunto mínimo 55, e sendo esta uma dificuldade desafiadora, iremos assumir 60
        como um valor razoável para a dificuldade máxima de um gene, possibilitando variabilidade e desafio no jogo.
'''

class Gene:
    def __init__(self, enemies):
        self.enemies = generate_gene() if enemies is None else enemies
        self.fitness = self.calculate_fitness()
    
    @property
    def enemy_letters(self):
        """Getter: retorna lista com apenas as letras dos inimigos"""
        return [enemy.letter for enemy in self.enemies]
    
    @property
    def enemy_count(self):
        """Getter: retorna a quantidade total de inimigos"""
        return len(self.enemies)
    
    @property
    def goblin_count(self):
        """Getter: retorna quantidade de Goblins (G)"""
        return self.enemy_letters.count('G')
    
    @property
    def wolf_count(self):
        """Getter: retorna quantidade de Wolves (W)"""
        return self.enemy_letters.count('W')
    
    @property
    def troll_count(self):
        """Getter: retorna quantidade de Trolls (T)"""
        return self.enemy_letters.count('T')
    
    @property
    def bear_count(self):
        """Getter: retorna quantidade de Bears (B)"""
        return self.enemy_letters.count('B')
    
    @property
    def difficulty(self):
        """Getter: retorna a dificuldade total do gene (calculado dinamicamente)"""
        return self.calculate_gene_difficulty(self.enemies)
    
    @property
    def is_valid(self):
        """Getter: verifica se o gene é válido"""
        return self.validate_gene(self.enemies)
    
    @property
    def average_difficulty(self):
        """Getter: retorna a dificuldade média por inimigo"""
        if self.enemy_count == 0:
            return 0
        return self.difficulty / self.enemy_count
    

    def __str__(self):
        return f"Gene: [{self.enemy_letters}] | Dificuldade Total: {self.difficulty}"

    def validate_gene(self, enemies):
        if len(enemies) < 3:
            return False
        # Conta os inimigos por letra (letter)
        enemy_letters = [enemy.letter for enemy in enemies]
        if enemy_letters.count('B') > 1:
            return False
        if enemy_letters.count('G') > 8:
            return False
        if enemy_letters.count('W') > 6:
            return False
        if self.calculate_gene_difficulty(enemies) > 60:
            return False
        if self.calculate_gene_difficulty(enemies) < 3:
            return False
        return True


    def calculate_gene_difficulty(self, enemies):
        difficulty = 0
        for enemy in enemies:
            difficulty += enemy.difficulty
        return difficulty


    def generate_gene(self):
        validGene = False
        enemies = []
    @staticmethod
    def generate_gene():
        """Gera um gene válido (método estático)"""
                enemies.append(Base())

    @staticmethod
    def generate_gene():
        """Gera um gene válido (método estático)"""
            validGene = self.validate_gene(enemies)
        return enemies
            validGene = self.validate_gene(enemies)            validGene = self.validate_gene(enemies)            # Validação usando método estático auxiliar
            validGene = Gene._validate_gene_static(enemies)    
    @staticmethod
            # Validação usando método estático auxiliar
            validGene = Gene._validate_gene_static(enemies)
        """Método estático auxiliar para validação"""
    
    @staticmethod
    def _validate_gene_static(enemies):
        """Método estático auxiliar para validação"""
        if len(enemies) < 3:
            return False
        enemy_letters = [enemy.letter for enemy in enemies]
        if enemy_letters.count('B') > 1:
            return False
        if enemy_letters.count('G') > 8:
            return False
        if enemy_letters.count('W') > 6:
            return False
        
        difficulty = 0
        for enemy in enemies:
            difficulty += enemy.difficulty
        
        if difficulty > 60:
            return False
        if difficulty < 3:
            return False
        return True
        if len(enemies) < 3:
            return False
        enemy_letters = [enemy.letter for enemy in enemies]
        if enemy_letters.count('B') > 1:
            return False
        if enemy_letters.count('G') > 8:
            return False
        if enemy_letters.count('W') > 6:
            return False
        
        difficulty = 0
        for enemy in enemies:
            difficulty += enemy.difficulty
        
        if difficulty > 60:
            return False
        if difficulty < 3:
            return False
        return True
