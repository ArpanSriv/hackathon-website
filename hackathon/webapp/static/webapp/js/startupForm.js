let currentMember = 1;
let memberDetails = {};
let memberFields = {
    'firstName': 'First Name',
    'lastName': 'Last Name',
    'dob': 'Date of Birth',
    'personalEmail': 'Personal Email',
    'mobileNo': 'Phone No.',
    'addressLine1': 'Address Line 1',
    'addressLine2': 'Address Line 2',
    'pincode': 'Pincode',
    'city': 'City',
    'state': 'State',
    'experienceDesc': 'Experience',
};

let teamName;
let startupName;
let startupEmail;
let startupDOR;
let startupDomain;
let startupDesc = "DESC";

let progress = 0;


function openModal(id) {
    console.log("Open Modal called: ID : " + id);

    // Before clearing the form, make sure teamName and teamEmail remain there if filled already.
    teamName = getInputValue('teamName');
    startupName = getInputValue('startupName');
    startupEmail = getInputValue('startupEmail');
    startupDOR = getInputValue('startupDOR');
    startupDomain = getInputValue('startupDomain');
    startupDesc = getInputValue('startupDesc');

    // Clear the form before opening
    $('#hidden-reset').trigger('click');

    $("[name='teamName']").val(teamName);
    $("[name='startupName']").val(startupName);
    $("[name='startupEmail']").val(startupEmail);
    $("[name='startupDOR']").val(startupDOR);
    $("[name='startupDomain']").val(startupDomain);
    $("[name='startupDesc']").val(startupDesc);

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

function submitForm() {

    let regCert = getInputValue('file-button');

    console.log("regCert = " + regCert);

    if (regCert !== '') {

        console.log("Continuing with upload.");

        teamName = getInputValue('teamName');
        startupName = getInputValue('startupName');
        startupEmail = getInputValue('startupEmail');
        startupDOR = getInputValue('startupDOR');
        startupDomain = getInputValue('startupDomain');
        startupDesc = getInputValue('startupDesc');

        // Get the Progress ID to send.
        let progress_id = $('[name="progress-id-input"]').val();


        let progressToast = $.toast({
            heading: "Info",
            text: "<strong>Please wait while we validate your data...</strong>",
            icon: 'information',
            hideAfter: 300000,
        });

        let json_to_send = {
            'teamName': teamName,
            'startupName': startupName,
            'startupEmail': startupEmail,
            'startupDOR': startupDOR,
            'startupDomain': startupDomain,
            'startupDesc': startupDesc,
            'memberDetails': memberDetails,
            'progressID': progress_id
        };

        console.log(json_to_send);

        let register_startup_url = $('[name="hidden-startup-register-url"]').attr("data-url");


        $.ajax({
            url: register_startup_url,
            type: 'post',
            dataType: 'json',
            contentType: 'application/json',
            headers: {'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value},
            success: function (data) {
                console.log("DATA: " + data);

                // Precautionary.
                if (data['correct'] === '1') {

                    let validationProgress = updateProgressInfo(data['unique_session_id']);

                    // progressToast.text(data['message'])
                    progressToast.update({
                        heading: 'Success',
                        text: data['message'],
                        icon: 'info',
                        hideAfter: false
                    });

                    console.log("Recieved: " + data['teamName']);
                    console.log("Recieved: " + data['teamRegNo']);

                    // TODO ADD HIDDEN INPUT VALUES.
                    $('[name="team-name-hidden"]').val(data['teamName']);
                    $('[name="team-reg-no-hidden"]').val(data['teamRegNo']);

                    console.log("Values set, upload starting...");
                    startUpload();

                }

            },
            error: function (data) {
                if (data['correct'] === '0') {
                    progressToast.update({
                        heading: 'Failure',
                        text: data['message'],
                        icon: 'error',
                        hideAfter: 5000
                    });
                }
            },
            data: JSON.stringify(json_to_send)
        });

        updateProgressInfo(progress_id);

        // $(".progress-bar-custom").animate({
        //     width: '20%',
        // }, "slow");

    } else {
        let errorToast = $.toast({
            heading: "Error",
            text: "<strong>Startup Registration Certificate is mandatory.</strong>",
            icon: 'error',
            hideAfter: 3000,
        });
    }
}

function getInputValue(name) {
    return $("[name=" + name + "]").val();
}


function updateProgressInfo(progress_id) {
    console.log("Querying for progress: id = " + progress_id);

    var progress_url = $("#poll-url").attr("data-url"); // ajax view serving progress info

    $.getJSON(progress_url, {'Progress-ID': progress_id}, function (data, status) {
        if (data) {

            progress = parseInt(data['progress']);

            console.log("Progress recieved: " + progress);

            if (progress !== -1) {

                $(".progress-bar-custom").animate({
                    width: `${progress}%`,
                }, "slow");

                // trigger the next  one after 1s
                window.setTimeout(function () {
                    updateProgressInfo(progress_id)
                }, 1000);

            } else {
                 $(".progress-bar-custom").animate({
                    width: `0%`,
                }, "slow");
            }
        }
    }); // TODO
};


// ---- FILE UPLOAD ----
function startUpload() {
    let data = new FormData($("#cert-form")[0]);

    $.ajax({
        url: "http://localhost:8080/upload",
        type: 'POST',
        data: data,
        cache: false,
        processData: false,
        contentType: false,
        error: function (data) {
            console.error(data);
            console.log("upload error: " + data)
        },
        success: function (data) {
            console.log(data);
            console.log("Upload Successful.");

            window.setTimeout(function () {
                let url = $("#thank-you-url").attr("data-url");
                window.location = url
            }, 1000)

        }
    })
}
