# MCP Gateway Platform

This repository stores the operational documentation for the shared MCP platform deployed for engineering use.

## Contents

- `docs/ENGINEER_MANUAL.md` — engineer-facing operating manual
- `docs/BOSS_PRESENTATION.md` — executive summary in slide-note format
- `docs/MCP_Gateway_Platform_Presentation.pdf` — generated presentation PDF
- `scripts/generate_mcp_platform_presentation_pdf.py` — PDF generator for the presentation

## Platform summary

Current deployed services:

- **MCPX Gateway** on `http://10.208.0.162:9000/mcp`
- **MCPX Dashboard** on `http://10.208.0.162:5173`
- **Coder** on `http://10.208.0.162:7080`
- **vSphere MCP** on `http://10.208.0.162:8000/mcp`
- **FortiGate MCP** on `http://10.208.0.162:8814/fortigate-mcp/sse`

## Regenerating the PDF

If `reportlab` is installed locally:

```bash
python3 scripts/generate_mcp_platform_presentation_pdf.py
```
