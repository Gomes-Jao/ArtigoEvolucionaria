from Models.Gene import Gene

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

    Considerando o AFG 2 e os valores de dificuldade atribuídos às bases, temos que:
        1.: Dificuldade máxima de um conjunto mínimo de inimigos de um gene é representada pelo conjunto {B, T, T} = 35 + 10 + 10 = 55
        2.: Dificuldade mínima de um gene é representada pelo conjunto {G, G, G} = 1 + 1 + 1 = 3
 
    Considerando as afirmações acima, iremos arbitrariamente definir um valor para dificuldade máxima de um gene:
        Considerando a dificuldade máxima de um conjunto mínimo 55, e sendo esta uma dificuldade desafiadora, iremos assumir 60
        como um valor razoável para a dificuldade máxima de um gene, possibilitando variabilidade e desafio no jogo.

========================================================================================================

Representação do Cromossomo:
    O cromossomo é uma lista de genes, representando as salas do mapa:
        Cromossomo: [Sala1, Sala2, Sala3, etc.]

    - AFC (Axiomas de Formação de Cromossomos):
        1.: O cromossomo deve possuir todos os genes (salas) preenchidos
        2.: Deve existir exatamente 1 gene com um inimigo do tipo B
'''
class Chromosome:
    def __init__(self, gene_count):
        self.genes = self.generate_chromosome(gene_count)
        self.fitness = self.calculate_fitness()

    @property
    def gene_info(self):
        gene_info = []
        for i, gene in enumerate(self.genes):
            gene_info.append(f"# {i+1}: Gene: {gene.enemy_letters} | Difficulty: {gene.difficulty}")
        return "\n".join(gene_info)  # Junta as linhas com quebra de linha real

    def validate_chromosome(self, genes, gene_count):
        if len(genes) != gene_count:
            return False
        
        genes_with_bear = 0
        for gene in genes:
            if gene.bear_count == 1:
                genes_with_bear += 1
        
        if genes_with_bear != 1:
            print(f"genes_with_bear: {genes_with_bear}")
            return False
        
        return True

    def generate_chromosome(self, gene_count):
        genes = []
        while not self.validate_chromosome(genes, gene_count):
            genes = []
            for _ in range(gene_count):
                genes.append(Gene())  # Gera automaticamente se não passar parâmetros
        return genes

    def calculate_fitness(self):
        fitness = 0
        for gene in self.genes:
            if gene.bear_count == 0:
                fitness += gene.difficulty
        return fitness / (len(self.genes) - 1)

    def __str__(self):
        return f"Chromosome:\n{self.gene_info}\nFitness: {self.fitness}"
