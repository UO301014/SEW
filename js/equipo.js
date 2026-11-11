class Equipo {
    // Atributos públicos
    nombreEquipo;
    codigoEquipo;
    paisEquipo;
    nombreDirector;
    categoria;
    direccionWeb;

    constructor(nombre, codigo, pais) {
        this.nombreEquipo = nombre;
        this.codigoEquipo = codigo;
        this.paisEquipo = pais;
    }

    rellenarAtributos(nombreDirector, categoria, direccionWeb) {
        this.nombreDirector = nombreDirector;
        this.categoria = categoria;
        this.direccionWeb = direccionWeb;
    }

    datosBasicos() {
        return `${this.nombreEquipo} - ${this.codigoEquipo}`;
    }

    getPais() {
        return this.paisEquipo;
    }

    getInformacionSecundaria() {
        return `<ul>
            <li>Director: ${this.nombreDirector}</li>
            <li>Categoría del equipo: ${this.categoria}</li>
        </ul>`;
    }

    getPaginaWeb() {
        const primeraSeccion = document.querySelector("section");
        if (primeraSeccion) {
            const parrafo = document.createElement("p");
            const enlace = document.createElement("a");
            enlace.href = this.direccionWeb;
            enlace.textContent = `Ficha de ${this.nombreEquipo} en La Vuelta`;
            parrafo.append("Página web: ", enlace);
            primeraSeccion.appendChild(parrafo);
        }
    }
}

// Instanciación del objeto
const miEquipo = new Equipo("Team Picnic-PostNL", "TPP", "Países Bajos");
miEquipo.rellenarAtributos("Phil West", "UCI WorldTeam",
    "https://www.lavuelta.es/es/equipo/TPP/team-picnic-postnl");

// Crear elemento <section> y encabezado <h3>
const nuevaSeccion = document.createElement("section");
nuevaSeccion.className = "informacion";
const encabezadoH3 = document.createElement("h3");
encabezadoH3.textContent = `${miEquipo.datosBasicos()} (${miEquipo.getPais()})`;

// Añadir <h3> e información secundaria a la sección
nuevaSeccion.appendChild(encabezadoH3);
nuevaSeccion.insertAdjacentHTML("beforeend", miEquipo.getInformacionSecundaria());

// Insertar la sección tras el <h2> del equipo (encima de la alineación)
const h2Equipo = document.querySelector("main h2");
if (h2Equipo) {
    h2Equipo.insertAdjacentElement("afterend", nuevaSeccion);
}

// Añadir el enlace a la ficha del equipo como párrafo final
miEquipo.getPaginaWeb();
