<!-- Thanks for contributing to DOS. See CONTRIBUTING.md for the architecture
     contract; the short version is below. Keep edits inside the layer they
     belong to. -->

## What & why

<!-- One or two sentences. What does this change, and what does it unblock? -->

## Layer check (the litmus tests)

DOS keeps mechanism (kernel) and policy (drivers) strictly apart. Tick what applies:

- [ ] This change stays **inside one layer** (kernel / seam / helper / driver) — see [CLAUDE.md](../CLAUDE.md).
- [ ] The kernel still **imports no host** (no `job`/lane names under `src/dos/` except `drivers/`).
- [ ] No new policy was added to `config.py` (new host policy → a `drivers/` module).
- [ ] `verify` still works **with no plan** (didn't couple the kernel to a plan schema).

## Verification

- [ ] `python -m pytest -q` is green.
- [ ] `dos doctor --workspace .` runs.
- [ ] If behavior changed, I added/updated a test that pins it.

<!-- For a new reason / renderer / judge: prefer a userland plugin or a dos.toml
     declaration over a kernel edit. If you did edit the kernel, say why it
     couldn't be expressed as policy. -->
