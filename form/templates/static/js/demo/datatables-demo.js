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
  $('#referred_candidate_table').DataTable();
  $('.dataTables_length').addClass('bs-select');
});
