/*
 * Purpose : Provide the necessary javascript for the functionality of the HTML file "view.html"
 * Organisation/Team : Individual Assignment for Monash University -> Samir Gupta
 * Author : Samir Gupta
 * Last Modified : 6th of April 2021
*/

"use strict";

// Firstly queueIndex and studentIndex are defined from their respecitve local storage keys
let queueIndex = localStorage.getItem(STUDENT_QUEUE_KEY);
let studentIndex = localStorage.getItem(STUDENT_INDEX_KEY);

// The student at the queue index and student index is retrieved using the method getStudent
let student = consultSession.getStudent(studentIndex,queueIndex);

// The student attributes are defined appropriately using the accessor properties of the retrieved student
let studentName = student._fullName;
let studentId = student._studentId;
let studentProblem = student._problem;

// Each of these attributes are embedded into the view.html file under respective element id's
document.getElementById("studentName").innerText = studentName;
document.getElementById("studentId").innerText = studentId;
document.getElementById("studentProblem").innerText = studentProblem;

// The queue number and student position in their queue is also embedded into the file to allows user viewage
// 1 is added to the index numbers as a position of 1 makes more sense than a position of 0 in a queue
document.getElementById("studentQueue").innerText = Number(queueIndex)+1;
document.getElementById("studentPosition").innerText = Number(studentIndex)+1;