const dynmaicFormDiv = document.getElementById('createForm');
var workExperienceBtn = document.getElementById('addWE');
var educationBtn = document.getElementById('addEd');
var certificationBtn = document.getElementById('addCert');
var projectBtn = document.getElementById('addProj');
var workExpCount = 0;
var edCount = 0;
var certCount = 0;
var projCount = 0;

function addWorkExperience() {
    console.log("addWorkExperince function called")
    console.log(workExpCount)

    let title = document.createElement("input");
    title.setAttribute("type", "text");
    title.setAttribute("name", "WE"+workExpCount+"title");
    title.setAttribute("id", "WE"+workExpCount+"title");
    title.setAttribute("placeholder", "Job Title");

    let company = document.createElement("input");
    company.setAttribute("type", "text");
    company.setAttribute("name", "WE"+workExpCount+"company");
    company.setAttribute("id", "WE"+workExpCount+"company");
    company.setAttribute("placeholder", "Company");

    let header = document.createElement("h2");
    header.innerHTML= "Work Experience";

    dynmaicFormDiv.appendChild(header);
    dynmaicFormDiv.appendChild(title);
    dynmaicFormDiv.appendChild(company);
    console.log("addWorkExperince function appended form into dynamic form div");
}

function addEducation() {
    console.log("addEducation function called");
    let edHeading = document.createElement("h2");
    edHeading.innerHTML = "Education";

    dynmaicFormDiv.appendChild(edHeading);
    console.log("addEducation function appended form into dynamic form div");
}

function addCertification() {
    console.log("addCertification function called");
    let certHeading = document.createElement("h2");
    certHeading.innerHTML = "Certification";

    dynmaicFormDiv.appendChild(certHeading);
    console.log("addCertification function appended form into dynamic form div");
}

function addProjects() {
    console.log("addProjects function called");

    let heading = document.createElement("h2");
    heading.innerHTML = "Projects";

    dynmaicFormDiv.appendChild(heading);
    console.log("addProjects function appended form into dynamic form div");
}
workExperienceBtn.onclick = function () {
    workExpCount++;
    console.log("WorkExpCount = "+workExpCount);
    addWorkExperience();
}

educationBtn.onclick = function () {
    edCount++;
    console.log("edcount = "+ edCount)
    addEducation();
}

certificationBtn.onclick = () => {
    certCount++;
    console.log("certCount = " + certCount);
    addCertification();
}

projectBtn.onclick = () => {
    projCount++;
    console.log("projCount = " + projCount)
    addProjects();

}


