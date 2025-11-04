from Models.Base import Base
from Models.Gene import Gene
from Models.Chromosome import Chromosome
from Models.Population import Population
from MapGeneration.MapGeneration import Map

def generate_base():
    return Base.Base(random.choice(['G', 'W', 'T', 'B']))


# def generate_gene():
#     gene = Gene.generate_gene()


def generate_chromosome():
    return


def generate_map(mapWidth, mapHeight, minRoomWidth, minRoomHeight, offset):
    map_instance = Map(mapWidth, mapHeight, minRoomWidth, minRoomHeight, offset) # (mapWidth, mapHeight, minRoomWidth, minRoomHeight, offset=1)
    rooms, corridors = map_instance.generate_map()

    # print(f"Total de salas geradas: {len(rooms)}\n")
    # print(f"Total de corredores gerados: {len(corridors)}\n")
    # print("Salas:")
    # for i, room in enumerate(rooms, 1):
    #     print(f"  {i}. {room}")    
    # print("Corredores:")
    # for i, corridor in enumerate(corridors, 1):
    #     print(f"  {i}. {corridor}")

    return map_instance, rooms, corridors

if __name__ == "__main__":
    map, rooms, corridors = generate_map(20, 20, 6, 6, 1)
    population = Population(100, len(rooms))
    print(population)
    map.visualize_map(rooms, corridors)
    # gene = Gene()
    # print(gene)

