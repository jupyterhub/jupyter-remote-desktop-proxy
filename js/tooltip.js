/**
 * Setup simplest popover possible to provide popovers.
 *
 * Mostly follows https://floating-ui.com/docs/tutorial
 */
import { computePosition, flip, shift, offset, arrow } from "@floating-ui/dom";
import "./tooltip.css";

/**
 * Setup trigger element to toggle showing / hiding tooltip element
 * @param {Element} trigger
 * @param {Element} tooltip
 */
export function setupTooltip(trigger, tooltip) {
  const arrowElement = tooltip.querySelector(".arrow");
  function updatePosition() {
    computePosition(trigger, tooltip, {
      placement: "bottom",
      middleware: [
        offset(6),
        flip(),
        shift({ padding: 5 }),
        arrow({ element: arrowElement }),
      ],
    }).then(({ x, y, placement, middlewareData }) => {
      Object.assign(tooltip.style, {
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
    tooltip.classList.toggle("hidden");
    trigger.classList.toggle("active");
    updatePosition();
    e.preventDefault();
  });
}
