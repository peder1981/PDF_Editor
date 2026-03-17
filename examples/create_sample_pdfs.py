#!/usr/bin/env python3
"""
Create Sample PDFs for Testing and Demonstration
"""

import fitz
import os
from pathlib import Path


def create_sample_contract():
    """Create a sample contract PDF for testing"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Add content
    content = [
        ("SERVICE AGREEMENT", 16, (72, 80)),
        ("", 12, (72, 100)),  # Empty line
        ("This Service Agreement ('Agreement') is entered into on January 1, 2023,", 12, (72, 120)),
        ("between ACME Corporation ('Company') and John Doe ('Contractor').", 12, (72, 140)),
        ("", 12, (72, 160)),  # Empty line
        ("1. SERVICES", 14, (72, 180)),
        ("Contractor agrees to provide software development services to Company.", 12, (72, 200)),
        ("The services shall be performed remotely from Contractor's office.", 12, (72, 220)),
        ("", 12, (72, 240)),  # Empty line
        ("2. COMPENSATION", 14, (72, 260)),
        ("Company agrees to pay Contractor $5,000 per month for services rendered.", 12, (72, 280)),
        ("Payment shall be made monthly on the 15th of each month.", 12, (72, 300)),
        ("", 12, (72, 320)),  # Empty line
        ("3. TERM", 14, (72, 340)),
        ("This Agreement shall commence on January 1, 2023 and continue until", 12, (72, 360)),
        ("December 31, 2023, unless terminated earlier in accordance with this Agreement.", 12, (72, 380)),
        ("", 12, (72, 400)),  # Empty line
        ("IN WITNESS WHEREOF, the parties have executed this Agreement.", 12, (72, 420)),
        ("", 12, (72, 440)),  # Empty line
        ("Company: ACME Corporation", 12, (72, 480)),
        ("Contractor: John Doe", 12, (72, 500)),
        ("Date: January 1, 2023", 12, (72, 520)),
    ]
    
    for text, size, pos in content:
        if text:  # Skip empty lines
            page.insert_text(pos, text, fontsize=size, color=(0, 0, 0))
    
    return doc


def create_sample_invoice():
    """Create a sample invoice PDF for testing"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Add content
    content = [
        ("INVOICE", 18, (72, 80)),
        ("", 12, (72, 100)),  # Empty line
        ("Invoice #: INV-2023-001", 12, (72, 120)),
        ("Date: March 15, 2023", 12, (72, 140)),
        ("Due Date: April 15, 2023", 12, (72, 160)),
        ("", 12, (72, 180)),  # Empty line
        ("Bill To:", 14, (72, 200)),
        ("ABC Company Inc.", 12, (72, 220)),
        ("123 Business Street", 12, (72, 240)),
        ("New York, NY 10001", 12, (72, 260)),
        ("", 12, (72, 280)),  # Empty line
        ("From:", 14, (72, 300)),
        ("XYZ Services LLC", 12, (72, 320)),
        ("456 Service Avenue", 12, (72, 340)),
        ("Los Angeles, CA 90210", 12, (72, 360)),
        ("", 12, (72, 380)),  # Empty line
        ("Description of Services:", 14, (72, 400)),
        ("Consulting Services - March 2023", 12, (72, 420)),
        ("Web Development Project Phase 1", 12, (72, 440)),
        ("Database Design and Implementation", 12, (72, 460)),
        ("", 12, (72, 480)),  # Empty line
        ("Amount: $7,500.00", 14, (72, 500)),
        ("Tax: $600.00", 12, (72, 520)),
        ("Total Amount Due: $8,100.00", 16, (72, 550)),
        ("", 12, (72, 570)),  # Empty line
        ("Payment Terms: Net 30 days", 12, (72, 590)),
        ("Thank you for your business!", 12, (72, 620)),
    ]
    
    for text, size, pos in content:
        if text:  # Skip empty lines
            page.insert_text(pos, text, fontsize=size, color=(0, 0, 0))
    
    return doc


def create_sample_report():
    """Create a sample report PDF for testing"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Add content
    content = [
        ("QUARTERLY BUSINESS REPORT", 18, (72, 80)),
        ("Q1 2023 Performance Analysis", 14, (72, 110)),
        ("", 12, (72, 130)),  # Empty line
        ("Executive Summary", 16, (72, 150)),
        ("", 12, (72, 170)),  # Empty line
        ("This report summarizes the performance of TechCorp Solutions during", 12, (72, 190)),
        ("the first quarter of 2023. Overall, the company has shown strong growth", 12, (72, 210)),
        ("in both revenue and customer acquisition.", 12, (72, 230)),
        ("", 12, (72, 250)),  # Empty line
        ("Key Metrics:", 14, (72, 270)),
        ("• Revenue: $2.5M (up 15% from Q4 2022)", 12, (72, 290)),
        ("• New Customers: 1,250 (up 22% from Q4 2022)", 12, (72, 310)),
        ("• Customer Retention Rate: 94%", 12, (72, 330)),
        ("• Employee Count: 85 (up from 78)", 12, (72, 350)),
        ("", 12, (72, 370)),  # Empty line
        ("Challenges and Opportunities", 14, (72, 390)),
        ("", 12, (72, 410)),  # Empty line
        ("While Q1 2023 showed strong performance, the company faces several", 12, (72, 430)),
        ("challenges including increased competition and supply chain constraints.", 12, (72, 450)),
        ("However, opportunities exist in emerging markets and new product lines.", 12, (72, 470)),
        ("", 12, (72, 490)),  # Empty line
        ("Outlook for Q2 2023", 14, (72, 510)),
        ("", 12, (72, 530)),  # Empty line
        ("Management projects continued growth with expected revenue of $2.8M", 12, (72, 550)),
        ("and plans to hire 10 additional employees to support expansion.", 12, (72, 570)),
        ("", 12, (72, 590)),  # Empty line
        ("Prepared by: Finance Department", 12, (72, 610)),
        ("Date: April 10, 2023", 12, (72, 630)),
    ]
    
    for text, size, pos in content:
        if text:  # Skip empty lines
            page.insert_text(pos, text, fontsize=size, color=(0, 0, 0))
    
    # Add second page
    page2 = doc.new_page()
    
    content2 = [
        ("DETAILED FINANCIAL ANALYSIS", 16, (72, 80)),
        ("", 12, (72, 100)),  # Empty line
        ("Revenue Breakdown by Product Line:", 14, (72, 120)),
        ("", 12, (72, 140)),  # Empty line
        ("Product A: $1,200,000 (48% of total)", 12, (72, 160)),
        ("Product B: $800,000 (32% of total)", 12, (72, 180)),
        ("Product C: $350,000 (14% of total)", 12, (72, 200)),
        ("Services: $150,000 (6% of total)", 12, (72, 220)),
        ("", 12, (72, 240)),  # Empty line
        ("Cost Analysis:", 14, (72, 260)),
        ("", 12, (72, 280)),  # Empty line
        ("Cost of Goods Sold: $1,500,000", 12, (72, 300)),
        ("Operating Expenses: $750,000", 12, (72, 320)),
        ("Marketing and Sales: $150,000", 12, (72, 340)),
        ("Research and Development: $100,000", 12, (72, 360)),
        ("", 12, (72, 380)),  # Empty line
        ("Net Income: $250,000", 14, (72, 400)),
        ("", 12, (72, 420)),  # Empty line
        ("This represents a 25% increase over Q4 2022 net income of $200,000.", 12, (72, 440)),
        ("", 12, (72, 460)),  # Empty line
        ("Recommendations:", 14, (72, 480)),
        ("", 12, (72, 500)),  # Empty line
        ("1. Continue investment in Product A expansion", 12, (72, 520)),
        ("2. Evaluate pricing strategy for Product C", 12, (72, 540)),
        ("3. Increase marketing budget by 15% for Q2", 12, (72, 560)),
        ("4. Consider strategic partnerships for market expansion", 12, (72, 580)),
        ("", 12, (72, 600)),  # Empty line
        ("End of Report", 12, (72, 620)),
    ]
    
    for text, size, pos in content2:
        if text:  # Skip empty lines
            page2.insert_text(pos, text, fontsize=size, color=(0, 0, 0))
    
    return doc


def create_samples_directory():
    """Create samples directory and generate sample PDFs"""
    samples_dir = Path("samples")
    samples_dir.mkdir(exist_ok=True)
    
    # Create sample PDFs
    samples = {
        "sample_contract.pdf": create_sample_contract,
        "sample_invoice.pdf": create_sample_invoice,
        "sample_report.pdf": create_sample_report,
    }
    
    created_files = []
    
    for filename, creator_func in samples.items():
        file_path = samples_dir / filename
        try:
            doc = creator_func()
            doc.save(str(file_path))
            doc.close()
            created_files.append(str(file_path))
            print(f"✅ Created: {file_path}")
        except Exception as e:
            print(f"❌ Failed to create {filename}: {e}")
    
    return created_files


def create_sample_configs():
    """Create sample configuration files"""
    samples_dir = Path("samples")
    samples_dir.mkdir(exist_ok=True)
    
    # Sample batch replacement configuration
    batch_config = {
        "jobs": [
            {
                "input": "samples/sample_contract.pdf",
                "output": "samples/contract_updated.pdf",
                "method": "exact",
                "operations": [
                    {
                        "search": "ACME Corporation",
                        "replace": "TechStart Inc.",
                        "case_sensitive": True
                    },
                    {
                        "search": "John Doe",
                        "replace": "Jane Smith",
                        "case_sensitive": True
                    },
                    {
                        "search": "2023",
                        "replace": "2024",
                        "case_sensitive": False
                    }
                ]
            },
            {
                "input": "samples/sample_invoice.pdf",
                "output": "samples/invoice_updated.pdf",
                "method": "structure",
                "operations": [
                    {
                        "search": "ABC Company Inc.",
                        "replace": "New Client Corp.",
                        "case_sensitive": True
                    },
                    {
                        "search": "$8,100.00",
                        "replace": "$9,500.00",
                        "case_sensitive": False
                    }
                ]
            }
        ]
    }
    
    config_path = samples_dir / "batch_replacements.json"
    import json
    with open(config_path, 'w') as f:
        json.dump(batch_config, f, indent=2)
    
    print(f"✅ Created batch configuration: {config_path}")
    
    # Sample simple replacements
    simple_replacements = [
        {
            "search": "Q1 2023",
            "replace": "Q2 2023",
            "case_sensitive": False
        },
        {
            "search": "TechCorp Solutions",
            "replace": "InnovateTech Ltd.",
            "case_sensitive": True
        },
        {
            "search": "$2.5M",
            "replace": "$3.2M",
            "case_sensitive": False
        }
    ]
    
    simple_config_path = samples_dir / "simple_replacements.json"
    with open(simple_config_path, 'w') as f:
        json.dump(simple_replacements, f, indent=2)
    
    print(f"✅ Created simple replacements: {simple_config_path}")
    
    return [str(config_path), str(simple_config_path)]


def main():
    """Create all sample files"""
    print("🚀 Creating sample PDFs and configurations...")
    print()
    
    # Create sample PDFs
    created_pdfs = create_samples_directory()
    print(f"\n📄 Created {len(created_pdfs)} sample PDF files")
    
    # Create sample configurations
    created_configs = create_sample_configs()
    print(f"\n⚙️  Created {len(created_configs)} configuration files")
    
    print("\n🎉 Sample files created successfully!")
    print("\nUsage examples:")
    print("  # Search in sample contract:")
    print("  python cli.py search samples/sample_contract.pdf 'ACME Corporation'")
    print()
    print("  # Replace text in sample invoice:")
    print("  python cli.py replace samples/sample_invoice.pdf 'ABC Company Inc.' 'New Client Corp.'")
    print()
    print("  # Batch processing:")
    print("  python cli.py batch samples/sample_report.pdf samples/simple_replacements.json")
    print()
    print("  # Launch GUI:")
    print("  python cli.py gui")
    print()
    print("  # Launch TUI:")
    print("  python cli.py tui")


if __name__ == "__main__":
    main()
