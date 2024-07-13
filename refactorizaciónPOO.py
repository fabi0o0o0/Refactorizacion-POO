import heapq

class Mapa:
    def __init__(self, dimension):
        self.dimension = dimension
        self.matriz = self.crear_matriz(dimension)

    def crear_matriz(self, dimension):
        return [[0 for _ in range(dimension)] for _ in range(dimension)]

    def imprimir_matriz(self):
        for fila in self.matriz:
            for columna in fila:
                print(columna, end=" ")
            print()

    def agregar_obstaculo(self, coordenada, tipo):
        x, y = coordenada
        ruta = {
            'camino': 0,
            'pasto': 1,
            'agua': 2,
            'edificio': 3,
        }
        if x >= 0 and x < len(self.matriz) and y >= 0 and y < len(self.matriz[0]) and tipo in ruta.keys() and tipo != 'camino':
            self.matriz[x][y] = ruta[tipo]
            self.imprimir_matriz()
        else:
            print("Lo ingresado no está dentro de las dimensiones de las coordenadas (matriz) o tu obstáculo no está dentro de los tipos: pasto, agua, edificio")

    def eliminar_obstaculo(self, coordenada):
        x, y = coordenada
        if x >= 0 and x < len(self.matriz) and y >= 0 and y < len(self.matriz[0]) and self.matriz[x][y] != 'I' and self.matriz[x][y] != 'F':
            self.matriz[x][y] = 0
            self.imprimir_matriz()
        else:
            print("No es posible eliminar la celda especificada (puede ser una celda de inicio/fin o está fuera de los límites)")

    def inicio_y_fin(self, inicio, fin):
        x_inicio, y_inicio = inicio
        x_final, y_final = fin
        if x_inicio >= 0 and x_inicio < len(self.matriz) and y_inicio >= 0 and y_inicio < len(self.matriz[0]) and \
           x_final >= 0 and y_final >= 0 and y_final < len(self.matriz[0]):
            self.matriz[x_inicio][y_inicio] = 'I'
            self.matriz[x_final][y_final] = 'F'
            self.imprimir_matriz()
        else:
            print("Las coordenadas no son válidas")

    def marcar_camino(self, camino):
        for x, y in camino:
            if self.matriz[x][y] == 0:
                self.matriz[x][y] = '*'
        self.imprimir_matriz()

    def es_celda_valida(self, fila, columna):
        return 0 <= fila < self.dimension and 0 <= columna < self.dimension

    def es_celda_accesible(self, fila, columna):
        return self.es_celda_valida(fila, columna) and self.matriz[fila][columna] != 3

class CalculadoraRuta:
    def __init__(self, mapa):
        self.mapa = mapa

    @staticmethod
    def heuristica(a, b): 
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def vecinos(self, nodo):
        x, y = nodo
        candidatos = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        resultados = []
        for cx, cy in candidatos:
            if 0 <= cx < len(self.mapa.matriz) and 0 <= cy < len(self.mapa.matriz[0]) and self.mapa.matriz[cx][cy] != 3:
                resultados.append((cx, cy))
        return resultados

    def a_star(self, inicio, fin):
        nodos_abiertos = [] 
        heapq.heappush(nodos_abiertos, (0, inicio)) 
        origen = {} 
        puntaje_g = {inicio: 0}
        puntaje_f = {inicio: self.heuristica(inicio, fin)}

        while nodos_abiertos:
            _, actual = heapq.heappop(nodos_abiertos)
            if actual == fin:
                camino_tomado = []
                while actual in origen:
                    camino_tomado.append(actual)
                    actual = origen[actual]
                camino_tomado.append(inicio)
                camino_tomado.reverse()
                return camino_tomado

            for vecino in self.vecinos(actual):
                if self.mapa.matriz[vecino[0]][vecino[1]] in ['I', 'F']:
                    peso_celda = 0
                else:
                    peso_celda = self.mapa.matriz[vecino[0]][vecino[1]]
                tentivo_puntaje_g = puntaje_g[actual] + peso_celda
                if vecino not in puntaje_g or tentivo_puntaje_g < puntaje_g[vecino]:
                    origen[vecino] = actual
                    puntaje_g[vecino] = tentivo_puntaje_g
                    puntaje_f[vecino] = tentivo_puntaje_g + self.heuristica(vecino, fin)
                    if vecino not in [i[1] for i in nodos_abiertos]:
                        heapq.heappush(nodos_abiertos, (puntaje_f[vecino], vecino))
        return []

def main():
    dimension = int(input("Ingrese la dimensión de la matriz: "))
    mapa = Mapa(dimension)
    mapa.imprimir_matriz()

    inicio_input = input("Ingrese las coordenadas de inicio (ej. '1,1'): ")
    fin_input = input("Ingrese las coordenadas de fin (ej. '3,3'): ")

    inicio = tuple(map(int, inicio_input.split(',')))
    fin = tuple(map(int, fin_input.split(',')))
    inicio = (inicio[0] - 1, inicio[1] - 1)
    fin = (fin[0] - 1, fin[1] - 1)

    mapa.inicio_y_fin(inicio, fin)

    num_obstaculos = int(input("Ingrese la cantidad de obstáculos: "))
    for _ in range(num_obstaculos):
        obstaculo_input = input("Ingrese las coordenadas y el tipo de obstáculo (ej. '1,1 agua'): ")
        coordenada_str, tipo = obstaculo_input.split()
        coordenada = tuple(map(int, coordenada_str.split(',')))
        coordenada = (coordenada[0] - 1, coordenada[1] - 1)
        mapa.agregar_obstaculo(coordenada, tipo)

    while True:
        eliminar = input("¿Desea eliminar algún obstáculo? (s/n): ").lower()
        if eliminar == 's':
            eliminar_input = input("Ingrese las coordenadas del obstáculo a eliminar (ej. '1,1'): ")
            coordenada = tuple(map(int, eliminar_input.split(',')))
            coordenada = (coordenada[0] - 1, coordenada[1] - 1)
            mapa.eliminar_obstaculo(coordenada)
        else:
            break

    calculadora = CalculadoraRuta(mapa)
    camino = calculadora.a_star(inicio, fin)

    if camino:
        print("\n***********\n")
        mapa.marcar_camino(camino)
        print("El camino más corto es:")
        for paso in camino:
            print(paso)
    else:
        print("No se encontró un camino.")

if __name__ == "__main__":
    main()
