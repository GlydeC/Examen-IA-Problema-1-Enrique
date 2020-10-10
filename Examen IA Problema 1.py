import sys
import re
import random
from collections import deque, defaultdict

# Como output
def mapa_mexico():
    return {
        'BCN':['BCS', 'Sonora'],
        'BCS':['BCN'],
        'Sonora':['BCN', 'Chihuahua', 'Sinaloa'],
        'Chihuahua':['Sonora', 'Sinaloa', 'Durango', 'Coahuila'],
        'Sinaloa':['Sonora', 'Durango', 'Chihuahua', 'Nayarit'],
        'Durango':['Chihuahua', 'Nayarit', 'Sinaloa', 'Coahuila', 'Zacatecas'],
        'Coahuila':['Chihuahua', 'Durango', 'Zacatecas', 'NL'],
        'Zacatecas':['Durango', 'Coahuila', 'SLP', 'Aguascalientes', 'Jalisco', 'Nayarit'],
        'Nayarit':['Sinaloa', 'Durango', 'Zacatecas', 'Jalisco'],
        'Jalisco':['Nayarit', 'Zacatecas', 'Aguascalientes', 'Guanajuato','Michoacan','Colima'],
        'Colima':['Jalisco', 'Michoacan'],
        'Aguascalientes':['Jalisco', 'Zacatecas'],
        'NL':['Coahuila', 'SLP', 'Tamaulipas'],
        'Tamaulipas':['NL', 'SLP', 'Veracruz'],
        'SLP':['NL', 'Tamaulipas', 'Veracruz', 'Hidalgo', 'Queretaro', 'Guanajuato', 'Zacatecas'],
        'Guanajuato':['SLP', 'Queretaro', 'Michoacan', 'Jalisco'],
        'Michoacan':['Colima', 'Jalisco', 'Guanajuato', 'Queretaro', 'CdMex', 'Guerrero'],
        'Queretaro':['Guanajuato', 'SLP', 'Hidalgo', 'CdMex', 'Michoacan'],
        'Hidalgo':['Veracruz', 'Tlaxcala', 'Puebla', 'CdMex', 'Queretaro', 'SLP'],
        'Puebla':['Tlaxcala', 'Hidalgo', 'CdMex', 'Morelos', 'Guerrero', 'Oaxaca', 'Veracruz'],
        'CdMex':['Guerrero', 'Michoacan', 'Queretaro', 'Hidalgo', 'Tlaxcala', 'Puebla', 'Morelos', 'DF'],
        'Tlaxcala': ['CdMex', 'Puebla', ],
        'DF':['CdMex', 'Morelos', 'Hidalgo'],
        'Guerrero':['Michoacan', 'CdMex', 'Morelos', 'Puebla', 'Oaxaca'],
        'Morelos':['Guerrero', 'CdMex', 'DF', 'Puebla'],
        'Oaxaca':['Guerrero', 'Puebla', 'Veracruz','Chiapas'],
        'Veracruz':['Tamaulipas', 'SLP', 'Hidalgo', 'Puebla', 'Oaxaca', 'Chiapas', 'Tabasco'],
        'Chiapas':['Tabasco', 'Veracruz', 'Oaxaca'],
        'Tabasco':['Veracruz', 'Chiapas', 'Campeche'],
        'Campeche':['Tabasco', 'Yucatan', 'Quintana Roo'],
        'Yucatan':['Quintana Roo', 'Campeche'],
        'Quintana Roo':['Campeche', 'Yucatan']
    }

class ColorearMapa:

    def __init__(self, mapa, coloreado=None):
        self.mapa = mapa
        self.coloreado = coloreado if coloreado else set()
        self.color_estado = dict()

    def colorearGrafo(self, nodo_inicial=None,  max_colores=5):

        limite_colisiones = len(self.mapa) ** 2
        self.max_colores = max_colores

        no_explorado = deque(nodo_inicial)
        color = random.randrange(1, self.max_colores)
        colisiones = 0

        def siguiente_color(_color):
            _color -= 1
            if _color < 1:
                _color = self.max_colores
            return _color

        def asignar_color(_color, _nodo):
            self.color_estado[_nodo] = _color    

        while no_explorado:
            nodo = no_explorado.popleft()
            if nodo not in self.coloreado:
                asignar_color(color, nodo)
                self.coloreado.add(nodo)
                color = siguiente_color(color)

            colision = False
            for nodo_adyacente in self.mapa[nodo]:
                if nodo_adyacente not in self.coloreado:
                    asignar_color(color, nodo_adyacente)
                    self.coloreado.add(nodo_adyacente)
                    no_explorado.append(nodo_adyacente)
                elif self.color_estado[nodo] == self.color_estado[nodo_adyacente]:
                    colision = True
                    colisiones += 1
                    self.coloreado.remove(nodo_adyacente)
                    no_explorado.append(nodo_adyacente)
            if colision:
                if colisiones % limite_colisiones == 0:
                    self.max_colores += 1
                color = siguiente_color(color)

        return self.color_estado

def main():
    mexico = mapa_mexico()

    MapaColoreado = ColorearMapa(mexico)

    estados_coloreados = MapaColoreado.colorearGrafo(nodo_inicial=['NL'], max_colores=5)

    grupos_estados_coloreados = defaultdict(list)
    for estado in mexico:
        if estado in estados_coloreados:
            grupos_estados_coloreados[estados_coloreados[estado]].append(estado)

    print('')

    for color in grupos_estados_coloreados:
        print(f"Estados coloreados con el color {color}: {grupos_estados_coloreados[color]}")

main()
    