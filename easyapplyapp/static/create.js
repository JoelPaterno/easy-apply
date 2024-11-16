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
    title.setAttribute("name", "WE"+  workExpCount + "title");
    title.setAttribute("placeholder", "Job Title");

    let company = document.createElement("input");
    company.setAttribute("type", "text");
    company.setAttribute("name", "WE"+  workExpCount +"company");
    company.setAttribute("placeholder", "Company");

    let weLocation = document.createElement("input");
    weLocation.setAttribute("type", "text");
    weLocation.setAttribute("name", "WE"+  workExpCount +"location");
    weLocation.setAttribute("placeholder", "location");

    let weStartDate = document.createElement("input");
    weStartDate.setAttribute("type", "text");
    weStartDate.setAttribute("name", "WE"+  workExpCount +"startdate");
    weStartDate.setAttribute("placeholder", "startdate");
    
    let weEndDate = document.createElement("input");
    weEndDate.setAttribute("type", "text");
    weEndDate.setAttribute("name", "WE"+  workExpCount +"enddate");
    weEndDate.setAttribute("placeholder", "enddate");

    let weResponsibilities = document.createElement("textarea")
    weResponsibilities.setAttribute("name", "WE" + workExpCount + "responsibil")
    weResponsibilities.setAttribute("placeholder", "responsibilities")

    let weSummary = document.createElement("textarea")
    weSummary.setAttribute("name", "WE" + workExpCount + "summary")
    weSummary.setAttribute("placeholder", "summary")

    let header = document.createElement("h2");
    header.innerHTML= "Work Experience";

    dynmaicFormDiv.appendChild(header);
    dynmaicFormDiv.appendChild(title);
    dynmaicFormDiv.appendChild(company);
    dynmaicFormDiv.appendChild(weLocation);
    dynmaicFormDiv.appendChild(weStartDate);
    dynmaicFormDiv.appendChild(weEndDate);
    dynmaicFormDiv.appendChild(weSummary);
    dynmaicFormDiv.appendChild(weResponsibilities);
    console.log("addWorkExperince function appended form into dynamic form div");
}

function addEducation() {
    console.log("addEducation function called");

    let edHeading = document.createElement("h2");
    edHeading.innerHTML = "Education";

    let institution = document.createElement("input");
    institution.setAttribute("type", "text");
    institution.setAttribute("name", "ED" + edCount + "institution");
    institution.setAttribute("placeholder", "Institution");

    let edLocation = document.createElement("input");
    edLocation.setAttribute("type", "text");
    edLocation.setAttribute("name", "ED" + edCount + "location");
    edLocation.setAttribute("placeholder", "Location");

    let edDegree = document.createElement("input");
    edDegree.setAttribute("type", "text");
    edDegree.setAttribute("name", "ED" + edCount + "degree");
    edDegree.setAttribute("placeholder", "degree");

    let edDate = document.createElement("input");
    edDate.setAttribute("type", "text");
    edDate.setAttribute("name", "ED" + edCount + "date");
    edDate.setAttribute("placeholder", "date");
    
    dynmaicFormDiv.appendChild(edHeading);
    dynmaicFormDiv.appendChild(edDegree);
    dynmaicFormDiv.appendChild(institution);
    dynmaicFormDiv.appendChild(edLocation);
    dynmaicFormDiv.appendChild(edDate);

    console.log("addEducation function appended form into dynamic form div");
}

function addCertification() {
    console.log("addCertification function called");

    let certHeading = document.createElement("h2");
    certHeading.innerHTML = "Certification";

    let certTitle = document.createElement("input");
    certTitle.setAttribute("type", "text");
    certTitle.setAttribute("name", "CT" + certCount + "title");
    certTitle.setAttribute("placeholder", "Title");


    let certIssuer = document.createElement("input");
    certIssuer.setAttribute("type", "text");
    certIssuer.setAttribute("name", "CT" + certCount + "issuer");
    certIssuer.setAttribute("placeholder", "Issuer");


    let certDate = document.createElement("input");
    certDate.setAttribute("type", "text");
    certDate.setAttribute("name", "CT" + certCount + "date");
    certDate.setAttribute("placeholder", "Date");


    dynmaicFormDiv.appendChild(certHeading);
    dynmaicFormDiv.appendChild(certTitle);
    dynmaicFormDiv.appendChild(certIssuer);
    dynmaicFormDiv.appendChild(certDate);

    console.log("addCertification function appended form into dynamic form div");
}

function addProjects() {
    console.log("addProjects function called");

    let heading = document.createElement("h2");
    heading.innerHTML = "Projects";

    let projTitle = document.createElement("input");
    projTitle.setAttribute("type", "text");
    projTitle.setAttribute("name", "PJ" + projCount + "title");
    projTitle.setAttribute("placeholder", "Title");

    let projDescription = document.createElement("input");
    projDescription.setAttribute("type", "text");
    projDescription.setAttribute("name", "PJ" + projCount + "description");
    projDescription.setAttribute("placeholder", "Description");

    let projURL = document.createElement("input");
    projURL.setAttribute("type", "text");
    projURL.setAttribute("name", "PJ" + projCount + "url");
    projURL.setAttribute("placeholder", "URL");

    let projDate = document.createElement("input");
    projDate.setAttribute("type", "text");
    projDate.setAttribute("name","PJ" + projCount + "date");
    projDate.setAttribute("placeholder", "Date");

    dynmaicFormDiv.appendChild(heading);
    dynmaicFormDiv.appendChild(projTitle);
    dynmaicFormDiv.appendChild(projDescription);
    dynmaicFormDiv.appendChild(projURL);
    dynmaicFormDiv.appendChild(projDate);

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