# Playbook 03 — `verify()` on an OSS library release

> **Archetype:** a published library — `src/` (the code), `docs/` (the manual),
> `tests/`, and a disciplined release convention. Think of any well-known
> single-package OSS library: ships are small, attributed, and tagged.
> **The DOS feature:** the **truth syscall** (`verify`) and the **stamp grammar**
> that teaches it your repo's commit convention. "Did `CODEC2` actually ship?"
> answered from git history alone — no plan doc, no status file, no trust.
>
> **Workspace:** [`../workspaces/libkv/`](../workspaces/libkv/).

A library maintainer's recurring question is *"is this change actually released,
or did someone just say it was?"* — at review time, at release time, when triaging
a bug report against a version. `verify` answers it from the one source that can't
lie to you: the commit graph. The only thing it needs from you is your **ship
grammar** — what one of your ship commits looks like.

---

## The shape

`libkv` scopes its ship commits under a directory. A real ship looks like:

```text
src/CODEC: CODEC2 — ship varint encoder
```

and a release cut looks like:

```text
v1.4.0: release — varint, range scans
```

So `libkv/dos.toml` declares the dir-scoped grammar:

```toml
[stamp]
style        = "grep"
subject_dirs = ["src", "docs"]    # a direct ship is prefixed: "src/<SERIES>: <PHASE>"
```

```bash
cd examples/workspaces/libkv
dos doctor --workspace .
#   stamp convention    src|docs  [style=grep]
```

Contrast with [`acme-store`](../workspaces/acme-store/), which sets
`subject_dirs = []` (bare `CART3: ...`). **Same mechanism, opposite strictness** —
each repo declares how *it* stamps. (Why does strict have to be opt-out and loose
opt-in? Because the dangerous error is a *false* "shipped." A too-strict grammar
fails visibly with `via none`; a too-loose one silently marks unshipped work as
done. So you loosen knowingly. See [HACKING.md](../../docs/HACKING.md).)

## Step 1 — ask whether a phase shipped

In a real `libkv` checkout with the commit above in history (the fixture under
[`../workspaces/libkv/`](../workspaces/libkv/) is a `dos.toml` only, not its own
git repo, so the SHA and `via grep-subject` line below are **illustrative** — they show
what a genuine ship returns; the `via none` negatives further down reproduce
exactly against the fixture):

```bash
dos verify --workspace . CODEC CODEC2
```
```text
SHIPPED CODEC CODEC2 58bf9b0 (via grep-subject)
```
```text
exit code: 0
```

Three things the kernel did, none of which trust a narrator:

1. checked a run **registry** first (none here — fine),
2. fell through to **git history** and found a commit whose subject attributes
   `CODEC2` as a ship under the `src/` prefix your grammar declares,
3. confirmed that commit is an **ancestor of `HEAD`** (a ship on an abandoned
   branch is not a ship).

`(via grep-subject)` names the rung that answered; `58bf9b0` is the receipt. A phase
that never shipped gives the honest negative:

```bash
dos verify --workspace . CODEC CODEC9
#   NOT_SHIPPED CODEC CODEC9 (via none)        exit 1
```

`(via none)` = *no evidence at all* — distinct from "an agent reported failure."

## Step 2 — the grammar is load-bearing: see it matter

This is the part worth internalizing. Suppose a contributor commits a ship
**without** the dir prefix — a bare `CART9: ship range scans`. Under `libkv`'s
`src|docs` grammar, that is **not recognized as a ship**:

```bash
dos verify --workspace . CART CART9
#   NOT_SHIPPED CART CART9 (via none)          exit 1
```

The work *is* in history — but your declared grammar says ships are prefixed, and
this commit isn't, so `verify` correctly reports no matching ship. Flip the
grammar to generic and the *same commit* now counts:

```toml
[stamp]
subject_dirs = []        # accept a bare "<SERIES><PHASE>:" with no dir prefix
```
```bash
dos verify --workspace . CART CART9
#   SHIPPED CART CART9 1741f37 (via grep-subject)      exit 0
```

**The grammar decides what counts as a ship.** Declare the one your repo actually
uses — that's the entire job of `[stamp]`.

## Step 3 — prove your grammar is correct (don't guess)

How do you know your `[stamp]` matches reality? Ask the completeness rail:

```bash
dos doctor --workspace . --check
```

It scans your recent commits for anything **ship-shaped**, and if your declared
grammar recognizes **none** of them, it fails loud (illustrative finding — the
commit it quotes is the scenario above, not the fixture's history):

```text
finding: declared [stamp] (subject_dirs=src, docs) recognizes none of this
repo's 3 recent ship-shaped commit(s) — e.g. 'CART9: ship range scans'.
verify will resolve `via none` for real ships; reconcile [stamp] to how this
repo stamps (see `dos doctor` / HACKING.md).
```
```text
exit code: 1
```

That finding is the kernel catching a misconfiguration *before* it silently
costs you a missed ship. A grammar that matches at least one real ship prints
nothing and exits 0. This is the
["openness is only safe if completeness is provable"](../../docs/HACKING.md)
invariant, applied to your ship convention.

> **The release anchor is free.** Every convention recognizes a `vX.Y.Z:`
> release-cut subject without you declaring anything — so `v1.4.0: release ...`
> is understood by both the strict and generic grammars. You only declare your
> *direct-ship* prefix.

## Step 4 — wire it into the release flow

Now `verify` is a gate, not a vibe. Two high-value placements:

**At PR-merge / CI** — fail the build if a PR claims to close a phase that didn't
actually ship (full recipe in
[`cookbook-ci-integration.md`](cookbook-ci-integration.md)):

```bash
dos verify --workspace . "$SERIES" "$PHASE" || {
  echo "::error::PR claims $SERIES $PHASE shipped, but no commit attributes it"
  exit 1
}
```

**At release time** — before cutting `v1.5.0`, confirm every phase the release
notes claim is real:

```bash
while read series phase; do
  dos verify --workspace . "$series" "$phase" \
    || echo "RELEASE NOTES LIE: $series $phase is not shipped"
done < release-manifest.txt
```

No more "the changelog says it's in, but is it?" The commit graph answers.

## Where DOS deliberately stops

`verify` tells you a phase **shipped** — that a change attributed to it is in the
ancestry of `HEAD`. It does **not** tell you the change is *correct*, *tested*, or
*good*. That's by design: DOS distrusts **claims about state** (did it ship?), not
**judgment** (is it right?). Correctness is your tests' job and your reviewers'
job; `verify` removes the *bookkeeping* lie ("I said it's done") so the humans can
spend their attention on the part that actually needs judgment.

## Anti-patterns

- ❌ **Declaring a `[stamp]` grammar and never running `--check`.** A wrong
  grammar makes `verify` answer `via none` for real ships, silently. `--check` is
  one command; run it after you edit `[stamp]`.
- ❌ **Reading a status file / changelog as ground truth.** That's the narrator
  you don't believe. `verify` reads the graph.
- ❌ **Expecting `verify` to judge code quality.** It verifies *shipped*, not
  *good*. Keep your test suite.

## Recap

```bash
cd examples/workspaces/libkv
dos doctor --workspace .                 # stamp convention: src|docs
dos verify --workspace . CODEC CODEC2    # SHIPPED ... (via grep-subject)   exit 0
dos verify --workspace . CODEC CODEC9    # NOT_SHIPPED ... (via none)   exit 1
dos doctor --workspace . --check         # prove the grammar matches real ships
```

Next: the polyglot fleet ([02](02_polyglot-web-service.md)); the temporal "is it
advancing?" verdict ([04](04_data-ml-pipeline.md)).
