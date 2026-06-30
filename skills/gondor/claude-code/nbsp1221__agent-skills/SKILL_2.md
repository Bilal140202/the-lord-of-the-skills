---
name: docker-compose
description: Write and review Docker Compose files with consistent best practices and conventions (file naming, override strategy, service naming, key ordering, env handling, ports, and healthchecks). Use when creating or standardizing compose.yaml/docker-compose.yml.
---

# Docker Compose

Opinionated conventions for consistent, maintainable Docker Compose files.

## Best Practices

### File naming and override strategy

- Prefer `compose.yaml` (or `compose.yml`) as the canonical base file.
- Keep local-only changes in `compose.override.yaml` (auto-merged by Compose).
  - If an override file is local-only, add it to `.gitignore` unless the team explicitly wants it committed (optionally keep a `.example` file).
- For environment-specific configs, use `compose.<env>.yaml` and combine with `-f`.
- Avoid the top-level `version` key (obsolete).

### Service naming and identity

- Use kebab-case service names; they become internal DNS names.
- Avoid `container_name` unless strictly required; it prevents scaling.
- Pin image tags (avoid `latest`); prefer digests for production.

### Env var conventions

- Use `.env` for interpolation, `env_file` for container runtime values.
- Keep secrets out of Compose files; commit `.env.example` only.
- Prefer mapping style for `environment` when values include special chars.
- If the same variable is set in both, `environment` overrides `env_file` (key order does not change behavior).

### Ports, volumes, and paths

- Quote `HOST:CONTAINER` port mappings to avoid YAML base-60 parsing issues.
- Prefer relative bind mounts starting with `./`.
- Use named volumes for persistent data.

### Readiness and dependencies

- Use `depends_on` for ordering; add `healthcheck` and `condition: service_healthy` for readiness-sensitive dependencies.

### Profiles for optional services

- Use `profiles` to gate optional services (e.g., debug, seed, admin) instead of maintaining separate files.
- If a service is profile-gated, any `depends_on` targets must be in the same profile or always enabled; otherwise the model is invalid.

### Project naming and file composition

- Set top-level `name` when you need stable project identifiers (network/volume names) across directories or CI.
- Use `include`/`fragments` to split large Compose files, but only if your Compose implementation supports them.

### DRY with extensions and anchors

- Use `x-` extension fields plus YAML anchors/merge to share repeated blocks (env, volumes, labels) across services.

### Secrets and configs

- Declare `secrets`/`configs` at top level and explicitly grant access per service; top-level declaration alone is not enough.
- Prefer `secrets`/`configs` for sensitive or shared files when the platform supports them.

### Deploy portability

- Treat `deploy` as platform-specific; some Compose implementations ignore it in local runs.
- Document when `deploy` is required so users do not assume it applies everywhere.

### Init for PID 1

- Set `init: true` for long-running services to handle PID 1 signal and zombie reaping correctly.

## Ordering Conventions

### Top-level order

1. `name` (optional)
2. `services`
3. `networks`
4. `volumes`
5. `configs`
6. `secrets`

### Service key order

Use this exact order for keys within each service to keep the file consistent.

1. Identity: `image` / `build`, `container_name`, `hostname`
2. Runtime: `command`, `entrypoint`, `restart`
3. Environment: `env_file`, `environment`, `labels`
4. Resources: `ports`, `expose`, `volumes`
5. Connectivity: `depends_on`, `networks`, `network_mode`
6. Health: `healthcheck`

## Validation

- Always run `docker compose config` before shipping changes.

## References

- For the official specification and detailed semantics, see https://compose-spec.io
