let subject_id_inc = 0;


function changeSubject(event) {
    if (event.currentTarget.value == 'none') {
        event.currentTarget.parentElement.remove();
    }
}


function chooseSubject(event) {
    event.currentTarget.onchange = changeSubject;
    const div_subjects = document.getElementById("subjects-selection-div");

    subject_id_inc++;

    const new_element = event.currentTarget.cloneNode(true);
    new_element.id = 'subject'.concat(subject_id_inc.toString());
    new_element.class = "form-select form-select-sm mb-3";
    new_element.name = 'subject'.concat(subject_id_inc.toString());

    let div = document.createElement('div');
    div.id = 'subject_div'.concat(subject_id_inc.toString());
    div.appendChild(new_element);
    div_subjects.appendChild(div);
}