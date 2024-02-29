// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#eligible_list_table').DataTable({
    order: [[1, 'desc']]
  });
  $('#candidate_table').DataTable({
    order: [[1, 'desc']]
  });
  $('#position_table').DataTable({
    order: [[0, 'asc']]
  });
  $('#referral_table').DataTable({
    order: [[0, 'asc']]
  });
  $('#department_table').DataTable({
    order: [[0, 'asc']]
  });
  $('#job_table').DataTable({
    order: [[0, 'asc']]
  });
  $('#application_table').DataTable({
    order: [[0, 'asc']]
  });
  $('#longrunningtask_table').DataTable({
    order: [[0, 'asc']]
  });

/* Relational Entities */
  $('#eligiblelistcandidate_table').DataTable({
    order: [[1, 'asc'], [4, 'asc']]
  });
  $('#eligiblelistcandidatereferral_table').DataTable({
    order: [[1, 'asc'], [3, 'asc']]
  });

/* Reference tables */
$('#referralstatus_table').DataTable({
  order: [[0, 'asc']]
});
$('#scoringmodel_table').DataTable({
  order: [[0, 'asc']]
});
$('#eligiblelistrule_table').DataTable({
  order: [[0, 'asc']]
});
$('#candidatereferralstatus_table').DataTable({
  order: [[0, 'asc']]
});
$('#longrunningtasktype_table').DataTable({
  order: [[0, 'asc']]
});
$('#longrunningtaskstatus_table').DataTable({
  order: [[0, 'asc']]
});

  $('.dataTables_length').addClass('bs-select');
});
