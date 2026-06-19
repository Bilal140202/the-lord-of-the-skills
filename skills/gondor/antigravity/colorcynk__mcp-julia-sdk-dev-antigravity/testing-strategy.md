---
trigger: always_on
---

### Testing Best Practices

```julia
# Use the standard Test library and @testset
using Test
using Dates

# Use `let` blocks or helper functions for setup
let
    sample_user = User(
        id=123,
        name="Test User",
        email="test@example.com",
        created_at=now()
    )

    # Use descriptive test set names
    @testset "User can update email with valid input" begin
        new_email = "newemail@example.com"
        update_email!(sample_user, new_email)
        @test sample_user.email == new_email
    end

    # Test edge cases and error conditions
    @testset "Invalid email format is rejected" begin
        @test_throws ArgumentError update_email!(sample_user, "not-an-email")
    end
end
```

### Test Commands

```bash
# Run all tests
julia --project=. -e 'using Pkg; Pkg.test()'

# Run a specific test suite
julia --project=. -e 'using Pkg; Pkg.test("PackageName")'

# Run tests with coverage
julia --project=. -e 'using Pkg; Pkg.test(coverage=true)'
```