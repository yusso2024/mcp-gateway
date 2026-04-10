# MCP Gateway Platform Summary

## Slide 1 — Executive Summary

- Built a **shared MCP platform** for engineering on a single VM
- Engineers no longer need to connect to each MCP tool individually
- Current platform includes **MCPX**, **Coder**, **vSphere MCP**, and **FortiGate MCP**
- Outcome: faster onboarding, centralized operations, lower tool sprawl

## Slide 2 — Business Problem Solved

Before:

- each engineer had to configure tools separately
- infrastructure integrations were fragmented
- browser-based access was missing
- admin visibility was poor

After:

- one MCP endpoint for all approved tools
- one browser workspace platform for engineers
- one place to add or remove infrastructure tools
- cleaner path to governance and audit controls

## Slide 3 — What Was Deployed

### Core services

- **MCPX** as the MCP gateway and tool router
- **Coder** as browser-based developer workspace platform
- **vSphere MCP server** for VMware / vCenter operations
- **FortiGate MCP server** for firewall operations

### VM footprint

- Ubuntu 24.04
- 38 GB usable storage after LVM expansion
- approximately 20 GB free after deployment

## Slide 4 — Current Architecture

```text
Engineer Browser / MCP Client
        |
        v
   Coder or MCP-capable client
        |
        v
      MCPX Gateway
      10.208.0.162:9000/mcp
        |                |
        |                |
        v                v
  vSphere MCP        FortiGate MCP
    :8000/mcp        :8814/.../sse
        |                |
        v                v
    vCenter API      FortiGate API
```

## Slide 5 — Benefits

- **Reduced onboarding effort**: one endpoint instead of many
- **More consistent engineer experience**: browser-first access with Coder
- **Safer integration model**: each tool isolated in its own container
- **Faster expansion**: new MCP tools can be added centrally
- **Operational visibility**: single place to manage available servers

## Slide 6 — Current Risks / Gaps

- MCPX dashboard currently has **no built-in authentication**
- FortiGate server still needs final production credentials
- Gateway is HTTP-only today; HTTPS should be added
- Saved Setups in MCPX is not useful without Lunar Hub integration

## Slide 7 — Recommended Next Phase

### Security hardening

- put Caddy or another reverse proxy in front
- add dashboard authentication
- add HTTPS
- protect the MCP endpoint with auth

### Operational maturity

- define read-only vs write-enabled tool access rules
- create service-account-based credentials per integration
- add backup / recovery runbook
- add monitoring and alerting for core services

## Slide 8 — Conclusion

- The MCP platform is already functional and usable by engineers
- The organization now has a central place to expose infrastructure tools to AI-assisted workflows
- The next step is not re-architecture; it is **hardening and standardization**
