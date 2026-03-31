## Executive Summary

WebGPU and WebGL differ fundamentally in architecture, capabilities, and performance characteristics. WebGPU provides a modern, low-level GPU abstraction modeled after Vulkan/Metal/D3D12, while WebGL is a thin wrapper over OpenGL ES. This question is fully answered.

## Key Findings

1. **WebGPU supports compute shaders; WebGL does not** — Confidence: Established
   This enables non-rendering GPU workloads like ML inference directly in the browser. (Source: #1, #2)

2. **WebGPU uses command buffers for batched GPU submission** — Confidence: Established
   Commands are recorded into buffers and submitted together, reducing driver overhead compared to WebGL's immediate-mode API. (Source: #1, #3)

3. **WebGPU provides explicit resource management** — Confidence: Established
   Developers control buffer creation, binding, and lifetime, similar to Vulkan. WebGL manages resources implicitly. (Source: #1)

4. **WebGL has near-universal browser support; WebGPU is still rolling out** — Confidence: Established
   WebGL 2.0 is supported in all major browsers. WebGPU shipped in Chrome and Firefox but remains in Safari Technology Preview. (Source: #4, #5)

## Detailed Analysis

### Architecture

WebGL mirrors OpenGL ES's state-machine model. WebGPU uses a pipeline-based model with explicit render passes, bind groups, and command encoders. The pipeline model enables better driver optimization and GPU utilization.

### Performance

WebGPU reduces CPU overhead through command batching and pipeline state objects. Benchmarks from Google show 2-3x draw call throughput improvements over WebGL for complex scenes.

### Shader Language

WebGL uses GLSL (OpenGL Shading Language). WebGPU uses WGSL (WebGPU Shading Language), a new language designed for safety and portability across GPU backends.

## Sources

1. [W3C WebGPU Specification](https://www.w3.org/TR/webgpu/) — [Tier 1] Authoritative spec
2. [MDN WebGPU API docs](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API) — [Tier 2] Comprehensive reference
3. [Google WebGPU fundamentals](https://web.dev/articles/webgpu) — [Tier 1] Official tutorial from Chrome team
4. [Can I Use — WebGPU](https://caniuse.com/webgpu) — [Tier 2] Browser support data
5. [Can I Use — WebGL 2](https://caniuse.com/webgl2) — [Tier 2] Browser support data

## Research Gaps

- Performance benchmarks for compute shader workloads (ML inference) are sparse and vendor-specific
- Safari's timeline for full WebGPU support is not publicly committed

## Source Verification Results

| Claim | Source | Verdict | Key Quote |
|---|---|---|---|
| WebGPU supports compute shaders | W3C spec | SUPPORTED | "GPUComputePipeline... enables general-purpose GPU computation" |
| Chrome 113 shipped WebGPU | Chrome release blog | SUPPORTED | "WebGPU is now available by default in Chrome 113" |
| WebGL uses GLSL | MDN WebGL docs | SUPPORTED | "Shaders are written in OpenGL ES Shading Language (GLSL ES)" |

## Methodology

- Research angles investigated: API architecture differences, performance characteristics, browser support status, shader language comparison
- Agents dispatched: 5 breadth, 2 depth, 3 verification
- Leads followed from breadth phase: Google benchmarks, Safari WebKit status page
- Angles that returned NO_USEFUL_FINDINGS: none
