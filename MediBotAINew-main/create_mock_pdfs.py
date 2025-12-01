"""
Create mock PDF medical documents for testing
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

def create_ecg_report():
    doc = SimpleDocTemplate("../mock_documents/ECG_Report_Sample.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30)
    story.append(Paragraph("ELECTROCARDIOGRAM REPORT", title_style))
    
    # Patient Info
    patient_data = [
        ['Patient:', 'John Smith', 'DOB:', '01/15/1980'],
        ['MRN:', '12345678', 'Date:', '2024-01-20'],
        ['Time:', '14:30', 'Physician:', 'Dr. Sarah Johnson']
    ]
    
    patient_table = Table(patient_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Clinical Indication
    story.append(Paragraph("<b>CLINICAL INDICATION:</b>", styles['Heading2']))
    story.append(Paragraph("Chest pain, rule out acute coronary syndrome", styles['Normal']))
    story.append(Spacer(1, 12))
    
    # ECG Findings
    story.append(Paragraph("<b>ECG FINDINGS:</b>", styles['Heading2']))
    findings = [
        "• Heart Rate: 85 bpm",
        "• Rhythm: Normal Sinus Rhythm", 
        "• PR Interval: 160 ms (Normal: 120-200 ms)",
        "• QRS Duration: 90 ms (Normal: <120 ms)",
        "• QT Interval: 400 ms",
        "• QTc: 420 ms (Normal: <450 ms)"
    ]
    
    for finding in findings:
        story.append(Paragraph(finding, styles['Normal']))
    
    story.append(Spacer(1, 12))
    
    # Interpretation
    story.append(Paragraph("<b>INTERPRETATION:</b>", styles['Heading2']))
    story.append(Paragraph("Normal 12-lead electrocardiogram. No acute ST changes. No evidence of arrhythmia.", styles['Normal']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>CLINICAL CORRELATION:</b>", styles['Heading2']))
    story.append(Paragraph("ECG does not show evidence of acute myocardial infarction or significant arrhythmia. Clinical correlation recommended.", styles['Normal']))
    
    doc.build(story)

def create_blood_test_report():
    doc = SimpleDocTemplate("../mock_documents/Blood_Test_Report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30)
    story.append(Paragraph("COMPLETE BLOOD COUNT REPORT", title_style))
    
    # Patient Info
    patient_data = [
        ['Patient:', 'Maria Garcia', 'DOB:', '03/22/1975'],
        ['MRN:', '87654321', 'Date:', '2024-01-20'],
        ['Lab ID:', 'LAB2024-001', 'Time:', '08:00 AM']
    ]
    
    patient_table = Table(patient_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Lab Results
    story.append(Paragraph("<b>COMPLETE BLOOD COUNT:</b>", styles['Heading2']))
    
    lab_data = [
        ['Test', 'Result', 'Reference Range', 'Flag'],
        ['White Blood Cell Count', '12,500 /μL', '4,000-11,000', 'HIGH'],
        ['Red Blood Cell Count', '3.8 million/μL', '4.2-5.4', 'LOW'],
        ['Hemoglobin', '8.5 g/dL', '12.0-16.0', 'LOW'],
        ['Hematocrit', '25.2%', '36-46%', 'LOW'],
        ['Platelet Count', '180,000 /μL', '150,000-400,000', 'NORMAL']
    ]
    
    lab_table = Table(lab_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    lab_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(lab_table)
    story.append(Spacer(1, 20))
    
    # Critical Values
    story.append(Paragraph("<b>⚠️ CRITICAL VALUES:</b>", styles['Heading2']))
    story.append(Paragraph("• Severe anemia (Hgb 8.5 g/dL)", styles['Normal']))
    story.append(Paragraph("• Leukocytosis (WBC 12,500)", styles['Normal']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>INTERPRETATION:</b>", styles['Heading2']))
    story.append(Paragraph("Severe microcytic anemia with leukocytosis. Findings suggest iron deficiency anemia with possible concurrent infection or inflammation.", styles['Normal']))
    
    doc.build(story)

def create_xray_report():
    doc = SimpleDocTemplate("../mock_documents/Chest_XRay_Report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30)
    story.append(Paragraph("CHEST X-RAY REPORT", title_style))
    
    # Patient Info
    patient_data = [
        ['Patient:', 'Robert Johnson', 'DOB:', '07/10/1965'],
        ['MRN:', '11223344', 'Date:', '2024-01-20'],
        ['Study ID:', 'XR-2024-0120', 'Indication:', 'SOB, cough, fever']
    ]
    
    patient_table = Table(patient_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>TECHNIQUE:</b> PA and lateral chest radiographs", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>FINDINGS:</b>", styles['Heading2']))
    findings = [
        "<b>LUNGS:</b> Right lower lobe consolidation with air bronchograms. Left lung clear.",
        "<b>HEART:</b> Normal cardiac silhouette",
        "<b>MEDIASTINUM:</b> Normal mediastinal width",
        "<b>BONES:</b> No acute osseous abnormalities"
    ]
    
    for finding in findings:
        story.append(Paragraph(finding, styles['Normal']))
        story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>IMPRESSION:</b>", styles['Heading2']))
    story.append(Paragraph("Right lower lobe pneumonia", styles['Normal']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>🚨 CRITICAL FINDING:</b>", styles['Heading2']))
    story.append(Paragraph("Acute pneumonia - communicated to ordering physician", styles['Normal']))
    
    doc.build(story)

def create_mri_report():
    doc = SimpleDocTemplate("../mock_documents/MRI_Brain_Report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30)
    story.append(Paragraph("BRAIN MRI REPORT", title_style))
    
    # Patient Info
    patient_data = [
        ['Patient:', 'Jennifer Davis', 'DOB:', '11/05/1988'],
        ['MRN:', '55667788', 'Date:', '2024-01-20'],
        ['Study ID:', 'MR-2024-0120', 'Contrast:', 'Gadolinium IV']
    ]
    
    patient_table = Table(patient_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>CLINICAL INDICATION:</b>", styles['Heading2']))
    story.append(Paragraph("Headaches, visual disturbances, rule out intracranial pathology", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>TECHNIQUE:</b>", styles['Heading2']))
    story.append(Paragraph("Multiplanar, multisequence MRI including T1, T2, FLAIR, DWI sequences", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>FINDINGS:</b>", styles['Heading2']))
    findings = [
        "• Normal gray and white matter signal intensity",
        "• No evidence of acute infarction on DWI",
        "• No hemorrhage identified",
        "• Normal ventricular system",
        "• No mass lesions"
    ]
    
    for finding in findings:
        story.append(Paragraph(finding, styles['Normal']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>IMPRESSION:</b>", styles['Heading2']))
    story.append(Paragraph("Normal brain MRI examination", styles['Normal']))
    
    doc.build(story)

def create_ct_report():
    doc = SimpleDocTemplate("../mock_documents/CT_Abdomen_Report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30)
    story.append(Paragraph("CT ABDOMEN AND PELVIS REPORT", title_style))
    
    # Patient Info
    patient_data = [
        ['Patient:', 'Thomas Wilson', 'DOB:', '09/18/1972'],
        ['MRN:', '99887766', 'Date:', '2024-01-20'],
        ['Study ID:', 'CT-2024-0120', 'Contrast:', 'IV Omnipaque']
    ]
    
    patient_table = Table(patient_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>CLINICAL INDICATION:</b>", styles['Heading2']))
    story.append(Paragraph("Abdominal pain, nausea, vomiting, rule out appendicitis", styles['Normal']))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("<b>FINDINGS:</b>", styles['Heading2']))
    findings = [
        "<b>GALLBLADDER:</b> Distended with multiple gallstones, wall thickening (5 mm), pericholecystic fluid",
        "<b>LIVER:</b> Normal size and attenuation",
        "<b>PANCREAS:</b> Normal enhancement",
        "<b>KIDNEYS:</b> Normal bilateral enhancement",
        "<b>BOWEL:</b> Normal caliber, appendix not visualized"
    ]
    
    for finding in findings:
        story.append(Paragraph(finding, styles['Normal']))
        story.append(Spacer(1, 6))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>IMPRESSION:</b>", styles['Heading2']))
    story.append(Paragraph("1. Acute cholecystitis with gallstones", styles['Normal']))
    story.append(Paragraph("2. No evidence of appendicitis", styles['Normal']))
    
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>🚨 CRITICAL FINDING:</b>", styles['Heading2']))
    story.append(Paragraph("Acute cholecystitis - surgical consultation recommended", styles['Normal']))
    
    doc.build(story)

def create_echo_report():
    doc = SimpleDocTemplate("../mock_documents/Echo_Ultrasound_Report.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, spaceAfter=30)
    story.append(Paragraph("ECHOCARDIOGRAM REPORT", title_style))
    
    # Patient Info
    patient_data = [
        ['Patient:', 'Patricia Brown', 'DOB:', '12/30/1955'],
        ['MRN:', '44556677', 'Date:', '2024-01-20'],
        ['Study ID:', 'ECHO-2024-0120', 'Type:', 'Transthoracic']
    ]
    
    patient_table = Table(patient_data, colWidths=[1*inch, 2*inch, 1*inch, 2*inch])
    patient_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    
    story.append(patient_table)
    story.append(Spacer(1, 20))
    
    # Measurements Table
    story.append(Paragraph("<b>MEASUREMENTS:</b>", styles['Heading2']))
    
    measurements_data = [
        ['Parameter', 'Value', 'Normal Range'],
        ['LV End Diastolic Dimension', '5.2 cm', '3.9-5.3 cm'],
        ['LV End Systolic Dimension', '3.1 cm', '2.3-3.5 cm'],
        ['Ejection Fraction', '60%', '≥55%'],
        ['Left Atrial Dimension', '3.8 cm', '1.9-4.0 cm']
    ]
    
    measurements_table = Table(measurements_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    measurements_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(measurements_table)
    story.append(Spacer(1, 20))
    
    story.append(Paragraph("<b>IMPRESSION:</b>", styles['Heading2']))
    impressions = [
        "1. Normal left ventricular systolic function (EF 60%)",
        "2. Normal cardiac chamber sizes", 
        "3. Normal valve function with trace regurgitation",
        "4. No pericardial effusion"
    ]
    
    for impression in impressions:
        story.append(Paragraph(impression, styles['Normal']))
    
    doc.build(story)

if __name__ == "__main__":
    print("Creating mock PDF medical reports...")
    create_ecg_report()
    print("ECG Report created")
    
    create_blood_test_report()
    print("Blood Test Report created")
    
    create_xray_report()
    print("Chest X-Ray Report created")
    
    create_mri_report()
    print("MRI Brain Report created")
    
    create_ct_report()
    print("CT Abdomen Report created")
    
    create_echo_report()
    print("Echo Ultrasound Report created")
    
    print("All PDF reports created successfully!")