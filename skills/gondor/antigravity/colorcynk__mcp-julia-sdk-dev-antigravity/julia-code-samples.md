---
trigger: always_on
---

### Error Handling: Exception Best Practices

```julia
# Create custom exceptions for your domain
struct PaymentError <: Exception
    msg::String
end

struct InsufficientFundsError <: PaymentError
    required::Float64
    available::Float64
    InsufficientFundsError(required, available) = new(
        "Insufficient funds: required $required, available $available",
        required,
        available
    )
end

# Use specific exception handling
try
    process_payment(amount)
catch e
    if e isa InsufficientFundsError
        @warn "Payment failed: $(e.msg)"
        return PaymentResult(success=false, reason="insufficient_funds")
    elseif e isa PaymentError
        @error "Payment error: $(e.msg)"
        return PaymentResult(success=false, reason="payment_error")
    else
        rethrow() # Re-throw unexpected errors
    end
end

# Use `do` block syntax or `try...finally` for resource management
function with_database_transaction(f)
    conn = get_connection()
    trans = begin_transaction(conn)
    try
        f(conn)
        commit(trans)
    catch
        rollback(trans)
        rethrow()
    finally
        close(conn)
    end
end

# Usage
with_database_transaction() do conn
    # database operations
end
```

### Logging Strategy

```julia
using Logging
using LoggingExtras

# Configure structured logging
logger = TeeLogger(
    ConsoleLogger(stderr, Logging.Info),
    FileLogger("app.log", append=true)
)
global_logger(logger)

# Log execution with a macro for debugging
macro log_execution(ex)
    func_name = ex.args[1].args[1]
    quote
        @debug "Entering $($func_name)"
        try
            result = $(esc(ex))
            @debug "Exiting $($func_name) successfully"
            result
        catch e
            @error "Error in $($func_name): $e" exception=(e, catch_backtrace())
            rethrow()
        end
    end
end

@log_execution function my_function(x, y)
    # ...
end
```

### Configuration Management: Environment Variables and Settings

```julia
using Configurations
using DotEnv

# Load environment variables from a .env file
DotEnv.config()

@option struct Settings
    """Application settings with validation."""
    app_name::String = "MyApp"
    debug::Bool = false
    database_url::String
    redis_url::String = "redis://localhost:6379"
    api_key::String
    max_connections::Int = 100
end

# Get cached settings instance using a singleton pattern
const SETTINGS = Ref{Settings}()
function get_settings()::Settings
    if !isassigned(SETTINGS)
        SETTINGS[] = from_env(Settings)
    end
    return SETTINGS[]
end

# Usage
settings = get_settings()
```

### Data Models and Validation: Example Model using Parameters.jl

```julia
using Parameters
using Dates
using UUIDs

@with_kw struct Product
    """Product model"""
    id::UUID = uuid4()
    name::String
    description::Union{String, Nothing} = nothing
    price::Float64
    category::String
    tags::Vector{String} = []
    created_at::DateTime = now()
    updated_at::DateTime = now()
    is_active::Bool = true

    # Validate using an inner constructor
    function Product(id, name, description, price, category, tags, created_at, updated_at, is_active)
        if price <= 0
            throw(ArgumentError("Price must be positive."))
        end
        if isempty(name)
            throw(ArgumentError("Name cannot be empty."))
        end
        new(id, name, description, price, category, tags, created_at, updated_at, is_active)
    end
end
```