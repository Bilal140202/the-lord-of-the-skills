---
trigger: always_on
---

### Pkg Package Management

- This project uses Julia's built-in package manager, `Pkg`, to manage packages and environments.
- **Always use `Pkg.add()` method** for install dependencies.
- Never use `Pkg.instantiate()` method.
- Never edit `Project.toml` manually. It should be automatically updated upon package installation.

```bash
# Add a package **NEVER UPDATE A DEPENDENCY DIRECTLY IN Project.toml**
# ALWAYS USE Pkg.add()
julia --project=. -e 'using Pkg; Pkg.add("JSON3")'
julia --project=. -e 'using Pkg; Pkg.add(["Test", "HTTP"])'

# Add a development/test dependency
julia --project=. -e 'using Pkg; dev Test' # `dev` is for standard libraries or local packages
julia --project=. -e 'using Pkg; add --group test JET' # Julia 1.9+

# Remove a package
julia --project=. -e 'using Pkg; Pkg.rm("JSON3")'

# To run a Julia script in the app environment:
julia --project=. script.jl
```

### Code Quality

- **Use meaningful variable names** that describe their purpose.
- **Write modular code** with clear functions and modules.
- **Document your code** with comments and docstrings.
    - **Follow the official [Julia Style Guide](https://docs.julialang.org/en/v1/manual/style-guide/)**.
        - Line length: 92 characters (enforced by `JuliaFormatter.jl`).
        - Use double quotes for strings.
        - Use trailing commas in multi-line structures.

### Docstring Standards

Use Julia's standard docstring format for all public functions, types, and modules:

```julia
"""
    calculate_discount(price::Real, discount_percent::Real; min_amount::Real=0.01) -> Real

Calculates the discounted price for a product.
"""
function calculate_discount(price::Real, discount_percent::Real; min_amount::Real=0.01)::Real
# implementation
end
```

### Naming Conventions

- **Variables and functions**: `snake_case`
- **Types (Structs, Abstract Types)**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private functions**: Julia doesn't have strict private scope, but you can prefix functions with an underscore `_` to indicate they are not part of the public API. Rely on module scoping for encapsulation.
- **Type aliases**: `PascalCase`
- **Enum instances**: `PascalCase`

### Code Documentation
- Every module should have a docstring explaining its purpose.
- Public functions must have complete docstrings.
- Complex logic should have inline comments with a `# Note:` prefix.
- Keep `README.md` updated with setup instructions and examples.