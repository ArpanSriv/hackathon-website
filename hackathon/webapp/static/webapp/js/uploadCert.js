// function startUpload() {
//     var data = new FormData()
//     data.append('image', $("#file-button")[0].files[0])
//
//     $.ajax({
//         url: "http://localhost:5000/upload",
//         type: 'POST',
//         data: new FormData($("#cert-form")[0]),
//         cache: false,
//         processData: false,
//         contentType: false,
//         error: function (data) {
//             console.log(data)
//             console.log("upload error: " + data)
//         },
//         success: function (data) {
//             console.log(data)
//             console.log("upload success")
//         }
//     })
// }