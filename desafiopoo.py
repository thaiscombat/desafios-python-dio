class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor

    def buzinar(self):
        print("BiBi")
    
    def parar(self):
        print("Biclicleta estacionada!")

    def correr(self):
        print("Biclicleta acelerando.")
    
    def __str__(self):
        return f"{self.__class__.__name__} : {', '.join([f"{chave}={valor}" for chave, valor in self.__dict__.itens()])}"

bike_1 = Bicicleta("azul", "caloi", 2017, 350)

bike_1.buzinar()
print (bike_1.cor)