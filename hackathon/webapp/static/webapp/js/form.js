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

// Timer to update the progress
let updateTimerHandle;
let progress = 0;


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
        } else {
            console.log(member[field])
        }
    }


    // Save member details
    let postDot = "member" + currentMember;
    memberDetails[postDot] = member;

    // Hide the modal
    $("#modalLong").modal('hide');
}

function validateEmail(teamEmail) {
    let re = /\S+@\S+/;
    return re.test(teamEmail);
}

function validateData() {
    // Check teamName
    if (teamName === "" || teamName.length <= 3) {
        $.toast({
            heading: 'Error',
            text: "A valid (more than 3 chars) team name is required.",
            icon: 'error',
            hideAfter: 3000
        });

        return false;
    }

    if (teamEmail === "" || !validateEmail(teamEmail)) {
        $.toast({
            heading: 'Error',
            text: "A valid team email is required.",
            icon: 'error',
            hideAfter: 3000
        });

        return false;
    }

    if (memberDetails.hasOwnProperty("member1") && memberDetails.hasOwnProperty("member2")) {

        if (!memberDetails['member1'].hasOwnProperty("firstName") || !memberDetails['member2'].hasOwnProperty("firstName")) {
            $.toast({
                heading: 'Error',
                text: "An error occurred.",
                icon: 'error',
                hideAfter: 3000
            });

            alert("Hmm. This shouldn't have happened. Contact arpansri98@gmail.com with the following information. " + JSON.stringify(memberDetails))

            console.log("memberDetails = " + JSON.stringify(memberDetails));
        }
    } else {
        $.toast({
            heading: 'Error',
            text: "Member 1 or Member 2 are missing. Are you sure you entered the details?",
            icon: 'error',
            hideAfter: 3000
        });
        return false;
    }

    return true;
}

function stopUpdatingProgress() {
    if (updateTimerHandle) {
        clearTimeout(updateTimerHandle);
        progress = 0;
    }
}

function submitForm() {

    let progress_id = $('[name="progress-id-input"]').val();

    teamName = getInputValue('teamName');
    teamEmail = getInputValue('teamEmail');

    if (validateData()) {

        $.toast({
            heading: 'Processing',
            text: "Your request is being processed. Hold tight!",
            icon: 'info',
            hideAfter: false
        });

        let json_to_send = {
            'teamName': teamName,
            'teamEmail': teamEmail,
            'memberDetails': memberDetails,
            'progressID': progress_id
        };

        let register_individual_url = $('[name="hidden-individual-register-url"]').attr("data-url");


        $.ajax({
            url: register_individual_url,
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function (data) {

                // progressToast.text(data['message'])
                $.toast({
                    heading: 'Success',
                    text: "Registration Successful.",
                    icon: 'success',
                    hideAfter: false
                });

                window.setTimeout(function () {
                    let url = $("#thank-you-url").attr("data-url");
                    window.location = url
                }, 2000)
            },
            error: function (xhr, _, _) {

                $.toast({
                    heading: 'Error',
                    text: xhr.responseJSON.message,
                    icon: 'error',
                    hideAfter: false
                });

                // stopUpdatingProgress()
            },
            data: JSON.stringify(json_to_send)
        });

        // updateProgressInfo(progress_id);
    } else {
        console.error("Validation error occurred.")
    }
}

function getInputValue(name) {
    return $("[name=" + name + "]").val();
}


function updateProgressInfo(progress_id) {
    console.log("Querying for progress: id = " + progress_id);

    let progress_url = $("#poll-url").attr("data-url"); // ajax view serving progress info

    $.getJSON(progress_url, {'Progress-ID': progress_id}, function (data, status) {
        if (data) {

            progress = parseInt(data['progress']);

            // console.log("Progress received: " + data['progress']);

            if (progress !== -1) {

                $(".progress-bar-custom").animate({
                    width: `${progress}%`,
                }, "slow");

                // trigger the next  one after 1s
                updateTimerHandle = window.setTimeout(function () {
                    updateProgressInfo(progress_id)
                }, 1000);

            } else {
                $(".progress-bar-custom").animate({
                    width: `0%`,
                }, "slow");
            }
        }
    });
};