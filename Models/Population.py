import random
from Models.Chromosome import Chromosome
'''
Representação da População:
    A população é uma lista de cromossomos, representando as soluções do problema:
        População: [Cromossomo1, Cromossomo2, Cromossomo3, etc.]
'''
class Population:
    def __init__(self, population_size, gene_count):
        self.chromosomes = self.generate_population(population_size, gene_count)

    @property
    def chromosome_info(self):
        chromosome_info = []
        for i, chromosome in enumerate(self.chromosomes):
            chromosome_info.append(f"{chromosome}")
        return "\n".join(chromosome_info)


    def crossover(self, parent1, parent2):
        return [Chromosome(gene_count) for _ in range(population_size)]


    def mutation(self, chromosome):
        return Chromosome(gene_count)

    def domitant_gene_func(self, gene1, gene2):
        if gene1.bear_count > 0 and gene2.bear_count > 0:
            return gene1 if gene1.difficulty >= gene2.difficulty else gene2
        elif gene1.bear_count == 0 and gene2.bear_count == 0:
            return gene1 if gene1.difficulty >= gene2.difficulty else gene2
        else:
            return Gene({letter: '_', difficulty: 0})
        return [Chromosome(gene_count) for _ in range(population_size)]


    def __str__(self):
        return f"Population:\n{self.chromosome_info}"


    def generate_population(self, population_size, gene_count):
        return [Chromosome(gene_count) for _ in range(population_size)]