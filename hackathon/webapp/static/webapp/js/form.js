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

            for (let field in memberFields) {
                $(`[name=${field}]`).val(memberDetails[postDot][field]);
            }
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
    // If members 1 and 2 are valid
    // if (memberDetails['member1'].firstName === undefined || memberDetails['member2'].firstName === undefined) {
    //     $.toast({
    //             heading: 'Error',
    //             text: `A minimum of two members is required for registration.`,
    //             showHideTransition: 'fade',
    //             icon: 'error',
    //             hideAfter: 10000,
    //         });
    // }

    let progressToast = $.toast({
        heading: "Info",
        text: "Please wait while we validate your data...",
        icon: 'information',
        hideAfter: 300000,
    });

    $.ajax({
        url: 'http://localhost:8000/app/register/individual',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
        success: function (data) {
            if (data.status === 'SUCCESSFUL') {
                progressToast.text("Successfull........")
            }

            else {
                alert(data)
            }
        },
        // error: function (data) {
        //     alert("Error Occured: " + data);
        // },
        data: JSON.stringify(memberDetails)
    });
}

function getInputValue(name) {
    return $("[name=" + name + "]").val();
}