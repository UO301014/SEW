class Formulario {
    // Atributos públicos
    puntuacion;
    dureza;
    descripcion;
    usuario;

    constructor() {
        this.puntuacion = 0;
        const boton = document.querySelector('form button[type="submit"]');
        if (boton) {
            boton.addEventListener("click", this.analizar.bind(this));
        }
    }

    analizar(event) {
        const form = event.target.closest("form");

        // Si falta algún campo obligatorio se deja que el navegador avise al usuario
        if (!form.checkValidity()) {
            return;
        }
        // El formulario no se envía: se corrige en la propia página
        event.preventDefault();

        this.puntuacion = 0;

        // Preguntas puntuables (respuestas correctas según etapa.xml)
        const numero = form.querySelector('input[name="numero-etapa"]').value;
        if (Number(numero) === 1) {
            this.puntuacion++;
        }

        const fecha = form.querySelector('input[name="fecha-etapa"]').value;
        if (fecha === "2026-08-22") {
            this.puntuacion++;
        }

        const salida = form.querySelector('select[name="ciudad-salida"]').value;
        if (salida === "Monaco") {
            this.puntuacion++;
        }

        const tipo = form.querySelector('input[name="tipo-etapa"]:checked');
        if (tipo && tipo.value === "contrarreloj individual") {
            this.puntuacion++;
        }

        const hitos = form.querySelector('input[name="hitos-etapa"]:checked');
        if (hitos && hitos.value === "sin hitos") {
            this.puntuacion++;
        }

        const longitud = form.querySelector('input[name="longitud-etapa"]').value;
        if (Number(longitud) === 9.4) {
            this.puntuacion++;
        }

        const desnivel = form.querySelector('input[name="desnivel-etapa"]').value;
        if (Number(desnivel) === 80) {
            this.puntuacion++;
        }

        // Preguntas no puntuables, necesarias para el mensaje de calificación
        this.dureza = form.querySelector('input[name="dureza-etapa"]').value;
        this.descripcion = form.querySelector('textarea[name="descripcion-etapa"]').value;
        this.usuario = form.querySelector('input[name="nombre-participante"]').value;

        this.calificar();
    }

    calificar() {
        const form = document.querySelector("form");

        // Si ya había una calificación anterior se sustituye
        const anterior = form.nextElementSibling;
        if (anterior && anterior.classList.contains("calificacion")) {
            anterior.remove();
        }

        const parrafo = document.createElement("p");
        parrafo.className = "calificacion";
        parrafo.textContent = `${this.usuario} has obtenido ${this.puntuacion} puntos, ` +
            `la dureza que has asignado a la etapa es ${this.dureza} ` +
            `y tu descripción ${this.descripcion}`;
        form.insertAdjacentElement("afterend", parrafo);
    }
}

const formulario = new Formulario();
