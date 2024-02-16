import logging
import random
import os
import csv
from django.contrib import messages
from datetime import datetime

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
        frame_middle = Frame(self.leftMargin, self.bottomMargin, self.width, self.height - 0.5 * inch, id='frame_middle')
        frame_bottom = Frame(self.leftMargin, self.bottomMargin, self.width, self.height - 2.5 * inch, id='frame_bottom')
        self.addPageTemplates([
            PageTemplate(
                id='First',
                frames=[frame_top,
                        frame_middle,
                        frame_bottom],
                pagesize=self.pagesize)
        ])
        BaseDocTemplate.build(self, flowables)


class EligibleListUtilities:
    def __init__(self, eligible_list, eligible_list_candidates):
        if not isinstance(eligible_list, EligibleList):
            raise TypeError('Eligible List object not supplied')
        self.eligible_list = eligible_list
        if not eligible_list_candidates:
            raise ValueError('No candidates on Eligible List')
        self.eligible_list_candidates = eligible_list_candidates


    # Eligible Lists
    def build_eligible_list_form(self, filename=None):
        doc = EligibleListDocTemplate(filename, rightMargin=15, leftMargin=15,
                                      topMargin=10, bottomMargin=10,
                                      title=f'Eligible List {self.eligible_list.code}')
        story = []
        title_text = f"Eligible List {self.eligible_list.code}"
        p = Paragraph(title_text, style=ParagraphStyle(name='Normal',
                                                       fontName='Helvetica',
                                                       fontSize=16,
                                                       alignment=TA_CENTER))
        story.append(p)

        story.append(Spacer(0, 0.1 * inch))

        story.append(FrameBreak)

        # Eligible List Details
        if not self.eligible_list.posted:
            posted = ''
        else:
            posted = datetime.strftime(self.eligible_list.posted, '%Y-%m-%d')
        if not self.eligible_list.inspection_start:
            inspection_start = ''
        else:
            inspection_start = datetime.strftime(self.eligible_list.inspection_end, '%Y-%m-%d')
        if not self.eligible_list.inspection_end:
            inspection_end = ''
        else:
            inspection_end = datetime.strftime(self.eligible_list.inspection_end, '%Y-%m-%d')
        if not self.eligible_list.adopted:
            adopted = ''
        else:
            adopted = datetime.strftime(self.eligible_list.adopted, '%Y-%m-%d')

        data = [['Eligible List Code:', self.eligible_list.code],
                ['Job Class:', self.eligible_list.job_class],
                ['Job Specialty:', self.eligible_list.specialty],
                ['Posted:', posted],
                ['Inspection Start:', inspection_start],
                ['Inspection End:', inspection_end],
                ['Adopted:', adopted],
                ['Number of eligibles on list:', len(self.eligible_list_candidates)]
        ]
        grid = [
            ('ALIGN', (0, 0), (0, 6), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 6), 'LEFT'),
        ]
        t = Table(data,
                  rowHeights=16,
                  style=TableStyle(grid),
                  hAlign='LEFT',
                  colWidths=[None, None,
                             None, None,
                             None, None,
                             None, None,
                             None, None,
                             None, None,
                             None, None])
        story.append(t)

        story.append(Spacer(0, 0.05 * inch))

        story.append(FrameBreak)

        story.append(Spacer(0, 0.05 * inch))

        # Rank, Score, FirstName, LastName table
        data = [['Rank', 'Score', 'First Name', 'Last Name']]
        for eligible_list_candidate in self.eligible_list_candidates:
            data.append([eligible_list_candidate.rank,
                         round(eligible_list_candidate.score, 5),
                         eligible_list_candidate.candidate.first_name,
                         eligible_list_candidate.candidate.last_name])
        grid = [('ALIGN', (0, 0), (3, 0), 'CENTER'),
                ('FONTSIZE', (0, 0), (3, 0), 12)]
        t = Table(data,
                  rowHeights=16,
                  style=TableStyle(grid),
                  hAlign='CENTER')
        story.append(t)

        story.append(Spacer(0, 0.1 * inch))

        p = Paragraph(
            f"Prepared at {datetime.strftime(datetime.now(), '%H:%M:%S on %Y-%m-%d')}",
            style=ParagraphStyle(
                name='Normal',
                fontName='Helvetica',
                fontSize=8,
                alignment=TA_CENTER)
        )
        story.append(p)
        doc.build(story)

    def construct_el_pdf_and_save_to_file(self):
        if not self.eligible_list_candidates:
            raise ValueError('No candidates on Eligible List')
        filename = os.path.abspath(os.path.dirname(__file__)) + f'/../pdfs/eligible_lists/eligible_list_{self.eligible_list.code}.pdf'
        width, height = letter
        pageinfo = f"Eligible List {self.eligible_list.code}"
        self.build_eligible_list_form(filename=filename)
        return True


    # Score Reports
    def build_score_report_form(self, filename=None):
        doc = EligibleListDocTemplate(filename, rightMargin=15, leftMargin=15,
                                      topMargin=10, bottomMargin=10,
                                      title=f'Score Report for Eligible List {self.eligible_list.code}')
        story = []
        title_text = f"Score Report for Eligible List {self.eligible_list.code}"
        p = Paragraph(title_text, style=ParagraphStyle(name='Normal',
                                                       fontName='Helvetica',
                                                       fontSize=16,
                                                       alignment=TA_CENTER))
        story.append(p)

        story.append(Spacer(0, 0.1 * inch))

        story.append(FrameBreak)

        # Eligible List Details
        if not self.eligible_list.posted:
            posted = ''
        else:
            posted = datetime.strftime(self.eligible_list.posted, '%Y-%m-%d')
        if not self.eligible_list.inspection_start:
            inspection_start = ''
        else:
            inspection_start = datetime.strftime(self.eligible_list.inspection_end, '%Y-%m-%d')
        if not self.eligible_list.inspection_end:
            inspection_end = ''
        else:
            inspection_end = datetime.strftime(self.eligible_list.inspection_end, '%Y-%m-%d')
        if not self.eligible_list.adopted:
            adopted = ''
        else:
            adopted = datetime.strftime(self.eligible_list.adopted, '%Y-%m-%d')

        data = [['Eligible List Code:', self.eligible_list.code],
                ['Job Class:', self.eligible_list.job_class],
                ['Job Specialty:', self.eligible_list.specialty],
                ['Posted:', posted],
                ['Inspection Start:', inspection_start],
                ['Inspection End:', inspection_end],
                ['Adopted:', adopted],
                ['Number of eligibles on list:', len(self.eligible_list_candidates)]
        ]
        grid = [
            ('ALIGN', (0, 0), (0, 6), 'RIGHT'),
            ('ALIGN', (1, 0), (1, 6), 'LEFT'),
        ]
        t = Table(data,
                  rowHeights=16,
                  style=TableStyle(grid),
                  hAlign='LEFT',
                  colWidths=[None, None,
                             None, None,
                             None, None,
                             None, None,
                             None, None,
                             None, None,
                             None, None])
        story.append(t)

        story.append(Spacer(0, 0.05 * inch))

        story.append(FrameBreak)

        story.append(Spacer(0, 0.05 * inch))

        # Rank, Final Score, Number of Eligibles table
        data = [['Rank', 'Final Score', 'Number of Eligibles at this Rank']]

        # Calculate how many ranks there are, with how many are on each rank
        # TODO: sanity checks. We take ranks and scores from scoring module.
        rank_tally = {} # Counts number of candidates with a certain rank
        rank_and_final_score = {} # Creates a map of each rank and the final score
        for eligible_list_candidate in self.eligible_list_candidates:
            if not eligible_list_candidate.rank in rank_tally.keys():
                rank_tally[eligible_list_candidate.rank] = 1
            else:
                rank_tally[eligible_list_candidate.rank] += 1
            if not eligible_list_candidate.rank in rank_and_final_score.keys():
                rank_and_final_score[eligible_list_candidate.rank] = eligible_list_candidate.score

        for rank in rank_tally.keys():
            data.append([rank,
                         round(rank_and_final_score[rank], 5),
                         rank_tally[rank],
                         ])
        grid = [('ALIGN', (0, 0), (3, 0), 'CENTER'),
                ('FONTSIZE', (0, 0), (3, 0), 12)]
        t = Table(data,
                  rowHeights=16,
                  style=TableStyle(grid),
                  hAlign='CENTER')
        story.append(t)

        story.append(Spacer(0, 0.1 * inch))

        p = Paragraph(
            f"Prepared at {datetime.strftime(datetime.now(), '%H:%M:%S on %Y-%m-%d')}",
            style=ParagraphStyle(
                name='Normal',
                fontName='Helvetica',
                fontSize=8,
                alignment=TA_CENTER)
        )
        story.append(p)
        doc.build(story)

    def construct_sr_pdf_and_save_to_file(self):
        filename = os.path.abspath(os.path.dirname(__file__)) + f'/../pdfs/score_reports/score_report_{self.eligible_list.code}.pdf'
        width, height = letter
        pageinfo = f"Score Report for Eligible List {self.eligible_list.code}"
        self.build_score_report_form(filename=filename)
        return True
