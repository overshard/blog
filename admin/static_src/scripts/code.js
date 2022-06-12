import CodeMirror from "codemirror/lib/codemirror.js";

// import "codemirror/mode/python/python.js";
// import "codemirror/mode/javascript/javascript.js";
// import "codemirror/mode/htmlmixed/htmlmixed.js";
// import "codemirror/mode/css/css.js";
// import "codemirror/mode/shell/shell.js";

import "codemirror/lib/codemirror.css";
import "codemirror/theme/material.css";

const initCodeMirror = (codeBlocks) => {
  for (let i = 0; i < codeBlocks.length; i++) {
    const codeBlock = codeBlocks[i];
    if (codeBlock.innerHTML === "Code") {
      let parentDiv = codeBlock.parentElement;
      while (parentDiv.className !== "c-sf-block") {
        parentDiv = parentDiv.parentElement;
      }

      const textarea = parentDiv.querySelector("textarea");
      if (!textarea.dataset.cmInitialized) {
        setTimeout(() => {
          CodeMirror.fromTextArea(textarea, {
            theme: "material",
            lineNumbers: true,
            lineWrapping: true,
            viewportMargin: Infinity,
            // mode: "javascript",
          });
        }, 100);
        textarea.dataset.cmInitialized = "true";
      }
    }
  }
};

document.addEventListener("DOMContentLoaded", () => {
  const codeBlocks = document.querySelectorAll(".c-sf-block__type");
  initCodeMirror(codeBlocks);

  var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      const codeBlocks = mutation.target.querySelectorAll(".c-sf-block__type");
      initCodeMirror(codeBlocks);
    });
  });

  observer.observe(
    document.querySelector("[data-contentpath='body']"),
    { childList: true, subtree: true }
  );
});
