from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY
import json
import configparser
import os

PAGE_WIDTH, PAGE_HEIGHT = A4
FULL_COLUMN_WIDTH = (PAGE_WIDTH - 1 * inch)
GARAMOND_REGULAR_FONT_PATH = './res/fonts/EBGaramond-Regular.ttf'
GARAMOND_REGULAR = 'Garamond_Regular'

GARAMOND_BOLD_FONT_PATH = './res/fonts/EBGaramond-Bold.ttf'
GARAMOND_BOLD = 'Garamond_Bold'

GARAMOND_SEMIBOLD_FONT_PATH = './res/fonts/EBGaramond-SemiBold.ttf'
GARAMOND_SEMIBOLD = 'Garamond_Semibold'

pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_REGULAR, GARAMOND_REGULAR_FONT_PATH))
pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_BOLD, GARAMOND_BOLD_FONT_PATH))
pdfmetrics.registerFont(ttfonts.TTFont(GARAMOND_SEMIBOLD, GARAMOND_SEMIBOLD_FONT_PATH))

JOB_DETAILS_PARAGRAPH_STYLE = ParagraphStyle('job_details_paragraph', leftIndent=12, fontName = GARAMOND_REGULAR, fontSize = 12, leading = 14, alignment = TA_JUSTIFY)
NAME_PARAGRAPH_STYLE = ParagraphStyle('name_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=16)
CONTACT_PARAGRAPH_STYLE = ParagraphStyle('contact_paragraph', fontName = GARAMOND_REGULAR, fontSize=12)
SECTION_PARAGRAPH_STYLE = ParagraphStyle('section_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=13, textTransform = 'uppercase')
COMPANY_HEADING_PARAGRAPH_STYLE = ParagraphStyle('company_heading_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=13)
COMPANY_TITLE_PARAGRAPH_STYLE = ParagraphStyle('company_title_paragraph', fontName = GARAMOND_REGULAR, fontSize=12)
COMPANY_DURATION_PARAGRAPH_STYLE = ParagraphStyle('company_duration_paragraph', fontName = GARAMOND_SEMIBOLD, fontSize=13, alignment = TA_RIGHT)
COMPANY_LOCATION_PARAGRAPH_STYLE = ParagraphStyle('company_location_paragraph', fontName = GARAMOND_REGULAR, fontSize=12, alignment = TA_RIGHT)

def appendSectionTableStyle(table_styles, running_row_index):
    table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 5))
    table_styles.append(('LINEBELOW', (0, running_row_index), (-1, running_row_index), 1, colors.black))

def draw_rounded_rectangle(canvas, x, y, width, height, corner_radius, fill_color=None, stroke_color=None):
    canvas.saveState()
    if fill_color:
        canvas.setFillColor(fill_color)
    if stroke_color:
        canvas.setStrokeColor(stroke_color)
    canvas.roundRect(x, y, width, height, corner_radius, fill=True, stroke=True)
    canvas.restoreState()

def add_image_to_canvas(canvas, image_path, width, height, corner_radius=10):
    canvas.drawImage(image_path, PAGE_WIDTH - width - 36, PAGE_HEIGHT - height - 3.5, width, height, corner_radius)

def generate_resume(file_path, json_file_path, author, email, address, phone, debug):
    doc = SimpleDocTemplate(file_path, pagesize=A4, showBoundary=0, leftMargin = 0.5 * inch, rightMargin= 0.5 * inch, topMargin = 0.2 * inch, bottomMargin = 0.1 * inch, title = f"Resume of {author}", author = author)
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    # data for the table
    table_data = []
    table_styles = []
    running_row_index = 0

    # Append some basic styles to the table styles array only in debug mode
    if (debug == 'true'):
        table_styles.append(('GRID', (0, 0), (-1, -1), 0, colors.black))
    
    table_styles.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
    table_styles.append(('ALIGN', (1, 0), (1, -1), 'RIGHT'))
    table_styles.append(('LEFTPADDING', (0, 0), (-1, -1), 0))
    table_styles.append(('RIGHTPADDING', (0, 0), (-1, -1), 0))
    # Add name and basic contact
    
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 6))
    table_data.append([
        Paragraph(author, NAME_PARAGRAPH_STYLE)
    ])
    running_row_index += 1

    table_data.append([
        Paragraph(f"{email} | {phone} | {address}", CONTACT_PARAGRAPH_STYLE),
    ])
    table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 1))
    running_row_index += 1

    # Append skills heading
    table_data.append(
        [Paragraph("Skills", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append skills
    for skill in data['skills']:
        table_data.append([
            Paragraph(skill, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    # Add experience heading
    table_data.append(
        [Paragraph("Experience", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append experience
    for job_experience in data['experience']:
        table_data.append([
            Paragraph(job_experience['company'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(job_experience['duration'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(job_experience['title'], COMPANY_TITLE_PARAGRAPH_STYLE),
            Paragraph(job_experience['location'], COMPANY_LOCATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1

        for line in job_experience['description']:
            table_data.append([
                Paragraph(line, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
            table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
            table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
            running_row_index += 1
    
    # Append education heading
    table_data.append(
        [Paragraph("Education", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1
    
    # Append education
    for education in data['education']:
        table_data.append([
            Paragraph(education['university'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(education['year'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(education['degree'], COMPANY_TITLE_PARAGRAPH_STYLE),
            Paragraph(education['location'], COMPANY_LOCATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1
    
    # Append certifications heading
    table_data.append(
        [Paragraph("Certifications", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # If you want to add the projects, uncomment the lines below, and add your projects in data.json file
    # for project in data['projects']:
    #     table_data.append([
    #         Paragraph(f"<font face='Garamond_Semibold'>{project['title']}: </font>{project['description']} {project['link']}", bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE),
    #     ])
    #     table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
    #     table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
    #     table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
    #     running_row_index += 1

    for certification in data['certifications']:
        table_data.append([
            Paragraph(f"<font face='Garamond_Semibold'>{certification['title']}: </font>{certification['link']}", bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    # Add achievements heading
    table_data.append(
        [Paragraph("Achievements", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append achievements
    for achievement in data['achievements']:
        table_data.append([
            Paragraph(achievement['title'], COMPANY_HEADING_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(achievement['awarding_institute'], COMPANY_TITLE_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1

        # for line in achievement['description']:
        table_data.append([
            Paragraph(achievement['description'], style=JOB_DETAILS_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    # Append interpersonal skills heading
    table_data.append(
        [Paragraph("Interpersonal Skills", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append interpersonal skills
    for interpersonal_skill in data['interpersonal_skills']:
        table_data.append([
            Paragraph(interpersonal_skill, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    # Append language heading
    table_data.append(
        [Paragraph("Languages", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append languages
    for language in data['languages']:
        table_data.append([
            Paragraph(language, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    # Add volunteer work heading
    table_data.append(
        [Paragraph("Volunteering", SECTION_PARAGRAPH_STYLE)]
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append volunteer work
    for volunteer_work in data['volunteer_works']:
        table_data.append([
            Paragraph(volunteer_work['company'], COMPANY_HEADING_PARAGRAPH_STYLE),
            Paragraph(volunteer_work['duration'], COMPANY_DURATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 5))
        running_row_index += 1

        table_data.append([
            Paragraph(volunteer_work['title'], COMPANY_TITLE_PARAGRAPH_STYLE),
            Paragraph(volunteer_work['location'], COMPANY_LOCATION_PARAGRAPH_STYLE),
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        running_row_index += 1

        for line in volunteer_work['description']:
            table_data.append([
                Paragraph(line, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
            table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
            table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
            running_row_index += 1

    # Append passions heading
    table_data.append(
        [Paragraph("Hobbies", SECTION_PARAGRAPH_STYLE)] # Hobbies or Passions
    )
    appendSectionTableStyle(table_styles, running_row_index)
    running_row_index += 1

    # Append passions
    for passion in data['passions']:
        table_data.append([
            Paragraph(passion, bulletText='•', style=JOB_DETAILS_PARAGRAPH_STYLE)
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

    table_style = TableStyle(table_styles)

    # Create the table and apply the style
    table = Table(table_data, colWidths=[FULL_COLUMN_WIDTH * 0.7, FULL_COLUMN_WIDTH * 0.3], spaceBefore=0, spaceAfter=0)
    table.setStyle(table_style)

    # Add the table to the elements list
    elements = [table]

    def on_first_page(canvas, doc):
        add_image_to_canvas(canvas, 'my_picture.jpg', width=1*inch, height=1*inch)

    doc.build(elements, onFirstPage=on_first_page)

    # Build the PDF document
    # doc.build(elements)

if __name__ == "__main__":
    config = None
    debug = 'false'
    author = 'Syed Muhammad Murtaza Ali Zaidi'
    email = "<a href='mailto:{email}' color=\"blue\">murtazazaidi1@outlook.com</a>"
    address = '<a href=\"https://murtazaverse.github.io/tech/\" color=\"blue\">(Portfolio website)</a>'
    phone = "<a href='tel:{phone}' color=\"blue\">+49 1556 6247907</a>"
    
    if (os.path.isfile('./config.ini')):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        # Check if debug option is present
        if (config.has_option('global', 'debug')):
            debug = config.get('global', 'debug')
        
        # Check if author is present
        if (config.has_option('global', 'author')):
            author = config.get('global', 'author')

        # Check if email address is present
        if (config.has_option('global', 'email')):
            email = config.get('global', 'email')

        # Check if address is present
        if (config.has_option('global', 'address')):
            address = config.get('global', 'address')

        # Check if author is present
        if (config.has_option('global', 'phone')):
            phone = config.get('global', 'phone')

    OUTPUT_PDF_PATH = f"./{author.lower().replace(' ', '_')}_resume.pdf"
    JSON_PATH = "./data.json"

    generate_resume(OUTPUT_PDF_PATH, JSON_PATH, author, email, address, phone, debug)