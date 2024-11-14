const dynmaicFormDiv = document.getElementById('createForm');
var workExperienceBtn = document.getElementById('addwe');
var counter = 0;

function addWorkExperience() {
    console.log("addWorkExperince function called")
    console.log(counter)

    let title = document.createElement("input");
    title.setAttribute("type", "text");
    title.setAttribute("name", "DYNAMICtitle"+counter);
    title.setAttribute("id", "DYNAMICtitle"+counter);
    title.setAttribute("placeholder", "Job Title");

    let company = document.createElement("input");
    company.setAttribute("type", "text");
    company.setAttribute("name", "DYNAMICcompany"+counter);
    company.setAttribute("id", "DYNAMICcompany"+counter);
    company.setAttribute("placeholder", "Company");

    let header = document.createElement("h2");
    header.innerHTML= "Work Experience";

    dynmaicFormDiv.appendChild(header);
    dynmaicFormDiv.appendChild(title);
    dynmaicFormDiv.appendChild(company);
    console.log("addWorkExperince function appended form into dynamic form div")
}

workExperienceBtn.onclick = function () {
    counter++;
    console.log(counter)
    addWorkExperience()
}