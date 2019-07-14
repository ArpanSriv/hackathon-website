let currentMember = 1;
let memberDetails = {};
let memberFields = {
    'firstName': 'First Name',
    'lastName': 'Last Name',
    'dob': 'Date of Birth',
    'personalEmail': 'Personal Email',
    'mobileNo': 'Phone No.',
    'university': 'University',
    'specialization': 'Specialization',
    'addressLine1': 'Address Line 1',
    'addressLine2': 'Address Line 2',
    'pincode': 'Pincode',
    'city': 'City',
    'state': 'State',
    'projects': 'Projects',
};



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

    let memberFieldValues = {};

    for (let field in Object.keys(memberFields)) {
        memberFieldValues.field = getInputValue(field);
    }

    console.log(memberFieldValues);

    return memberFieldValues;
}

function handleFormSave() {

    let member = extractDataFromModal();

    // Check if none of them is null
    for (let field in Object.keys(memberFields)) {

        if (member.field === '') {
            $.toast({
                heading: 'Error',
                text: memberFields[field] + ' is required. Please try again.',
                showHideTransition: 'fade',
                icon: 'error'
            });
        }
    }


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