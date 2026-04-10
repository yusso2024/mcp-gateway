from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "docs" / "MCP_Gateway_Platform_Presentation.pdf"


SLIDES = [
    {
        "title": "MCP Gateway Platform Summary",
        "bullets": [
            "Shared MCP platform deployed on a single Ubuntu 24.04 VM.",
            "Centralized access for engineers through MCPX instead of per-tool setup.",
            "Current integrations: vSphere MCP, FortiGate MCP, MCPX, and Coder.",
            "Business result: faster onboarding, lower tool sprawl, better operational control.",
        ],
    },
    {
        "title": "Business Problem Solved",
        "bullets": [
            "Before: each engineer had to wire tools independently.",
            "Before: infrastructure automations were fragmented and hard to govern.",
            "After: one gateway endpoint serves approved MCP tools.",
            "After: browser workspaces reduce local setup friction.",
        ],
    },
    {
        "title": "What Was Deployed",
        "bullets": [
            "MCPX gateway at 10.208.0.162:9000/mcp.",
            "Coder browser workspaces at 10.208.0.162:7080.",
            "vSphere MCP upstream at 10.208.0.162:8000/mcp.",
            "FortiGate MCP upstream at 10.208.0.162:8814/fortigate-mcp/sse.",
            "Expanded VM storage from a 19 GB root filesystem to 38 GB usable LVM.",
        ],
    },
    {
        "title": "Current Architecture",
        "bullets": [
            "Engineer browser or MCP client connects to Coder or directly to MCPX.",
            "MCPX routes requests to isolated upstream MCP servers.",
            "vSphere MCP handles VMware and vCenter operations.",
            "FortiGate MCP handles firewall operations once production credentials are set.",
        ],
    },
    {
        "title": "Benefits",
        "bullets": [
            "One endpoint for engineers instead of many.",
            "Consistent browser-first workflow via Coder.",
            "Per-tool container isolation reduces blast radius.",
            "New MCP servers can be added centrally through MCPX config.",
        ],
    },
    {
        "title": "Current Gaps and Risks",
        "bullets": [
            "MCPX dashboard has no built-in authentication.",
            "Gateway and dashboard are still HTTP, not HTTPS.",
            "FortiGate integration still needs production credentials.",
            "Saved Setups in MCPX is limited without Lunar Hub connectivity.",
        ],
    },
    {
        "title": "Recommended Next Phase",
        "bullets": [
            "Put Caddy or equivalent reverse proxy in front of MCPX and Coder.",
            "Add dashboard authentication and protect the MCP endpoint.",
            "Replace placeholder FortiGate credentials with scoped production tokens.",
            "Add operating rules for read-only vs write-enabled tool access.",
        ],
    },
    {
        "title": "Conclusion",
        "bullets": [
            "The platform is operational today and already usable by engineers.",
            "The main remaining work is hardening, not redesign.",
            "This creates a practical foundation for AI-assisted infrastructure operations.",
        ],
    },
]


def _fit_title(title: str, max_width: float, font_name: str, font_size: float) -> str:
    if stringWidth(title, font_name, font_size) <= max_width:
        return title
    words = title.split()
    lines = []
    current = []
    for word in words:
        candidate = " ".join(current + [word])
        if stringWidth(candidate, font_name, font_size) <= max_width:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return "<br/>".join(lines)


def build() -> None:
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "SlideTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=colors.HexColor("#17324d"),
        spaceAfter=18,
    )
    bullet_style = ParagraphStyle(
        "SlideBullet",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=16,
        leading=22,
        textColor=colors.black,
        leftIndent=22,
        firstLineIndent=-10,
        spaceAfter=10,
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=landscape(letter),
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.5 * inch,
    )

    story = []
    usable_width = landscape(letter)[0] - doc.leftMargin - doc.rightMargin
    for idx, slide in enumerate(SLIDES):
        fitted_title = _fit_title(slide["title"], usable_width, "Helvetica-Bold", 24)
        story.append(Paragraph(fitted_title, title_style))
        story.append(Spacer(1, 0.15 * inch))
        for bullet in slide["bullets"]:
            story.append(Paragraph(f"• {bullet}", bullet_style))
        if idx < len(SLIDES) - 1:
            story.append(PageBreak())

    doc.build(story)


if __name__ == "__main__":
    build()
