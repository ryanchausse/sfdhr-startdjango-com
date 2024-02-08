import logging
import requests
import random
import os
import csv
from django.contrib import messages

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Flowable, PageTemplate, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import BaseDocTemplate, PageBreak, FrameBreak, Frame

from ..models import EligibleList
from ..models import EligibleListCandidate
from ..models import EligibleListCandidateReferral
from ..models import CandidateReferralStatus

class EligibleListDocTemplate(BaseDocTemplate):
    def build(self, flowables):
        self._calc()
        # print(self.height)  # 821.89
        # print(self.width)  # 565.28
        frame_top = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='frame_top')
        frame_middle_content = Frame(self.leftMargin, -110, self.width, self.height, id='frame_middle_content')
        frame_left = Frame(self.leftMargin, -142, 115, self.height, id='frame_left')
        frame_right = Frame(self.leftMargin + 110, -147, 450, self.height, id='frame_right')
        frame_bottom = Frame(self.leftMargin, self.bottomMargin, 7 * inch, 4.7 * inch, id='frame_bottom')
        self.addPageTemplates([PageTemplate(id='First', frames=[frame_top, frame_middle_content, frame_left, frame_right,
                                                                frame_bottom],
                                            pagesize=self.pagesize)])
        BaseDocTemplate.build(self, flowables)


class EligibleListUtilities:
    def __init__(self, eligible_list):
        if not isinstance(eligible_list, EligibleList):
            raise TypeError('Eligible List object not supplied')
        self.eligible_list = eligible_list

    # Eligible Lists
    def build_eligible_list_form(self, form_to_save=None, filename=None):
        if not form_to_save or not filename:
            raise ValueError('Form or filename has not been supplied')
        doc = EligibleListDocTemplate(filename, rightMargin=15, leftMargin=15,
                                      topMargin=10, bottomMargin=10,
                                      title=f'Eligible List {form_to_save.code}')
        story = []
        title_text = f"Eligible List {self.eligible_list.code}"
        p = Paragraph(title_text, style=ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=16,
                                                    alignment=TA_CENTER))
        story.append(p)

        story.append(Spacer(0, 0.1 * inch))

        story.append(FrameBreak)

        story.append(Spacer(0, 0.05 * inch))
        # p = Paragraph('Appetite Change', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
        #                                                          fontSize=8, alignment=TA_RIGHT))
        # story.append(p)

        story.append(FrameBreak)

        grid = [
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ('RIGHTPADDING', (0, 0), (0, 0), 2),
            ('LEFTPADDING', (1, 0), (1, 0), 2),
        ]

        # data = [[# 'Aggressive Behavior:',
        #     # Eventually, do CheckedBox() if {{ physical }} else UncheckedBox
        #         CheckedBox() if form_to_save.agg_behavior_physical else UncheckedBox(), 'Physical',
        #         CheckedBox() if form_to_save.agg_behavior_verbal else UncheckedBox(), 'Verbal',
        #         CheckedBox() if form_to_save.agg_behavior_gestures else UncheckedBox(), 'Gestures',
        #         CheckedBox() if form_to_save.agg_behavior_threatening else UncheckedBox(), 'Threatening Behaviors',
        # ]]
        # t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
        #           colWidths=[None, None, None, None,
        #                      None, None, None, 3.7 * inch])
        # story.append(t)

        data = [[
            'a ', 'b ',
            'c ', 'd ',
            'e ', 'f ',
            'g ', 'h ',
            'i ', 'j ',
            'k ', 'l ',
            'm ', 'n ',
        ]]
        t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
                colWidths=[None, None, None, None,
                            1.03 * inch, None,
                            None, None, None, None])
        story.append(t)
        story.append(FrameBreak)
        p = Paragraph('Thus ends the EL PDF',
                        style=ParagraphStyle(
                            name='Normal',
                            fontName='Helvetica',
                            fontSize=12,
                            alignment=TA_CENTER))
        story.append(p)
        doc.build(story)

    def construct_el_pdf_and_save_to_file(self):
        eligible_list_candidates = EligibleListCandidate.objects.filter(
            eligible_list = self.eligible_list,
            active = True
        )
        filename = os.path.abspath(os.path.dirname(__file__)) + f'/../pdfs/eligible_lists/eligible_list_{self.eligible_list.code}.pdf'
        width, height = letter
        pageinfo = f"Eligible List {self.eligible_list.code}"
        self.build_eligible_list_form(form_to_save=self.eligible_list, filename=filename)
        return True

    # Score Reports
    def build_score_report_form(self, form_to_save=None, filename=None):
        if not form_to_save or not filename:
            raise ValueError('Form or filename has not been supplied')
        doc = EligibleListDocTemplate(filename, rightMargin=15, leftMargin=15,
                                      topMargin=10, bottomMargin=10,
                                      title=f'Score Report for Eligible List {form_to_save.code}')
        story = []
        title_text = f"Score Report for Eligible List {self.eligible_list.code}"
        p = Paragraph(title_text, style=ParagraphStyle(name='Normal', fontName='Helvetica', fontSize=16,
                                                    alignment=TA_CENTER))
        story.append(p)

        story.append(Spacer(0, 0.1 * inch))

        story.append(FrameBreak)

        story.append(Spacer(0, 0.05 * inch))
        # p = Paragraph('Appetite Change', style=ParagraphStyle(name='Normal', fontName='Helvetica-Bold',
        #                                                          fontSize=8, alignment=TA_RIGHT))
        # story.append(p)

        story.append(FrameBreak)

        grid = [
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (0, 0), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 0), 'LEFT'),
            ('RIGHTPADDING', (0, 0), (0, 0), 2),
            ('LEFTPADDING', (1, 0), (1, 0), 2),
        ]

        # data = [[# 'Aggressive Behavior:',
        #     # Eventually, do CheckedBox() if {{ physical }} else UncheckedBox
        #         CheckedBox() if form_to_save.agg_behavior_physical else UncheckedBox(), 'Physical',
        #         CheckedBox() if form_to_save.agg_behavior_verbal else UncheckedBox(), 'Verbal',
        #         CheckedBox() if form_to_save.agg_behavior_gestures else UncheckedBox(), 'Gestures',
        #         CheckedBox() if form_to_save.agg_behavior_threatening else UncheckedBox(), 'Threatening Behaviors',
        # ]]
        # t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
        #           colWidths=[None, None, None, None,
        #                      None, None, None, 3.7 * inch])
        # story.append(t)

        data = [[
            'a ', 'b ',
            'c ', 'd ',
            'e ', 'f ',
            'g ', 'h ',
            'i ', 'j ',
            'k ', 'l ',
            'm ', 'n ',
        ]]
        t = Table(data, rowHeights=16, style=TableStyle(grid), hAlign=TA_LEFT,
                colWidths=[None, None, None, None,
                            1.03 * inch, None,
                            None, None, None, None])
        story.append(t)
        story.append(FrameBreak)
        p = Paragraph('Thus ends the Score Report PDF',
                        style=ParagraphStyle(
                            name='Normal',
                            fontName='Helvetica',
                            fontSize=12,
                            alignment=TA_CENTER))
        story.append(p)
        doc.build(story)

    def construct_sr_pdf_and_save_to_file(self):
        eligible_list_candidates = EligibleListCandidate.objects.filter(
            eligible_list = self.eligible_list,
            active = True
        )
        filename = os.path.abspath(os.path.dirname(__file__)) + f'/../pdfs/score_reports/score_report_{self.eligible_list.code}.pdf'
        width, height = letter
        pageinfo = f"Score Report for Eligible List {self.eligible_list.code}"
        self.build_score_report_form(form_to_save=self.eligible_list, filename=filename)
        return True
