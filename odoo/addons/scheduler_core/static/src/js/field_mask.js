/** @odoo-module **/

import { registry } from "@web/core/registry";
import { CharField } from "@web/views/fields/char/char_field";

// garante que o Inputmask global seja carregado
if (typeof window.Inputmask === "undefined" && typeof Inputmask !== "undefined") {
    window.Inputmask = Inputmask;
}

export class FieldMask extends CharField {
    setup() {
        super.setup();
    }

    mounted() {
        super.mounted();

        const mask = this.el.dataset.mask || "999.999.999-99";  // CPF default

        if (window.Inputmask) {
            window.Inputmask({ mask }).mask(this.el.querySelector("input"));
        } else {
            console.warn("Inputmask não encontrado no contexto global!");
        }
    }
}

registry.category("fields").add("mask", FieldMask);
