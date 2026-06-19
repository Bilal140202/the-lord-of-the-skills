# ROS 2 Workspace Best Practices for AI Agents

## 1. System Context: ROS 2 Jazzy (Noble Numbat)

**Target OS**: Ubuntu 24.04 LTS (Noble).

**Python Version**: Python 3.12 (system default).

**Build System**: colcon with ament_cmake (C++) or ament_python (Python).

**Standard Sourcing**: Always assume the base environment is `/opt/ros/jazzy/setup.bash` and the local overlay is `install/setup.bash`.

**Middleware**: Default is Fast DDS. Use Quality of Service (QoS) profiles explicitly (`rclcpp::QoS`, `rclpy.qos.QoSProfile`) rather than defaults for critical nodes.

---

## 2. Workspace Structure & Convention

### Root Layout

- **src/**: All source code (packages).
- **build/, install/, log/**: (Excluded from indexing but relevant for terminal tools).
- **.agent/**: Directory for agent-specific configurations.

### Package Structure

**All Packages**:
- Every package MUST include a `package.xml` (format 3 for Jazzy).
- Every package MUST include a `README.md` with node documentation and usage examples.

**C++ Packages**:
- `CMakeLists.txt` with minimum required version 3.22.

**Python Packages**:
- `setup.py` with entry points for all nodes.
- `setup.cfg` for package metadata (preferred for cleaner separation).
- Optionally `pyproject.toml` for modern Python tooling.
- `resource/<package_name>` directory with marker file for package discovery.

### Naming Conventions

- **Packages, nodes, topics**: Use `snake_case`.
- **Message, Service, Action types**: Use `PascalCase`.

### Python Package Best Practices

- **Standard Layout**: Use the modern `src/<package_name>/` layout or `<package_name>/<package_name>/` structure.
- **setup.py vs setup.cfg**: Jazzy supports both, but prefer `setup.cfg` + `pyproject.toml` for cleaner separation of concerns.
- **Entry Points**: Always declare nodes in `setup.py` entry points for proper `ros2 run` integration:
  ```python
  entry_points={
      'console_scripts': [
          'node_name = package_name.node_module:main',
      ],
  }
  ```
- **Type Hints**: Use Python 3.12 type hints extensively throughout your code (required for Ubuntu 24.04).
- **Testing**: Include pytest-based tests in `test/` directory with proper `pytest.ini` configuration.

---

## 3. Python Package Template Reference

Standard structure for Python ROS 2 packages:

```
<package_name>/
├── package.xml              # Format 3, Python dependencies
├── setup.py                 # Entry points and package metadata
├── setup.cfg                # Package configuration (optional but recommended)
├── resource/                # Package marker for discovery
│   └── <package_name>
├── <package_name>/          # Source code directory
│   ├── __init__.py
│   └── <node_name>.py       # Node implementation
├── launch/                  # Launch files (optional)
│   └── <launch_file>.launch.py
├── test/                    # pytest tests
│   ├── test_copyright.py
│   ├── test_flake8.py
│   └── test_pep257.py
├── config/                  # Configuration files (optional)
│   └── params.yaml
└── README.md                # Documentation
```

---

## 4. Antigravity Specific Configurations

To optimize Antigravity's agentic behavior, implement the following in your `.agent/` directory:

### A. Agent Rules (.agent/rules/ros2-standard.md)

**Explicit Sourcing**: "When running any terminal command involving `ros2` or `colcon`, you MUST prefix it with `source /opt/ros/jazzy/setup.bash && source install/setup.bash || true`."

**Defensive Programming**: "Check return codes for all service calls. Use `ParameterEventHandler` (new in Jazzy) for dynamic reconfigurations in Python."

**Dependency Management**: "Before adding a new dependency, check `package.xml` and run `rosdep install --from-paths src --ignore-src --simulate` to verify availability."

### B. Skills (.agent/skills/)

Define executable "Skills" to automate ROS 2 workflows:

**C++ and General**:
- `build-workspace`: Script that runs `colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON`.
- `test-package`: Script that runs `colcon test --packages-select <package_name> --return-code-on-test-failure`.
- `lint-ros`: Script that runs `ament_lint_auto` and `ament_copyright`.

**Python-Specific**:
- `build-workspace-python`: Script that runs `colcon build --symlink-install --packages-select <package_name> --event-handlers console_direct+`.
- `lint-python`: Script running `ament_flake8`, `ament_pep257`, and `ament_copyright`.
- `check-types`: Script running `mypy` with ROS 2 stubs for type checking.
- `format-python`: Script running `black` and `isort` with ROS 2 compatible configurations.

### C. Implementation Artifacts

**Implementation Plan**: Before editing code, the agent MUST generate an `implementation_plan.md` in the `.agent/` directory outlining changes to topics, message types, and node logic.

**Verification Walkthrough**: After edits, the agent must provide a `walkthrough.md` with the exact `ros2 launch` or `ros2 run` commands to verify the fix.

---

## 5. ROS 2 Jazzy "Gotchas" (Anti-Hallucination)

### General Gotchas

**TwistStamped**: Jazzy strongly prefers `geometry_msgs/msg/TwistStamped` over `Twist` for `cmd_vel`. Ensure `frame_id` and `stamp` are populated.

**API Changes**: `rclpy` now includes `ParameterEventHandler`. Do not use old `add_on_set_parameters_callback` for simple monitoring.

**ros2_control**: Note that many parameters in `diff_drive_controller` have moved (e.g., limits are now set to `.NAN` to disable, rather than `has_velocity_limits: false`).

### Python-Specific Gotchas

**Node Executors**: Use `MultiThreadedExecutor` explicitly; `SingleThreadedExecutor` can cause callback deadlocks with timers and services.

**Parameter Descriptors**: Always use `ParameterDescriptor` with `description`, `read_only`, and `constraints` for better introspection:
```python
self.declare_parameter('param_name', default_value,
                       ParameterDescriptor(description='Description here'))
```

**Type Annotations**: Messages and services now require proper type hints; use `from typing import TYPE_CHECKING` to avoid circular imports:
```python
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from std_msgs.msg import String
```

**asyncio Integration**: `rclpy.executors.ExternalShutdownException` must be caught for clean shutdown in asyncio contexts.

**QoS Profiles**: Import from `rclpy.qos`, not `rclpy.qos_profile` (deprecated path). Use:
```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
```

**Parameter Callbacks**: For parameter updates, use the new `ParameterEventHandler` instead of `add_on_set_parameters_callback`:
```python
from rclpy.parameter_event_handler import ParameterEventHandler
param_handler = ParameterEventHandler(self)
param_handler.add_parameter_callback('param_name', callback_func)
```

---

## 6. Python Dependency Management

**rosdep Keys**: Use standardized rosdep keys (e.g., `python3-numpy`) not pip package names in `package.xml`.

**Custom Dependencies**: Document pip-only dependencies in `README.md` with installation instructions. Add them to `package.xml` as:
```xml
<exec_depend>python3-pip</exec_depend>
<!-- Document: pip install custom-package -->
```

**Virtual Environments**: **AVOID** using venv/virtualenv; they conflict with colcon overlay mechanism. Use system Python 3.12.

**System Python**: Jazzy expects Python 3.12; check compatibility before adding dependencies. Verify with:
```bash
python3 --version  # Should show 3.12.x
```

**Testing Dependencies**: Separate test dependencies in `package.xml`:
```xml
<test_depend>python3-pytest</test_depend>
<test_depend>python3-pytest-cov</test_depend>
```

---

## 7. Deployment & Orchestration

### Launch Files

**Python Launch Files**: Use Python-based launch files (`*.launch.py`) exclusively in Jazzy.

**Launch Arguments**: Always include `DeclareLaunchArgument` with `description` and `default_value`:
```python
DeclareLaunchArgument(
    'param_name',
    default_value='default',
    description='Description of this parameter'
)
```

**Parameter Substitution**: Use `LaunchConfiguration` for parameter substitution:
```python
param_value = LaunchConfiguration('param_name')
```

**Grouping**: Use `GroupAction` for cleaner organization of related nodes:
```python
GroupAction([
    Node(...),
    Node(...),
])
```

**Global Parameters**: Use `SetParameter` for global parameter setting across multiple nodes.

### Node Composition

**C++ Nodes**: Favor `rclcpp_components` for C++ nodes to allow for efficient intra-process communication.

**Python Nodes**: While Python doesn't support composition like C++, design nodes to be lightweight and focused on single responsibilities.

### Lifecycle Nodes

Use lifecycle nodes for hardware drivers or critical state-dependent nodes (e.g., sensors, planners) to ensure deterministic startup sequences.

---

## 8. Python Testing Best Practices

### Unit Tests

- **Framework**: Use `pytest` with ROS 2 fixtures from `launch_testing`.
- **Test Files**: Include standard linting tests in every package:
  - `test_flake8.py` - Style checking
  - `test_pep257.py` - Docstring checking
  - `test_copyright.py` - Copyright header checking

### Integration Tests

- **Launch Testing**: Use `launch_testing.actions.ReadyToTest` for integration tests.
- **Example**:
  ```python
  from launch_testing.actions import ReadyToTest
  
  def generate_test_description():
      return LaunchDescription([
          Node(...),
          ReadyToTest(),
      ])
  ```

### Coverage

Run tests with coverage reporting:
```bash
colcon test --pytest-args --cov=<package_name> --cov-report=html
```

### Continuous Testing

Set up package-level testing that runs automatically:
```bash
colcon test --packages-select <package_name> --event-handlers console_direct+
```

---

## 9. How to Use this with Antigravity

1. **Clone/Create Workspace**: Set up your `ros2_ws/src`.

2. **Add Rules**: Place this document as `AGENTS.md` in the workspace root.

3. **Link for Gemini/Claude**: On Linux, run:
   ```bash
   ln -s AGENTS.md .agent/rules.md
   ln -s AGENTS.md .cursorrules  # If using Cursor alongside
   ```
   On Windows (PowerShell as Administrator):
   ```powershell
   New-Item -ItemType SymbolicLink -Path .agent\rules.md -Target AGENTS.md
   New-Item -ItemType SymbolicLink -Path .cursorrules -Target AGENTS.md
   ```

4. **Initial Prompt**: "Agent, read the @AGENTS.md and follow the workspace rules. Start by building the current workspace to index all ROS 2 interfaces."

5. **For New Python Packages**: "Create a new Python package named `<package_name>` following the template in AGENTS.md with proper testing setup."

---

## 10. Quick Reference Commands

### Building
```bash
# Full workspace
colcon build --symlink-install

# Single Python package (with immediate console output)
colcon build --symlink-install --packages-select <package_name> --event-handlers console_direct+

# With compile commands (for C++)
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

### Testing
```bash
# Run all tests for a package
colcon test --packages-select <package_name> --event-handlers console_direct+

# Run with coverage
colcon test --packages-select <package_name> --pytest-args --cov=<package_name>

# Show test results
colcon test-result --verbose
```

### Dependencies
```bash
# Check dependencies (simulation)
rosdep install --from-paths src --ignore-src --simulate

# Install dependencies
rosdep install --from-paths src --ignore-src -y
```

### Linting (Python)
```bash
# Run all Python linters
ament_flake8 src/<package_name>
ament_pep257 src/<package_name>
ament_copyright src/<package_name>
```