class Buscador {
    // Atributos públicos
    lupa;
    campo;

    constructor() {
        this.lupa = document.querySelector("search label img");
        this.campo = document.querySelector("search input");

        if (this.lupa) {
            this.lupa.addEventListener("click", this.buscar.bind(this));
        }
        if (this.campo) {
            this.campo.addEventListener("keypress", (evento) => {
                if (evento.key === "Enter") {
                    this.buscar();
                }
            });
        }
    }

    buscar() {
        this.limpiar_busqueda();

        const resultados = [];
        const texto = this.campo.value.trim();
        if (texto === "") {
            return;
        }

        // 1) Expresión regular global e insensible a mayúsculas/minúsculas.
        //    Se escapan los caracteres especiales para buscar el texto tal cual.
        const textoEscapado = texto.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
        const regexp = new RegExp(textoEscapado, "gi");

        // 2) Nodos de texto del body
        const recorrido = document.createTreeWalker(document.querySelector("body"), NodeFilter.SHOW_TEXT);

        // 3) Primer nodo
        let nodo = recorrido.nextNode();

        // 4) Se guardan los nodos cuyo texto contiene la búsqueda
        while (nodo) {
            regexp.lastIndex = 0; // test() con 'g' recuerda la última posición
            if (regexp.test(nodo.textContent)) {
                resultados.push(nodo);
            }
            nodo = recorrido.nextNode();
        }

        // 5) Se resalta cada aparición con <mark>.
        //    Se sustituye solo el nodo de texto (no el innerHTML del padre)
        //    para no perder los elementos hermanos, como enlaces o imágenes.
        resultados.forEach(nodoTexto => {
            const fragmento = document.createDocumentFragment();
            let ultimaPosicion = 0;
            for (const coincidencia of nodoTexto.textContent.matchAll(regexp)) {
                fragmento.append(nodoTexto.textContent.slice(ultimaPosicion, coincidencia.index));
                const marca = document.createElement("mark");
                marca.textContent = coincidencia[0];
                fragmento.append(marca);
                ultimaPosicion = coincidencia.index + coincidencia[0].length;
            }
            fragmento.append(nodoTexto.textContent.slice(ultimaPosicion));
            nodoTexto.replaceWith(fragmento);
        });
    }

    limpiar_busqueda() {
        document.querySelectorAll("mark").forEach(marca => {
            marca.replaceWith(document.createTextNode(marca.textContent));
        });
        document.body.normalize();
    }
}

const buscador = new Buscador();
