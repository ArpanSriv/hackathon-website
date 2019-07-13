let currentMember = 1;
var memberDetails = {};

function openModal(id){
	$('input').val('');
	$('select').val();
	$('textarea').val(''); 

	let index = id - 1;

	let postdot = "member" + currentMember;

	if (memberDetails[postdot] != undefined) {

		if (memberDetails[postdot].firstName != undefined) {

		// let firstName = memberDetails.postdot.firstName;
		// let lastName...

		// $('').val...

		}
	}

	else {

		// console.log(id);
		let x = $("#" + id).data("member");

		console.log("id " + x);
		// console.log(x);

		currentMember = x;
		
		if(x == 1){
			$("#modalTitle").text("Team Member " + x + " (Mentor)");
		}else{
			$("#modalTitle").text("Team Member " + x);
		}
	}

	$("#modalLong").modal('show');
}

function handleFormSave(event) {

	// alert("OKJ");

	var teamName = document.getElementsByName("teamName")[0].value;
	var firstName = document.getElementsByName("fName")[0].value;
	var lastName = document.getElementsByName("lName")[0].value;
	var dob = document.getElementsByName("dob")[0].value;
	var email = document.getElementsByName("email")[0].value;
	var mobno = document.getElementsByName("mobno")[0].value;
	var uni = document.getElementsByName("uni")[0].value;
	var specialization = document.getElementsByName("specialization")[0].value;
	var address1 = document.getElementsByName("address1")[0].value;
	var address2 = document.getElementsByName("address2")[0].value;
	var pincode = document.getElementsByName("pincode")[0].value;
	var city = document.getElementsByName("city")[0].value;
	// var state = document.getElementsByName("state")[0].value;
	// var projects = document.getElementsByName("projects")[0].value;

	let member = {
		'teamName': teamName,
		'firstName': firstName,
		'lastName': lastName,
		'dob': dob,
		'email': email,
		'mobno': mobno,
		'uni': uni,
		'specialization': specialization,
		'address1': address1,
		'address2': address2,
		'pincode': pincode,
		'city': city,
		// 'state': state,
		// 'projects': projects
	}

	// Check if none of them is null

	let postdot = "member" + currentMember;

	memberDetails[postdot] = member;

	$("#modalLong").modal('hide');
}

function submitForm() {
	// If members 1 and 2 are valid
	// if (memberDetails[1].firstName != null)

	// make a post request with the data = memberDetails
	// $('#individualForm').attr("action", "http://192.168.0.105:8000/app/register/individual");

	// $.ajax("http://192.168.0.105:8000/app/register/individual", memberDetails, )

	$.ajax({
        url: 'http://192.168.0.105:8000/app/register/individual',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            alert("Application Successful");
        },
        failure: function(data) {
        	alert("Error Occured: " + data);
        },
        data: memberDetails
    });
}