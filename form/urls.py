"""norm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HRHomePage.as_view(), name='hr_home_page'),
    path('index.html', views.HRHomePage.as_view(), name='index'),

    # Eligible Lists
    path('eligible_lists', views.EligibleLists.as_view(), name='eligible_lists'),
    path('eligible_lists/<int:pk>', views.EligibleLists.as_view(), name='eligible_lists'),
    path('create_eligible_list_form', views.CreateEligibleList.as_view(), name='create_eligible_list_form'),
    path('update_eligible_list_form/<int:pk>', views.UpdateEligibleList.as_view(), name='update_eligible_list_form'),
    path('post_eligible_list', views.PostEligibleList.as_view(), name='post_eligible_list'),
    path('adopt_eligible_list', views.AdoptEligibleList.as_view(), name='adopt_eligible_list'),
    path('score_report_pdf/<int:pk>', views.ScoreReportPDF.as_view(), name='score_report_pdf'),
    path('eligible_list_pdf/<int:pk>', views.EligibleListPDF.as_view(), name='eligible_list_pdf'),
    path('eligible_list_csv/<int:pk>', views.EligibleListCSV.as_view(), name='eligible_list_csv'),
    path('score_report_csv/<int:pk>', views.ScoreReportCSV.as_view(), name='score_report_csv'),
    # Candidates
    path('candidates', views.Candidates.as_view(), name='candidates'),
    path('candidates/<int:pk>', views.Candidates.as_view(), name='candidates'),
    path('create_candidate_form', views.CreateCandidate.as_view(), name='create_candidate_form'),
    path('update_candidate_form/<int:pk>', views.UpdateCandidate.as_view(), name='update_candidate_form'),
    # Positions
    path('positions', views.Positions.as_view(), name='positions'),
    path('positions/<int:pk>', views.Positions.as_view(), name='positions'),
    path('create_position_form', views.CreatePosition.as_view(), name='create_position_form'),
    path('update_position_form/<int:pk>', views.UpdatePosition.as_view(), name='update_position_form'),
    # Referrals
    path('referrals', views.Referrals.as_view(), name='referrals'),
    path('referrals/<int:pk>', views.Referrals.as_view(), name='referrals'),
    path('create_referral_form', views.CreateReferral.as_view(), name='create_referral_form'),
    path('update_referral_form/<int:pk>', views.UpdateReferral.as_view(), name='update_referral_form'),
    # Departments
    path('departments', views.Departments.as_view(), name='departments'),
    path('departments/<int:pk>', views.Departments.as_view(), name='departments'),
    path('create_department_form', views.CreateDepartment.as_view(), name='create_department_form'),
    path('update_department_form/<int:pk>', views.UpdateDepartment.as_view(), name='update_department_form'),
    # Jobs
    path('jobs', views.Jobs.as_view(), name='jobs'),
    path('jobs/<int:pk>', views.Jobs.as_view(), name='jobs'),
    path('create_job_form', views.CreateJob.as_view(), name='create_job_form'),
    path('update_job_form/<int:pk>', views.UpdateJob.as_view(), name='update_job_form'),
    # Applications
    path('applications', views.Applications.as_view(), name='applications'),
    path('applications/<int:pk>', views.Applications.as_view(), name='applications'),
    path('create_application_form', views.CreateApplication.as_view(), name='create_application_form'),
    path('update_application_form/<int:pk>', views.UpdateApplication.as_view(), name='update_application_form'),
    # Long Running Tasks
    path('longrunningtasks', views.LongRunningTasks.as_view(), name='longrunningtasks'),
    path('longrunningtasks/<int:pk>', views.LongRunningTasks.as_view(), name='longrunningtasks'),
    path('create_longrunningtask_form', views.CreateLongRunningTask.as_view(), name='create_longrunningtask_form'),
    path('update_longrunningtask_form/<int:pk>', views.UpdateLongRunningTask.as_view(), name='update_longrunningtask_form'),

    # EligibleListCandidate (relational table)
    path('eligiblelistcandidates', views.EligibleListCandidates.as_view(), name='eligiblelistcandidates'),
    path('eligiblelistcandidates/<int:pk>', views.EligibleListCandidates.as_view(), name='eligiblelistcandidates'),
    path('create_eligiblelistcandidate_form', views.CreateEligibleListCandidate.as_view(), name='create_eligiblelistcandidate_form'),
    path('update_eligiblelistcandidate_form/<int:pk>', views.UpdateEligibleListCandidate.as_view(), name='update_eligiblelistcandidate_form'),
    path('toggle_active_status_eligiblelistcandidate', views.ToggleActiveStatusEligibleListCandidate.as_view(), name='toggle_active_status_eligiblelistcandidate'),
    # EligibleListCandidateReferral (relational table)
    path('eligiblelistcandidatereferrals', views.EligibleListCandidateReferrals.as_view(), name='eligiblelistcandidatereferrals'),
    path('eligiblelistcandidatereferrals/<int:pk>', views.EligibleListCandidateReferrals.as_view(), name='eligiblelistcandidatereferrals'),
    path('create_eligiblelistcandidatereferral_form', views.CreateEligibleListCandidateReferral.as_view(), name='create_eligiblelistcandidatereferral_form'),
    path('update_eligiblelistcandidatereferral_form/<int:pk>', views.UpdateEligibleListCandidateReferral.as_view(), name='update_eligiblelistcandidate_form'),
    path('toggle_active_status_eligiblelistcandidatereferral', views.ToggleActiveStatusEligibleListCandidateReferral.as_view(), name='toggle_active_status_eligiblelistcandidatereferral'),
    # ScoreBandingModel (relational table)
    path('scorebandingmodelscorebands', views.ScoreBandingModelScoreBands.as_view(), name='scorebandingmodelscorebands'),
    path('scorebandingmodelscorebands/<int:pk>', views.ScoreBandingModelScoreBands.as_view(), name='scorebandingmodelscorebands'),
    path('create_scorebandingmodelscoreband_form', views.CreateScoreBandingModelScoreBand.as_view(), name='create_scorebandingmodelscoreband_form'),
    path('update_scorebandingmodelscoreband_form/<int:pk>', views.UpdateScoreBandingModelScoreBand.as_view(), name='update_scorebandingmodelscoreband_form'),

    # ReferralStatus (reference table)
    path('referralstatuses', views.ReferralStatuses.as_view(), name='referralstatuses'),
    path('referralstatuses/<int:pk>', views.ReferralStatuses.as_view(), name='referralstatuses'),
    path('create_referralstatus_form', views.CreateReferralStatus.as_view(), name='create_referralstatus_form'),
    path('update_referralstatus_form/<int:pk>', views.UpdateReferralStatus.as_view(), name='update_referralstatus_form'),
    # ScoringModel (reference table)
    path('scoringmodels', views.ScoringModels.as_view(), name='scoringmodels'),
    path('scoringmodels/<int:pk>', views.ScoringModels.as_view(), name='scoringmodels'),
    path('create_scoringmodel_form', views.CreateScoringModel.as_view(), name='create_scoringmodel_form'),
    path('update_scoringmodel_form/<int:pk>', views.UpdateScoringModel.as_view(), name='update_scoringmodel_form'),
    # ScoreBandingModel (reference table)
    path('scorebandingmodels', views.ScoreBandingModels.as_view(), name='scorebandingmodels'),
    path('scorebandingmodels/<int:pk>', views.ScoreBandingModels.as_view(), name='scorebandingmodels'),
    path('create_scorebandingmodel_form', views.CreateScoreBandingModel.as_view(), name='create_scorebandingmodel_form'),
    path('update_scorebandingmodel_form/<int:pk>', views.UpdateScoreBandingModel.as_view(), name='update_scorebandingmodel_form'),
    # ScoreBand (reference table)
    path('scorebands', views.ScoreBands.as_view(), name='scorebands'),
    path('scorebands/<int:pk>', views.ScoreBands.as_view(), name='scorebands'),
    path('create_scoreband_form', views.CreateScoreBand.as_view(), name='create_scoreband_form'),
    path('update_scoreband_form/<int:pk>', views.UpdateScoreBand.as_view(), name='update_scoreband_form'),
    # JobClass (reference table)
    path('jobclasses', views.JobClasses.as_view(), name='jobclasses'),
    path('jobclasses/<int:pk>', views.JobClasses.as_view(), name='jobclasses'),
    path('create_jobclass_form', views.CreateJobClass.as_view(), name='create_jobclass_form'),
    path('update_jobclass_form/<int:pk>', views.UpdateJobClass.as_view(), name='update_jobclass_form'),
    # EligibleListRule (reference table)
    path('eligiblelistrules', views.EligibleListRules.as_view(), name='eligiblelistrules'),
    path('eligiblelistrules/<int:pk>', views.EligibleListRules.as_view(), name='eligiblelistrules'),
    path('create_eligiblelistrule_form', views.CreateEligibleListRule.as_view(), name='create_eligiblelistrule_form'),
    path('update_eligiblelistrule_form/<int:pk>', views.UpdateEligibleListRule.as_view(), name='update_eligiblelistrule_form'),
    # CandidateReferralStatus (reference table)
    path('candidatereferralstatuses', views.CandidateReferralStatuses.as_view(), name='candidatereferralstatuses'),
    path('candidatereferralstatuses/<int:pk>', views.CandidateReferralStatuses.as_view(), name='candidatereferralstatuses'),
    path('create_candidatereferralstatus_form', views.CreateCandidateReferralStatus.as_view(), name='create_candidatereferralstatus_form'),
    path('update_candidatereferralstatus_form/<int:pk>', views.UpdateCandidateReferralStatus.as_view(), name='update_candidatereferralstatus_form'),
    # LongRunningTaskType (reference table)
    path('longrunningtasktypes', views.LongRunningTaskTypes.as_view(), name='longrunningtasktypes'),
    path('longrunningtasktypes/<int:pk>', views.LongRunningTaskTypes.as_view(), name='longrunningtasktypes'),
    path('create_longrunningtasktype_form', views.CreateLongRunningTaskType.as_view(), name='create_longrunningtasktype_form'),
    path('update_longrunningtasktype_form/<int:pk>', views.UpdateLongRunningTaskType.as_view(), name='update_longrunningtasktype_form'),
    # LongRunningTaskStatus (reference table)
    path('longrunningtaskstatuses', views.LongRunningTaskStatuses.as_view(), name='longrunningtaskstatuses'),
    path('longrunningtaskstatuses/<int:pk>', views.LongRunningTaskStatuses.as_view(), name='longrunningtaskstatuses'),
    path('create_longrunningtaskstatus_form', views.CreateLongRunningTaskStatus.as_view(), name='create_longrunningtaskstatus_form'),
    path('update_longrunningtaskstatus_form/<int:pk>', views.UpdateLongRunningTaskStatus.as_view(), name='update_longrunningtaskstatus_form'),

    # Project Roadmap
    path('roadmap', views.Roadmap.as_view(), name='roadmap'),
]
