/*
 * Purpose : Provide the necessary javascript for the HTML file "index.html"
 * Organisation/Team : Individual Assignment for Monash University -> Samir Gupta
 * Author : Samir Gupta
 * Last Modified : 6th of April 2021
*/

"use strict";

// This function is used to create a live clock on the page
// There are no parameters or return values
function liveClock() {
    
    // timeNow is defined as a new Date
    let timeNow = new Date;

    // Seconds, minutes and hours of the date are placed in respective variables
    let seconds = timeNow.getSeconds();
    let minutes = timeNow.getMinutes();
    let hours = timeNow.getHours();

    // These two arrays are used to convert the 24hr time provided by Date in 12hr am/pm time
    // hoursArray provides the numerical value of the hour
    // amPmArray provides the 'am' or 'pm' of the specific hour
    let hoursArray = [12,1,2,3,4,5,6,7,8,9,10,11,12,1,2,3,4,5,6,7,8,9,10,11];
    let amPmArray = ["am","am","am","am","am","am","am","am","am","am","am","am","pm","pm","pm","pm","pm","pm","pm","pm","pm","pm","pm","pm"];

    // These two if statements takes single digit seconds or minutes variable and add a 0 in front of it
    if (seconds < 10){
        seconds = "0" + seconds;
    }
    if (minutes < 10){
        minutes = "0" + minutes;
    }

    // timeNowString is a string defined from the variables above in the correct format
    // The string is then placed into the index.html page at the id "currentTime"
    let timeNowString = `${hoursArray[hours]}:${minutes}:${seconds} ${amPmArray[hours]}`;
    document.getElementById("currentTime").innerText = timeNowString;
}

// This function is used to cause functions to run as soon as the page is loaded to provide information to the user
// - liveClock() provides the current time to the user
// - The setInterval funcition creates an interval that updates the time every 1000ms (1s)
// - updateQueueStatus is run with the data for the queue in order to display the queue to the user on loading
window.onload = function(){
    liveClock();
    setInterval(liveClock,1000);
    updateQueueStatus(consultSession._queue);
}

// This function is used to provide functionality to the info (i) button
// The function takes two parameters
// - The index of the student in the queue (the student's position in the queue)
// - The queue index (the number of the queue)
// There is no return value
function view(index,queueIndex){

    // These next two lines are used to set the constants for index and queue in localStorage
    // These constants are set in order to use them in later functions
    localStorage.setItem(STUDENT_INDEX_KEY,index);
    localStorage.setItem(STUDENT_QUEUE_KEY,queueIndex);

    // When the button is clicked the user it taken to the view.html page
    window.location.assign("view.html");
}

// This function is used to provide functionality to the done (tick) button and clear a student from the queue
// The function takes two parameters
// - Index of the student (their position in the queue)
// - The queue index (number of the queue)
// There is no return value
function markDone(index,queueIndex){
    
    // The user is first asked to confirm whether they would like clear this student
    // If the user cancels this confirmation the function is terminated with 'return'
    if (confirm("Are you sure you want to mark student as done?") === false){
        return;
    }

    // If the user confirms the confirmation popup these three function will run
    // - The method 'removeStudent' of consultSession is run in order to remove (splice out) the student as the specified index and queue index
    // - The storage is updated with the new consultSession data
    // - The queue status is updated with the new consultSession._queue data
    consultSession.removeStudent(index,queueIndex);
    updateStorage(APP_DATA_KEY,consultSession);
    updateQueueStatus(consultSession._queue);
}

// This function is used to display the current queues to the user on the index.html page at the div with id "queueContent"
// The data is the only parameter and the data that is used to create the lists
// There is no return value
// The function utilisies for loops and doesn't use magic numbers to add list elements dynamically
// This is in order to dynamically create elements on the page, depending on the number of queues and number of students
// The elements created have classNames defined that are sourced from the examples through mdl
function updateQueueStatus(data){
    // Firstly the div is cleared in order to make sure the elements don't double up when run more than once
    document.getElementById("queueContent").innerHTML = "";

    // The first for loop defined below iterates over the whole array in the data provided
    // For each queue in the data, a 'ul' list and 'h4' header is created
    // The className of the list is defined 
    // The 'h4' element has a text node containing Queue (number of queue) appended
    // The addded 1 for the h4 text node makes queue 0 becomes queue 1 as this makes more sense
    for (let i = 0; i < data.length; i++){
        let ul = document.getElementById("queueContent").appendChild(document.createElement("ul"));
        ul.className = "mdl-list";
        let h4 = document.getElementById("queueContent").appendChild(document.createElement("h4"));
        h4.appendChild(document.createTextNode("Queue " + (i+1)));
        ul.appendChild(h4);

        // This if statement is used to determined whether a subqueue (or entire queue) is empty or not
        // If the subqueue is empty, appropriate text is shown to display this
        // If the subqueue is not empty, a row is needed to be created in the else statement
        if (data[i].length === 0 || data[i] == ""){
            let text = document.getElementById("queueContent").appendChild(document.createElement("span"));
            text.appendChild(document.createTextNode("This Queue is Empty"));
        }
        else { 

            // This for loop iterates over each subqueue within the queue
            // It determines the amount of students in each queue and creates 3 main span elements on the page for each student
            for (let j = 0; j < data[i].length; j++){

                // A list is first created for each student
                let list = document.getElementById("queueContent").appendChild(document.createElement("li"));
                list.className = "mdl-list__item mdl-list__item--three-line";
                
                // 1. A 'person' icon with the student name next to it
                // - A list, two spans and an icon element are created and appended 
                // - The name span has text defined by the subqueue's student's full name (data[i][j]._fullName)
                let nameSpan = document.getElementById("queueContent").appendChild(document.createElement("span"));
                nameSpan.className = "mdl-list__item-primary-content";
                let iNameSpan = document.getElementById("queueContent").appendChild(document.createElement("i"));
                iNameSpan.className = "material-icons mdl-list__item-avatar";
                iNameSpan.innerText = "person";
                let name = document.getElementById("queueContent").appendChild(document.createElement("span"));
                name.innerText = data[i][j]._fullName;
                nameSpan.appendChild(iNameSpan);
                nameSpan.appendChild(name);

                // 2. The 'info' icon
                // - A span, icon, and 'a' element are created
                // - The view function is assigned to the onclick property, with j and i representing the two paramters
                let infoSpan = document.getElementById("queueContent").appendChild(document.createElement("span"));
                infoSpan.className = "mdl-list__item-secondary-content";
                let infoA = document.getElementById("queueContent").appendChild(document.createElement("a"));
                infoA.className = "mdl-list__item-secondary-action";
                infoA.onclick = function(){
                    view(j,i);
                }
                let infoI = document.getElementById("queueContent").appendChild(document.createElement("i"));
                infoI.className = "material-icons";
                infoI.innerText = "info";
                infoA.appendChild(infoI);
                infoSpan.appendChild(infoA);

                // 3. The 'tick' icon
                // - A span, icon and 'a' element are created
                // - The markDone function is assigned to the onclick property of the 'tick', j and i represent the parameters of the function
                let doneSpan = document.getElementById("queueContent").appendChild(document.createElement("span"));
                doneSpan.className = "mdl-list__item-secondary-content";
                let doneA = document.getElementById("queueContent").appendChild(document.createElement("a"));
                doneA.className = "mdl-list__item-secondary-action";
                doneA.onclick = function(){
                    markDone(j,i);
                }
                let doneI = document.getElementById("queueContent").appendChild(document.createElement("i"));
                doneI.className = "material-icons";
                doneI.innerText = "done";
                doneA.appendChild(doneI);
                doneSpan.appendChild(doneA);

                // Each span is appended to the list created at the start of the else block
                list.appendChild(nameSpan);
                list.appendChild(infoSpan);
                list.appendChild(doneSpan); 
            } 
        }
    }
}