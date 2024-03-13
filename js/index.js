/**
 * Derived from https://github.com/novnc/noVNC/blob/v1.4.0/vnc_lite.html, which was licensed
 * under the 2-clause BSD license
 */

import "reset-css";
import "./index.css";

// RFB holds the API to connect and communicate with a VNC server
import RFB from "@novnc/novnc/core/rfb";

import { setupTooltip } from "./tooltip.js";

// Show a status text in the top bar
function setStatusText(text) {
  document.getElementById("status").textContent = text;
}

// This page is served under the /desktop/, and the websockify websocket is served
// under /desktop-websockify/ with the same base url as /desktop/. We resolve it relatively
// this way.
let websockifyUrl = new URL("../desktop-websockify/", window.location);
websockifyUrl.protocol = window.location.protocol === "https:" ? "wss" : "ws";

/**
 * Setup two way clipboard sync with the given rfb
 *
 * @param {RFB} rfb
 */
function setupClipboardSync(rfb) {
  const clipboardText = document.getElementById("clipboard-text");

  // Listen for clipboard events on the remote system, and automatically
  // update our local textarea with those values
  rfb.addEventListener("clipboard", (e) => {
    clipboardText.value = e.detail.text;
  });

  const clipboardClientChange = () => {
    const text = clipboardText.value;
    rfb.clipboardPasteFrom(text);
  };
  rfb.addEventListener("connect", () => {
    console.log("connecting clipboard sync");
    clipboardText.addEventListener("change", clipboardClientChange);
  });
  rfb.addEventListener("disconnect", () => {
    console.log("disconnecting clipboard sync");
    clipboardText.removeEventListener("change", clipboardClientChange);
  });
}

function connect() {
  // Creating a new RFB object will start a new connection
  const rfb = new RFB(
    document.getElementById("screen"),
    websockifyUrl.toString(),
    {},
  );

  // Update status when connection is made or broken
  rfb.addEventListener("connect", () => {
    console.log("connected");
    setStatusText("Connected");
  });
  rfb.addEventListener("disconnect", () => {
    console.log("disconnected");
    let countDown = 5;
    setStatusText(`Reconnecting in ${countDown}s`);
    const intervalHandle = setInterval(() => {
      countDown -= 1;
      setStatusText(`Reconnecting in ${countDown}s`);
      console.log(countDown);
      if (countDown === 0) {
        clearInterval(intervalHandle);
        connect();
      }
    }, 1000);
  });

  // Scale our viewport so the user doesn't have to scroll
  rfb.scaleViewport = true;

  // Use a CSS variable to set background color
  rfb.background = "var(--jupyter-medium-dark-grey)";
  setupClipboardSync(rfb);
}

connect();

setupTooltip(
  document.getElementById("clipboard-button"),
  document.getElementById("clipboard-container"),
);
