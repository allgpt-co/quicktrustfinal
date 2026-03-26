"""PDF, CSV, and PPTX report rendering for QuickTrust GRC reports.

Supports report types: compliance_summary, risk_report, evidence_audit,
training_completion, vendor_risk.
"""

from __future__ import annotations

import csv
import io
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)


# ---------------------------------------------------------------------------
# PDF rendering
# ---------------------------------------------------------------------------

def render_pdf(report_data: dict, report_type: str) -> bytes:
    """Generate a PDF document from *report_data* and return raw bytes."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=20,
        textColor=colors.HexColor("#1a237e"),
    )
    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=8,
        textColor=colors.HexColor("#283593"),
    )
    body_style = styles["BodyText"]

    elements: list = []

    # Title
    title_map = {
        "compliance_summary": "Compliance Summary Report",
        "risk_report": "Risk Assessment Report",
        "evidence_audit": "Evidence Audit Report",
        "training_completion": "Training Completion Report",
        "vendor_risk": "Vendor Risk Report",
    }
    title = title_map.get(report_type, "Report")
    elements.append(Paragraph(title, title_style))

    # Metadata
    generated_at = report_data.get("generated_at", datetime.utcnow().isoformat())
    elements.append(Paragraph(f"Generated: {generated_at}", body_style))
    elements.append(Spacer(1, 12))

    # Build sections based on report type
    if report_type == "compliance_summary":
        elements.extend(_build_compliance_summary_pdf(report_data, heading_style, body_style))
    elif report_type == "risk_report":
        elements.extend(_build_risk_report_pdf(report_data, heading_style, body_style))
    elif report_type == "evidence_audit":
        elements.extend(_build_evidence_audit_pdf(report_data, heading_style, body_style))
    elif report_type == "training_completion":
        elements.extend(_build_training_completion_pdf(report_data, heading_style, body_style))
    elif report_type == "vendor_risk":
        elements.extend(_build_vendor_risk_pdf(report_data, heading_style, body_style))

    doc.build(elements)
    return buf.getvalue()


def _make_table(headers: list[str], rows: list[list], col_widths: list[float] | None = None) -> Table:
    """Create a styled table with header row."""
    data = [headers] + rows
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f5f5f5")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#bdbdbd")),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("TOPPADDING", (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return table


def _build_compliance_summary_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    # Control stats
    ctrl = data.get("control_stats", {})
    if ctrl:
        elements.append(Paragraph("Control Status Overview", heading))
        rows = [
            ["Total Controls", str(ctrl.get("total", 0))],
            ["Implemented", str(ctrl.get("implemented", 0))],
            ["Draft", str(ctrl.get("draft", 0))],
            ["Partially Implemented", str(ctrl.get("partially_implemented", 0))],
            ["Not Implemented", str(ctrl.get("not_implemented", 0))],
            ["Not Applicable", str(ctrl.get("not_applicable", 0))],
        ]
        total = ctrl.get("total", 1) or 1
        impl = ctrl.get("implemented", 0)
        rows.append(["Compliance Score", f"{round(impl / total * 100)}%"])
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Controls detail table
    controls = data.get("controls", [])
    if controls:
        elements.append(Paragraph(f"Controls Detail ({len(controls)} items)", heading))
        ctrl_rows = [[c.get("title", "")[:60], c.get("status", ""), c.get("automation_level", "")] for c in controls[:30]]
        elements.append(_make_table(["Control", "Status", "Automation"], ctrl_rows, [3.5 * inch, 1.2 * inch, 1.2 * inch]))
        if len(controls) > 30:
            elements.append(Paragraph(f"... and {len(controls) - 30} more controls", body))
        elements.append(Spacer(1, 12))

    # Frameworks
    frameworks = data.get("frameworks", [])
    if frameworks:
        elements.append(Paragraph(f"Active Frameworks ({len(frameworks)})", heading))
        fw_rows = [[f.get("name", ""), f.get("version", "")] for f in frameworks]
        elements.append(_make_table(["Framework", "Version"], fw_rows, [4 * inch, 1.5 * inch]))
        elements.append(Spacer(1, 12))

    # Policy stats
    pol = data.get("policy_stats", {})
    if pol:
        elements.append(Paragraph("Policy Status", heading))
        rows = [
            ["Total Policies", str(pol.get("total", 0))],
            ["Published", str(pol.get("published", 0))],
        ]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Policies detail
    policies = data.get("policies", [])
    if policies:
        elements.append(Paragraph(f"Policies ({len(policies)})", heading))
        pol_rows = [[p.get("title", "")[:60], p.get("status", "")] for p in policies]
        elements.append(_make_table(["Policy", "Status"], pol_rows, [4.5 * inch, 1.2 * inch]))
        elements.append(Spacer(1, 12))

    # Risk stats
    risk = data.get("risk_stats", {})
    if risk:
        elements.append(Paragraph("Risk Overview", heading))
        rows = [
            ["Total Risks", str(risk.get("total", 0))],
            ["Average Score", str(risk.get("average_score", 0))],
        ]
        by_level = risk.get("by_risk_level", {})
        for level, count in by_level.items():
            rows.append([f"Risk Level: {level}", str(count)])
        elements.append(_make_table(["Metric", "Value"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Evidence stats
    ev = data.get("evidence_stats", {})
    if ev:
        elements.append(Paragraph("Evidence Collection", heading))
        rows = [["Total Evidence Items", str(ev.get("total", 0))]]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Evidence detail
    evidence_items = data.get("evidence_items", [])
    if evidence_items:
        elements.append(Paragraph(f"Evidence Items ({len(evidence_items)})", heading))
        ev_rows = [[e.get("title", "")[:55], e.get("status", ""), e.get("collection_method", "")] for e in evidence_items[:30]]
        elements.append(_make_table(["Evidence", "Status", "Method"], ev_rows, [3.5 * inch, 1.2 * inch, 1.2 * inch]))
        if len(evidence_items) > 30:
            elements.append(Paragraph(f"... and {len(evidence_items) - 30} more items", body))

    return elements


def _build_risk_report_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    risk = data.get("risk_stats", {})
    if risk:
        elements.append(Paragraph("Risk Summary", heading))
        rows = [
            ["Total Risks", str(risk.get("total", 0))],
            ["Average Risk Score", str(risk.get("average_score", 0))],
        ]
        by_level = risk.get("by_risk_level", {})
        for level, count in by_level.items():
            rows.append([f"Risk Level: {level.title()}", str(count)])
        by_status = risk.get("by_status", {})
        for status, count in by_status.items():
            rows.append([f"Status: {status.title()}", str(count)])
        elements.append(_make_table(["Metric", "Value"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Risk detail table
    risks = data.get("risks", [])
    if risks:
        elements.append(Paragraph(f"Risk Register ({len(risks)} items)", heading))
        risk_rows = [
            [r.get("title", "")[:50], r.get("risk_level", ""), r.get("status", ""), str(r.get("score", "N/A"))]
            for r in risks[:30]
        ]
        elements.append(_make_table(["Risk", "Level", "Status", "Score"], risk_rows, [3 * inch, 1 * inch, 1 * inch, 0.8 * inch]))
        if len(risks) > 30:
            elements.append(Paragraph(f"... and {len(risks) - 30} more risks", body))
    elif risk.get("total", 0) == 0:
        elements.append(Paragraph("No risks have been identified yet. This is a positive indicator of your security posture.", body))

    return elements


def _build_evidence_audit_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    ctrl = data.get("control_stats", {})
    if ctrl:
        elements.append(Paragraph("Controls Coverage", heading))
        total = ctrl.get("total", 1) or 1
        impl = ctrl.get("implemented", 0)
        rows = [
            ["Total Controls", str(ctrl.get("total", 0))],
            ["Implemented", str(impl)],
            ["Draft", str(ctrl.get("draft", 0))],
            ["Partially Implemented", str(ctrl.get("partially_implemented", 0))],
            ["Coverage Rate", f"{round(impl / total * 100)}%"],
        ]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    ev = data.get("evidence_stats", {})
    if ev:
        elements.append(Paragraph("Evidence Summary", heading))
        rows = [["Total Evidence Items", str(ev.get("total", 0))]]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Evidence detail table
    evidence_items = data.get("evidence_items", [])
    if evidence_items:
        elements.append(Paragraph(f"Evidence Inventory ({len(evidence_items)} items)", heading))
        ev_rows = [
            [e.get("title", "")[:50], e.get("status", ""), e.get("collection_method", "")]
            for e in evidence_items[:40]
        ]
        elements.append(_make_table(["Evidence Item", "Status", "Collection Method"], ev_rows, [3.5 * inch, 1.2 * inch, 1.2 * inch]))
        if len(evidence_items) > 40:
            elements.append(Paragraph(f"... and {len(evidence_items) - 40} more items", body))
        elements.append(Spacer(1, 12))

    # Controls with evidence mapping
    controls = data.get("controls", [])
    if controls:
        elements.append(Paragraph(f"Controls Audit Status ({len(controls)})", heading))
        ctrl_rows = [[c.get("title", "")[:50], c.get("status", ""), c.get("automation_level", "")] for c in controls[:30]]
        elements.append(_make_table(["Control", "Status", "Automation"], ctrl_rows, [3.5 * inch, 1.2 * inch, 1.2 * inch]))
        if len(controls) > 30:
            elements.append(Paragraph(f"... and {len(controls) - 30} more controls", body))

    return elements


def _build_training_completion_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    ts = data.get("training_stats", {})
    if ts:
        elements.append(Paragraph("Training Completion Summary", heading))
        total = ts.get("total_assignments", 0)
        completed = ts.get("completed", 0)
        overdue = ts.get("overdue", 0)
        rows = [
            ["Total Assignments", str(total)],
            ["Completed", str(completed)],
            ["Overdue", str(overdue)],
            ["Completion Rate", f"{ts.get('completion_rate', 0)}%"],
        ]
        elements.append(_make_table(["Metric", "Value"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    if ts.get("total_assignments", 0) == 0:
        elements.append(Paragraph("No training assignments have been created yet. Create training courses and assign them to employees to track completion.", body))

    # Training courses
    courses = data.get("courses", [])
    if courses:
        elements.append(Paragraph(f"Training Courses ({len(courses)})", heading))
        course_rows = [[c.get("title", "")[:50], c.get("status", ""), str(c.get("assigned_count", 0))] for c in courses]
        elements.append(_make_table(["Course", "Status", "Assigned"], course_rows, [3.5 * inch, 1.2 * inch, 1 * inch]))

    return elements


def _build_vendor_risk_pdf(data: dict, heading: ParagraphStyle, body: ParagraphStyle) -> list:
    elements: list = []

    # Summary section
    vs = data.get("vendor_stats", {})
    if vs:
        elements.append(Paragraph("Vendor Risk Summary", heading))
        rows = [
            ["Total Vendors", str(vs.get("total", 0))],
            ["Critical Tier", str(vs.get("critical", 0))],
            ["High Tier", str(vs.get("high", 0))],
            ["Medium Tier", str(vs.get("medium", 0))],
            ["Low Tier", str(vs.get("low", 0))],
        ]
        elements.append(_make_table(["Metric", "Count"], rows, [3.5 * inch, 2 * inch]))
        elements.append(Spacer(1, 12))

    # Vendor listing table
    vendors = data.get("vendors", [])
    if vendors:
        elements.append(Paragraph("Vendor Details", heading))
        vendor_rows = [
            [
                str(v.get("name", "")),
                str(v.get("risk_tier", "")),
                str(v.get("status", "")),
                str(v.get("last_assessment_date", "N/A")),
            ]
            for v in vendors
        ]
        elements.append(
            _make_table(
                ["Name", "Risk Tier", "Status", "Last Assessment Date"],
                vendor_rows,
                [2.5 * inch, 1.5 * inch, 1.5 * inch, 2 * inch],
            )
        )

    return elements


# ---------------------------------------------------------------------------
# CSV rendering
# ---------------------------------------------------------------------------

def render_csv(report_data: dict, report_type: str) -> bytes:
    """Generate a CSV file from *report_data* and return raw bytes (UTF-8)."""
    buf = io.StringIO()
    writer = csv.writer(buf)

    if report_type == "compliance_summary":
        _write_compliance_summary_csv(writer, report_data)
    elif report_type == "risk_report":
        _write_risk_report_csv(writer, report_data)
    elif report_type == "evidence_audit":
        _write_evidence_audit_csv(writer, report_data)
    elif report_type == "training_completion":
        _write_training_completion_csv(writer, report_data)
    elif report_type == "vendor_risk":
        _write_vendor_risk_csv(writer, report_data)
    else:
        # Fallback: dump all top-level keys as rows
        writer.writerow(["Key", "Value"])
        for key, value in report_data.items():
            writer.writerow([key, str(value)])

    return buf.getvalue().encode("utf-8")


def _write_compliance_summary_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Section", "Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Metadata", "Generated At", generated_at])

    ctrl = data.get("control_stats", {})
    if ctrl:
        writer.writerow(["Controls", "Total", ctrl.get("total", 0)])
        writer.writerow(["Controls", "Implemented", ctrl.get("implemented", 0)])
        writer.writerow(["Controls", "Draft", ctrl.get("draft", 0)])

    risk = data.get("risk_stats", {})
    if risk:
        for k, v in risk.items():
            writer.writerow(["Risk", k, v])

    pol = data.get("policy_stats", {})
    if pol:
        writer.writerow(["Policies", "Total", pol.get("total", 0)])
        writer.writerow(["Policies", "Published", pol.get("published", 0)])

    ev = data.get("evidence_stats", {})
    if ev:
        writer.writerow(["Evidence", "Total", ev.get("total", 0)])


def _write_risk_report_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Generated At", generated_at])

    risk = data.get("risk_stats", {})
    if risk:
        for k, v in risk.items():
            writer.writerow([k, v])


def _write_evidence_audit_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Section", "Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Metadata", "Generated At", generated_at])

    ctrl = data.get("control_stats", {})
    if ctrl:
        writer.writerow(["Controls", "Total", ctrl.get("total", 0)])
        writer.writerow(["Controls", "Implemented", ctrl.get("implemented", 0)])
        writer.writerow(["Controls", "Draft", ctrl.get("draft", 0)])

    ev = data.get("evidence_stats", {})
    if ev:
        writer.writerow(["Evidence", "Total", ev.get("total", 0)])


def _write_training_completion_csv(writer: csv.writer, data: dict) -> None:
    writer.writerow(["Metric", "Value"])

    generated_at = data.get("generated_at", "")
    writer.writerow(["Generated At", generated_at])

    ts = data.get("training_stats", {})
    if ts:
        writer.writerow(["Total Assignments", ts.get("total_assignments", 0)])
        writer.writerow(["Completed", ts.get("completed", 0)])
        writer.writerow(["Completion Rate (%)", ts.get("completion_rate", 0)])


def _write_vendor_risk_csv(writer: csv.writer, data: dict) -> None:
    generated_at = data.get("generated_at", "")

    # Summary header
    writer.writerow(["Section", "Metric", "Value"])
    writer.writerow(["Metadata", "Generated At", generated_at])

    vs = data.get("vendor_stats", {})
    if vs:
        writer.writerow(["Summary", "Total Vendors", vs.get("total", 0)])
        writer.writerow(["Summary", "Critical Tier", vs.get("critical", 0)])
        writer.writerow(["Summary", "High Tier", vs.get("high", 0)])
        writer.writerow(["Summary", "Medium Tier", vs.get("medium", 0)])
        writer.writerow(["Summary", "Low Tier", vs.get("low", 0)])

    # Vendor details
    vendors = data.get("vendors", [])
    if vendors:
        writer.writerow([])  # blank separator row
        writer.writerow(["Name", "Risk Tier", "Status", "Last Assessment Date"])
        for v in vendors:
            writer.writerow([
                v.get("name", ""),
                v.get("risk_tier", ""),
                v.get("status", ""),
                v.get("last_assessment_date", "N/A"),
            ])


# ---------------------------------------------------------------------------
# PPTX rendering
# ---------------------------------------------------------------------------

def render_pptx(report_type: str, report_data: dict) -> bytes:
    """Generate a PPTX presentation from *report_data* and return raw bytes."""
    from pptx import Presentation
    from pptx.util import Inches, Pt, Emu
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN

    BRAND_DARK = RGBColor(0x1A, 0x23, 0x7E)
    BRAND_MID = RGBColor(0x28, 0x35, 0x93)
    BRAND_LIGHT = RGBColor(0x3F, 0x51, 0xB5)
    WHITE = RGBColor(0xFF, 0xFF, 0xFF)
    DARK_TEXT = RGBColor(0x21, 0x21, 0x21)

    title_map = {
        "compliance_summary": "Compliance Summary Report",
        "risk_report": "Risk Assessment Report",
        "evidence_audit": "Evidence Audit Report",
        "training_completion": "Training Completion Report",
        "vendor_risk": "Vendor Risk Report",
    }

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # -----------------------------------------------------------------------
    # Helper: add a solid-colour background rectangle behind the slide
    # -----------------------------------------------------------------------
    def _add_bg_rect(slide, color: RGBColor):
        from pptx.util import Emu as _Emu
        shape = slide.shapes.add_shape(
            1,  # MSO_SHAPE.RECTANGLE
            _Emu(0), _Emu(0),
            prs.slide_width, prs.slide_height,
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        # Send to back so text sits above
        sp = shape._element
        sp.getparent().remove(sp)
        slide.shapes._spTree.insert(2, sp)

    # -----------------------------------------------------------------------
    # Helper: add a table slide
    # -----------------------------------------------------------------------
    def _add_table_slide(title_text: str, headers: list[str], rows: list[list[str]]):
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # blank layout
        # Title
        txBox = slide.shapes.add_textbox(Inches(0.75), Inches(0.4), Inches(11), Inches(0.8))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = BRAND_DARK
        p.alignment = PP_ALIGN.LEFT

        if not rows:
            return slide

        num_rows = min(len(rows) + 1, 20)  # cap at 20 rows for readability
        num_cols = len(headers)
        table_width = Inches(11)
        table_left = Inches(1.0)
        table_top = Inches(1.5)
        table_height = Inches(0.4) * num_rows

        table_shape = slide.shapes.add_table(
            num_rows, num_cols, table_left, table_top, table_width, table_height
        )
        table = table_shape.table

        # Style header row
        for col_idx, header in enumerate(headers):
            cell = table.cell(0, col_idx)
            cell.text = header
            for paragraph in cell.text_frame.paragraphs:
                paragraph.font.size = Pt(12)
                paragraph.font.bold = True
                paragraph.font.color.rgb = WHITE
                paragraph.alignment = PP_ALIGN.CENTER
            cell.fill.solid()
            cell.fill.fore_color.rgb = BRAND_DARK

        # Style data rows
        for row_idx, row in enumerate(rows[: num_rows - 1]):
            for col_idx, value in enumerate(row):
                cell = table.cell(row_idx + 1, col_idx)
                cell.text = str(value)
                for paragraph in cell.text_frame.paragraphs:
                    paragraph.font.size = Pt(11)
                    paragraph.font.color.rgb = DARK_TEXT
                    paragraph.alignment = PP_ALIGN.LEFT
                # Alternate row colours
                cell.fill.solid()
                cell.fill.fore_color.rgb = (
                    RGBColor(0xF5, 0xF5, 0xF5) if row_idx % 2 == 0 else WHITE
                )

        return slide

    # -----------------------------------------------------------------------
    # Slide 1 — Title slide
    # -----------------------------------------------------------------------
    slide_title = prs.slides.add_slide(prs.slide_layouts[5])  # blank
    _add_bg_rect(slide_title, BRAND_DARK)

    txBox = slide_title.shapes.add_textbox(
        Inches(1.5), Inches(2.0), Inches(10), Inches(1.5)
    )
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title_map.get(report_type, "Report")
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Subtitle with date
    generated_at = report_data.get("generated_at", datetime.utcnow().isoformat())
    txBox2 = slide_title.shapes.add_textbox(
        Inches(1.5), Inches(3.8), Inches(10), Inches(0.8)
    )
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = f"Generated: {generated_at}"
    p2.font.size = Pt(18)
    p2.font.color.rgb = RGBColor(0xBB, 0xDE, 0xFB)
    p2.alignment = PP_ALIGN.CENTER

    # Footer branding
    txBox3 = slide_title.shapes.add_textbox(
        Inches(1.5), Inches(5.5), Inches(10), Inches(0.5)
    )
    tf3 = txBox3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "QuickTrust GRC Platform"
    p3.font.size = Pt(14)
    p3.font.color.rgb = RGBColor(0x90, 0xCA, 0xF9)
    p3.alignment = PP_ALIGN.CENTER

    # -----------------------------------------------------------------------
    # Slide 2 — Summary / Key Metrics
    # -----------------------------------------------------------------------
    summary_headers = ["Metric", "Value"]
    summary_rows: list[list[str]] = []

    if report_type == "compliance_summary":
        ctrl = report_data.get("control_stats", {})
        risk = report_data.get("risk_stats", {})
        pol = report_data.get("policy_stats", {})
        ev = report_data.get("evidence_stats", {})
        if ctrl:
            summary_rows.append(["Total Controls", str(ctrl.get("total", 0))])
            summary_rows.append(["Implemented Controls", str(ctrl.get("implemented", 0))])
            summary_rows.append(["Draft Controls", str(ctrl.get("draft", 0))])
        if risk:
            for k, v in risk.items():
                summary_rows.append([str(k), str(v)])
        if pol:
            summary_rows.append(["Total Policies", str(pol.get("total", 0))])
            summary_rows.append(["Published Policies", str(pol.get("published", 0))])
        if ev:
            summary_rows.append(["Total Evidence Items", str(ev.get("total", 0))])

    elif report_type == "risk_report":
        risk = report_data.get("risk_stats", {})
        if risk:
            for k, v in risk.items():
                summary_rows.append([str(k), str(v)])

    elif report_type == "evidence_audit":
        ctrl = report_data.get("control_stats", {})
        ev = report_data.get("evidence_stats", {})
        if ctrl:
            summary_rows.append(["Total Controls", str(ctrl.get("total", 0))])
            summary_rows.append(["Implemented Controls", str(ctrl.get("implemented", 0))])
            summary_rows.append(["Draft Controls", str(ctrl.get("draft", 0))])
        if ev:
            summary_rows.append(["Total Evidence Items", str(ev.get("total", 0))])

    elif report_type == "training_completion":
        ts = report_data.get("training_stats", {})
        if ts:
            summary_rows.append(["Total Assignments", str(ts.get("total_assignments", 0))])
            summary_rows.append(["Completed", str(ts.get("completed", 0))])
            summary_rows.append(["Completion Rate", f"{ts.get('completion_rate', 0)}%"])

    elif report_type == "vendor_risk":
        vs = report_data.get("vendor_stats", {})
        if vs:
            summary_rows.append(["Total Vendors", str(vs.get("total", 0))])
            summary_rows.append(["Critical Tier", str(vs.get("critical", 0))])
            summary_rows.append(["High Tier", str(vs.get("high", 0))])
            summary_rows.append(["Medium Tier", str(vs.get("medium", 0))])
            summary_rows.append(["Low Tier", str(vs.get("low", 0))])

    _add_table_slide("Key Metrics", summary_headers, summary_rows)

    # -----------------------------------------------------------------------
    # Slide 3+ — Details (type-specific breakdowns)
    # -----------------------------------------------------------------------
    if report_type == "compliance_summary":
        # Control status breakdown
        ctrl = report_data.get("control_stats", {})
        if ctrl:
            _add_table_slide(
                "Control Status Breakdown",
                ["Status", "Count"],
                [
                    ["Implemented", str(ctrl.get("implemented", 0))],
                    ["Draft", str(ctrl.get("draft", 0))],
                    ["Total", str(ctrl.get("total", 0))],
                ],
            )

        # Policy breakdown
        pol = report_data.get("policy_stats", {})
        if pol:
            _add_table_slide(
                "Policy Status",
                ["Metric", "Count"],
                [
                    ["Published", str(pol.get("published", 0))],
                    ["Total", str(pol.get("total", 0))],
                ],
            )

    elif report_type == "risk_report":
        risk = report_data.get("risk_stats", {})
        if risk:
            _add_table_slide(
                "Risk Statistics Detail",
                ["Metric", "Value"],
                [[str(k), str(v)] for k, v in risk.items()],
            )

    elif report_type == "evidence_audit":
        ctrl = report_data.get("control_stats", {})
        ev = report_data.get("evidence_stats", {})
        detail_rows: list[list[str]] = []
        if ctrl:
            detail_rows.append(["Controls - Total", str(ctrl.get("total", 0))])
            detail_rows.append(["Controls - Implemented", str(ctrl.get("implemented", 0))])
            detail_rows.append(["Controls - Draft", str(ctrl.get("draft", 0))])
        if ev:
            detail_rows.append(["Evidence - Total", str(ev.get("total", 0))])
        if detail_rows:
            _add_table_slide("Evidence Audit Details", ["Category", "Value"], detail_rows)

    elif report_type == "training_completion":
        ts = report_data.get("training_stats", {})
        if ts:
            _add_table_slide(
                "Training Completion Details",
                ["Metric", "Value"],
                [
                    ["Total Assignments", str(ts.get("total_assignments", 0))],
                    ["Completed", str(ts.get("completed", 0))],
                    ["Completion Rate", f"{ts.get('completion_rate', 0)}%"],
                ],
            )

    elif report_type == "vendor_risk":
        vendors = report_data.get("vendors", [])
        if vendors:
            _add_table_slide(
                "Vendor Risk Details",
                ["Vendor", "Risk Tier", "Status"],
                [
                    [
                        str(v.get("name", "")),
                        str(v.get("risk_tier", "")),
                        str(v.get("status", "")),
                    ]
                    for v in vendors[:18]
                ],
            )

    # Serialize to bytes
    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()
