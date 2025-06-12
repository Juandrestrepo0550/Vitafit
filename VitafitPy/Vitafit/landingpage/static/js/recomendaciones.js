document.addEventListener("DOMContentLoaded", () => {
  const toggleChatBtn = document.getElementById("toggleChat");
  const chatWidget = document.getElementById("chatWidget");
  const closeChatBtn = document.getElementById("closeChat");
  const minimizeChatBtn = document.getElementById("minimizeChat");
  const chatbox = document.getElementById("chatbox");
  const input = document.getElementById("userInput");

  toggleChatBtn.addEventListener("click", () => {
    chatWidget.classList.toggle("hidden");
  });

  closeChatBtn.addEventListener("click", () => {
    chatWidget.classList.add("hidden");
  });

  minimizeChatBtn.addEventListener("click", () => {
    chatbox.classList.toggle("hidden");
  });

  window.enviarMensaje = function () {
    const mensaje = input.value.trim();
    if (!mensaje) return;

    agregarMensaje("Tú", mensaje);
    input.value = "";

    setTimeout(() => {
      const respuesta = generarRespuesta(mensaje);
      agregarMensaje("Asistente", respuesta);
    }, 800);
  };

  function agregarMensaje(remitente, texto) {
    const burbuja = document.createElement("div");

    if (remitente === "Tú") {
      // Estilo para el mensaje del usuario
      burbuja.className =
        "p-2 rounded-lg max-w-[75%] bg-white text-black self-end ml-auto shadow";
    } else {
      // Estilo para el asistente
      burbuja.className =
        "p-2 rounded-lg max-w-[75%] bg-green-600 bg-opacity-70 text-white self-start shadow";
    }

    burbuja.innerHTML = `<strong>${remitente}:</strong> ${texto}`;

    const contenedor = document.createElement("div");
    contenedor.className = "flex flex-col";
    contenedor.appendChild(burbuja);

    chatbox.appendChild(contenedor);
    chatbox.scrollTop = chatbox.scrollHeight;
  }

  function generarRespuesta(mensaje) {
    const respuestas = [
      "Recuerda mantenerte hidratado.",
      "Haz al menos 30 minutos de ejercicio al día.",
      "Incluye frutas y verduras en cada comida.",
      "Dormir bien es clave para tu salud.",
    ];
    return respuestas[Math.floor(Math.random() * respuestas.length)];
  }
});
