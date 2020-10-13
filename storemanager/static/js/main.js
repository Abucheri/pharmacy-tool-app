// $(document).ready(function(){
//   $('.table').paging({limit:15});
//   $(".datetimeinput").datepicker({changeYear: true,changeMonth: true, dateFormat: 'yy-mm-dd'});
// });
$(function(){
  $('.table').paging({limit:7});
  NProgress.start();
  NProgress.done();
  $(".datetimeinput").datepicker({changeYear: true,changeMonth: true, dateFormat: 'yy-mm-dd'});
});