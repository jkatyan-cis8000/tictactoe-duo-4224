# src/providers

Contains cross-cutting concerns: auth, telemetry, connectors, flags.

This layer should contain:
- Authentication services
- Logging/telemetry
- External API connectors
- Feature flags

May import from: types, config, utils, providers
