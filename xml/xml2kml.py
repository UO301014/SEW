#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Usuario
#
# Created:     07/10/2026
# Copyright:   UO301014 - Universidad de Oviedo
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as ET


class Kml(object):
    """
    Genera archivo KML con puntos y líneas usando ElementTree
    """

    # Colores en formato KML: aabbggrr (alfa, azul, verde, rojo), sin '#'
    COLOR_ROJO = "ff0000ff"       # salida / meta
    COLOR_VERDE = "ff00ff00"      # puertos de montaña
    COLOR_AZUL = "ffff0000"       # sprints intermedios
    COLOR_AMARILLO = "ff00ffff"   # puntos anónimos

    def __init__(self):
        """
        Crea el elemento raíz y el espacio de nombres
        """
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz, 'Document')

    def addPlacemark(self, nombre, descripcion, long, lat, alt, modoAltitud, color):
        """
        Añade un elemento <Placemark> con puntos <Point>, coloreado según el
        tipo de hito (rojo=salida/meta, verde=puerto, azul=sprint, amarillo=anónimo)
        """
        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        ET.SubElement(pm, 'description').text = descripcion

        estilo = ET.SubElement(pm, 'Style')
        icono = ET.SubElement(estilo, 'IconStyle')
        ET.SubElement(icono, 'color').text = color

        punto = ET.SubElement(pm, 'Point')
        ET.SubElement(punto, 'coordinates').text = '{},{},{}'.format(long, lat, alt)
        ET.SubElement(punto, 'altitudeMode').text = modoAltitud

    def addLineString(self, nombre, extrude, tesela, listaCoordenadas, modoAltitud, color, ancho):
        """
        Añade un elemento <Placemark> con líneas <LineString>
        """
        # Según el código del profesor, añade un <name> suelto en el document antes del placemark
        ET.SubElement(self.doc, 'name').text = nombre
        pm = ET.SubElement(self.doc, 'Placemark')
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls, 'extrude').text = extrude
        ET.SubElement(ls, 'tessellation').text = tesela
        ET.SubElement(ls, 'coordinates').text = listaCoordenadas
        ET.SubElement(ls, 'altitudeMode').text = modoAltitud

        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement(linea, 'color').text = color
        ET.SubElement(linea, 'width').text = ancho

    def escribir(self, nombreArchivoKML):
        """
        Escribe el archivo KML con declaración y codificación
        """
        arbol = ET.ElementTree(self.raiz)
        """
        Introduce indentación y saltos de línea para generar XML en modo texto
        (Solo funciona bien en versiones modernas de Python, en antiguas puede requerir minidom)
        """
        if hasattr(ET, 'indent'):
            ET.indent(arbol)
        arbol.write(nombreArchivoKML, encoding='utf-8', xml_declaration=True)


class EtapaXmlReader:
    """
    Clase encargada de leer el archivo etapaEsquema.xml usando XPath
    """

    # Altitud absoluta: los valores del XML son cota real sobre el nivel
    # del mar, no altura sobre el terreno en ese punto concreto.
    MODO_ALTITUD = "absolute"

    def __init__(self, archivo_xml):
        self.tree = ET.parse(archivo_xml)
        self.root = self.tree.getroot()
        self.ns = {"v": "http://www.uniovi.es"}

    def _extraer_coordenadas(self, nodo):
        lon = nodo.find("v:longitud_coord", self.ns).text
        lat = nodo.find("v:latitud_coord", self.ns).text
        alt = nodo.find("v:altitud_coord", self.ns).text
        return lon, lat, alt

    def procesar_etapa(self, kml_generator):
        """
        Extrae los datos y llama a los métodos del generador KML.
        """
        # Variable para almacenar las coordenadas y luego dibujar la línea
        coordenadas_linea = ""

        # 1. Salida (rojo)
        salida = self.root.find("v:salida_coord", self.ns)
        lon, lat, alt = self._extraer_coordenadas(salida)
        kml_generator.addPlacemark(
            "Salida, Plaza del Casino", "Inicio de la etapa", lon, lat, alt,
            self.MODO_ALTITUD, Kml.COLOR_ROJO
        )
        coordenadas_linea += f"{lon},{lat},{alt}\n"

        # 2. Hitos (iterados en orden)
        hitos = self.root.find("v:hitos", self.ns)
        if hitos is not None:
            for hito in hitos:
                tag = hito.tag.split('}')[-1]
                if tag == "puerto":
                    nombre = "Puerto: " + hito.find("v:nombre_puerto", self.ns).text
                    color = Kml.COLOR_VERDE
                elif tag == "sprint":
                    nombre = "Sprint: " + hito.find("v:nombre_sprint", self.ns).text
                    color = Kml.COLOR_AZUL
                else:
                    nodo_nombre = hito.find("v:nombre_punto", self.ns)
                    nombre = "Punto: " + nodo_nombre.text if nodo_nombre is not None else "Punto anónimo"
                    color = Kml.COLOR_AMARILLO

                lon, lat, alt = self._extraer_coordenadas(hito)
                kml_generator.addPlacemark(
                    nombre, tag.capitalize(), lon, lat, alt,
                    self.MODO_ALTITUD, color
                )
                coordenadas_linea += f"{lon},{lat},{alt}\n"

        # 3. Llegada (rojo)
        llegada = self.root.find("v:llegada_coord", self.ns)
        lon, lat, alt = self._extraer_coordenadas(llegada)
        kml_generator.addPlacemark(
            "Llegada", "Fin de la etapa", lon, lat, alt,
            self.MODO_ALTITUD, Kml.COLOR_ROJO
        )
        coordenadas_linea += f"{lon},{lat},{alt}\n"

        # 4. Trazado de la etapa (Línea)
        # Quitamos el último salto de línea
        coordenadas_linea = coordenadas_linea.strip()

        kml_generator.addLineString(
            nombre="Ruta Etapa",
            extrude="1",
            tesela="1",
            listaCoordenadas=coordenadas_linea,
            modoAltitud=self.MODO_ALTITUD,
            color=Kml.COLOR_ROJO,
            ancho="5"
        )

    @staticmethod
    def ejecutar(archivo_entrada="etapaEsquema.xml", archivo_salida="etapa.kml"):
        """
        Punto de entrada del programa: lee el XML, genera el KML y lo escribe.
        Movido a método de clase para que el programa sea totalmente orientado
        a objetos (ninguna función suelta a nivel de módulo).
        """
        print("Iniciando generación de KML a partir de XML...")

        # 1. Instanciamos la clase del profesor para crear el KML
        nuevoKML = Kml()

        # 2. Instanciamos el lector de nuestro XML
        lector_xml = EtapaXmlReader(archivo_entrada)

        # 3. Procesamos el XML y rellenamos el objeto KML
        lector_xml.procesar_etapa(nuevoKML)

        # 4. Escribimos el archivo final
        nuevoKML.escribir(archivo_salida)
        print("Creado el archivo: ", archivo_salida)


if __name__ == "__main__":
    EtapaXmlReader.ejecutar()