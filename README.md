# App for Replacing MeritBridge

NB: I had to freeze the pip package django-jsignature manually and patch/replace the library's jSignature.min.js with an updated version from the jSignature JavaScript library on local and startdjango.com. The PyPi django-jsignature package is not often or well maintained, and I already tried a PR for an upstream patch.

Created and maintained by Ryan Chausse (chausse@gmail.com)

## Main functions (TODO)
- Create an Eligible List
- Add and remove Candidates to and from an Eligible List
- Calculate Scores for Candidates on an Eligible List
- Adopt a tentative Eligible List
- Create a Referral, which associates a Position to an Eligible List at a point in time (certification)
- View Candidates and their statuses on a Referral (Reachable/Hired/etc.)
- Create and send a Score Report or Eligible List PDF
- Sends Candidates on a Referral to a Job

Note: all data can be edited in Admin section

### Create an Eligible List
- Needs to sync with PeopleSoft
  - Receive webhook from PeopleSoft when an Eligible List is created

### Add and remove Candidates to and from an Eligible List
- Needs to sync with SmartRecruiters
  - Receive webhook from SmartRecruiters when a Candidate is added to Exam job

### Calculate Scores for Candidates on an Eligible List
- Needs score logic from existing MeritBridge app
- Should be triggered by a button, not a webhook from SmartRecruiters

### Adopt a tentative Eligible List
- Triggered by a button

### Create a Referral, which associates a Position to an Eligible List at a point in time (certification)
- Triggered by a button

### View Candidates and their statuses on a Referral (Reachable/Hired/etc.)
- Needs to sync with SmartRecruiters
  - Receive webhook from SmartRecruiters when a Candidate is hired, rejected, etc.
- Reachable statuses calculated in real time every time this page is viewed

### Create and send a Score Report or Eligible List PDF
- Use native Python library reportlab, not PHP library
  - Design for relative placement of names, scores, other information
- Sends emails automatically to Candidates and EIS Team

### Sends Candidates on a Referral to a Job
- Needs to sync with SmartRecruiters
  - Robust rate limiting of requests and responses via Singleton design pattern
  - Robust error handling/pre- and post-condition checks to ensure correctness
