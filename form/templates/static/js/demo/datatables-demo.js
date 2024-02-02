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

/* Relational Entities */
  $('#referralcandidate_table').DataTable({
    order: [[0, 'asc']]
  });
  $('#eligiblelistcandidate_table').DataTable({
    order: [[1, 'asc'], [4, 'asc']]
  });
  $('.dataTables_length').addClass('bs-select');
});
