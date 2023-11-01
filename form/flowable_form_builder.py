from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, PageTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageBreak, FrameBreak, Frame
import random
import os
import csv
from .models import Icd10Codes

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
        # print(self.height)  # 821.89
        # print(self.width)  # 565.28
        frame_top = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='frame_top')
        frame_mental_status = Frame(self.leftMargin, -110, self.width, self.height, id='frame_mental_status')
        frame_left = Frame(self.leftMargin, -142, 115, self.height, id='frame_left')
        frame_right = Frame(self.leftMargin + 110, -147, 450, self.height, id='frame_right')
        frame_bottom = Frame(self.leftMargin, self.bottomMargin, 7 * inch, 4.7 * inch, id='frame_bottom')
        self.addPageTemplates([PageTemplate(id='First', frames=[frame_top, frame_mental_status, frame_left, frame_right,
                                                                frame_bottom],
                                            pagesize=self.pagesize)])
        BaseDocTemplate.build(self, flowables)


def build_form(form_to_save=None, filename=None, signature_file_path=None):
    if not form_to_save or not filename:
        raise ValueError('Form or filename has not been supplied')
    doc = NormFormDocTemplate(filename, rightMargin=15, leftMargin=15,
                              topMargin=10, bottomMargin=10, title=form_to_save.filename)
    # doc = SimpleDocTemplate("templates/forms/flowable_test.pdf", rightMargin=15, leftMargin=15,
    #                         topMargin=10, bottomMargin=10)
    story = []
    title_text = "Psychologist Consultation / Follow-Up"
    p = Paragraph(title_text, style=ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=16,
                                                   alignment=TA_CENTER))
    story.append(p)

    story.append(Spacer(0, 0.1*inch))

    data = [['Patient Name',
             'Date',
             'Facility',
             'Physician'],
            [f'{form_to_save.patient.last_name}, {form_to_save.patient.first_name}',
             f'{form_to_save.date}', f'{form_to_save.facility.name}', f'{form_to_save.physician}']]
    grid = [('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')]
    t = Table(data, colWidths=[2.7 * inch, 0.8 * inch, 2.2 * inch, 2.1 * inch], hAlign=TA_LEFT, style=TableStyle(grid))
    story.append(t)

    story.append(Spacer(0, 0.1 * inch))

    p = Paragraph(f'Subjective (Chief Complaints, Presenting Problems, and History):',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    if form_to_save.chief_complaints_problems_history:
        p = Paragraph(f'{form_to_save.chief_complaints_problems_history}',
                      style=ParagraphStyle(name='Normal', leftIndent=10, fontName='Helvetica',
                                           fontSize=9, alignment=TA_LEFT))
        story.append(p)

    story.append(FrameBreak)

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

    # p = Paragraph('Aggressive Behavior<br /><br />'
    #               'General Appearance<br /><br />'
    #               'Treatment & Compliance<br /><br />'
    #               'Inappropriate Behavior<br /><br />'
    #               'Attitude<br /><br />'
    #               'Speech<br /><br />'
    #               'Verbal Abilities<br /><br />'
    #               'Communication<br /><br />'
    #               'Perceptual Disturbances<br /><br />'
    #               'Level of Consciousness<br /><br />'
    #               'Thought Process<br /><br />'
    #               'Thought Content<br /><br />'
    #               'Mood<br /><br />'
    #               'Affect<br /><br />'
    #               'Harmfulness<br /><br />'
    #               'Attention & Concentration<br /><br />'
    #               'Orientation<br /><br />'
    #               'Insight & Judgment<br /><br />'
    #               'Sleep Disturbance<br /><br />'
    #               'Appetite change',
    #               style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
    #                                    fontSize=8, alignment=TA_RIGHT))
    # story.append(p)

    p = Paragraph('Aggressive Behavior', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                              fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('General Appearance', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                              fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('Treatment & Compliance', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Inappropriate Behavior', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('Attitude', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Speech', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Verbal Abilities', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Communication', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('Perceptual Disturbances', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Level of Consciousness', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('Thought Process', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Thought Content', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Mood & Affect', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('(cont.)', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Harmfulness', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Attention & Concentration', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('Orientation', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('Insight & Judgment', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.06 * inch))
    p = Paragraph('Sleep Disturbance', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                             fontSize=8, alignment=TA_RIGHT))
    story.append(p)
    story.append(Spacer(0, 0.05 * inch))
    p = Paragraph('Appetite Change', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
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
            CheckedBox() if form_to_save.agg_behavior_physical else UncheckedBox(), 'Physical',
            CheckedBox() if form_to_save.agg_behavior_verbal else UncheckedBox(), 'Verbal',
            CheckedBox() if form_to_save.agg_behavior_gestures else UncheckedBox(), 'Gestures',
            CheckedBox() if form_to_save.agg_behavior_threatening else UncheckedBox(), 'Threatening Behaviors',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, 3.7 * inch])
    story.append(t)

    # Separate tables needed for formatting / length overruns on vertically justified columns
    data = [[# 'General Appearance:',
             CheckedBox() if form_to_save.gen_appearance_well_groomed else UncheckedBox(), 'Well Groomed',
             CheckedBox() if form_to_save.gen_appearance_fairly_groomed else UncheckedBox(), 'Fairly Groomed',
             CheckedBox() if form_to_save.gen_appearance_poorly_groomed else UncheckedBox(), 'Poorly Groomed',
             CheckedBox() if form_to_save.gen_appearance_disheveled else UncheckedBox(), 'Disheveled',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, 2.6 * inch])
    story.append(t)

    data = [[# 'Treatment & Compliance:',
             CheckedBox() if form_to_save.treat_and_compliance_acceptable else UncheckedBox(), 'Acceptable',
             CheckedBox() if form_to_save.treat_and_compliance_low_motivation else UncheckedBox(), 'Low Motivation',
             CheckedBox() if form_to_save.treat_and_compliance_resistive else UncheckedBox(), 'Resistive',
             CheckedBox() if form_to_save.treat_and_compliance_argumentative else UncheckedBox(), 'Argumentative',
             CheckedBox() if form_to_save.treat_and_compliance_exit_seeking else UncheckedBox(), 'Exit Seeking',
             CheckedBox() if form_to_save.treat_and_compliance_wandering else UncheckedBox(), 'Wandering',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, None, None, 1.07 * inch])
    story.append(t)

    data = [[# 'Inappropriate Behavior:',
        CheckedBox() if form_to_save.inappropriate_behavior else UncheckedBox(), 'Inappropriate Behavior',
        ' ', ' ',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, 4.57 * inch])
    story.append(t)

    data = [[# 'Attitude:',
        CheckedBox() if form_to_save.attitude_cooperative else UncheckedBox(), 'Cooperative',
        CheckedBox() if form_to_save.attitude_uncooperative else UncheckedBox(), 'Uncooperative',
        CheckedBox() if form_to_save.attitude_marginally_cooperative else UncheckedBox(), 'Marginally Cooperative',
        ' ', ' ',
        ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, 2.51 * inch])
    story.append(t)

    data = [[# 'Speech:',
        CheckedBox() if form_to_save.speech_intact else UncheckedBox(), 'Intact',
        CheckedBox() if form_to_save.speech_pressured else UncheckedBox(), 'Pressured',
        CheckedBox() if form_to_save.speech_hyperverbal else UncheckedBox(), 'Hyperverbal',
        CheckedBox() if form_to_save.speech_loud else UncheckedBox(), 'Loud',
        CheckedBox() if form_to_save.speech_slow else UncheckedBox(), 'Slow',
        CheckedBox() if form_to_save.speech_unintelligible else UncheckedBox(), 'Unintelligible',
        CheckedBox() if form_to_save.speech_yelling_out else UncheckedBox(), 'Yelling Out',
        CheckedBox() if form_to_save.speech_perseverative else UncheckedBox(), 'Perseverative',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[0.2 * inch, 0.4 * inch, 0.17 * inch, 0.58 * inch,
                         0.17 * inch, 0.7 * inch, 0.17 * inch, 0.32 * inch,
                         0.17 * inch, 0.32 * inch, 0.17 * inch, 0.72 * inch,
                         0.17 * inch, 0.62 * inch, 0.17 * inch, None])
    story.append(t)

    data = [[# 'Verbal Abilities:',
        Paragraph('Receptive Language:', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=8, alignment=TA_RIGHT)),
        '',
        CheckedBox() if form_to_save.verbal_abilities_receptive_language_sufficient else UncheckedBox(), 'Sufficient',
        CheckedBox() if form_to_save.verbal_abilities_receptive_language_impaired else UncheckedBox(), 'Impaired',
        Paragraph('Expressive Language:', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=8, alignment=TA_RIGHT)),
        '',
        CheckedBox() if form_to_save.verbal_abilities_expressive_language_sufficient else UncheckedBox(), 'Sufficient',
        CheckedBox() if form_to_save.verbal_abilities_expressive_language_impaired else UncheckedBox(), 'Impaired',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[1.5 * inch, None, 0.1 * inch, None,
                         None, None, 1.5 * inch, None,
                         0.1 * inch, None, None, 1.15 * inch]
              )
    story.append(t)

    data = [[# 'Communication:',
        CheckedBox() if form_to_save.communication_verbal else UncheckedBox(), 'Verbal',
        CheckedBox() if form_to_save.communication_non_verbal else UncheckedBox(), 'Non-verbal',
        CheckedBox() if form_to_save.communication_minimally_verbal else UncheckedBox(), 'Minimally Verbal',
        CheckedBox() if form_to_save.communication_withdrawn else UncheckedBox(), 'Withdrawn',
        CheckedBox() if form_to_save.communication_avoidant else UncheckedBox(), 'Avoidant',
        CheckedBox() if form_to_save.communication_evasive else UncheckedBox(), 'Evasive',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, None, None, 1.5 * inch])
    story.append(t)

    data = [[# 'Perceptual Disturbances:',
        CheckedBox() if form_to_save.perceptual_disturbances_none else UncheckedBox(), 'None',
        CheckedBox() if form_to_save.perceptual_disturbances_hallucinations else UncheckedBox(), 'Hallucinations',
        CheckedBox() if form_to_save.perceptual_disturbances_visual else UncheckedBox(), 'Visual',
        CheckedBox() if form_to_save.perceptual_disturbances_auditory else UncheckedBox(), 'Auditory',
        CheckedBox() if form_to_save.perceptual_disturbances_command else UncheckedBox(), 'Command',
        CheckedBox() if form_to_save.perceptual_disturbances_tactile else UncheckedBox(), 'Tactile',
        CheckedBox() if form_to_save.perceptual_disturbances_olfactory else UncheckedBox(), 'Olfactory',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, None, None, None,
                         None, 1.25 * inch])
    story.append(t)

    data = [[# 'Level of Consciousness:',
        CheckedBox() if form_to_save.level_of_consciousness_alert else UncheckedBox(), 'Alert',
        CheckedBox() if form_to_save.level_of_consciousness_confused else UncheckedBox(), 'Confused',
        CheckedBox() if form_to_save.level_of_consciousness_drowsy else UncheckedBox(), 'Drowsy',
        CheckedBox() if form_to_save.level_of_consciousness_somnolent else UncheckedBox(), 'Somnolent',
        CheckedBox() if form_to_save.level_of_consciousness_fluctuating else UncheckedBox(), 'Fluctuating',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, 2.87 * inch])
    story.append(t)

    data = [[# 'Thought Process:',
        CheckedBox() if form_to_save.thought_process_linear else UncheckedBox(), 'Linear',
        CheckedBox() if form_to_save.thought_process_disorganized else UncheckedBox(), 'Disorganized',
        CheckedBox() if form_to_save.thought_process_fragmented else UncheckedBox(), 'Fragmented',
        CheckedBox() if form_to_save.thought_process_racing else UncheckedBox(), 'Racing',
        CheckedBox() if form_to_save.thought_process_circumstantial else UncheckedBox(), 'Circumstantial',
        CheckedBox() if form_to_save.thought_process_tangential else UncheckedBox(), 'Tangential',
        CheckedBox() if form_to_save.thought_process_blocking else UncheckedBox(), 'Blocking',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, None, None, None,
                         None, 0.62 * inch])
    story.append(t)

    data = [[# 'Thought Content:',
        CheckedBox() if form_to_save.thought_content_normal else UncheckedBox(), 'Normal',
        CheckedBox() if form_to_save.thought_content_delusions else UncheckedBox(), 'Delusions',
        CheckedBox() if form_to_save.thought_content_persecutory else UncheckedBox(), 'Persecutory',
        CheckedBox() if form_to_save.thought_content_grandiose else UncheckedBox(), 'Grandiose',
        CheckedBox() if form_to_save.thought_content_religious else UncheckedBox(), 'Religious',
        CheckedBox() if form_to_save.thought_content_self_referential else UncheckedBox(), 'Self-Referential',
        CheckedBox() if form_to_save.thought_content_poverty_of_content else UncheckedBox(), 'Poverty of Content',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[0.17 * inch, 0.5 * inch, 0.17 * inch, 0.6 * inch,
                         0.17 * inch, 0.7 * inch, 0.17 * inch, 0.6 * inch,
                         0.17 * inch, 0.6 * inch, 0.17 * inch, 0.9 * inch,
                         0.19 * inch, 0.89 * inch])
    story.append(t)

    data = [[# 'Mood:',
        CheckedBox() if form_to_save.mood_euthymic else UncheckedBox(), 'Euthymic',
        CheckedBox() if form_to_save.mood_depressed else UncheckedBox(), 'Depressed',
        CheckedBox() if form_to_save.mood_anxious else UncheckedBox(), 'Anxious',
        CheckedBox() if form_to_save.mood_irritable else UncheckedBox(), 'Irritable',
        CheckedBox() if form_to_save.mood_angry else UncheckedBox(), 'Angry',
        CheckedBox() if form_to_save.mood_tearful else UncheckedBox(), 'Tearful',
        CheckedBox() if form_to_save.mood_elated else UncheckedBox(), 'Elated',
        CheckedBox() if form_to_save.mood_labile else UncheckedBox(), 'Labile',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, None, None, None,
                         None, None, None, 0.67 * inch])
    story.append(t)

    data = [[# 'Affect:',
        CheckedBox() if form_to_save.affect_appropriate else UncheckedBox(), 'Appropriate',
        CheckedBox() if form_to_save.affect_flat else UncheckedBox(), 'Flat',
        CheckedBox() if form_to_save.affect_blunted else UncheckedBox(), 'Blunted',
        CheckedBox() if form_to_save.affect_expansive else UncheckedBox(), 'Expansive',
        CheckedBox() if form_to_save.affect_agitated else UncheckedBox(), 'Agitated',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, 2.82 * inch])
    story.append(t)

    data = [[# 'Harmfulness:',
        CheckedBox() if form_to_save.harmfulness_self else UncheckedBox(), 'Self',
        CheckedBox() if form_to_save.harmfulness_others else UncheckedBox(), 'Others',
        CheckedBox() if form_to_save.harmfulness_negative_statements else UncheckedBox(), 'Negative Statements',
        ' ', ' '
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, 3.38 * inch])
    story.append(t)

    data = [[# 'Attention & Concentration:',
        CheckedBox() if form_to_save.attention_concentration_good else UncheckedBox(), 'Good',
        CheckedBox() if form_to_save.attention_concentration_fair else UncheckedBox(), 'Fair',
        CheckedBox() if form_to_save.attention_concentration_poor else UncheckedBox(), 'Poor',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, 4.72 * inch])
    story.append(t)

    data = [[# 'Orientation:',
        CheckedBox() if form_to_save.orientation_time else UncheckedBox(), 'Time',
        CheckedBox() if form_to_save.orientation_place else UncheckedBox(), 'Place',
        CheckedBox() if form_to_save.orientation_person else UncheckedBox(), 'Person',
        CheckedBox() if form_to_save.orientation_disoriented else UncheckedBox(), 'Disoriented',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, 3.94 * inch])
    story.append(t)

    data = [[# 'Insight & Judgment:',
        CheckedBox() if form_to_save.insight_judgement_good else UncheckedBox(), 'Good',
        CheckedBox() if form_to_save.insight_judgement_fair else UncheckedBox(), 'Fair',
        CheckedBox() if form_to_save.insight_judgement_poor else UncheckedBox(), 'Poor',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, 4.71 * inch])
    story.append(t)

    data = [[# 'Sleep Disturbances:',
        CheckedBox() if form_to_save.sleep_disturbance else UncheckedBox(), 'Disturbance',
        CheckedBox() if form_to_save.sleep_disturbance_apnea else UncheckedBox(), 'Apnea',
        CheckedBox() if form_to_save.sleep_disturbance_narcolepsy else UncheckedBox(), 'Narcolepsy',
        CheckedBox() if form_to_save.agg_behavior_physical else UncheckedBox(), 'Nightmares',
        CheckedBox() if form_to_save.agg_behavior_physical else UncheckedBox(), 'Hypnagogic / Hypnopompic Hallucinations',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         None, None, None, None,
                         None, 2.41 * inch])
    story.append(t)

    data = [[# 'Appetite Change:',
        CheckedBox() if form_to_save.appetite_change_no else UncheckedBox(), 'No',
        CheckedBox() if form_to_save.appetite_change_yes else UncheckedBox(), 'Yes',
        ' ', ' ',
        # CheckedBox() if form_to_save.tobacco_screen else UncheckedBox(), 'Tobacco Screen',
        # CheckedBox() if form_to_save.tele_health else UncheckedBox(), 'Tele-Health',
        Paragraph('Other:', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                                fontSize=8, alignment=TA_RIGHT)), ' ',
        CheckedBox() if form_to_save.mental_capacity else UncheckedBox(), 'Mental Capacity',
        CheckedBox() if form_to_save.placement_issues else UncheckedBox(), 'Placement Issues',
        CheckedBox() if form_to_save.tele_health else UncheckedBox(), 'Tele-Health',
    ]]
    t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
              colWidths=[None, None, None, None,
                         1.03 * inch, None,
                         None, None, None, None])
    story.append(t)

    story.append(FrameBreak)

    p = Paragraph(f'Assessment:',
                  style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
                                       fontSize=10, alignment=TA_LEFT))
    story.append(p)
    if form_to_save.inappropriate_behavior_notes or form_to_save.attitude_notes \
            or form_to_save.harmfulness_notes or form_to_save.appetite_change_notes:
        p = Paragraph(f'Comments:',
                      style=ParagraphStyle(name='Normal', leftIndent=5, fontName='Helvetica-Bold',
                                           fontSize=9, alignment=TA_LEFT))
        story.append(p)
        comments_string = f''
        if form_to_save.inappropriate_behavior_notes:
            comments_string += f'Inappropriate behavior: {form_to_save.inappropriate_behavior_notes}. '
        if form_to_save.attitude_notes:
            comments_string += f'Attitude: {form_to_save.attitude_notes}. '
        if form_to_save.harmfulness_notes:
            comments_string += f'Harmfulness: {form_to_save.harmfulness_notes}. '
        if form_to_save.appetite_change_notes:
            comments_string += f'Appetite change: {form_to_save.appetite_change_notes}.'
        p = Paragraph(comments_string,
                      style=ParagraphStyle(name='Normal', leftIndent=15, fontName='Helvetica',
                                           fontSize=9, alignment=TA_LEFT))
        story.append(p)
    p = Paragraph(f'Diagnostic Impression:',
                  style=ParagraphStyle(name='Normal', leftIndent=5, fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    if form_to_save.diagnostic_impression:
        p = Paragraph(f'{form_to_save.diagnostic_impression}',
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

    if form_to_save.current_medication:
        p = Paragraph(f'{form_to_save.current_medication}',
                      style=ParagraphStyle(name='Normal', leftIndent=15, fontName='Helvetica',
                                           fontSize=9, alignment=TA_LEFT))
        story.append(p)

    story.append(Spacer(0, 0.2 * inch))

    p = Paragraph(f'Discussion and Treatment Considerations:',
                  style=ParagraphStyle(name='Normal', leftIndent=5, fontName='Helvetica-Bold',
                                       fontSize=9, alignment=TA_LEFT))
    story.append(p)

    if form_to_save.discussion_treatment:
        p = Paragraph(f'{form_to_save.discussion_treatment}',
                      style=ParagraphStyle(name='Normal', leftIndent=15, fontName='Helvetica',
                                           fontSize=9, alignment=TA_LEFT))
        story.append(p)

    story.append(Spacer(0, 0.35 * inch))

    # p = Paragraph(
    #     f'Signature:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{form_to_save.signature}',
    #     style=ParagraphStyle(name='Normal', leftIndent=0, fontName='Helvetica-Bold',
    #                          fontSize=9, alignment=TA_LEFT))
    # story.append(p)

    # Signature file name
    if signature_file_path:
        filename = signature_file_path
    else:
        filename = os.path.abspath(os.path.dirname(__file__)) + '/private_images/' +\
                                                                'signature' +\
                                                                str(random.randint(1, 18)) +\
                                                                '.png'
    i = Image(filename=filename, hAlign=TA_LEFT, height=1.07 * inch, width=2.5 * inch)
    story.append(i)

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
