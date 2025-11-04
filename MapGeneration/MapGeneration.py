import queue
import random
import math
from statistics import mean
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D

class Corridor:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def createCorridor(self, start, end):
        corridor = []
        position = start.copy()
        corridor.append(position.copy())  # Adiciona cópia inicial
        
        # Move verticalmente primeiro (eixo Y)
        while abs(position[1] - end[1]) > 0.01:  # Usa tolerância pequena para floats
            if position[1] < end[1]:
                position[1] += 1.0
                if position[1] > end[1]:  # Se passou do destino, ajusta para o destino
                    position[1] = end[1]
            else:
                position[1] -= 1.0
                if position[1] < end[1]:  # Se passou do destino, ajusta para o destino
                    position[1] = end[1]
            corridor.append(position.copy())
            # Proteção contra loop infinito
            if abs(position[1] - end[1]) < 0.01:
                position[1] = end[1]
                break

        # Move horizontalmente depois (eixo X)
        while abs(position[0] - end[0]) > 0.01:  # Usa tolerância pequena para floats
            if position[0] < end[0]:
                position[0] += 1.0
                if position[0] > end[0]:  # Se passou do destino, ajusta para o destino
                    position[0] = end[0]
            else:
                position[0] -= 1.0
                if position[0] < end[0]:  # Se passou do destino, ajusta para o destino
                    position[0] = end[0]
            corridor.append(position.copy())
            # Proteção contra loop infinito
            if abs(position[0] - end[0]) < 0.01:
                position[0] = end[0]
                break
        
        # Garante que a posição final exata é adicionada
        final_pos = [end[0], end[1]]
        if abs(corridor[-1][0] - final_pos[0]) > 0.01 or abs(corridor[-1][1] - final_pos[1]) > 0.01:
            corridor.append(final_pos)
        
        return corridor

    def __str__(self):
        return f"Corridor(start=({self.start[0]}, {self.start[1]}), end=({self.end[0]}, {self.end[1]}))"
    
    def __repr__(self):
        return self.__str__()



class Room:
    def __init__(self, x, y, width, height):
        self.number = None # Será definido posteriormente
        self.center = None
        self.width = width
        self.height = height
        self.xStart = x
        self.yStart = y
        self.xEnd = x + width
        self.yEnd = y + height

    def splitHorizontal(self, room, dividePoint, roomQueue ):
        roomQueue.put(Room(room.xStart, room.yStart, dividePoint, room.height))
        roomQueue.put(Room(room.xStart + dividePoint, room.yStart, room.width - dividePoint, room.height))
    
    def splitVertical(self, room, dividePoint, roomQueue ):
        roomQueue.put(Room(room.xStart, room.yStart, room.width, dividePoint))
        roomQueue.put(Room(room.xStart, room.yStart + dividePoint, room.width, room.height - dividePoint))
    
    def __str__(self):
        number_str = f"#{self.number}" if self.number is not None else ""
        return f"Room{number_str}(pos=({self.xStart}, {self.yStart}), size=({self.width}x{self.height}), end=({self.xEnd}, {self.yEnd}))"
    
    def __repr__(self):
        return self.__str__()


class Map:
    def __init__(self, mapWidth, mapHeight, minRoomWidth, minRoomHeight, offset=1):
        self.mapWidth = mapWidth
        self.mapHeight = mapHeight
        self.minRoomWidth = minRoomWidth
        self.minRoomHeight = minRoomHeight
        self.offset = offset


    def generate_map(self):
        roomQueue = queue.Queue()
        roomList = []

        roomQueue.put(Room(0, 0, self.mapWidth, self.mapHeight))

        while not roomQueue.empty():
            room = roomQueue.get()

            if random.random() < 0.5:
                if room.width >= self.minRoomWidth * 2:
                    dividePoint = random.randint(self.minRoomWidth, room.width - self.minRoomWidth)
                    room.splitHorizontal(room, dividePoint, roomQueue)
                elif room.height >= self.minRoomHeight * 2:
                    dividePoint = random.randint(self.minRoomHeight, room.height - self.minRoomHeight)
                    room.splitVertical(room, dividePoint, roomQueue)
                else:
                    roomList.append(room)
            else:
                if room.width >= self.minRoomWidth * 2:
                    dividePoint = random.randint(self.minRoomWidth, room.width - self.minRoomWidth)
                    room.splitHorizontal(room, dividePoint, roomQueue)
                elif room.height >= self.minRoomHeight * 2:
                    dividePoint = random.randint(self.minRoomHeight, room.height - self.minRoomHeight)
                    room.splitVertical(room, dividePoint, roomQueue)
                else:
                    roomList.append(room)
        
        # Atribuir número e localizar os centros das salas
        roomCenterList = []
        for i, room in enumerate(roomList):
            room.number = i + 1
            room.center = [room.xStart + room.width / 2, room.yStart + room.height / 2]
            roomCenterList.append(room.center)
        self.applyOffset(roomList)

        corridorList = self.connectRooms(roomCenterList)

        return roomList, corridorList
    

    def calculateCorridorWidth(self):
        """Calcula a largura do corredor proporcional ao tamanho do mapa"""
        # Usa aproximadamente 5% do menor lado do mapa como largura base
        minDimension = min(self.mapWidth, self.mapHeight)
        return max(1.0, minDimension * 0.05)
    
    def isPointInsideRoom(self, point, room):
        """Verifica se um ponto está dentro de uma sala"""
        return (room.xStart <= point[0] <= room.xEnd and 
                room.yStart <= point[1] <= room.yEnd)
    
    def isRectangleInsideRoom(self, rect_x, rect_y, rect_width, rect_height, room):
        """Verifica se um retângulo está completamente dentro de uma sala"""
        # Verifica os 4 cantos do retângulo
        corners = [
            [rect_x, rect_y],
            [rect_x + rect_width, rect_y],
            [rect_x, rect_y + rect_height],
            [rect_x + rect_width, rect_y + rect_height]
        ]
        # Se todos os cantos estão dentro da sala, o retângulo está dentro
        return all(self.isPointInsideRoom(corner, room) for corner in corners)
    
    def createCorridorRectangles(self, corridor_path, width, rooms):
        """Cria uma lista de retângulos representando o corredor com largura, excluindo partes dentro de salas"""
        rectangles = []
        half_width = width / 2.0
        
        for i in range(len(corridor_path) - 1):
            p1 = corridor_path[i]
            p2 = corridor_path[i + 1]
            
            # Calcula a direção do segmento
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            
            # Se é um segmento horizontal (dy = 0)
            if abs(dy) < 0.01:
                x = min(p1[0], p2[0])
                y = p1[1] - half_width
                rect_width = abs(dx) if abs(dx) > 0.01 else 1.0
                rect_height = width
            # Se é um segmento vertical (dx = 0)
            elif abs(dx) < 0.01:
                x = p1[0] - half_width
                y = min(p1[1], p2[1])
                rect_width = width
                rect_height = abs(dy) if abs(dy) > 0.01 else 1.0
            else:
                # Segmento diagonal - cria um retângulo que cobre ambos os pontos
                x = min(p1[0], p2[0]) - half_width
                y = min(p1[1], p2[1]) - half_width
                rect_width = abs(dx) + width
                rect_height = abs(dy) + width
            
            # Verifica se o retângulo está completamente dentro de alguma sala
            is_inside_room = any(self.isRectangleInsideRoom(x, y, rect_width, rect_height, room) 
                                for room in rooms)
            
            # Só adiciona o retângulo se não estiver completamente dentro de uma sala
            if not is_inside_room:
                rectangles.append({
                    'x': x,
                    'y': y,
                    'width': rect_width,
                    'height': rect_height
                })
        
        return rectangles
    
    def connectRooms(self, roomCenterList):
        corridorList = []
        currentRoomCenter = random.choice(roomCenterList)
        roomCenterList.remove(currentRoomCenter)

        while len(roomCenterList) > 0:
            closestRoomCenter = self.findClosestRoomCenter(currentRoomCenter, roomCenterList)
            roomCenterList.remove(closestRoomCenter)
            corridor = Corridor(currentRoomCenter, closestRoomCenter)
            corridorList.append(corridor.createCorridor(currentRoomCenter, closestRoomCenter))
            currentRoomCenter = closestRoomCenter  # Atualiza para conectar a partir da sala mais recente
        return corridorList


    def findClosestRoomCenter(self, currentRoomCenter, roomCenterList):
        closestRoomCenter = None
        closestDistance = float('inf')

        for roomCenter in roomCenterList:
            distance = self.calculateDistance(currentRoomCenter, roomCenter)
            if distance < closestDistance:
                closestDistance = distance
                closestRoomCenter = roomCenter
        return closestRoomCenter


    def calculateDistance(self, currentRoomCenter, roomCenter):
        return math.sqrt((currentRoomCenter[0] - roomCenter[0]) ** 2 + (currentRoomCenter[1] - roomCenter[1]) ** 2)


    def applyOffset(self, roomList):
        """Aplica padding (offset) nas salas, reduzindo seu tamanho"""
        for room in roomList:
            room.xStart += self.offset
            room.xEnd -= self.offset
            room.width = room.xEnd - room.xStart
            room.yStart += self.offset
            room.yEnd -= self.offset
            room.height = room.yEnd - room.yStart


    def visualize_map(self, rooms, corridors):
        """Desenha as salas em um gráfico usando matplotlib"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        
        # Define uma cor única para todas as salas e corredores
        common_color = '#4A90E2'  # Azul claro
        
        for i, room in enumerate(rooms):
            # Cria um retângulo para cada sala
            rect = patches.Rectangle(
                (room.xStart, room.yStart),
                room.width,
                room.height,
                linewidth=2,
                edgecolor='black',
                facecolor=common_color,
                alpha=0.7
            )
            ax.add_patch(rect)
            
            # Adiciona número da sala no centro
            center_x = room.xStart + room.width / 2
            center_y = room.yStart + room.height / 2
            ax.text(center_x, center_y, str(i + 1), 
                   ha='center', va='center', fontsize=8, fontweight='bold')
        
        # Calcula a largura dos corredores proporcional ao mapa
        corridorWidth = self.calculateCorridorWidth()
        
        for i, corridor_path in enumerate(corridors):
            # corridor_path é uma lista de posições [x, y]
            if len(corridor_path) > 1:
                # Cria retângulos para representar o corredor com largura, excluindo partes dentro de salas
                rectangles = self.createCorridorRectangles(corridor_path, corridorWidth, rooms)
                for rect_data in rectangles:
                    rect = patches.Rectangle(
                        (rect_data['x'], rect_data['y']),
                        rect_data['width'],
                        rect_data['height'],
                        linewidth=0,  # Sem bordas
                        edgecolor='none',  # Sem bordas
                        facecolor=common_color,
                        alpha=0.6
                    )
                    ax.add_patch(rect)
        
        # Configura os limites do gráfico
        ax.set_xlim(0, self.mapWidth)
        ax.set_ylim(0, self.mapHeight)
        ax.set_aspect('equal')
        ax.set_xlabel('Largura', fontsize=12)
        ax.set_ylabel('Altura', fontsize=12)
        ax.set_title(f'Mapa Gerado - {len(rooms)} Salas', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # Inverte o eixo Y para que (0,0) fique no canto superior esquerdo
        ax.invert_yaxis()
        
        plt.tight_layout()
        plt.show()
        
        return fig, ax


# if __name__ == "__main__":
#     map_instance = Map(30, 30, 5, 5, 1) # (mapWidth, mapHeight, minRoomWidth, minRoomHeight, offset=1)
#     rooms, corridors = map_instance.generate_map()
    
#     print(f"Total de salas geradas: {len(rooms)}\n")
#     print(f"Total de corredores gerados: {len(corridors)}\n")
#     print("Salas:")
#     for i, room in enumerate(rooms, 1):
#         print(f"  {i}. {room}")    
#     print("Corredores:")
#     for i, corridor in enumerate(corridors, 1):
#         print(f"  {i}. {corridor}")
#     # Visualização gráfica
#     print("\nGerando visualização gráfica...")
#     map_instance.visualize_map(rooms, corridors)
