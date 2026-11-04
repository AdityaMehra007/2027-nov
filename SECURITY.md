# Security Policy

## Supported Versions
Only the latest release on the primary development branch is actively supported with security patches.

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability
The security of autonomous agents and quantitative systems is of paramount importance. 

If you discover a security vulnerability (such as a flaw in the `SecurityGovernor`, an unauthenticated command execution risk, or sensitive data exposure):
1. **Do not open a public issue.**
2. Send a detailed report to security@omniverse.ai with reproduction steps.
3. We will acknowledge receipt within 24 hours and provide an estimated remediation timeline.

## Safety Principles
- **No Autonomous Live Capital Transfer**: All financial settlements, wire transfers, and broker orders must be held for human approval by default.
- **Credential Protection**: Never commit `.env` files or API secrets into git.
