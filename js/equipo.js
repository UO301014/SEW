class Ciclista {
    // Atributos públicos
    dorsal;
    nombre;
    apellidos;
    nacionalidad;
    nacionalidadCodigo;
    fechaNacimiento;

    constructor(dorsal, nombre, apellidos, nacionalidad, nacionalidadCodigo, fechaNacimiento) {
        this.dorsal = dorsal;
        this.nombre = nombre;
        this.apellidos = apellidos;
        this.nacionalidad = nacionalidad;
        this.nacionalidadCodigo = nacionalidadCodigo;
        this.fechaNacimiento = fechaNacimiento;
    }

    getNombreCompleto() {
        return `${this.nombre} - ${this.apellidos}`;
    }

    getDorsal() {
        return this.dorsal;
    }

    getInformacionAdicional() {
        return `${this.fechaNacimiento}, ${this.nacionalidad}`;
    }
}

class Equipo {
    // Atributos públicos
    nombreEquipo;
    codigoEquipo;
    paisEquipo;
    nombreDirector;
    categoria;
    direccionWeb;
    alineacion;

    constructor(nombre, codigo, pais) {
        this.nombreEquipo = nombre;
        this.codigoEquipo = codigo;
        this.paisEquipo = pais;
        this.alineacion = [];
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

    // Lee el fichero JSON y se queda con la información de este equipo
    async leerEquipo() {
        const respuesta = await fetch("js/lavuelta.json");
        const datos = await respuesta.json();
        const equipo = datos.equipos.find(e => e.codigo_uci === this.codigoEquipo);
        if (equipo) {
            this.alinearCiclistas(equipo);
        }
    }

    // Crea un objeto Ciclista por cada corredor del equipo
    alinearCiclistas(equipo) {
        equipo.corredores.forEach(corredor => {
            this.alineacion.push(new Ciclista(
                corredor.dorsal,
                corredor.nombre,
                corredor.apellidos,
                corredor.nacionalidad,
                corredor.nacionalidad_codigo,
                corredor.fecha_nacimiento
            ));
        });
    }

    // Añade la alineación, ordenada por dorsal, a la sección de corredores
    mostrarAlineacion() {
        const seccionAlineacion = document.querySelector("main section:last-of-type");
        if (!seccionAlineacion) {
            return;
        }
        const ordenados = [...this.alineacion].sort((a, b) => a.getDorsal() - b.getDorsal());
        ordenados.forEach(ciclista => {
            const articulo = `<article>
                <h4>${ciclista.getNombreCompleto()}</h4>
                <img src="multimedia/icono_cilcista.png" alt="Icono de corredor" />
                <p>Dorsal ${ciclista.getDorsal()}</p>
                <p>${ciclista.getInformacionAdicional()}</p>
            </article>`;
            seccionAlineacion.insertAdjacentHTML("beforeend", articulo);
        });
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

// Leer la alineación real del JSON y mostrarla después del enlace
miEquipo.leerEquipo().then(() => miEquipo.mostrarAlineacion());
