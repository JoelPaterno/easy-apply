const dynmaicFormDiv = document.getElementById('dynamicForm');
function addWorkExperience() {
    let newform = document.createElement('form');
    newform.setAttribute('method', 'post');

    var header2 = document.createElement("h2");
    header2.innerHTML("Work Experience");

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

    newform.appendChild(header2);
    newform.appendChild(title);
    newform.appendChild(company);
    newform.appendChild(submit);
    dynmaicFormDiv.appendChild(newform)
}