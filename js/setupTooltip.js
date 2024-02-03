import { computePosition, flip, shift, offset, arrow } from "@floating-ui/dom";

/**
 *
 * @param {Element} button
 * @param {Element} tooltip
 */
export function setupTooltip(button, tooltip) {
  const arrowElement = document.querySelector(".arrow");
  function updatePosition() {
    computePosition(button, tooltip, {
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
  function toggleTooltip() {
    if (tooltip.style.display === "block") {
      tooltip.style.display = "none";
    } else {
      tooltip.style.display = "block";
    }
    updatePosition();
  }

  function hideTooltip() {
    tooltip.style.display = "";
  }

  [
    ["click", toggleTooltip],
    ["blur", hideTooltip],
  ].forEach(([event, listener]) => {
    button.addEventListener(event, listener);
  });
}
