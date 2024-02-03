/**
 * Derived from https://github.com/novnc/noVNC/blob/v1.4.0/vnc_lite.html, which was licensed
 * under the 2-clause BSD license
 */

// RFB holds the API to connect and communicate with a VNC server
import RFB from "@novnc/novnc/core/rfb";

// When this function is called we have successfully connected to a server
function connectedToServer() {
  status("Connected!");
}

// This function is called when we are disconnected
function disconnectedFromServer(e) {
  if (e.detail.clean) {
    status("Disconnected");
  } else {
    status("Something went wrong, connection is closed");
  }
}

// Show a status text in the top bar
function status(text) {
  document.getElementById("status").textContent = text;
}

// Construct the websockify websocket URL we want to connect to
let websockifyUrl = new URL("websockify", window.location);
websockifyUrl.protocol = window.location.protocol === "https" ? "wss" : "ws";

// Creating a new RFB object will start a new connection
const rfb = new RFB(
  document.getElementById("screen"),
  websockifyUrl.toString(),
  {},
);

// Add listeners to important events from the RFB module
rfb.addEventListener("connect", connectedToServer);
rfb.addEventListener("disconnect", disconnectedFromServer);

// Scale our viewport so the user doesn't have to scroll
rfb.scaleViewport = true;

// Clipboard
function toggleClipboardPanel() {
  document
    .getElementById("noVNC_clipboard_area")
    .classList.toggle("noVNC_clipboard_closed");
}
document
  .getElementById("noVNC_clipboard_button")
  .addEventListener("click", toggleClipboardPanel);

function clipboardReceive(e) {
  document.getElementById("noVNC_clipboard_text").value = e.detail.text;
}
rfb.addEventListener("clipboard", clipboardReceive);

function clipboardSend() {
  const text = document.getElementById("noVNC_clipboard_text").value;
  rfb.clipboardPasteFrom(text);
}
document
  .getElementById("noVNC_clipboard_text")
  .addEventListener("change", clipboardSend);
