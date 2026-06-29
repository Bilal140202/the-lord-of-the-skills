---
name: google-antigravity-sdk-rust
description: "Design, implement, and debug autonomous AI agents and multi-agent systems in Rust using the Google Antigravity (AGY) Rust SDK. ACTIVATE this skill when the user wants to create, configure, or orchestrate Google Antigravity agents in Rust."
---

# Google Antigravity Rust SDK

This skill provides comprehensive instructions, architectural guidelines, and reference examples for building autonomous AI agents in Rust using the Google Antigravity SDK.

## Installation & Setup

Ensure the following prerequisites are met before building or running agents:

1. **Cargo Configuration**: Include the SDK dependency in your `Cargo.toml`:
   ```toml
   [dependencies]
   antigravity-sdk-rust = { path = "path/to/antigravity-sdk-rust" }
   tokio = { version = "1", features = ["full"] }
   ```
2. **API Credentials**: Set the `GEMINI_API_KEY` environment variable or supply it programmatically via `GeminiConfig`:
   * Obtain API keys from Google AI Studio: [https://aistudio.google.com/app/api-keys](https://aistudio.google.com/app/api-keys).
3. **Subprocess Harness**: Ensure the `localharness` binary is accessible either on your system `PATH` or configured via `AgentConfig::binary_path`.

---

## WebAssembly (wasm32-wasip1) Target Guidelines

When designing and deploying agents to WebAssembly targets such as `wasm32-wasip1` (e.g., inside Spin or standard WASI runtimes):

1. **Compilation Check**: Always verify clean target compilation:
   ```sh
   cargo check --target wasm32-wasip1
   ```
2. **Connection Protocol**: Be aware that process spawning is not supported inside WebAssembly sandboxes. Instead of native subprocess IPC, use the direct network socket strategy (`WasmConnectionStrategy` / `WasmConnection`) to connect to a host-side `localharness` WebSocket server.
3. **Core Async Traits**: Do NOT use the `#[async_trait]` attribute macro. The SDK uses native async traits (stable since Rust 1.75 / Rust 2024). Standard traits like `Connection`, `Hook`, `Tool`, and `Trigger` are implemented as native async traits (using `impl Future + Send` returns for trait-level `Send` bounds). For dynamic dispatch and runtime storage (e.g. `Arc<dyn DynHook>`), the SDK provides companion object-safe traits (`DynHook`, `DynTool`, `DynTrigger`) which are automatically implemented via blanket implementations for any type implementing the base trait.
4. **Mock Test Suite Guidelines**: To test connection, event loops, and tool extractions under simulated WebSocket messaging, run:
   ```sh
   cargo test wasm::tests
   ```
   * **Writing Mock Tests**: Mock tests should spin up a local WebSocket listener, bind to port `0` to allocate a free TCP port dynamically, record that port, configure `WasmConnectionStrategy` to point to it, and mock standard JSON frames (`StepUpdate`, `TrajectoryStateUpdate`, etc.) to verify client state transitions.

---

## Routing Table

Use the links below to navigate specific topics and code configurations:

### References

* **Architecture**: Understand connection strategies, thread safety, and WebSocket handshake mechanisms.
  See [architecture.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/references/architecture.md).
* **Agent Configuration**: Detail configurations for models, workspaces, system instructions, and response schemas.
  See [agent_configuration.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/references/agent_configuration.md).
* **Built-in Tools**: Review native tools (file IO, shell command runner, grep search) and capabilities setup.
  See [built_in_tools.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/references/built_in_tools.md).
* **Safety Policies**: Formulate declarative middleware policies to block or confirm tool execution.
  See [safety_policies.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/references/safety_policies.md).
* **Error Handling**: Register hooks to catch and handle errors or redirect execution flow.
  See [error_handling.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/references/error_handling.md).
* **Observability**: Extract token usage metrics and inspect thinking model trajectories.
  See [observability.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/references/observability.md).
* **MCP & Custom Tools**: Register custom Rust tools or integrate Model Context Protocol (MCP) servers.
  See [mcp_integration.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/references/mcp_integration.md).

### Examples

* **Hello World**: Basic single-turn chat, streaming text and thoughts, and interactive loop.
  See [hello_world.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/hello_world.md).
* **Custom Tools**: Write custom stateful and stateless tools using the `Tool` trait.
  See [custom_tool.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/custom_tool.md).
* **Persona & System Instructions**: Guide the agent's identity, tone, and directives.
  See [persona_config.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/persona_config.md).
* **Multimodal Inputs/Outputs**: Configure image generation capabilities and understand input constraints.
  See [multimodal.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/multimodal.md).
* **Subagent Delegation**: Coordinate multi-agent tasks using subagents.
  See [subagents.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/subagents.md).
* **Model Context Protocol (MCP)**: Integrate external MCP tools via global configuration files.
  See [mcp_tools.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/mcp_tools.md).
* **Triggers & Background Loops**: Implement background workers reacting to system events.
  See [periodic_trigger.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/periodic_trigger.md).
* **Lifecycle Hooks**: Hook callbacks into pre-turn, tool execute, and error handling events.
  See [hooks.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/hooks.md).
* **Session Persistence**: Resume past execution sessions using a unique `conversation_id`.
  See [persistence.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/persistence.md).
* **App Data Directory Override**: Override directory settings controlling log and artifact storage paths.
  See [app_data_dir_override.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/app_data_dir_override.md).
* **Structured Output**: Direct agents to reply strictly with JSON objects adhering to a JSON schema.
  See [structured_output.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/structured_output.md).
* **Agent Skills**: Dynamically load filesystem-based skill structures into the agent.
  See [agent_skills.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/agent_skills.md).
* **Policies**: Lock workspace directories and filter command lines.
  See [policies.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/policies.md).
* **Streaming**: Stream chat responses and distinguish reasoning thoughts from response text in real time.
  See [streaming.md](file:///Volumes/goldcoders/antigravity-sdk-rust/skills/google-antigravity-sdk-rust/examples/getting_started/streaming.md).
