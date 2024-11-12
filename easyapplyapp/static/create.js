const dynmaicFormDiv = document.getElementById('dynamicForm');
function addWorkExperience() {
    console.log("addWorkExperince function called")
    let newform = document.createElement('form');
    newform.setAttribute('method', 'post');

    var title = document.createElement("input");
    title.setAttribute("type", "text");
    title.setAttribute("name", "Title");
    title.setAttribute("placeholder", "Job Title");

    var company = document.createElement("input");
    company.setAttribute("type", "text");
    company.setAttribute("name", "company");
    company.setAttribute("placeholder", "Company");

    let submit = document.createElement('input');
    submit.setAttribute('type', 'submit');
    submit.setAttribute('value', 'Submit');

    var header = document.createElement("h2");
    header.innerHTML= "Work Experience";

    newform.appendChild(title);
    newform.appendChild(company);
    newform.appendChild(submit);
    dynmaicFormDiv.appendChild(header)
    dynmaicFormDiv.appendChild(newform)
    console.log("addWorkExperince function appended form into dynamic form div")
}