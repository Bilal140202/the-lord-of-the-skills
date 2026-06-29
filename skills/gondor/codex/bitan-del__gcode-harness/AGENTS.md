# Repository Guidelines

## Development Workflow

- **Commit as you go** - Make small, focused commits after completing each feature or fix
- If the git state is not clean, or there are other agents working in the codebase in parallel, do your best to still commit your work. 
- **Push when done** - Push all commits to remote when finishing a task or session
- **Use fast iteration by default** - Prefer `cargo check`, targeted tests, and dev builds while iterating
- **Rebuild when done** - When you are done making changes, build the source.
- **Bump version for releases** - Update version in `Cargo.toml` when making releases. When cutting a new release, look at all the changes that happened since the last release and determine what the version bump should be ie patch or minor, etc. 
- **Remote builds available** - Use `scripts/remote_build.sh` to offload heavy cargo work to another machine. If your build is terminated, likely is because there are not enough resources on this machine to build. use remote build in that case. Try checking the resource avaliablity on the machine before you run a build. 

## Logs
- Logs are written to `~/.gcode/logs/` (daily files like `gcode-YYYY-MM-DD.log`).

## Debug Socket
- Use the debug socket for runtime level debugging

## Install Notes
- `~/.local/bin/gcode` is the launcher symlink used from `PATH`.
- `~/.gcode/builds/current/gcode` is the active local/source-build channel; self-dev builds and `scripts/install_release.sh` point the launcher here.
- `~/.gcode/builds/stable/gcode` is the stable release channel; `scripts/install.sh` installs this and points the launcher here.
- `~/.gcode/builds/versions/<version>/gcode` stores immutable binaries.
- `~/.gcode/builds/canary/gcode` still exists for canary/testing flows, but it is not the primary self-dev install path.
- On Windows, the equivalents are `%LOCALAPPDATA%\\gcode\\bin\\gcode.exe` for the launcher, `%LOCALAPPDATA%\\gcode\\builds\\stable\\gcode.exe` for stable, and `%LOCALAPPDATA%\\gcode\\builds\\versions\\<version>\\gcode.exe` for immutable installs; `scripts/install.ps1` currently installs the stable channel.
- Ensure `~/.local/bin` is **before** `~/.cargo/bin` in `PATH`.

