"""
Executive Resume Generator for Sylvester Floyd Carter IV.
Compiles a top 5% Executive Resume PDF using ReportLab.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
from reportlab.lib.units import inch

def build_pdf(filename="career_agent/resumes/Sylvester_Floyd_Carter_IV_Resume.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1A2B4C")   # Deep Executive Navy
    secondary_color = colors.HexColor("#334E68") # Slate Blue
    body_color = colors.HexColor("#243B53")      # Charcoal Navy
    accent_bar = colors.HexColor("#CBD2D9")      # Light Slate Divider

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=secondary_color,
        alignment=0
    )

    contact_style = ParagraphStyle(
        'ContactLine',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=body_color,
        alignment=0
    )

    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4
    )

    job_title_style = ParagraphStyle(
        'JobTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=primary_color
    )

    job_company_style = ParagraphStyle(
        'JobCompany',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=secondary_color
    )

    job_meta_style = ParagraphStyle(
        'JobMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#627D98"),
        alignment=2 # Right
    )

    bullet_style = ParagraphStyle(
        'BulletText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=body_color,
        leftIndent=12,
        firstLineIndent=-12,
        spaceBefore=2
    )

    body_summary = ParagraphStyle(
        'BodySummary',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=body_color,
        spaceBefore=2,
        spaceAfter=6
    )

    story = []

    # Header Block
    story.append(Paragraph("SYLVESTER FLOYD CARTER IV", title_style))
    story.append(Spacer(1, 2))
    story.append(Paragraph("EXECUTIVE AI TRANSFORMATION LEADER & AGENTIC STRATEGY DIRECTOR", subtitle_style))
    story.append(Spacer(1, 3))
    contact_line = (
        "Montgomery, TX (Greater Houston Area / Remote Executive) &nbsp;|&nbsp; "
        "sylvesterfcarter@icloud.com &nbsp;|&nbsp; "
        "linkedin.com/in/sylvestercarter &nbsp;|&nbsp; "
        "github.com/BrijStream-Technologies"
    )
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=2, spaceAfter=8))

    # Executive Profile
    story.append(Paragraph("EXECUTIVE PROFILE & VALUE PROPOSITION", section_header))
    summary_text = (
        "Accomplished executive leader with over 20 years of operational P&amp;L mastery, high-stakes IP asset management, "
        "and pioneer-level agentic AI system orchestration. Proven history managing global multi-million-dollar entertainment "
        "and catalog assets for iconic Diamond and Grammy-winning artists (Destiny's Child/Beyoncé, Mary J. Blige, TLC, Mary Mary), "
        "paired with executive advisory for K-Pop pioneers (Park Bom / 2NE1). As founder and chief AI architect of BrijStream Technologies, "
        "pioneered high-leverage agentic orchestration—steering autonomous AI agent swarms to construct and verify production-grade, "
        "multi-tenant microservices, patent-backed dynamic synchronization engines (Patent PMG-2025-001), and open-source verification "
        "tooling (attest-cli, resolution-normalise). Specializes in bridging commercial strategy, corporate governance, and production "
        "agentic workflows to accelerate enterprise software delivery and eliminate operational bloat."
    )
    story.append(Paragraph(summary_text, body_summary))
    story.append(HRFlowable(width="100%", thickness=0.5, color=accent_bar, spaceBefore=4, spaceAfter=6))

    # Core Competencies Table
    story.append(Paragraph("CORE STRATEGIC COMPETENCIES", section_header))
    competencies = [
        [
            Paragraph("<b>• Enterprise AI Transformation:</b> Agentic workflow architecture, LLM system steering, automated QA & testing pipelines.", bullet_style),
            Paragraph("<b>• Executive Operations &amp; P&amp;L:</b> 20+ years managing multi-million-dollar catalog budgets, licensing, and corporate royalties.", bullet_style)
        ],
        [
            Paragraph("<b>• Intellectual Property & Patents:</b> Sole inventor, Patent PMG-2025-001 (Autonomous Media & Dynamic Audio Synchronization).", bullet_style),
            Paragraph("<b>• Verification & Governance:</b> Vendor-neutral billing attestation, Phonorecords IV compliance, zero-slop audit mechanisms.", bullet_style)
        ],
        [
            Paragraph("<b>• Force-Multiplier Product Velocity:</b> Directing AI fleets to ship full-stack platforms with zero large-team engineering drag.", bullet_style),
            Paragraph("<b>• Cross-Sector Stakeholder Alignment:</b> Media/Entertainment, Energy/Industrial transformation, and fintech settlement rails.", bullet_style)
        ]
    ]
    comp_table = Table(competencies, colWidths=[265, 265])
    comp_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(comp_table)
    story.append(HRFlowable(width="100%", thickness=0.5, color=accent_bar, spaceBefore=6, spaceAfter=6))

    # Executive Experience
    story.append(Paragraph("EXECUTIVE & TECHNICAL LEADERSHIP EXPERIENCE", section_header))

    # Role 1: BrijStream
    r1_header = [
        [Paragraph("Co-Founder & Chief AI System Orchestrator", job_title_style), Paragraph("2019 – Present", job_meta_style)],
        [Paragraph("BrijStream Technologies / Kyvryn Platform &nbsp;•&nbsp; Houston / The Woodlands & Remote", job_company_style), Paragraph("", job_meta_style)]
    ]
    t1 = Table(r1_header, colWidths=[380, 150])
    t1.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
    story.append(t1)
    story.append(Spacer(1, 3))
    story.append(Paragraph("• <b>Autonomous AI Fleet Steering:</b> Architected and orchestrated multi-agent AI coding swarms (Antigravity, Claude Code) to build, test, and deploy 88,000+ lines of production-grade microservices across Go, Python, TypeScript, and SQL with 100% test integrity (455/456 automated test suites).", bullet_style))
    story.append(Paragraph("• <b>Patent-Backed Media Architecture:</b> Invented and implemented core algorithms for Provisional Patent PMG-2025-001, providing autonomous dynamic audio ducking, energy tempo matching, and real-time soundtrack substitution for streaming platforms.", bullet_style))
    story.append(Paragraph("• <b>Open-Source Attestation Tooling:</b> Built and open-sourced <i>attest-cli</i> and <i>resolution-normalise</i> (github.com/BrijStream-Technologies), creating vendor-neutral compute verification, billing attestation, and deterministic prompt auditability.", bullet_style))
    story.append(Paragraph("• <b>Settlement & Royalty Infrastructure:</b> Designed high-concurrency automated split settlement engine enforcing exact statutory royalties (54.7% net master, 15.3% statutory publishing, 30.0% platform retention) with instant stablecoin (cUSD) micro-payout rails.", bullet_style))
    story.append(Spacer(1, 6))

    # Role 2: Executive Advisor Park Bom
    r2_header = [
        [Paragraph("Executive Strategic Advisor", job_title_style), Paragraph("2018 – Present", job_meta_style)],
        [Paragraph("Brij Brands &nbsp;•&nbsp; Seoul, KR / Los Angeles, CA", job_company_style), Paragraph("", job_meta_style)]
    ]
    t2 = Table(r2_header, colWidths=[380, 150])
    t2.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
    story.append(t2)
    story.append(Spacer(1, 3))
    story.append(Paragraph("• Advised Park Bom of iconic K-Pop group 2NE1 (Billboard 200 pioneers, MAMA Daesang Winners, 66M+ digital downloads) on global intellectual property, streaming distribution, and cross-border commercial partnerships.", bullet_style))
    story.append(Paragraph("• Structured digital monetization and catalog sync initiatives across North American and East Asian media rights ecosystems.", bullet_style))
    story.append(Spacer(1, 6))

    # Role 3: Music World / Sanctuary Group
    r3_header = [
        [Paragraph("Senior Director of Operations (Records, Publishing, Touring, Merch)", job_title_style), Paragraph("2004 – 2006", job_meta_style)],
        [Paragraph("Music World Entertainment / Sanctuary Group &nbsp;•&nbsp; Houston, TX", job_company_style), Paragraph("", job_meta_style)]
    ]
    t3 = Table(r3_header, colWidths=[380, 150])
    t3.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
    story.append(KeepTogether([
        t3,
        Spacer(1, 3),
        Paragraph("• Directed end-to-end operational execution across four commercial divisions for the world's #1 urban artist management enterprise.", bullet_style),
        Paragraph("• Managed multi-million-dollar operational budgets and tour logistics for global superstar roster: Destiny's Child / Beyoncé (32x Grammy Award Winner), Mary J. Blige (9x Grammy Award Winner), Earth Wind &amp; Fire, and Chaka Khan.", bullet_style),
        Paragraph("• Negotiated and audited multi-tier publishing administration, master licensing agreements, and vendor supply chain logistics.", bullet_style),
        Spacer(1, 6),
    ]))

    # Role 4: Yysman & Left Eye
    r4_header = [
        [Paragraph("Founder & CEO / Principal Artist Manager", job_title_style), Paragraph("1997 – 2004", job_meta_style)],
        [Paragraph("Yysman, Inc. & Left Eye Management &nbsp;•&nbsp; Atlanta, GA / Houston, TX", job_company_style), Paragraph("", job_meta_style)]
    ]
    t4 = Table(r4_header, colWidths=[380, 150])
    t4.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('PADDING', (0,0), (-1,-1), 0)]))
    story.append(t4)
    story.append(Spacer(1, 3))
    story.append(Paragraph("• Managed Lisa 'Left Eye' Lopes of TLC (5x Grammy Winner, RIAA 12x Diamond Certified, 65M+ records sold), steering business operations, television production, and endorsement contracts.", bullet_style))
    story.append(Paragraph("• Built Yysman Inc. into premier management firm representing Mary Mary (4x Grammy Winners), Myron Butler, and multi-platinum producers.", bullet_style))
    story.append(Spacer(1, 6))

    # Education & Verification Flagships
    story.append(HRFlowable(width="100%", thickness=0.5, color=accent_bar, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph("EDUCATION, PATENTS & VERIFIED FLAGSHIPS", section_header))

    ed_flagships = [
        [
            Paragraph("<b>Education:</b> Bachelor of Arts (BA) in Finance, Clark Atlanta University", bullet_style),
            Paragraph("<b>Patent PMG-2025-001:</b> Autonomous Dynamic Audio & Media Synchronization", bullet_style)
        ],
        [
            Paragraph("<b>Flagship 1:</b> BrijStream Streaming Engine (High-concurrency media & settlement)", bullet_style),
            Paragraph("<b>Flagship 2:</b> attest-cli (Vendor-neutral billing & execution attestation)", bullet_style)
        ],
        [
            Paragraph("<b>Flagship 3:</b> resolution-normalise (Deterministic prompt & schema governance)", bullet_style),
            Paragraph("<b>Domain Expertise:</b> Enterprise AI Transformation, Phonorecords IV, Creator AI Rights", bullet_style)
        ]
    ]
    ed_table = Table(ed_flagships, colWidths=[265, 265])
    ed_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(ed_table)

    doc.build(story)
    print(f"Successfully generated executive resume at {filename} (Size: {os.path.getsize(filename)} bytes)")

if __name__ == "__main__":
    build_pdf()
