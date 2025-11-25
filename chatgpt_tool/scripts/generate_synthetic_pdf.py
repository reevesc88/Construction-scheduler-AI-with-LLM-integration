from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_synthetic_spec(filename="synthetic_project_spec.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.5*inch, height - 0.5*inch, "Construction Project Specification")
    
    # Project Info
    c.setFont("Helvetica", 11)
    y = height - 1.0*inch
    
    specs = [
        "PROJECT ID: WH-2025-001",
        "LOCATION: Seattle, Washington",
        "PROJECT TYPE: Warehouse Extension",
        "",
        "SCOPE OF WORK:",
        "1. Site preparation and clearing",
        "2. Pour 200 cubic yards of concrete foundation",
        "3. Install 50 tons of structural steel",
        "4. Install 4000 sf of metal siding",
        "5. Install HVAC systems",
        "6. Paint 5000 sf of interior finishes",
        "",
        "CONSTRAINTS:",
        "- Concrete requires 7 days curing time",
        "- Steel delivery takes 3 weeks from order",
        "- Work must not proceed during rain",
        "",
        "NOTES:",
        "Priority: Complete foundation before framing begins"
    ]
    
    for spec in specs:
        c.drawString(0.5*inch, y, spec)
        y -= 15
    
    c.save()
    print(f"✓ Generated {filename}")

if __name__ == "__main__":
    create_synthetic_spec()