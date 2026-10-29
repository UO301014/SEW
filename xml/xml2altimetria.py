#-------------------------------------------------------------------------------
# Name:        xml2altimetria
# Purpose:     Genera el perfil de altimetría (altimetria.svg) de una etapa
#              a partir de etapaEsquema.xml
#
# Author:      Usuario
#
# Created:     07/10/2026
# Copyright:   UO301014 - Universidad de Oviedo
#-------------------------------------------------------------------------------
# La clase Svg está basada en 02030-SVG.py (Juan Manuel Cueva Lovelle,
# Universidad de Oviedo), con la misma API (addRect, addCircle, addLine,
# addPolyline, addText, escribir, ver).
#-------------------------------------------------------------------------------

import math
import xml.etree.ElementTree as ET


class Svg(object):
    """
    Genera archivos SVG con rectángulos, círculos, líneas, polilíneas y texto
    """

    def __init__(self):
        """
        Crea el elemento raíz, el espacio de nombres y la versión
        """
        self.raiz = ET.Element('svg', xmlns="http://www.w3.org/2000/svg", version="2.0")

    def addRect(self, x, y, width, height, fill, strokeWidth, stroke):
        """
        Añade un elemento rect
        """
        ET.SubElement(self.raiz, 'rect',
                      x=x,
                      y=y,
                      width=width,
                      height=height,
                      fill=fill,
                      stroke=stroke,
                      **{'stroke-width': strokeWidth})

    def addCircle(self, cx, cy, r, fill):
        """
        Añade un elemento circle
        """
        ET.SubElement(self.raiz, 'circle',
                      cx=cx,
                      cy=cy,
                      r=r,
                      fill=fill)

    def addLine(self, x1, y1, x2, y2, stroke, strokeWidth):
        """
        Añade un elemento line
        """
        ET.SubElement(self.raiz, 'line',
                      x1=x1,
                      y1=y1,
                      x2=x2,
                      y2=y2,
                      stroke=stroke,
                      **{'stroke-width': strokeWidth})

    def addPolyline(self, points, stroke, strokeWidth, fill):
        """
        Añade un elemento polyline
        """
        ET.SubElement(self.raiz, 'polyline',
                      points=points,
                      stroke=stroke,
                      fill=fill,
                      **{'stroke-width': strokeWidth})

    def addText(self, texto, x, y, fontFamily, fontSize, style):
        """
        Añade un elemento texto
        """
        ET.SubElement(self.raiz, 'text',
                      x=x,
                      y=y,
                      style=style,
                      **{'font-family': fontFamily,
                         'font-size': fontSize}).text = texto

    def escribir(self, nombreArchivoSVG):
        """
        Escribe el archivo SVG con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)

        """
        Introduce indentación y saltos de línea
        para generar XML en modo texto
        """
        ET.indent(arbol)

        arbol.write(nombreArchivoSVG,
                    encoding='utf-8',
                    xml_declaration=True
                    )

    def ver(self):
        """
        Muestra el archivo SVG. Se utiliza para depurar
        """
        print("\nElemento raiz = ", self.raiz.tag)

        if self.raiz.text is not None:
            print("Contenido = ", self.raiz.text.strip('\n'))
        else:
            print("Contenido = ", self.raiz.text)

        print("Atributos = ", self.raiz.attrib)

        # Recorrido de los elementos del árbol
        for hijo in self.raiz.findall('.//'):  # Expresión XPath
            print("\nElemento = ", hijo.tag)
            if hijo.text is not None:
                print("Contenido = ", hijo.text.strip('\n'))
            else:
                print("Contenido = ", hijo.text)
            print("Atributos = ", hijo.attrib)


class EtapaAltimetria:
    """
    Lee etapaEsquema.xml mediante expresiones XPath y dibuja el perfil de
    altimetría de la etapa (distancia en el eje X, altitud en el eje Y)
    """

    # Dimensiones del lienzo y márgenes (en píxeles)
    ANCHO = 1000
    ALTO = 450
    MARGEN_IZQ = 70
    MARGEN_DER = 30
    MARGEN_SUP = 60
    MARGEN_INF = 70

    FUENTE = "Arial"

    def __init__(self, archivo_xml):
        self.tree = ET.parse(archivo_xml)
        self.root = self.tree.getroot()
        self.ns = {"v": "http://www.uniovi.es"}
        self.titulo = ""
        self.longitud = 0.0
        self.puntos = []        # lista de (distancia_km, altitud_m)

    def _numero(self, ruta, nodo=None):
        """
        Devuelve como float el texto del primer elemento que cumple la ruta XPath
        """
        origen = nodo if nodo is not None else self.root
        return float(origen.find(ruta, self.ns).text)

    def leer_datos(self):
        """
        Extrae del XML título, longitud total y los puntos (distancia, altitud)
        """
        nombre = self.root.find("v:nombre", self.ns).text
        numero = self.root.find("v:numero", self.ns).text
        self.titulo = "Altimetría - Etapa {}: {}".format(numero, nombre)
        self.longitud = self._numero("v:longitud")

        # Salida: distancia 0
        alt_salida = self._numero("v:salida_coord/v:altitud_coord")
        self.puntos.append((0.0, alt_salida))

        # Hitos (puertos, sprints y puntos anónimos), en el orden del XML
        for hito in self.root.findall("v:hitos/*", self.ns):
            distancia = self._numero("v:distancia", hito)
            altitud = self._numero("v:altitud_coord", hito)
            self.puntos.append((distancia, altitud))

        # Llegada: distancia = longitud total de la etapa
        alt_llegada = self._numero("v:llegada_coord/v:altitud_coord")
        self.puntos.append((self.longitud, alt_llegada))

    def _escalas(self):
        """
        Calcula los límites del eje Y (múltiplos de 10 m) y el tamaño útil
        """
        alt_max = max(a for _, a in self.puntos)
        self.y_max = (int(alt_max // 10) + 1) * 10
        self.y_min = 0
        self.ancho_util = self.ANCHO - self.MARGEN_IZQ - self.MARGEN_DER
        self.alto_util = self.ALTO - self.MARGEN_SUP - self.MARGEN_INF

    def _x(self, km):
        """
        Convierte una distancia (km) en coordenada x del SVG
        """
        return self.MARGEN_IZQ + (km / self.longitud) * self.ancho_util

    def _y(self, metros):
        """
        Convierte una altitud (m) en coordenada y del SVG (eje invertido)
        """
        fraccion = (metros - self.y_min) / (self.y_max - self.y_min)
        return self.MARGEN_SUP + self.alto_util - fraccion * self.alto_util

    def dibujar(self, svg):
        """
        Dibuja fondo, cuadrícula, ejes, perfil de altimetría y textos
        """
        self._escalas()
        base = self.MARGEN_SUP + self.alto_util
        derecha = self.MARGEN_IZQ + self.ancho_util
        f = self.FUENTE

        # Fondo
        svg.addRect('0', '0', str(self.ANCHO), str(self.ALTO), 'white', '0', 'white')

        # Título
        svg.addText(self.titulo, str(self.ANCHO / 2), '30', f, '20',
                    "text-anchor: middle; font-weight: bold;")

        # Líneas horizontales de escala (cada 10 m) con su texto
        for m in range(self.y_min, self.y_max + 1, 10):
            y = self._y(m)
            svg.addLine(str(self.MARGEN_IZQ), str(y), str(derecha), str(y), '#dddddd', '1')
            svg.addText(str(m), str(self.MARGEN_IZQ - 8), str(y + 4), f, '12',
                        "text-anchor: end;")

        # Líneas verticales de escala (cada km) con su texto
        for km in range(0, int(math.floor(self.longitud)) + 1):
            x = self._x(km)
            svg.addLine(str(x), str(self.MARGEN_SUP), str(x), str(base), '#dddddd', '1')
            svg.addText(str(km), str(x), str(base + 18), f, '12',
                        "text-anchor: middle;")

        # Marca de la longitud total si no es un número entero de km
        if self.longitud != math.floor(self.longitud):
            x = self._x(self.longitud)
            svg.addLine(str(x), str(self.MARGEN_SUP), str(x), str(base), '#dddddd', '1')
            svg.addText("{:g}".format(self.longitud), str(x), str(base + 18), f, '12',
                        "text-anchor: middle;")

        # Ejes
        svg.addLine(str(self.MARGEN_IZQ), str(self.MARGEN_SUP),
                    str(self.MARGEN_IZQ), str(base), 'black', '2')
        svg.addLine(str(self.MARGEN_IZQ), str(base), str(derecha), str(base), 'black', '2')

        # Perfil de altimetría (polilínea)
        puntos_svg = " ".join("{:.2f},{:.2f}".format(self._x(d), self._y(a))
                              for d, a in self.puntos)
        svg.addPolyline(puntos_svg, '#d32f2f', '3', 'none')

        # Títulos de los ejes (texto horizontal y texto vertical)
        svg.addText('Distancia desde la salida (km)',
                    str(self.MARGEN_IZQ + self.ancho_util / 2), str(self.ALTO - 20),
                    f, '14', "text-anchor: middle;")
        svg.addText('Altitud (m)',
                    '25', str(self.MARGEN_SUP + self.alto_util / 2 - 80),
                    f, '14', "writing-mode: tb; glyph-orientation-vertical: 0;")

    @staticmethod
    def ejecutar(archivo_entrada="etapaEsquema.xml", archivo_salida="altimetria.svg"):
        """
        Punto de entrada del programa (método de clase, sin funciones sueltas)
        """
        print("Iniciando generación de la altimetría a partir de XML...")

        # 1. Leemos los datos del XML
        etapa = EtapaAltimetria(archivo_entrada)
        etapa.leer_datos()

        # 2. Creamos el SVG y dibujamos el perfil
        nuevoSVG = Svg()
        etapa.dibujar(nuevoSVG)

        # 3. Escribimos el archivo final
        nuevoSVG.escribir(archivo_salida)
        print("Creado el archivo: ", archivo_salida)


if __name__ == "__main__":
    EtapaAltimetria.ejecutar()