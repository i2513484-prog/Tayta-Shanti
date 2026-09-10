function buscarDocumento() {
    let tipoDoc = document.getElementById("tipo_doc");
    let numeroDoc = document.getElementById("numero_doc");
    let nombreInput = document.getElementById("nombre");
    let nombreCompletoInput = document.getElementById("nombre_completo");

    if (!tipoDoc || !numeroDoc || !nombreInput || !nombreCompletoInput) {
        return;
    }

    let tipo = tipoDoc.value;
    let numero = numeroDoc.value.replace(/\D/g, "");

    if (numeroDoc.value !== numero) {
        numeroDoc.value = numero;
    }

    if ((tipo === "dni" && numero.length !== 8) || (tipo === "ruc" && numero.length !== 11)) {
        nombreInput.value = "";
        nombreCompletoInput.value = "";
        return;
    }

    // 🔵 DNI
    if (tipo === "dni") {
        fetch("/api/dni", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({dni: numero})
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            let nombre = (data.nombres || "") + " " + (data.apellidoPaterno || "") + " " + (data.apellidoMaterno || "");
            nombre = nombre.trim();

            nombreInput.value = nombre;
            nombreCompletoInput.value = nombre;
        })
        .catch(error => console.error("Error consultando DNI:", error));
    }

    // 🟢 RUC
    if (tipo === "ruc") {
        fetch("/api/ruc", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ruc: numero})
        })
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
                return;
            }

            let razon = data.razonSocial || "";

            nombreInput.value = razon;
            nombreCompletoInput.value = razon;
        })
        .catch(error => console.error("Error consultando RUC:", error));
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let tipoDoc = document.getElementById("tipo_doc");
    let numeroDoc = document.getElementById("numero_doc");

    if (tipoDoc) {
        tipoDoc.addEventListener("change", buscarDocumento);
    }

    if (numeroDoc) {
        numeroDoc.addEventListener("input", buscarDocumento);
    }
});

let slides = document.querySelectorAll(".slide");
let index = 0;

function cambiarBanner() {
    if (slides.length === 0) {
        return;
    }

    slides[index].classList.remove("active");

    index++;
    if (index >= slides.length) {
        index = 0;
    }

    slides[index].classList.add("active");
}

if (slides.length > 0) {
    setInterval(cambiarBanner, 4000);
}
