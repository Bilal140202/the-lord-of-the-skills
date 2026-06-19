# CALL SKILL: /caveman-hardware-design-functional
# ALIAS: /system-design

# SYSTEM OVERRIDE: 2% CONTEXT TAX
!! Talker mode = OFF. 
!! Engineering Mode = MAX.
!! No introductory fluff. Direct architectural output only.

# OBJECTIVE
Define the physical "soul" of the machine. This skill bridges industrial engineering with functional code by outputting physics-based constraints.

# 1. THE CHASSIS (PHYSICALITY)
- **Primary Material**: [Titanium | Aluminum | Polycarbonate | Wood | Beige Plastic]
- **Finish**: [Reflective | Matte | Brushed | High-Gloss]
- **Thermal Envelope**: [Passive | Active | CRT Scan-Heat]
  - *Logic*: Define `MAX_FPS` based on thermal headroom.

# 2. THE OPTICS (VISUAL DENSITY)
- **Panel Technology**: [Tandem OLED | mini-LED | IPS | Monochrome CRT]
- **Luminance**: Peak Nits (for HDR-matched UI scaling).
- **Refresh Rate**: [60Hz | 120Hz ProMotion | 1-bit static]
  - *Logic*: Map `--ui-blur-quality` to panel response time.

# 3. THE INPUT (HAPTICS)
- **Tactile feedback**: [Force Touch | Butterfly | Mechanical | 1983 Spring-loaded]
- **Navigation**: [Gesture-based | Multi-button | Single-button | Command-line]

# 4. THE JSON BRIDGE (REQUIRED)
Export a `hardware_profile.json` to allow the UI to auto-calibrate to the era.

# TRIGGER
Design functional hardware for: {{Era/Device}}. Output specs and JSON only.

```json
{
  "system_id": "string",
  "materials": {
    "body": "string",
    "gloss_factor": "float",
    "corner_radius": "string"
  },
  "display": {
    "type": "string",
    "peak_nits": "int",
    "refresh_hz": "int"
  },
  "logic_constraints": {
    "throttle_at_temp": "int",
    "pixel_perfect": "boolean"
  }
}
