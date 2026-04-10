# MCP Gateway Engineer Manual

## 1. Purpose

This environment gives engineers **one shared MCP endpoint** instead of requiring each engineer to configure multiple tool servers individually.

The platform currently exposes:

- **vSphere / vCenter tools** through a dedicated vSphere MCP server
- **FortiGate tools** through a dedicated FortiGate MCP server
- **A shared MCP gateway** through MCPX
- **Browser-based engineering workspaces** through Coder

## 2. Deployed architecture

### VM

- **Host IP:** `10.208.0.162`
- **OS:** Ubuntu 24.04
- **Disk:** 38 GB usable LVM filesystem
- **Current free space at handoff:** ~20 GB

### Running services

| Service | Purpose | URL / Port |
|---|---|---|
| MCPX Gateway | Shared MCP endpoint for engineers | `http://10.208.0.162:9000/mcp` |
| MCPX Dashboard | Gateway control plane | `http://10.208.0.162:5173` |
| Coder | Browser workspaces | `http://10.208.0.162:7080` |
| vSphere MCP Server | vCenter / ESXi operations | `http://10.208.0.162:8000/mcp` |
| FortiGate MCP Server | FortiGate operations | `http://10.208.0.162:8814/fortigate-mcp/sse` |
| MCPX Metrics | Internal metrics | `http://10.208.0.162:3000` |

### Current MCPX upstream configuration

MCPX currently proxies these upstream MCP servers:

- `vsphere` → streamable HTTP → `http://10.208.0.162:8000/mcp`
- `fortigate` → SSE → `http://10.208.0.162:8814/fortigate-mcp/sse`

## 3. Design principles

### Single gateway, multiple tools

Engineers connect to **one endpoint only**:

`http://10.208.0.162:9000/mcp`

The gateway centralizes discovery and access to all approved MCP servers.

### Per-tool isolation

Each MCP integration runs in its own container:

- one container for vSphere
- one container for FortiGate
- one container for MCPX
- one container for Coder

This reduces blast radius and makes updates safer.

### Browser-first access

Coder provides a browser workspace so engineers do not need a full local setup to work against the environment.

### Avoid direct infrastructure access when possible

The preferred operating model is:

1. engineer uses AI client or browser workspace
2. AI client calls MCPX
3. MCPX routes to the right tool server
4. tool server calls the infrastructure API

### Least privilege

Infrastructure credentials should be scoped to the minimum permissions needed. The current FortiGate placeholder config must be replaced with a real restricted token before production use.

## 4. What engineers should use

## Recommended path: Coder

### Login

1. Open `http://10.208.0.162:7080`
2. Sign in with the Coder account created for you
3. Open or create your workspace
4. Launch **VS Code in the browser**

### Why Coder is the recommended path

- no local install required
- same environment for every engineer
- works fully inside the internal network
- easy user management

## Alternative path: local MCP-capable client

If the engineer is on the same private network and has an MCP-capable client, they can connect directly to the shared gateway endpoint:

`http://10.208.0.162:9000/mcp`

If they use `mcp-remote`, HTTP requires:

```bash
npx mcp-remote@0.1.21 http://10.208.0.162:9000/mcp --allow-http
```

## 5. Example engineer workflows

### vSphere / vCenter

Examples of safe prompts:

- "List all datastores and their free space"
- "Show me all virtual machines and their power state"
- "List all ESXi hosts"
- "Get details for VM named X"

### FortiGate

Examples once real credentials are configured:

- "List FortiGate interfaces"
- "Show firewall policies"
- "Check device health"
- "List address objects"

## 6. Current important limitations

### MCPX dashboard authentication

**MCPX does not have built-in dashboard authentication.**

This means the UI at `http://10.208.0.162:5173` is reachable by anyone on the same network unless protected externally.

Recommended next step:

- place Caddy in front of MCPX
- add basic auth or SSO
- restrict direct access to port 5173

### Saved Setups in MCPX

The **Saved Setups** feature depends on Lunar Hub / cloud linkage and is not useful in the current standalone deployment.

### FortiGate configuration status

The FortiGate MCP server is deployed and connected to MCPX, but it currently uses **placeholder device credentials** and must be updated before real operations.

## 7. Admin operations

### Coder upgrade model

Coder was deployed with Docker Compose, so upgrades follow the official docs:

```bash
cd /opt/coder
docker compose pull coder
docker compose up -d coder
```

Before upgrade, take a PostgreSQL backup.

### MCPX upstreams

MCPX upstreams are controlled by:

`/opt/mcpx/config/mcp.json`

### vSphere MCP deployment path

`/opt/vsphere-mcp`

### FortiGate MCP deployment path

`/opt/fortigate-mcp`

### Coder deployment path

`/opt/coder`

## 8. Security guidance

### Minimum controls recommended next

1. Put MCPX behind Caddy
2. Protect dashboard with auth
3. Protect gateway endpoint with API key or reverse proxy auth
4. Replace placeholder FortiGate credentials
5. Use read-only or low-privilege API roles where possible
6. Document change approval for any write operations

### Strongly recommended operational rules

- do not expose the dashboard directly to the public internet
- do not store production secrets in repo files
- prefer token-based access over shared passwords
- use separate service accounts per integration where possible

## 9. Troubleshooting

### MCPX dashboard loads but a server shows `connection-failed`

Check:

1. upstream container is running
2. upstream URL in `/opt/mcpx/config/mcp.json` is correct
3. target transport is correct (`streamable-http` vs `sse`)
4. disk space is available

### Coder workspace shows Copilot Chat install popup

This is caused by code-server / VS Code web trying to install a proprietary extension that does not exist in Open VSX. It is not required for the platform.

### `mcp-remote` rejects HTTP

Use:

```bash
--allow-http
```

or move the gateway behind HTTPS.

## 10. Handoff summary

The platform is operational and currently supports:

- shared browser workspaces via Coder
- centralized tool routing via MCPX
- connected vSphere MCP tools
- connected FortiGate MCP transport and gateway registration

The main production hardening tasks still recommended are:

- dashboard authentication
- HTTPS in front of gateway and dashboard
- FortiGate real credential setup
- role-based operating guidance for engineers
