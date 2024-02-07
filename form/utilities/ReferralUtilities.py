import logging
import requests
from django.contrib import messages
from ..models import Referral
from ..models import Position
from ..models import EligibleList
from ..models import EligibleListCandidate
from ..models import EligibleListCandidateReferral
from ..models import CandidateReferralStatus

class ReferralUtilities:
    def __init__(self, referral):
        if not isinstance(referral, Referral):
            raise TypeError('Referral object not supplied')
        self.referral = referral
    
    def refer_el_candidates(self):
        # Immediately after the Referral is created, all Eligible List
        # Candidates with status Active should have ELCandidateReferral
        # records created
        # TODO: possibly add check to ensure status of Referral
        eligible_list_candidates = EligibleListCandidate.objects.filter(
            eligible_list = self.referral.eligible_list,
            active = True
        )
        for eligible_list_candidate in eligible_list_candidates:
            new_el_candidate_referral = EligibleListCandidateReferral(
                eligible_list_candidate=eligible_list_candidate,
                referral=self.referral,
                status=CandidateReferralStatus.objects.get(status='Reachable'),
                active=True)
            new_el_candidate_referral.save()
            if not isinstance(new_el_candidate_referral, EligibleListCandidateReferral):
                raise TypeError('Problem saving EL Candidate on Referral')
        # TODO: Call SR API to add candidates to PRSP jobs
        return True
