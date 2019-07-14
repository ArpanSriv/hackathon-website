let currentMember = 1;
let memberDetails = {};

function openModal(id) {
    console.log("Open Modal called: ID : " + id);

    // Clear the form before opening
    $('#hidden-reset').trigger('click');

    let $buttonClicked = $("#" + id);

    let postDot = "member" + $buttonClicked.data("member");

    if (memberDetails[postDot] !== undefined) {

        if (memberDetails[postDot].firstName !== undefined) {

            // let firstName = memberDetails.postDot.firstName;
            // let lastName...

            // $('').val...

        }
    } else {

        // console.log(id);
        let x = $buttonClicked.data("member");

        console.log("id " + x);
        // console.log(x);

        currentMember = x;

        if (x === 1) {
            $("#modalTitle").text("Team Member " + x + " (Mentor)");
        } else {
            $("#modalTitle").text("Team Member " + x);
        }
    }

    $("#modalLong").modal('show');
}

function extractDataFromModal() {
    let teamName = getInputValue("teamName").val();
    let firstName = getInputValue("fName").val();
    let lastName = getInputValue("lName").val();
    let dob = getInputValue("dob").val();
    let email = getInputValue("email").val();
    let mobno = getInputValue("mobno").val();
    let uni = getInputValue("uni").val();
    let specialization = getInputValue("specialization").val();
    let address1 = getInputValue("address1").val();
    let address2 = getInputValue("address2").val();
    let pincode = getInputValue("pincode").val();
    let city = getInputValue("city").val();

    return {
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
    };
}

function handleFormSave() {

    let member = extractDataFromModal();

    // Check if none of them is null


    // Save member details
    let postDot = "member" + currentMember;
    memberDetails[postDot] = member;

    // Hide the modal
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
        failure: function (data) {
            alert("Error Occured: " + data);
        },
        data: JSON.stringify(memberDetails)
    });
}

function getInputValue(name) {
    return $("input[name=" + name + "]").val();
}