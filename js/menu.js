class Menu {
    // Atributos públicos
    boton;
    menu;

    constructor() {
        this.boton = document.querySelector("header > button");
        this.menu = document.querySelector("header nav");
        if (this.boton) {
            this.boton.addEventListener("click", this.desplegar.bind(this));
        }
    }

    desplegar() {
        const nav = document.querySelector("nav");
        const abierto = nav.classList.toggle("abierto");

        this.boton.textContent = abierto ? "x" : "☰";
        this.boton.setAttribute("aria-expanded", abierto ? "true" : "false");
        this.boton.setAttribute("aria-label",
            abierto ? "Cerrar menú de navegación" : "Abrir menú de navegación");
    }
}

const menu = new Menu();
