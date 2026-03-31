## Executive Summary

WebGPU is a modern graphics API for the web that provides low-level GPU access, succeeding WebGL. This question is fully answered by available documentation.

## Key Findings

1. **WebGPU is a W3C standard providing low-level GPU access in browsers** — Confidence: Established
   It exposes GPU compute and rendering capabilities with an API modeled after Vulkan, Metal, and Direct3D 12. (Source: #1, #2)

2. **WebGPU shipped in Chrome 113 (May 2023) and Firefox 141 (early 2025)** — Confidence: Established
   Safari support remains in Technology Preview. (Source: #1, #3)

3. **WebGPU supports compute shaders, which WebGL does not** — Confidence: Established
   This enables GPU-accelerated ML inference, physics simulations, and other non-rendering workloads in the browser. (Source: #2)

## Sources

1. [WebGPU specification](https://www.w3.org/TR/webgpu/) — [Tier 1] W3C specification, primary reference
2. [MDN WebGPU documentation](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) — [Tier 2] Comprehensive API reference
3. [Chrome 113 release notes](https://developer.chrome.com/blog/webgpu-release) — [Tier 1] Official announcement
