/*
 * Purpose : Provides javascript that is shared amongst add.html, view.html and index.html for functionality
 * Organisation/Team : Individual Assignment for Monash University -> Samir Gupta
 * Author : Samir Gupta
 * Last Modified : 6th of April 2021
*/

"use strict";

// Keys for defined for localStorage as constants
const STUDENT_INDEX_KEY = "studentIndex";
const STUDENT_QUEUE_KEY = "queueIndex";
const APP_DATA_KEY = "consultationAppData";

// A Student class is first created
class Student{

    // The constructor takes three parameters, full name of student, the student's id, and their problem description
    constructor (fullName, studentId, problem){
        this._fullName = fullName;
        this._studentId = studentId;
        this._problem = problem;
    }
    // These three 'gets' allow these properties to be accessed
    get fullName(){
        return this._fullName;
    }
    get studentId(){
        return this._studentId;
    }
    get problem(){
        return this._problem;
    }

    // This function is used to restore a Student instance once it is retrieved from local storage
    // The parameter data is the data that comes from localStorage and is parsed if required
    fromData(data){
        this._fullName = data._fullName;
        this._studentId = data._studentId;
        this._problem = data._problem;
    }
}

// A Session class is created 
class Session {
    
    // The constructor takes on no parameters and creates a session
    constructor(){
        
        // A date is defined and adapted into a more readable string in dataString, before being defined in this._startTime
        let date = new Date;
        let dateString = `${date.getMonth()+1}/${date.getDate()} ${date.getHours()}:${date.getMinutes()}:${date.getSeconds()} `;
        this._startTime = dateString;

        // The attribute queue is defined as an empty array
        this._queue = [];
    }

    // These two get accessors allow these attributes to be accessed
    get startTime(){
        return this._startTime;
    }
    get queue(){
        return this._queue;
    }

    // This function is used to add a subqueue to the queue defined above
    // There are no parameters, just an empty array is pushed into the queue, there is no return value
    addSubQueue(){
        this._queue.push([]);
    }

    // This function takes on three parameters and is used to add a new Student instance in the session queue
    // The parameters are all the parameters of the constructor of the Student class
    // There is no return value
    addStudent(fullName,studentId,problem){

        // A new student is defined with the parameters 
        let newStudent = new Student(fullName,studentId,problem);

        // This next part is to determine an index (lowestIndex) where the length of the queue is the lowest
        // This is due to the fact that a student must be added to the queue with the lowest amount of people
        // If queues have the same length the student must be added to the first queue of lowest length

        // Subqueue lengths is defined as an empty array
        let subQueueLengths = [];

        // The for loop below is used to push the length of each subqueue into the array defined abobve
        for (let i = 0; i < this._queue.length; i++){
            subQueueLengths.push(this._queue[i].length);
        }

        // Now that we have the array of all the lengths, we need to determine the index where the length is the smallest
        // lowestIndex is initialised at the index of 0
        // The for loop iterates over each of the indexes above 0
        // If the length of the subqueue at the index (i) is lower than the length of the subqueue at lowestIndex, lowestIndex is redefined as that i value
        // This ensures that the index of lowest subqueue length is defined in the variable
        // Starting a 0 and working upwards also ensures that if the lengths are the same, the smaller index is kept (making the index be the smallest index of lowest value)
        let lowestIndex = 0;
            for (let i = 1; i < subQueueLengths.length; i++) {
                if (subQueueLengths[i] < subQueueLengths[lowestIndex]){
                    lowestIndex = i;
                }
            }
        
        // Now that we have a new student and the index of the queue at which to add it to, we push the student into that queue
        this._queue[lowestIndex].push(newStudent);
    }

    // This function is used to remove a student from the queue and is called upon with the markDone function
    // There are two parameters in this function
    // - positionInQueue, which the students position in their queue
    // - queueNumber, which is the number of the queue the student is in
    // There is no return value
    removeStudent(positionInQueue,queueNumber){
        
        // The students position is utilised to splice them out
        this._queue[queueNumber].splice(positionInQueue,1);
    }

    // This function takes on the same two parameters as the above function and is used to get a student's data
    // This function is called upon in the view function 
    // The return value is the student's data at the queue number and position
    getStudent(positionInQueue,queueNumber){
        return this._queue[queueNumber][positionInQueue];
    }

    // This function is used to restore a Session instance from local storage using a data variable
    // The function accepts data as its parameter
    // There is no return value
    fromData(data){ 

        // First off the queue data is stored in dataHold
        // The queue is reinitialised as an array with two empty arrays nested inside
        let dataHold = data._queue;

        // These for loops and if statement are used to turn the data in dataHold into instances of Students and push them into the queue array
        // The first for loop represents the subqueues in the queue, a subqueue is added for each instance of subqueue in the data
        for (let i = 0; i < dataHold.length; i++){
            this.addSubQueue();
            // This if statement is to differentiate whether a subqueue is empty or not
            // Clearly if a subqueue is empty there should not be a Student instance created and this if statement ensures this
            if (dataHold[i]!=""){

                // This nested for loops iterates over all of the elements inside the subqueues and created a new instance of a student
                for(let j = 0; j < dataHold[i].length; j++){

                    // A new student is created
                    let student = new Student();

                    // The student's data is recreated using the fromData method
                    // The parameter of this method comes from the dataHold variable
                    // This student is then pushed into the queue
                    student.fromData(dataHold[i][j]);
                    this._queue[i].push(student);
                }
            }
        }

        // This assigns the start time attribute to the Session from the data
        this._startTime = data._startTime;
    }
}

// This function is used to check if data exists in localStorage
// It takes the parameter 'key' which is the specified key at which to check if data exists and returns a boolean value
// If the key has no data (null) the function returns false, if there is data the function returns true
function checkDataExists(key){
    if (localStorage.getItem(key) === null){
        return false;
    }
    else {
        return true;
    }
}

// This function is used to update the localStorage and has two parameters
// - key, which is the specified key at which to add the data
// - data, the data at which to add the specified key
// There is no return value
function updateStorage(key,data){
    
    // Since the data is entering local storage it needs to be stringified first
    let dataStringify = JSON.stringify(data);
    localStorage.setItem(key,dataStringify);
}

// This function is used to retrieve data from local storage
// The only parameter is the 'key' in localStoroage at which the data you want is
// The return value is dataParse, which is the data and edited if need be
function getData(key){

    // The data variable is first defined as the data stored in local storage at the parameter 'key'
    // dataParse is initialised as an empty string
    let data = localStorage.getItem(key);
    let dataParse = "";

    // This try, catch, finally method is used to parse the returned data if it is needed to 
    // If parsing it returns an error, dataParse is simply defined as the data
    // If there is no error, the data is parsed, and dataParse is defined as such
    // Finally, dataParse is returned
    try {
        dataParse = JSON.parse(data);
    }
    catch(error) {
        dataParse = data;
    }
    finally {
        return dataParse;
    }
}

// The below section of code is code that runs as the page loads in order to help display information to the user
// Firstly, consultSession is created as a new instance of a Session
let consultSession = new Session ();

// This if statement is used to determine whether there is data stored in localStorage at the key APP_DATA_KEY, which stores the queue
// If there is data; the session is recreated through the fromData method, where the data parameter utilised the getData function to get the data at the specified index
// If there is no data; defaul two subqueues are added to the session and the storage is update using updateStorage
if (checkDataExists(APP_DATA_KEY) === true){
    consultSession.fromData(getData(APP_DATA_KEY));
}
else {
    consultSession.addSubQueue();
    consultSession.addSubQueue();
    updateStorage(APP_DATA_KEY,consultSession);
}