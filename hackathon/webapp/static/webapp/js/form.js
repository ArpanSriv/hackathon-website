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

let teamName;
let teamEmail;


function openModal(id) {
    console.log("Open Modal called: ID : " + id);

    // Before clearing the form, make sure teamName and teamEmail remain there if filled already.
    teamName = getInputValue('teamName');
    teamEmail = getInputValue('teamEmail');

    // Clear the form before opening
    $('#hidden-reset').trigger('click');

    $("input[name='teamName']").val(teamName);
    $("input[name='teamEmail']").val(teamEmail);

    let $buttonClicked = $("#" + id);

    let postDot = "member" + $buttonClicked.data("member");

    if (memberDetails[postDot] !== undefined) {

        if (memberDetails[postDot].firstName !== undefined) {

            // Fill up with data
            for (let field in memberFields) {
                $(`[name=${field}]`).val(memberDetails[postDot][field]);
            }
        }
    } else {
        let x = $buttonClicked.data("member");

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

    for (let field in memberFields) {
        memberFieldValues[field] = getInputValue(field);
    }

    console.log(memberFieldValues);

    return memberFieldValues;
}

function handleFormSave() {

    let member = extractDataFromModal();

    // Check if none of them is null
    for (let field in memberFields) {
        console.log("Checking: " + memberFields[field]);

        if (member[field] === '') {
            console.log("Empty detected.");

            $.toast({
                heading: 'Error',
                text: `<div style="padding: 5px;">
                            <b>"${memberFields[field]}"</b> is required. Please try again.
                       </div>`,
                showHideTransition: 'fade',
                icon: 'error',
                hideAfter: 10000,
            });

            return;
        }

        else {
            console.log(member[field])
        }
    }


    // Save member details
    let postDot = "member" + currentMember;
    memberDetails[postDot] = member;

    // Hide the modal
    $("#modalLong").modal('hide');
}

function submitForm() {

    let progressToast = $.toast({
        heading: "Info",
        text: "<strong>Please wait while we validate your data...</strong>",
        icon: 'information',
        hideAfter: 300000,
    });

    let json_to_send = {
        'teamName': teamName,
        'teamEmail': teamEmail,
        'memberDetails': memberDetails
    };

    $.ajax({
        url: 'http://localhost:8000/app/register/individual',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success: function (data) {
            console.log("DATA: " + data);

            // Precautionary.
            if (data['correct'] === '1') {
                // progressToast.text(data['message'])
                progressToast.update({
                    heading: 'Success',
                    text: data['message'],
                    icon: 'information',
                    hideAfter: false
                });
            }
        },
        error: function (data) {
            if (data['correct'] === '0') {
                progressToast.update({
                    heading: 'Success',
                    text: data['message'],
                    icon: 'information',
                    hideAfter: false
                });
            }
        },
        data: JSON.stringify(json_to_send)
    });
}

function getInputValue(name) {
    return $("[name=" + name + "]").val();
}