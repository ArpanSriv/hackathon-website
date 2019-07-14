let currentMember = 1;
let memberDetails = {};

function openModal(id){
	console.log("Open Modal called: ID : " + id);

	// $('input').val('');
	// $('select').val();
	// $('textarea').val('');

	// $('.modal-member-form').trigger('reset');
	document.getElementById("modal-member-form").reset();

	let $buttonClicked = $("#" + id);

	let postdot = "member" + $buttonClicked.data("member");

	if (memberDetails[postdot] !== undefined) {

		if (memberDetails[postdot].firstName !== undefined) {

		// let firstName = memberDetails.postdot.firstName;
		// let lastName...

		// $('').val...

		}
	}

	else {

		// console.log(id);
		let x = $buttonClicked.data("member");

		console.log("id " + x);
		// console.log(x);

		currentMember = x;
		
		if (x === 1){
			$("#modalTitle").text("Team Member " + x + " (Mentor)");
		}else{
			$("#modalTitle").text("Team Member " + x);
		}
	}

	$("#modalLong").modal('show');
}

function handleFormSave(event) {

	// alert("OKJ");

	let teamName = document.getElementsByName("teamName")[0].value;
	let firstName = document.getElementsByName("fName")[0].value;
	let lastName = document.getElementsByName("lName")[0].value;
	let dob = document.getElementsByName("dob")[0].value;
	let email = document.getElementsByName("email")[0].value;
	let mobno = document.getElementsByName("mobno")[0].value;
	let uni = document.getElementsByName("uni")[0].value;
	let specialization = document.getElementsByName("specialization")[0].value;
	let address1 = document.getElementsByName("address1")[0].value;
	let address2 = document.getElementsByName("address2")[0].value;
	let pincode = document.getElementsByName("pincode")[0].value;
	let city = document.getElementsByName("city")[0].value;
	// let state = document.getElementsByName("state")[0].value;
	// let projects = document.getElementsByName("projects")[0].value;

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

	console.log("Submitting stringified....");

	$.ajax({
        url: 'http://localhost:8000/app/register/individual',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            alert("Application Successful");
        },
        failure: function(data) {
        	alert("Error Occured: " + data);
        },
        data: JSON.stringify(memberDetails)
    });
}