/**
 * Setup simplest popover possible to provide popovers.
 *
 * Mostly follows https://floating-ui.com/docs/tutorial
 */
import { computePosition, flip, shift, offset, arrow } from "@floating-ui/dom";
import "./clipboard.css";

/**
 * Setup trigger element to toggle showing / hiding clipboard element
 * @param {Element} trigger
 * @param {Element} clipboard
 * @param {Array[Element]} closers array of elements that should close the clipboard if clicked
 */
export function setupClipboard(trigger, clipboard, closers) {
  const arrowElement = clipboard.querySelector(".arrow");
  function updatePosition() {
    computePosition(trigger, clipboard, {
      placement: "bottom",
      middleware: [
        offset(6),
        flip(),
        shift({ padding: 5 }),
        arrow({ element: arrowElement }),
      ],
    }).then(({ x, y, placement, middlewareData }) => {
      Object.assign(clipboard.style, {
        left: `${x}px`,
        top: `${y}px`,
      });

      // Accessing the data
      const { x: arrowX, y: arrowY } = middlewareData.arrow;

      const staticSide = {
        top: "bottom",
        right: "left",
        bottom: "top",
        left: "right",
      }[placement.split("-")[0]];

      Object.assign(arrowElement.style, {
        left: arrowX != null ? `${arrowX}px` : "",
        top: arrowY != null ? `${arrowY}px` : "",
        right: "",
        bottom: "",
        [staticSide]: "-4px",
      });
    });
  }

  trigger.addEventListener("click", (e) => {
    clipboard.classList.toggle("hidden");
    trigger.classList.toggle("active");
    updatePosition();
    e.preventDefault();
    e.stopPropagation();
  });

  // If the clipboard is clicked this should not be passed to the desktop
  clipboard.addEventListener("click", (e) => {
    e.stopPropagation();
  });
  // Close the popup if we click outside it
  closers.forEach((el) => {
    el.addEventListener("click", () => {
      if (trigger.classList.contains("active")) {
        clipboard.classList.toggle("hidden");
        trigger.classList.toggle("active");
      }
    });
  });
}
