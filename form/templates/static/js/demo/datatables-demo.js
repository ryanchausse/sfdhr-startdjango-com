// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#eligible_list_table').DataTable({
    order: [[1, 'desc']]
  });
  $('#position_table').DataTable();
  $('#referred_candidate_table').DataTable();
  $('.dataTables_length').addClass('bs-select');
});
