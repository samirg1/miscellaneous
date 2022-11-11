/*
 * Purpose : Provide javascript for functionality of the add.html page
 * Organisation/Team : Individual Assignment for Monash University -> Samir Gupta
 * Author : Samir Gupta
 * Last Modified : 6th of April 2021
*/

"use strict";

// This function addStudent is assigned to the button "Add Student" on the add.html page
// There are no parameters and no return value
function addStudent(){

    // First, each input value is retrieved from add.html and stored in an appropriate variable
    let fullName = document.getElementById("fullName").value;
    let studentId = document.getElementById("studentId").value;
    let problemDescription = document.getElementById("problem").value;

    // This if statement is used to determine whether the name input is blank
    // If it is blank an appropriate error message is shown and the function is terminated
    if (fullName === ""){
        document.getElementById("fullName_msg").innerText = "Please Enter Student Name";
        return;
    }

    // The constant regex is defined in order to be able to match up the id input and make sure it is valid
    // The if statement determines whether the id inputted matches the regex definition 
    // If there is no match (null returned) an appropriate error message is shown and the function is terminated
    const regex = /^[1-3]{1}[0-9]{7}$/;
    if (studentId.match(regex) === null){
        document.getElementById("studentId_msg").innerText = "Id is invalid";
        return;
    }

    // This last if statement is used to determine if the problem input is blank
    // If the input is blank an error message is shown and function does not continue
    if (problemDescription === ""){
        document.getElementById("problem_msg").innerText = "Please Enter A Description";
        return;
    }

    // If all above statements return false (all inputs are valid and not blank) the following functions run
    // - Method 'addStudent' of consultSession is utilised to create a new instance of Student in the Session
    // - Local storage is updated with the updated consultSession data
    // - An alert is shown to the user to notify them that the addition was successful
    // - The page returns the the 'home' page of index.html
    // - The queue status on index.html is updated
    consultSession.addStudent(fullName,studentId,problemDescription);
    updateStorage(APP_DATA_KEY,consultSession);
    alert("Student Added Successfully");
    window.location.assign("index.html");
    updateQueueStatus(consultSession._queue);
}