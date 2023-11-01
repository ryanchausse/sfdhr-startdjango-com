from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.colors import white
from reportlab.platypus import paragraph
import datetime
import os

filename = 'sample_form_template.pdf'
pdf = canvas.Canvas(filename=os.path.abspath(os.path.dirname(__file__)) + '/templates/forms/' + filename,
                    pagesize=letter)
width, height = letter
# Width = 612(px?), Height = 792
pdf.setLineWidth(.3)
pdf.setTitle(filename)
doc_title_text = 'Psychologist Consultation / Follow-Up'
doc_title_text_width = stringWidth(doc_title_text, 'Helvetica-Bold', 20)
pdf.setFont('Helvetica', 20)
pdf.drawString((width-doc_title_text_width)/2, 760, doc_title_text)

# Intro demographic info and Subjective section
pdf.setFont('Helvetica', 10)
pdf.drawString(30, 730, 'Patient Name:')
pdf.setFont('Helvetica-Bold', 10)
pdf.drawString(97, 730, f'last_name, first_name')
pdf.setFont('Helvetica', 10)
pdf.drawString(300, 730, 'Facility:')
pdf.setFont('Helvetica-Bold', 10)
pdf.drawString(337, 730, f'facility.name')
pdf.setFont('Helvetica', 10)
pdf.drawString(480, 730, 'Date:')
pdf.setFont('Helvetica-Bold', 10)
pdf.drawString(505, 730, f'date')
pdf.setFont('Helvetica-Bold', 10)
pdf.drawString(30, 710, 'Subjective (Chief Complaints, Presenting Problems, and History):')

# Title for Mental Status Exam (Objective section)
mental_status_text = 'Mental Status Examination'
mental_status_text_width = stringWidth(mental_status_text, 'Helvetica', 14)
pdf.setFont('Helvetica', 14)
pdf.drawString((width-mental_status_text_width)/2, 635, mental_status_text)

# Fields for Objective section
# Can also use acroforms for interactive form fields like checkboxes
# e.g. pdf.acroForm.checkbox(x=95, y=547, size=13, fillColor=white, checked=True)
pdf.setFont('Helvetica-Bold', 10)
pdf.drawString(30, 617, 'Objective (Staff/Other Sources Reported):')

#
# Aggressive Behavior
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 600, 'Aggressive Behavior:')

# Physical
pdf.rect(x=140, y=600, width=10, height=10)
if 'form to save.physical':
    pdf.drawString(142, 602, '✔')
pdf.drawString(155, 600, 'Physical')

# Verbal
pdf.rect(x=200, y=600, width=10, height=10)
if 'form to save.verbal':
    pdf.drawString(202, 602, '✔')
pdf.drawString(215, 600, 'Verbal')

# Gestures
pdf.rect(x=255, y=600, width=10, height=10)
if 'form to save.gestures':
    pdf.drawString(257, 602, '✔')
pdf.drawString(270, 600, 'Gestures')

# Threatening Behaviors
pdf.rect(x=312, y=600, width=10, height=10)
if 'form to save.threatening_behaviors':
    pdf.drawString(314, 602, '✔')
pdf.drawString(327, 600, 'Threatening Behaviors')

# Aggressive behavior notes
# pdf.drawString(412, 600, '<<Aggressive behavior notes here>>')

#
# General appearance
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 580, 'General Appearance:')

# Well groomed
pdf.rect(x=140, y=580, width=10, height=10)
if 'form to save.well_groomed':
    pdf.drawString(142, 582, '✔')
pdf.drawString(155, 580, 'Well Groomed')

# Fairly groomed
pdf.rect(x=215, y=580, width=10, height=10)
if 'form to save.fairly_groomed':
    pdf.drawString(217, 582, '✔')
pdf.drawString(229, 580, 'Fairly groomed')

# Poorly groomed
pdf.rect(x=289, y=580, width=10, height=10)
if 'form to save.poorly_groomed':
    pdf.drawString(291, 582, '✔')
pdf.drawString(301, 580, 'Poorly groomed')

# Disheveled
pdf.rect(x=365, y=580, width=10, height=10)
if 'form to save.disheveled':
    pdf.drawString(367, 582, '✔')
pdf.drawString(379, 580, 'Disheveled')

# General Appearance notes
# pdf.drawString(422, 580, '<<General appearance notes here>>')

#
# Treatment & Compliance
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 560, 'Treatment & Compliance:')

# Acceptable
pdf.rect(x=140, y=560, width=10, height=10)
if 'form to save.acceptable':
    pdf.drawString(142, 562, '✔')
pdf.drawString(155, 560, 'Acceptable')

# Low Motivation
pdf.rect(x=205, y=560, width=10, height=10)
if 'form to save.low_motivation':
    pdf.drawString(207, 562, '✔')
pdf.drawString(219, 560, 'Low Motivation')

# Resistive
pdf.rect(x=282, y=560, width=10, height=10)
if 'form to save.resistive':
    pdf.drawString(284, 562, '✔')
pdf.drawString(294, 560, 'Resistive')

# Argumentative
pdf.rect(x=337, y=560, width=10, height=10)
if 'form to save.argumentative':
    pdf.drawString(339, 562, '✔')
pdf.drawString(351, 560, 'Argumentative')

# Exit seeking
pdf.rect(x=409, y=560, width=10, height=10)
if 'form to save.exit_seeking':
    pdf.drawString(411, 562, '✔')
pdf.drawString(423, 560, 'Exit Seeking')

# Treatment & Compliance notes
# pdf.drawString(469, 560, '<<Treatment & Compliance notes here>>')

#
# Inappropriate Behavior
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 540, 'Inappropriate Behavior:')

# Inappropriate Behavior
pdf.rect(x=140, y=540, width=10, height=10)
if 'form to save.inappropriate_behavior':
    pdf.drawString(142, 542, '✔')
pdf.drawString(155, 540, 'Inappropriate Behavior')

# Inappropriate Behavior notes
# pdf.drawString(245, 540, '<<Inappropriate Behavior notes here>>')

#
# Attitude
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 520, 'Attitude:')

# Cooperative
pdf.rect(x=140, y=520, width=10, height=10)
if 'form to save.cooperative':
    pdf.drawString(142, 522, '✔')
pdf.drawString(155, 520, 'Cooperative')

# Uncooperative
pdf.rect(x=205, y=520, width=10, height=10)
if 'form to save.uncooperative':
    pdf.drawString(207, 522, '✔')
pdf.drawString(219, 520, 'Uncooperative')

# Marginally Cooperative
pdf.rect(x=278, y=520, width=10, height=10)
if 'form to save.marginally_cooperative':
    pdf.drawString(280, 522, '✔')
pdf.drawString(292, 520, 'Marginally Cooperative')

# Attitude - other
pdf.rect(x=383, y=520, width=10, height=10)
if 'form to save.other':
    pdf.drawString(385, 522, '✔')
pdf.drawString(395, 520, 'Other')

# Attitude notes
# pdf.drawString(424, 520, '<<Attitude notes here>>')

#
# Speech
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 500, 'Speech:')

# Intact
pdf.rect(x=140, y=500, width=10, height=10)
if 'form to save.speech_intact':
    pdf.drawString(142, 502, '✔')
pdf.drawString(155, 500, 'Intact')

# Pressured
pdf.rect(x=185, y=500, width=10, height=10)
if 'form to save.speech_pressured':
    pdf.drawString(187, 502, '✔')
pdf.drawString(198, 500, 'Pressured')

# Hyperverbal
pdf.rect(x=244, y=500, width=10, height=10)
if 'form to save.speech_hyperverbal':
    pdf.drawString(246, 502, '✔')
pdf.drawString(257, 500, 'Hyperverbal')

# Loud
pdf.rect(x=310, y=500, width=10, height=10)
if 'form to save.speech_loud':
    pdf.drawString(312, 502, '✔')
pdf.drawString(323, 500, 'Loud')

# Slow
pdf.rect(x=350, y=500, width=10, height=10)
if 'form to save.speech_slow':
    pdf.drawString(352, 502, '✔')
pdf.drawString(363, 500, 'Slow')

# Unintelligible
pdf.rect(x=385, y=500, width=10, height=10)
if 'form to save.speech_unintelligible':
    pdf.drawString(387, 502, '✔')
pdf.drawString(400, 500, 'Unintelligible')

# Yelling Out
pdf.rect(x=140, y=480, width=10, height=10)
if 'form to save.speech_yelling_out':
    pdf.drawString(142, 482, '✔')
pdf.drawString(155, 480, 'Yelling Out')

# Perseverative
pdf.rect(x=204, y=480, width=10, height=10)
if 'form to save.speech_perseverative':
    pdf.drawString(206, 482, '✔')
pdf.drawString(218, 480, 'Perseverative')

# Speech notes
# pdf.drawString(275, 480, '<<Speech notes here>>')

#
# Verbal Abilities
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 460, 'Verbal Abilities:')

# Receptive language
pdf.setFont('Helvetica-Bold', 8)
pdf.drawString(140, 462, 'Receptive Language:')
pdf.setFont('Helvetica', 8)
pdf.rect(x=230, y=460, width=10, height=10)
if 'form to save.sufficient':
    pdf.drawString(232, 462, '✔')
pdf.drawString(245, 462, 'Sufficient')
pdf.rect(x=288, y=460, width=10, height=10)
if 'form to save.impaired':
    pdf.drawString(290, 462, '✔')
pdf.drawString(300, 462, 'Impaired')

# Expressive language
pdf.setFont('Helvetica-Bold', 8)
pdf.drawString(340, 462, 'Expressive Language:')
pdf.setFont('Helvetica', 8)
pdf.rect(x=433, y=460, width=10, height=10)
if 'form to save.sufficient':
    pdf.drawString(435, 462, '✔')
pdf.drawString(447, 462, 'Sufficient')
pdf.rect(x=486, y=460, width=10, height=10)
if 'form to save.impaired':
    pdf.drawString(488, 462, '✔')
pdf.drawString(500, 462, 'Impaired')

# Verbal Abilities notes
# pdf.drawString(550, 460, '<<Verbal Abilities notes here>>')

#
# Communication
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 440, 'Communication:')

# Verbal
pdf.rect(x=140, y=440, width=10, height=10)
if 'form to save.communication_verbal':
    pdf.drawString(142, 442, '✔')
pdf.drawString(155, 440, 'Verbal')

# Nonverbal
pdf.rect(x=185, y=440, width=10, height=10)
if 'form to save.nonverbal':
    pdf.drawString(187, 442, '✔')
pdf.drawString(200, 440, 'Non-verbal')

# Minimally Verbal
pdf.rect(x=250, y=440, width=10, height=10)
if 'form to save.minimally_verbal':
    pdf.drawString(252, 442, '✔')
pdf.drawString(265, 440, 'Minimally Verbal')

# Withdrawn
pdf.rect(x=335, y=440, width=10, height=10)
if 'form to save.withdrawn':
    pdf.drawString(337, 442, '✔')
pdf.drawString(350, 440, 'Withdrawn')

# Avoidant
pdf.rect(x=395, y=440, width=10, height=10)
if 'form to save.avoidant':
    pdf.drawString(397, 442, '✔')
pdf.drawString(410, 440, 'Avoidant')

# Evasive
pdf.rect(x=450, y=440, width=10, height=10)
if 'form to save.evasive':
    pdf.drawString(452, 442, '✔')
pdf.drawString(465, 440, 'Evasive')

# Communication notes
# pdf.drawString(424, 440, '<<Communication notes here>>')

#
# Perceptual Disturbances
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 420, 'Perceptual Disturbances:')

# None
pdf.rect(x=140, y=420, width=10, height=10)
if 'form to save.perceptual_disturbances_none':
    pdf.drawString(142, 422, '✔')
pdf.drawString(155, 420, 'None')

# Hallucinations
pdf.rect(x=182, y=420, width=10, height=10)
if 'form to save.perceptual_disturbances_hallucinations':
    pdf.drawString(184, 422, '✔')
pdf.drawString(197, 420, 'Hallucinations')

# Visual
pdf.rect(x=255, y=420, width=10, height=10)
if 'form to save.perceptual_disturbances_visual':
    pdf.drawString(257, 422, '✔')
pdf.drawString(269, 420, 'Visual')

# Auditory
pdf.rect(x=300, y=420, width=10, height=10)
if 'form to save.perceptual_disturbances_auditory':
    pdf.drawString(302, 422, '✔')
pdf.drawString(313, 420, 'Auditory')

# Command
pdf.rect(x=350, y=420, width=10, height=10)
if 'form to save.perceptual_disturbances_command':
    pdf.drawString(352, 422, '✔')
pdf.drawString(364, 420, 'Command')

# Tactile
pdf.rect(x=410, y=420, width=10, height=10)
if 'form to save.perceptual_disturbances_tactile':
    pdf.drawString(412, 422, '✔')
pdf.drawString(423, 420, 'Tactile')

# Olfactory
pdf.rect(x=455, y=420, width=10, height=10)
if 'form to save.perceptual_disturbances_olfactory':
    pdf.drawString(457, 422, '✔')
pdf.drawString(470, 420, 'Olfactory')

# Perceptual Disturbance notes
# pdf.drawString(424, 440, '<<Perceptual Disturbances notes here>>')

#
# Level of Consciousness
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 400, 'Level of Consciousness:')

# Alert
pdf.rect(x=140, y=400, width=10, height=10)
if 'form to save.level_of_consciousness_alert':
    pdf.drawString(142, 402, '✔')
pdf.drawString(155, 400, 'Alert')

# Confused
pdf.rect(x=182, y=400, width=10, height=10)
if 'form to save.level_of_consciousness_confused':
    pdf.drawString(184, 402, '✔')
pdf.drawString(197, 400, 'Confused')

# Drowsy
pdf.rect(x=240, y=400, width=10, height=10)
if 'form to save.level_of_consciousness_drowsy':
    pdf.drawString(242, 402, '✔')
pdf.drawString(255, 400, 'Drowsy')

# Somnolent
pdf.rect(x=290, y=400, width=10, height=10)
if 'form to save.level_of_consciousness_somnolent':
    pdf.drawString(292, 402, '✔')
pdf.drawString(305, 400, 'Somnolent')

# Fluctuating
pdf.rect(x=352, y=400, width=10, height=10)
if 'form to save.level_of_consciousness_fluctuating':
    pdf.drawString(354, 402, '✔')
pdf.drawString(366, 400, 'Fluctuating')

# Level of Consciousness notes
# pdf.drawString(424, 440, '<<Level of Consciousness notes here>>')

#
# Thought Process
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 380, 'Thought Process:')

# Linear
pdf.rect(x=140, y=380, width=10, height=10)
if 'form to save.thought_process_linear':
    pdf.drawString(142, 382, '✔')
pdf.drawString(155, 380, 'Linear')

# Disorganized
pdf.rect(x=182, y=380, width=10, height=10)
if 'form to save.thought_process_disorganized':
    pdf.drawString(184, 382, '✔')
pdf.drawString(197, 380, 'Disorganized')

# Fragmented
pdf.rect(x=250, y=380, width=10, height=10)
if 'form to save.thought_process_fragmented':
    pdf.drawString(252, 382, '✔')
pdf.drawString(265, 380, 'Fragmented')

# Racing
pdf.rect(x=315, y=380, width=10, height=10)
if 'form to save.thought_process_racing':
    pdf.drawString(317, 382, '✔')
pdf.drawString(330, 380, 'Racing')

# Circumstantial
pdf.rect(x=360, y=380, width=10, height=10)
if 'form to save.thought_process_circumstantial':
    pdf.drawString(362, 382, '✔')
pdf.drawString(375, 380, 'Circumstantial')

# Tangential
pdf.rect(x=433, y=380, width=10, height=10)
if 'form to save.thought_process_tangential':
    pdf.drawString(435, 382, '✔')
pdf.drawString(445, 380, 'Tangential')

# Blocking
pdf.rect(x=490, y=380, width=10, height=10)
if 'form to save.thought_process_blocking':
    pdf.drawString(492, 382, '✔')
pdf.drawString(503, 380, 'Blocking')

# Thought Process notes
# pdf.drawString(424, 440, '<<Thought Process notes here>>')

#
# Thought Content
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 360, 'Thought Content:')

# Normal
pdf.rect(x=140, y=360, width=10, height=10)
if 'form to save.thought_content_normal':
    pdf.drawString(142, 362, '✔')
pdf.drawString(155, 360, 'Normal')

# Delusions
pdf.rect(x=192, y=360, width=10, height=10)
if 'form to save.thought_content_delusions':
    pdf.drawString(194, 362, '✔')
pdf.drawString(207, 360, 'Delusions')

# Persecutory
pdf.rect(x=250, y=360, width=10, height=10)
if 'form to save.thought_content_persecutory':
    pdf.drawString(252, 362, '✔')
pdf.drawString(265, 360, 'Persecutory')

# Grandiose
pdf.rect(x=315, y=360, width=10, height=10)
if 'form to save.thought_content_grandiose':
    pdf.drawString(317, 362, '✔')
pdf.drawString(330, 360, 'Grandiose')

# Religious
pdf.rect(x=375, y=360, width=10, height=10)
if 'form to save.thought_content_religious':
    pdf.drawString(377, 362, '✔')
pdf.drawString(389, 360, 'Religious')

# Self-Referential
pdf.rect(x=433, y=360, width=10, height=10)
if 'form to save.thought_content_self_referential':
    pdf.drawString(435, 362, '✔')
pdf.drawString(445, 360, 'Self-Referential')

# Poverty of Content
pdf.rect(x=140, y=340, width=10, height=10)
if 'form to save.thought_content_poverty_of_content':
    pdf.drawString(142, 342, '✔')
pdf.drawString(155, 340, 'Poverty of Content')

# Thought Content notes
# pdf.drawString(424, 340, '<<Thought Content notes here>>')

#
# Mood
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 320, 'Mood:')

# Euthymic
pdf.rect(x=140, y=320, width=10, height=10)
if 'form to save.mood_euthymic':
    pdf.drawString(142, 322, '✔')
pdf.drawString(155, 320, 'Euthymic')

# Depressed
pdf.rect(x=194, y=320, width=10, height=10)
if 'form to save.mood_depressed':
    pdf.drawString(196, 322, '✔')
pdf.drawString(209, 320, 'Depressed')

# Anxious
pdf.rect(x=254, y=320, width=10, height=10)
if 'form to save.mood_anxious':
    pdf.drawString(256, 322, '✔')
pdf.drawString(267, 320, 'Anxious')

# Irritable
pdf.rect(x=305, y=320, width=10, height=10)
if 'form to save.mood_irritable':
    pdf.drawString(307, 322, '✔')
pdf.drawString(320, 320, 'Irritable')

# Angry
pdf.rect(x=358, y=320, width=10, height=10)
if 'form to save.mood_angry':
    pdf.drawString(360, 322, '✔')
pdf.drawString(372, 320, 'Angry')

# Tearful
pdf.rect(x=400, y=320, width=10, height=10)
if 'form to save.mood_tearful':
    pdf.drawString(402, 322, '✔')
pdf.drawString(414, 320, 'Tearful')

# Elated
pdf.rect(x=445, y=320, width=10, height=10)
if 'form to save.mood_elated':
    pdf.drawString(447, 322, '✔')
pdf.drawString(460, 320, 'Elated')

# Labile
pdf.rect(x=490, y=320, width=10, height=10)
if 'form to save.mood_labile':
    pdf.drawString(492, 322, '✔')
pdf.drawString(505, 320, 'Labile')

# Mood notes
# pdf.drawString(424, 320, '<<Mood notes here>>')

#
# Affect
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 300, 'Affect:')

# Appropriate
pdf.rect(x=140, y=300, width=10, height=10)
if 'form to save.affect_appropriate':
    pdf.drawString(142, 302, '✔')
pdf.drawString(155, 300, 'Appropriate')

# Flat
pdf.rect(x=205, y=300, width=10, height=10)
if 'form to save.affect_flat':
    pdf.drawString(207, 302, '✔')
pdf.drawString(220, 300, 'Flat')

# Blunted
pdf.rect(x=245, y=300, width=10, height=10)
if 'form to save.affect_blunted':
    pdf.drawString(247, 302, '✔')
pdf.drawString(260, 300, 'Blunted')

# Expansive
pdf.rect(x=300, y=300, width=10, height=10)
if 'form to save.affect_expansive':
    pdf.drawString(302, 302, '✔')
pdf.drawString(315, 300, 'Expansive')

# Agitated
pdf.rect(x=362, y=300, width=10, height=10)
if 'form to save.affect_agitated':
    pdf.drawString(364, 302, '✔')
pdf.drawString(376, 300, 'Agitated')

# Affect notes
# pdf.drawString(424, 320, '<<Affect notes here>>')

#
# Harmfulness
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 280, 'Harmfulness:')

# Self
pdf.rect(x=140, y=280, width=10, height=10)
if 'form to save.harmfulness_self':
    pdf.drawString(142, 282, '✔')
pdf.drawString(155, 280, 'Self')

# Others
pdf.rect(x=175, y=280, width=10, height=10)
if 'form to save.harmfulness_others':
    pdf.drawString(177, 282, '✔')
pdf.drawString(190, 280, 'Others')

# Negative Statements
pdf.rect(x=222, y=280, width=10, height=10)
if 'form to save.harmfulness_negative_statements':
    pdf.drawString(224, 282, '✔')
pdf.drawString(237, 280, 'Negative Statements')

# Other
pdf.rect(x=320, y=280, width=10, height=10)
if 'form to save.harmfulness_other':
    pdf.drawString(322, 282, '✔')
pdf.drawString(333, 280, 'Other')

# Harmfulness notes
pdf.drawString(360, 280, '<<Harmfulness notes>>')

#
# Attention & Concentration
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 260, 'Attention & Concentration:')

# Good
pdf.rect(x=140, y=260, width=10, height=10)
if 'form to save.attention_concentration_good':
    pdf.drawString(142, 262, '✔')
pdf.drawString(155, 260, 'Good')

# Fair
pdf.rect(x=185, y=260, width=10, height=10)
if 'form to save.attention_concentration_fair':
    pdf.drawString(187, 262, '✔')
pdf.drawString(198, 260, 'Fair')

# Poor
pdf.rect(x=222, y=260, width=10, height=10)
if 'form to save.attention_concentration_poor':
    pdf.drawString(224, 262, '✔')
pdf.drawString(235, 260, 'Poor')

# Attention & Concentration notes
pdf.drawString(360, 260, '<<Attention and Concentration Notes>>')

#
# Orientation
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 240, 'Orientation:')

# Time
pdf.rect(x=140, y=240, width=10, height=10)
if 'form to save.orientation_time':
    pdf.drawString(142, 242, '✔')
pdf.drawString(155, 240, 'Time')

# Place
pdf.rect(x=180, y=240, width=10, height=10)
if 'form to save.orientation_place':
    pdf.drawString(182, 242, '✔')
pdf.drawString(195, 240, 'Place')

# Person
pdf.rect(x=222, y=240, width=10, height=10)
if 'form to save.orientation_person':
    pdf.drawString(224, 242, '✔')
pdf.drawString(235, 240, 'Person')

# Situation
pdf.rect(x=265, y=240, width=10, height=10)
if 'form to save.orientation_situation':
    pdf.drawString(267, 242, '✔')
pdf.drawString(278, 240, 'Situation')

# Disoriented
pdf.rect(x=315, y=240, width=10, height=10)
if 'form to save.orientation_disoriented':
    pdf.drawString(317, 242, '✔')
pdf.drawString(330, 240, 'Disoriented')

# Orientation notes
pdf.drawString(380, 240, '<<Orientation Notes>>')

#
# Insight & Judgment
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 220, 'Insight & Judgment:')

# Good
pdf.rect(x=140, y=220, width=10, height=10)
if 'form to save.insight_judgement_good':
    pdf.drawString(142, 222, '✔')
pdf.drawString(155, 220, 'Good')

# Fair
pdf.rect(x=180, y=220, width=10, height=10)
if 'form to save.insight_judgement_fair':
    pdf.drawString(182, 222, '✔')
pdf.drawString(195, 220, 'Fair')

# Poor
pdf.rect(x=220, y=220, width=10, height=10)
if 'form to save.insight_judgement_poor':
    pdf.drawString(222, 222, '✔')
pdf.drawString(235, 220, 'Poor')

# Insight & Judgment notes
pdf.drawString(270, 220, '<<Insight & Judgment Notes>>')

#
# Sleep Disturbance
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 200, 'Sleep Disturbance:')

# Disturbance
pdf.rect(x=140, y=200, width=10, height=10)
if 'form to save.sleep_disturbance':
    pdf.drawString(142, 202, '✔')
pdf.drawString(155, 200, 'Disturbance')

# Apnea
pdf.rect(x=205, y=200, width=10, height=10)
if 'form to save.sleep_disturbance_apnea':
    pdf.drawString(207, 202, '✔')
pdf.drawString(219, 200, 'Apnea')

# Narcolepsy
pdf.rect(x=250, y=200, width=10, height=10)
if 'form to save.sleep_disturbance_narcolepsy':
    pdf.drawString(252, 202, '✔')
pdf.drawString(263, 200, 'Narcolepsy')

# Describe
pdf.rect(x=310, y=200, width=10, height=10)
if 'form to save.sleep_disturbance_describe':
    pdf.drawString(312, 202, '✔')
pdf.drawString(323, 200, 'Describe')

# Sleep Disturbance notes
pdf.drawString(360, 200, '<<Sleep Disturbance Notes>>')

#
# Appetite & Misc.
#
pdf.setFont('Helvetica', 8)
pdf.drawString(30, 180, 'Appetite & Misc.:')

# Appetite Change
pdf.rect(x=140, y=180, width=10, height=10)
if 'form to save.appetite_change':
    pdf.drawString(142, 182, '✔')
pdf.drawString(155, 180, 'Appetite Change')

# Appetite Change notes
pdf.drawString(220, 180, '<<Appetite Change Notes>>')

# Tobacco Screen
pdf.rect(x=390, y=180, width=10, height=10)
if 'form to save.tobacco_screen':
    pdf.drawString(392, 182, '✔')
pdf.drawString(402, 180, 'Tobacco Screen')

# Tele-Health
pdf.rect(x=465, y=180, width=10, height=10)
if 'form to save.tele_health':
    pdf.drawString(467, 182, '✔')
pdf.drawString(478, 180, 'Tele-Health')

# Assessment
pdf.setFont('Helvetica-Bold', 10)
pdf.drawString(30, 160, 'Assessment:')

# Diagnostic Impression
pdf.setFont('Helvetica-Bold', 8)
pdf.drawString(30, 150, 'Diagnostic Impression:')
pdf.setFont('Helvetica', 8)
if 'form to save.diagnostic_impression':
    pdf.drawString(50, 140, 'form to save.diagnostic_impression')

# Plan
pdf.setFont('Helvetica-Bold', 10)
pdf.drawString(30, 115, 'Plan:')

# Current Medication
pdf.setFont('Helvetica-Bold', 8)
pdf.drawString(30, 105, 'Current Medication:')
pdf.setFont('Helvetica', 8)
if 'form to save.current_medication':
    pdf.drawString(50, 95, 'form to save.current_medication')

# Discussion and Treatment Considerations
pdf.setFont('Helvetica-Bold', 8)
pdf.drawString(30, 75, 'Discussion and Treatment Considerations[1]:')
pdf.setFont('Helvetica', 8)
if 'form to save.discussion_treatment':
    pdf.drawString(50, 65, 'form to save.discussion_treatment')

# Signature
pdf.setFont('Helvetica-Bold', 8)
pdf.drawString(30, 30, 'Signature:')
pdf.setFont('Helvetica', 8)
if 'form to save.signature':
    pdf.drawString(80, 30, 'form to save.signature')
    pdf.drawString(80, 20, 'Norman Hendricksen, Ph.D.')

# Disclaimer
pdf.drawString(380, 20, '[1] If in agreement with PCP, Risk-Benefit Analysis, IDT. RP')

pdf.setFont('Helvetica', 8)
pdf.drawString(5, 5, f'Time printed: {str(datetime.datetime.now())}')
pdf.showPage()
pdf.save()
