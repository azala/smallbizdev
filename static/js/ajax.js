// $(document).ready(function(){
//  $("#submit-invoice").click(function(){
//     $.ajax({
//       type:"GET"
//     , amount: "29.99"
//     , dataType: "application/json"
//     , url: "http://54.84.158.190:8888/new"
//     , desc: "tester"
//     , success: function(data){
//          window.location.replace(data)
//          // console.log('you are', data)
//       }
//     });
//     // window.location.replace("https://stage.wepay.com/api/preapproval/93099784/9fd8da3d")
//   });
// });

$("#c_upload").on("click", function() {
  var s = JSON.stringify({
      amount: $("#amount").val(),
      desc: $("#desc").val(),
      time: $("#time").val()
    });
  $.ajax({
    type:"POST"
    , contentType: "application/json"
    , url: "http://54.84.158.190:8888/new"
    , data: s
    , success: function(data){
         window.location.replace(JSON.parse(data).url)
      }
    });
});

