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

$("#upload").on("click", function() {
  $.ajax(type:"POST"
    , amount: "29.99"
    , dataType: "application/json"
    , url: "http://54.84.158.190:8888/new"
    , desc: "tester"
    , time: "15"
    , success: function(data){
         window.location.replace(data.url)
      }
    });
});
