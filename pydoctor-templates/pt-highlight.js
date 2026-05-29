// Lua syntax highlighting for the generated API reference.
//
// pydoctor's `code` / `code-block` directives discard the language and render
// every example as a plain reStructuredText literal block
// (`<pre class="rst-literal-block">`). Every code example on this site is Lua,
// so we wrap each literal block's text in a `<code class="language-lua">` and
// let highlight.js tokenize it. Wrapping in `<code>` matches the highlight.js
// theme selectors (`pre code.hljs`).
(function () {
  "use strict";
  function highlightLua() {
    if (typeof hljs === "undefined") return;
    var blocks = document.querySelectorAll("pre.rst-literal-block");
    for (var i = 0; i < blocks.length; i++) {
      var pre = blocks[i];
      if (pre.dataset.luaHighlighted) continue;
      var code = document.createElement("code");
      code.className = "language-lua";
      code.textContent = pre.textContent; // textContent keeps the raw source
      pre.textContent = "";
      pre.appendChild(code);
      hljs.highlightElement(code);
      pre.dataset.luaHighlighted = "1";
    }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", highlightLua);
  } else {
    highlightLua();
  }
})();
