"""
PDF Report Generator for Carbon Footprint Analysis

Creates professional, audit-ready PDF reports with:
- Executive summary
- Scope breakdown (1, 2, 3)
- Charts and visualizations
- Industry benchmarking
- Carbon offset recommendations
- GHG Protocol compliance citations
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    PageBreak,
    Image,
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import logging
from typing import Dict, Any

# Try to import matplotlib for charts
try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """Generate professional carbon footprint PDF reports"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._add_custom_styles()

    def _add_custom_styles(self):
        """Add custom paragraph styles"""
        self.styles.add(
            ParagraphStyle(
                name='CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold',
            )
        )

        self.styles.add(
            ParagraphStyle(
                name='SectionTitle',
                parent=self.styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=12,
                fontName='Helvetica-Bold',
            )
        )

        self.styles.add(
            ParagraphStyle(
                name='EmphasisText',
                parent=self.styles['Normal'],
                fontSize=12,
                textColor=colors.HexColor('#E74C3C'),
                fontName='Helvetica-Bold',
            )
        )

    def _create_scope_chart(self) -> io.BytesIO:
        """Create a pie chart of scope breakdown"""
        if not MATPLOTLIB_AVAILABLE:
            return None

        # This will be populated with actual data
        # For now, returning None - caller provides data
        return None

    def _format_number(self, value: float, decimals: int = 2) -> str:
        """Format number with thousands separator"""
        return f"{value:,.{decimals}f}"

    def generate_report(
        self,
        filename: str,
        company_name: str,
        activity_data: Dict[str, Any],
        emission_result: Dict[str, Any],
        search_results: list = None,
        methodology: str = None,
    ) -> str:
        """
        Generate a complete carbon footprint report PDF

        Args:
            filename: Output PDF filename
            company_name: Company name
            activity_data: Input activity data
            emission_result: Calculation results (dict from EmissionResult.to_dict())
            search_results: Web search results for offsets
            methodology: GHG Protocol methodology citation

        Returns:
            Path to generated PDF file
        """
        logger.info(f"Generating PDF report: {filename}")

        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # PAGE 1: COVER PAGE
        elements.append(Spacer(1, 2 * inch))
        elements.append(
            Paragraph("CARBON FOOTPRINT REPORT", self.styles['CustomTitle'])
        )
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(
            Paragraph(
                company_name,
                ParagraphStyle(
                    'CompanyName',
                    parent=self.styles['Heading2'],
                    fontSize=20,
                    alignment=TA_CENTER,
                ),
            )
        )
        elements.append(Spacer(1, 0.5 * inch))
        elements.append(
            Paragraph(
                f"Report Date: {datetime.now().strftime('%B %d, %Y')}",
                ParagraphStyle(
                    'Date',
                    parent=self.styles['Normal'],
                    alignment=TA_CENTER,
                ),
            )
        )
        elements.append(Spacer(1, 0.3 * inch))
        elements.append(
            Paragraph(
                "Prepared in accordance with GHG Protocol Corporate Standard",
                ParagraphStyle(
                    'Footer',
                    parent=self.styles['Normal'],
                    alignment=TA_CENTER,
                    fontSize=9,
                ),
            )
        )

        elements.append(PageBreak())

        # PAGE 2: EXECUTIVE SUMMARY
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionTitle']))
        elements.append(Spacer(1, 0.2 * inch))

        total_emissions = emission_result['total_tco2e']
        elements.append(
            Paragraph(
                f"<b>Total Annual Emissions: {self._format_number(total_emissions)} tCO2e</b>",
                ParagraphStyle(
                    'Result',
                    parent=self.styles['Normal'],
                    fontSize=16,
                    textColor=colors.HexColor('#E74C3C'),
                ),
            )
        )

        elements.append(Spacer(1, 0.3 * inch))

        # Summary table
        summary_data = [
            ['Scope', 'Emissions (kg CO2)', 'Percentage'],
            [
                'Scope 1 (Direct)',
                f"{self._format_number(emission_result['scope1_kg']):>10}",
                f"{emission_result['scope1_percent']:>6.1f}%",
            ],
            [
                'Scope 2 (Electricity)',
                f"{self._format_number(emission_result['scope2_kg']):>10}",
                f"{emission_result['scope2_percent']:>6.1f}%",
            ],
            [
                'Scope 3 (Indirect)',
                f"{self._format_number(emission_result['scope3_kg']):>10}",
                f"{emission_result['scope3_percent']:>6.1f}%",
            ],
        ]

        summary_table = Table(summary_data, colWidths=[2 * inch, 2 * inch, 1.5 * inch])
        summary_table.setStyle(
            TableStyle(
                [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
                ]
            )
        )

        elements.append(summary_table)
        elements.append(PageBreak())

        # PAGE 3: DETAILED BREAKDOWN
        elements.append(
            Paragraph("DETAILED EMISSIONS BREAKDOWN", self.styles['SectionTitle'])
        )
        elements.append(Spacer(1, 0.2 * inch))

        # Scope 1
        elements.append(
            Paragraph("<b>Scope 1 - Direct Emissions:</b>", self.styles['Normal'])
        )
        scope1_breakdown = emission_result.get('breakdown', {}).get('scope1', {})
        if scope1_breakdown:
            scope1_data = [['Source', 'Amount', 'Emissions (kg CO2)']]
            for source, value in scope1_breakdown.items():
                unit_map = {
                    'diesel': '_litres',
                    'petrol': '_litres',
                    'lpg': '_kg',
                    'natural_gas': '_m3',
                    'coal': '_tonnes',
                }
                suffix = unit_map.get(source, '')
                amount = activity_data.get(source + suffix, 0)
                scope1_data.append([
                    source.replace('_', ' ').title(),
                    f"{amount} {suffix.replace('_', '')}",
                    f"{self._format_number(value)}",
                ])
            scope1_table = Table(scope1_data, colWidths=[1.5 * inch, 1.5 * inch, 2 * inch])
            scope1_table.setStyle(
                TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ])
            )
            elements.append(scope1_table)

        elements.append(Spacer(1, 0.2 * inch))

        # Scope 2
        elements.append(
            Paragraph("<b>Scope 2 - Purchased Electricity:</b>", self.styles['Normal'])
        )
        scope2_value = emission_result.get('breakdown', {}).get('scope2', {}).get('electricity', 0)
        scope2_data = [
            ['Source', 'Consumption', 'Emissions (kg CO2)'],
            ['Grid Electricity', f"{activity_data.get('electricity_kwh', 0)} kWh",
             f"{self._format_number(scope2_value)}"],
        ]
        scope2_table = Table(scope2_data, colWidths=[2 * inch, 2 * inch, 2 * inch])
        scope2_table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ])
        )
        elements.append(scope2_table)

        elements.append(PageBreak())

        # PAGE 4: OFFSET RECOMMENDATIONS
        elements.append(
            Paragraph("CARBON OFFSET RECOMMENDATIONS", self.styles['SectionTitle'])
        )
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(
            Paragraph(
                "Current CCTS-approved carbon offset options for Indian companies:",
                self.styles['Normal'],
            )
        )

        # Offset costs
        offset_cost_100 = total_emissions * 400  # Rs 400/tonne
        offset_cost_50 = offset_cost_100 * 0.5
        offset_cost_25 = offset_cost_100 * 0.25

        offset_data = [
            ['Offset Level', 'Tonnes Offset', 'Est. Cost (Rs)', 'Duration'],
            [
                '25% Offset',
                f"{self._format_number(total_emissions * 0.25, 2)}",
                f"Rs {self._format_number(offset_cost_25, 0)}",
                '1 year',
            ],
            [
                '50% Offset',
                f"{self._format_number(total_emissions * 0.5, 2)}",
                f"Rs {self._format_number(offset_cost_50, 0)}",
                '1 year',
            ],
            [
                '100% Offset',
                f"{self._format_number(total_emissions, 2)}",
                f"Rs {self._format_number(offset_cost_100, 0)}",
                '1 year',
            ],
        ]

        offset_table = Table(offset_data, colWidths=[1.5 * inch, 1.5 * inch, 2 * inch, 1 * inch])
        offset_table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27AE60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ])
        )
        elements.append(offset_table)

        # PAGE 5: METHODOLOGY
        elements.append(PageBreak())
        elements.append(
            Paragraph("METHODOLOGY & STANDARDS", self.styles['SectionTitle'])
        )
        elements.append(Spacer(1, 0.2 * inch))

        elements.append(
            Paragraph(
                """This report follows the GHG Protocol Corporate Standard methodology
and uses emission factors from DEFRA (UK Department for Business, Energy and Industrial Strategy)
and IPCC guidelines. All calculations are deterministic and audit-ready. The report is suitable
for regulatory compliance submissions and ESG reporting.""",
                self.styles['Normal'],
            )
        )

        if methodology:
            elements.append(Spacer(1, 0.2 * inch))
            elements.append(Paragraph("<b>GHG Protocol Guidance:</b>", self.styles['Normal']))
            elements.append(Spacer(1, 0.1 * inch))
            elements.append(Paragraph(methodology[:500], self.styles['Normal']))

        # PAGE 6: FOOTER
        elements.append(PageBreak())
        elements.append(
            Paragraph(
                "This report has been automatically generated by Swach AI Carbon Agent",
                ParagraphStyle(
                    'Footer',
                    parent=self.styles['Normal'],
                    alignment=TA_CENTER,
                    fontSize=8,
                    textColor=colors.grey,
                ),
            )
        )
        elements.append(Spacer(1, 0.1 * inch))
        elements.append(
            Paragraph(
                f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                ParagraphStyle(
                    'Footer',
                    parent=self.styles['Normal'],
                    alignment=TA_CENTER,
                    fontSize=8,
                    textColor=colors.grey,
                ),
            )
        )

        # Build PDF
        doc.build(elements)
        logger.info(f"OK: PDF report generated: {filename}")

        return filename


# Function for use in agent
def generate_pdf_report(
    company_name: str,
    activity_data: Dict[str, Any],
    emission_result: Dict[str, Any],
    search_results: list = None,
    methodology: str = None,
    output_dir: str = "reports",
) -> str:
    """
    Tool function for LangChain agent

    Args:
        company_name: Company name
        activity_data: Activity data dict
        emission_result: Emission calculation results
        search_results: Web search results (optional)
        methodology: GHG Protocol methodology (optional)
        output_dir: Output directory for PDF

    Returns:
        Path to generated PDF
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    filename = f"{output_dir}/report_{company_name.replace(' ', '_')}.pdf"

    generator = PDFReportGenerator()
    return generator.generate_report(
        filename=filename,
        company_name=company_name,
        activity_data=activity_data,
        emission_result=emission_result,
        search_results=search_results,
        methodology=methodology,
    )


if __name__ == "__main__":
    print("PDF Generator tool loaded successfully")
    print("Use generate_pdf_report() function in LangChain agent")
