class Ciudad {
    // Atributos públicos
    nombre;
    pais;
    gentilicio;
    cantidad_poblacion;
    coordenadas_centro; 

    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre; 
        this.pais = pais; 
        this.gentilicio = gentilicio; 
    }

    rellenarAtributos(poblacion, coordenadas) {
        this.cantidad_poblacion = poblacion; 
        this.coordenadas_centro = coordenadas; 
    }   

    getCiudad() {
        return this.nombre; 
    }

    getPais() {
        return this.pais; 
    }

    getInformacionSecundaria() {
        return `<ul>
            <li>Gentilicio: ${this.gentilicio}</li>
            <li>Población: ${this.cantidad_poblacion}</li>
        </ul>`; 
    }

    escribeCoordenadas() {
        const primeraSeccion = document.querySelector("section"); 
        if (primeraSeccion) {
            const parrafo = document.createElement("p"); 
            parrafo.textContent = `Coordenadas: ${this.coordenadas_centro}`; 
            primeraSeccion.appendChild(parrafo); 
        }
    }
}

// Instanciación del objeto
const miCiudad = new Ciudad("Mónaco", "Principado de Mónaco", "Monegasco");
miCiudad.rellenarAtributos(39150, "43.7384° N, 7.4246° E");

// Crear elemento <section> y encabezado <h3>
const nuevaSeccion = document.createElement('section');
nuevaSeccion.className = "informacion";
const encabezadoH3 = document.createElement('h3'); 
encabezadoH3.textContent = `${miCiudad.getCiudad()} - ${miCiudad.getPais()}`;

// Añadir <h3> e información secundaria a la sección
nuevaSeccion.appendChild(encabezadoH3); 
nuevaSeccion.insertAdjacentHTML("beforeend", miCiudad.getInformacionSecundaria()); 

// Buscar el <h2> de meteorología
const encabezadosH2 = document.querySelectorAll("h2"); 
let h2Meteorologia = null; 

encabezadosH2.forEach(h2 => { 
    const texto = h2.textContent.toLowerCase();
    if (texto.includes("meteorología") || texto.includes("meteorologia")) {
        h2Meteorologia = h2;
    }
});

// Insertar la sección tras el <h2>
if (h2Meteorologia) {
    h2Meteorologia.insertAdjacentElement("afterend", nuevaSeccion); 
}

// Añadir coordenadas como párrafo final
miCiudad.escribeCoordenadas(); 