from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageBreak, FrameBreak, Frame

width, height = letter
pageinfo = "Dr. Hendricksen evaluation form"


class UncheckedBox(Flowable):
    def __init__(self, width=10, height=10):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        self.canv.rect(0, 2, self.width, self.height, fill=0)


class CheckedBox(Flowable):
    def __init__(self, width=10, height=10):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        self.canv.rect(0, 2, self.width, self.height, fill=0)
        self.canv.drawCentredString(0.5 * self.width, 0.5 * self.height, '✓')


class NormFormDocTemplate(BaseDocTemplate):
    def build(self, flowables):
        self._calc()
        print(self.height)  # 821.89
        print(self.width)  # 565.28
        frame_top = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='frame_top')
        frame_left = Frame(self.leftMargin, -125, 115, self.height, id='frame_left')
        frame_right = Frame(self.leftMargin + 110, -123, 450, self.height, id='frame_right')
        frame_bottom = Frame(self.leftMargin, self.bottomMargin, 7 * inch, 3 * inch, id='frame_bottom')
        self.addPageTemplates([PageTemplate(id='First', frames=[frame_top, frame_left, frame_right, frame_bottom],
                                            pagesize=self.pagesize)])
        BaseDocTemplate.build(self, flowables)


def build_form():
    doc = NormFormDocTemplate("templates/forms/flowable_test.pdf", rightMargin=15, leftMargin=15,
                              topMargin=10, bottomMargin=10)
    # doc = SimpleDocTemplate("templates/forms/flowable_test.pdf", rightMargin=15, leftMargin=15,
    #                         topMargin=10, bottomMargin=10)
    story = []
    title_text = "Psychologist Consultation / Follow-Up"
    p = Paragraph(title_text, style=ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=12,
                                                   alignment=TA_CENTER))
    story.append(p)

    story.append(Spacer(0, 0.1*inch))

    data = [['Patient Name', 'Facility', 'Date'],
            ['Lastname, Firstname', 'TestFacility', '01/01/1950']]
    grid = [('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')]
    t = Table(data, colWidths=[3.95*inch, 2.95*inch, 0.95*inch], hAlign=TA_LEFT, style=TableStyle(grid))
    story.append(t)

    story.append(Spacer(0, 0.1 * inch))

    p = Paragraph(f'Subjective (Chief Complaints, Presenting Problems, and History):',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)
    p = Paragraph(f'Insert eval here',
                  style=ParagraphStyle(name='Normal', leftIndent=10, fontName='Helvetica',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    story.append(Spacer(0, 0.3 * inch))

    p = Paragraph(f'Mental Status Examination',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica',
                                       fontSize=12, alignment=TA_CENTER))
    story.append(p)
    p = Paragraph(f'Objective (Staff / Other Sources Reported)',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    story.append(Spacer(0, 0.1 * inch))

    story.append(FrameBreak)

    p = Paragraph('Aggressive Behavior<br /><br />'
                  'General Appearance<br /><br />'
                  'Treatment & Compliance<br /><br />'
                  'Inappropriate Behavior<br /><br />'
                  'Attitude<br /><br />'
                  'Speech<br /><br />'
                  'Verbal Abilities<br /><br />'
                  'Communication<br /><br />'
                  'Perceptual Disturbances<br /><br />'
                  'Level of Consciousness<br /><br />'
                  'Thought Process<br /><br />'
                  'Thought Content<br /><br />'
                  'Mood<br /><br />'
                  'Affect<br /><br />'
                  'Harmfulness<br /><br />'
                  'Attention & Concentration<br /><br />'
                  'Orientation<br /><br />'
                  'Insight & Judgment<br /><br />'
                  'Sleep Disturbance<br /><br />'
                  'Appetite change',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=8, alignment=TA_RIGHT))
    story.append(p)

    story.append(FrameBreak)

    grid = [
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
        ('ALIGN', (1, 0), (1, 0), 'LEFT'),
        ('RIGHTPADDING', (0, 0), (0, 0), 2),
        ('LEFTPADDING', (1, 0), (1, 0), 2),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('ALIGN', (3, 0), (3, 0), 'LEFT'),
        ('RIGHTPADDING', (2, 0), (2, 0), 2),
        ('LEFTPADDING', (3, 0), (3, 0), 2),
        ('ALIGN', (4, 0), (4, 0), 'RIGHT'),
        ('ALIGN', (5, 0), (5, 0), 'LEFT'),
        ('RIGHTPADDING', (4, 0), (4, 0), 2),
        ('LEFTPADDING', (5, 0), (5, 0), 2),
        ('ALIGN', (6, 0), (6, 0), 'RIGHT'),
        ('ALIGN', (7, 0), (7, 0), 'LEFT'),
        ('RIGHTPADDING', (6, 0), (6, 0), 2),
        ('LEFTPADDING', (7, 0), (7, 0), 2),
        ('ALIGN', (8, 0), (8, 0), 'RIGHT'),
        ('ALIGN', (9, 0), (9, 0), 'LEFT'),
        ('RIGHTPADDING', (8, 0), (8, 0), 2),
        ('LEFTPADDING', (9, 0), (9, 0), 2),
        ('ALIGN', (10, 0), (10, 0), 'RIGHT'),
        ('ALIGN', (11, 0), (11, 0), 'LEFT'),
        ('RIGHTPADDING', (10, 0), (10, 0), 2),
        ('LEFTPADDING', (11, 0), (11, 0), 2),
        ('ALIGN', (12, 0), (12, 0), 'RIGHT'),
        ('ALIGN', (13, 0), (13, 0), 'LEFT'),
        ('RIGHTPADDING', (12, 0), (12, 0), 2),
        ('LEFTPADDING', (13, 0), (13, 0), 2),
        ('ALIGN', (14, 0), (14, 0), 'RIGHT'),
        ('ALIGN', (15, 0), (15, 0), 'LEFT'),
        ('RIGHTPADDING', (14, 0), (14, 0), 2),
        ('LEFTPADDING', (15, 0), (15, 0), 2),
        ('ALIGN', (16, 0), (16, 0), 'RIGHT'),
        ('ALIGN', (17, 0), (17, 0), 'LEFT'),
        ('RIGHTPADDING', (16, 0), (16, 0), 2),
        ('LEFTPADDING', (17, 0), (17, 0), 2),
        ('ALIGN', (18, 0), (18, 0), 'RIGHT'),
        ('ALIGN', (19, 0), (19, 0), 'LEFT'),
        ('RIGHTPADDING', (18, 0), (18, 0), 2),
        ('LEFTPADDING', (19, 0), (19, 0), 2),
        ('BOTTOMPADDING', (0, -1), (-1, -1), 8.9)
    ]

    data = [[# 'Aggressive Behavior:',
        # Eventually, do CheckedBox() if {{ physical }} else UncheckedBox
            'Physical', CheckedBox(),
            'Verbal', UncheckedBox(),
            'Gestures', UncheckedBox(),
            'Threatening Behaviors', UncheckedBox()
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, 2.5*inch])
    story.append(t)

    # Separate tables needed for formatting / length overruns on vertically justified columns
    data = [[# 'General Appearance:',
             'Well Groomed', CheckedBox(),
             'Fairly Groomed', UncheckedBox(),
             'Poorly Groomed', UncheckedBox(),
             'Disheveled', UncheckedBox()
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, 2*inch])
    story.append(t)

    data = [[# 'Treatment & Compliance:',
             'Acceptable', CheckedBox(),
             'Low Motivation', UncheckedBox(),
             'Resistive', UncheckedBox(),
             'Argumentative', UncheckedBox(),
             'Exit Seeking', UncheckedBox(),
             'Wandering', UncheckedBox()
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, None, None, 0.5*inch])
    story.append(t)

    data = [[# 'Inappropriate Behavior:',
            'Inappropriate Behavior', UncheckedBox(),
            # 'Describe:', 'dawdadawdawdawdawdadwawdawdaw324252342342342342342342342342',
            'Describe:', 'test describe text'
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, 4*inch])
    story.append(t)

    data = [[# 'Attitude:',
             'Cooperative', CheckedBox(),
             'Uncooperative', UncheckedBox(),
             'Marginally Cooperative', UncheckedBox(),
             'Describe:', 'test describe text'
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, 2*inch])
    story.append(t)

    data = [[# 'Speech:',
        'Intact', CheckedBox(),
        'Pressured', UncheckedBox(),
        'Hyperverbal', UncheckedBox(),
        'Loud', UncheckedBox(),
        'Slow', UncheckedBox(),
        'Yelling Out', UncheckedBox(),
        'Perseverative', UncheckedBox()
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT)
    story.append(t)

    data = [[# 'Verbal Abilities:',
        Paragraph('Receptive Language:', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=8, alignment=TA_RIGHT)),
        '',
        'Sufficient', UncheckedBox(),
        'Impaired', UncheckedBox(),
        Paragraph('Expressive Language:', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=8, alignment=TA_RIGHT)),
        '',
        'Sufficient', UncheckedBox(),
        'Impaired', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[1.5*inch, 0.01*inch, None, None,
                         None, None, 1.5*inch, 0.01*inch,
                         None, None, None, 0.65*inch]
              )
    story.append(t)

    data = [[# 'Communication:',
        'Verbal', CheckedBox(),
        'Non-verbal', UncheckedBox(),
        'Minimally Verbal', UncheckedBox(),
        'Withdrawn', UncheckedBox(),
        'Avoidant', UncheckedBox(),
        'Evasive', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, None, None, inch])
    story.append(t)

    data = [[# 'Perceptual Disturbances:',
        'None', CheckedBox(),
        'Hallucinations', UncheckedBox(),
        'Visual', UncheckedBox(),
        'Auditory', UncheckedBox(),
        'Command', UncheckedBox(),
        'Tactile', UncheckedBox(),
        'Olfactory', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, 0.5*inch])
    story.append(t)

    data = [[# 'Level of Consciousness:',
        'Alert', CheckedBox(),
        'Confused', UncheckedBox(),
        'Drowsy', UncheckedBox(),
        'Somnolent', UncheckedBox(),
        'Fluctuating', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, 2*inch])
    story.append(t)

    data = [[# 'Thought Process:',
        'Linear', CheckedBox(),
        'Disorganized', UncheckedBox(),
        'Fragmented', UncheckedBox(),
        'Racing', UncheckedBox(),
        'Circumstantial', UncheckedBox(),
        'Tangential', UncheckedBox(),
        'Blocking', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, 0.1 * inch])
    story.append(t)

    data = [[# 'Thought Content:',
        'Normal', CheckedBox(),
        'Delusions', UncheckedBox(),
        'Persecutory', UncheckedBox(),
        'Grandiose', UncheckedBox(),
        'Religious', UncheckedBox(),
        'Self-Referential', UncheckedBox(),
        'Poverty of Content', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, 0.17 * inch, None, 0.17 * inch,
                                                                       None, 0.17 * inch, None, 0.17 * inch,
                                                                       None, 0.17 * inch, None, 0.17 * inch,
                                                                       None, 0.19 * inch])
    story.append(t)

    data = [[# 'Mood:',
        'Euthymic', CheckedBox(),
        'Depressed', UncheckedBox(),
        'Anxious', UncheckedBox(),
        'Irritable', UncheckedBox(),
        'Angry', UncheckedBox(),
        'Tearful', UncheckedBox(),
        'Elated', UncheckedBox(),
        'Labile', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, None, None, 0.25 * inch])
    story.append(t)

    data = [[# 'Affect:',
        'Appropriate', CheckedBox(),
        'Flat', UncheckedBox(),
        'Blunted', UncheckedBox(),
        'Expansive', UncheckedBox(),
        'Agitated', UncheckedBox()
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, 2.4 * inch])
    story.append(t)

    data = [[# 'Harmfulness:',
        'Self', CheckedBox(),
        'Others', UncheckedBox(),
        'Negative Statements', UncheckedBox(),
        'Describe: ', 'test describe text',
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, 2.8 * inch])
    story.append(t)

    data = [[# 'Attention & Concentration:',
        'Good', CheckedBox(),
        'Fair', UncheckedBox(),
        'Poor', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, 4.5 * inch])
    story.append(t)

    data = [[# 'Orientation:',
        'Time', CheckedBox(),
        'Place', UncheckedBox(),
        'Person', UncheckedBox(),
        'Disoriented', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, 3.4 * inch])
    story.append(t)

    data = [[# 'Insight & Judgment:',
        'Good', CheckedBox(),
        'Fair', UncheckedBox(),
        'Poor', UncheckedBox()
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, 4.5 * inch])
    story.append(t)

    data = [[# 'Sleep Disturbances:',
        'Disturbance', CheckedBox(),
        'Apnea', UncheckedBox(),
        'Narcolepsy', UncheckedBox(),
        'Nightmares', UncheckedBox(),
        'Hypnagogic / Hypnopompic Hallucinations', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, None, None, None,
                                                                       None, 0.4 * inch])
    story.append(t)

    data = [[# 'Appetite Change:',
        'No', CheckedBox(),
        'Yes', UncheckedBox(),
        'Describe:', 'test describe text',
        'Tobacco Screen', UncheckedBox(),
        'Tele-Health', UncheckedBox(),
    ]]
    t = Table(data, style=TableStyle(grid), hAlign=TA_LEFT, colWidths=[None, None, None, None,
                                                                       None, 2.35*inch, None, None,
                                                                       None, None])
    story.append(t)

    story.append(FrameBreak)

    p = Paragraph(f'Assessment:',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=10, alignment=TA_LEFT))
    story.append(p)

    p = Paragraph(f'Diagnostic Impression:',
                  style=ParagraphStyle(name='Normal', leftIndent=5, fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    p = Paragraph(f'Insert diagnostic impression text here',
                  style=ParagraphStyle(name='Normal', leftIndent=15, fontName='Helvetica',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    story.append(Spacer(0, 0.30 * inch))

    p = Paragraph(f'Plan:',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=10, alignment=TA_LEFT))
    story.append(p)

    p = Paragraph(f'Current Medication:',
                  style=ParagraphStyle(name='Normal', leftIndent=5, fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    p = Paragraph(f'Insert current medication text here',
                  style=ParagraphStyle(name='Normal', leftIndent=15, fontName='Helvetica',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    story.append(Spacer(0, 0.2 * inch))

    p = Paragraph(f'Discussion and Treatment Considerations:',
                  style=ParagraphStyle(name='Normal', leftIndent=5, fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    p = Paragraph(f'Insert discussion and treatment consideration text here. '
                  f'Also, test the word wrap functionality to ensure the maximum width of the available space '
                  f'is being filled.',
                  style=ParagraphStyle(name='Normal', leftIndent=15, fontName='Helvetica',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    story.append(Spacer(0, 0.35 * inch))

    p = Paragraph(
        f'Signature:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Norm Hendricksen',
        style=ParagraphStyle(name='Normal', leftIndent=0, fontName='Helvetica-Bold',
                             fontSize=9, alignment=TA_LEFT))
    story.append(p)

    p = Paragraph(
        f'Norman Hendricksen, Ph.D. &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        f'[1] If in agreement with PCP, Risk-Benefit Analysis, IDT, RP',
        style=ParagraphStyle(name='Normal', leftIndent=64, fontName='Helvetica',
                             fontSize=9, alignment=TA_LEFT))
    story.append(p)

    # doc.build(story, onFirstPage=first_page)
    doc.build(story)


if __name__ == "__main__":
    build_form()
