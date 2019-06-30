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
        if item in self.items:
            return True
        else:
            return False