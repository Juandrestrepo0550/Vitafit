document.addEventListener("DOMContentLoaded", () => {
  const toggleChatBtn = document.getElementById("toggleChat");
  const chatWidget = document.getElementById("chatWidget");
  const closeChatBtn = document.getElementById("closeChat");
  const chatbox = document.getElementById("chatbox");
  const input = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn"); // Asegúrate que tu botón tenga este ID en el HTML

  // Función para obtener el token CSRF desde las cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const csrftoken = getCookie("csrftoken");

  // Mostrar/Ocultar el chat
  toggleChatBtn.addEventListener("click", () => {
    chatWidget.classList.toggle("hidden");
  });

  // Cerrar chat
  closeChatBtn.addEventListener("click", () => {
    chatWidget.classList.add("hidden");
  });

  // Enviar mensaje con botón
  sendBtn.addEventListener("click", enviarMensaje);

  // Enviar mensaje con Enter
  input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      enviarMensaje();
    }
  });

  // Función principal para enviar mensaje
  async function enviarMensaje() {
    const mensaje = input.value.trim();
    if (!mensaje) return;

    agregarMensaje("Tú", mensaje);
    input.value = "";

    try {
      const response = await fetch("/app.com/api/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrftoken,
          "X-Requested-With": "XMLHttpRequest",
        },
        body: JSON.stringify({ mensaje: mensaje }),
      });

      const data = await response.json();

      if (data && data.respuesta) {
        agregarMensaje("Asistente", data.respuesta);
      } else if (data.error) {
        agregarMensaje("Asistente", "⚠️ " + data.error);
      } else {
        agregarMensaje("Asistente", "No se recibió respuesta válida del servidor.");
      }
    } catch (error) {
      console.error("Error al enviar mensaje:", error);
      agregarMensaje("Asistente", "Hubo un error de conexión.");
    }
  }

  function agregarMensaje(remitente, texto) {
    const burbuja = document.createElement("div");

    burbuja.className =
      remitente === "Tú"
        ? "p-2 rounded-lg max-w-[75%] bg-white text-black self-end ml-auto shadow"
        : "p-2 rounded-lg max-w-[75%] bg-green-600 bg-opacity-70 text-white self-start shadow";

    burbuja.innerHTML = `<strong>${remitente}:</strong> ${texto}`;

    const contenedor = document.createElement("div");
    contenedor.className = "flex flex-col";
    contenedor.appendChild(burbuja);

    chatbox.appendChild(contenedor);
    chatbox.scrollTop = chatbox.scrollHeight;
  }
});
