/**
 * Derived from https://github.com/novnc/noVNC/blob/v1.4.0/vnc_lite.html, which was licensed
 * under the 2-clause BSD license
 */

import "reset-css";
import "./index.css";

// RFB holds the API to connect and communicate with a VNC server
import RFB from "@novnc/novnc/lib/rfb";

import { setupClipboard } from "./clipboard.js";

const maxRetryCount = 5;
const retryInterval = 3; // seconds

// When this function is called we have successfully connected to a server
function connectedToServer() {
  status("Connected");
}

// This function is called when we are disconnected
function disconnectedFromServer(e) {
  if (e.detail.clean) {
    status("Disconnected");
  } else {
    status("Something went wrong, connection is closed");
    if (retryCount < maxRetryCount) {
      status(`Reconnecting in ${retryInterval} seconds`);
      setTimeout(() => {
        connect();
        retryCount++;
      }, retryInterval * 1000);
    } else {
      status("Failed to connect, giving up");
    }
  }
}

// Show a status text in the top bar
function status(text) {
  document.getElementById("status").textContent = text;
}

// This page is served under the /desktop/, and the websockify websocket is served
// under /desktop-websockify/ with the same base url as /desktop/. We resolve it relatively
// this way.
let websockifyUrl = new URL("../desktop-websockify/", window.location);
websockifyUrl.protocol = window.location.protocol === "https:" ? "wss" : "ws";

let retryCount = 0;

function connect() {
  // Creating a new RFB object will start a new connection
  let rfb = new RFB(
    document.getElementById("screen"),
    websockifyUrl.toString(),
    {},
  );

  // Add listeners to important events from the RFB module
  rfb.addEventListener("connect", connectedToServer);
  rfb.addEventListener("disconnect", disconnectedFromServer);

  // Resize our viewport so the user doesn't have to scroll
  rfb.resizeSession = true;

  // Use a CSS variable to set background color
  rfb.background = "var(--jupyter-medium-dark-grey)";

  // Clipboard
  function clipboardReceive(e) {
    document.getElementById("clipboard-text").value = e.detail.text;
  }
  rfb.addEventListener("clipboard", clipboardReceive);

  function clipboardSend() {
    const text = document.getElementById("clipboard-text").value;
    rfb.clipboardPasteFrom(text);
  }
  document
    .getElementById("clipboard-text")
    .addEventListener("change", clipboardSend);

  setupClipboard(
    document.getElementById("clipboard-button"),
    document.getElementById("clipboard-container"),
    [document.body, document.getElementsByTagName("canvas")[0]],
  );
}

// Start the connection
connect();
