class Cola:
    def __init__(self, max_capacidad):
        self.items = []
        self.max_capacidad = max_capacidad

    def estaVacia(self):
        return self.items == []

    def insertar(self, item):
        self.items.insert(0,item)
        if self.tamano() > self.max_capacidad:
            self.extraer()

    def extraer(self):
        return self.items.pop()

    def tamano(self):
        return len(self.items)

    def buscar(self, item):
        for i in range(0, self.tamano()):
            iguales = True
            for j in range(0, len(item)):
                if self.items[i][j] != item[j]:
                    iguales = False
                    break
            if iguales:
                return True

            for j in range(0, len(item)):
                if self.items[i][len(item)-1-j] != item[j]:
                    iguales = False
                    break
            if iguales:
                return True

        return False