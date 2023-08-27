class FormSubjectSelector {
    constructor(subjectsNames) {
        this.subjectsNames = subjectsNames;
        this.subjectIdInt = 0;
    }

    createSelector = (selectedSubject, onChangeFunction) => {
        if (onChangeFunction === null) {
            onChangeFunction = this.chooseSubject;
        }
        
        const div_subjects = document.getElementById("subjects-selection-div");
    
        this.subjectIdInt++;

        let new_select = document.createElement('select');
        new_select.id = 'subject'.concat(this.subjectIdInt.toString());
        new_select.classList.add('form-select', 'form-select-sm', 'mb-3');
        new_select.name = 'subject'.concat(this.subjectIdInt.toString());
        new_select.setAttribute('form', 'noteform');
        new_select.onchange = onChangeFunction;

        let option = document.createElement('option');
        option.value = 'none';
        option.innerHTML= 'Choose subject';
        if (selectedSubject == 'none') {
            option.setAttribute('selected', true);
        }
        new_select.appendChild(option);

        this.subjectsNames.forEach((subject) => {
            name = subject['name'];
            option = document.createElement('option');
            option.value = name;
            option.innerHTML= name;
            if (selectedSubject == name) {
                option.setAttribute('selected', true);
            }
            new_select.appendChild(option);        
        });
        
        let div = document.createElement('div');
        div.id = 'subject_div'.concat(this.subjectIdInt.toString());
        div.appendChild(new_select);
        div_subjects.appendChild(div);
    }

    chooseSubject = (event) => {
        this.createSelector('none', null);    
        event.currentTarget.onchange = this.changeSubject;
    }

    changeSubject = (event) => {
        if (event.currentTarget.value == 'none') {
            event.currentTarget.parentElement.remove();
        }
    }
}

class NewSubjectFieldCreator {
    constructor(parent_id, id_number, html_template) {
        this.parent_id = parent_id;
        this.html_template = html_template;
        this.id_number = id_number;
    }

    additionalSubject = (event) => {
        const parent = document.getElementById(this.parent_id)
        const replace = this.parent_id + '-\\d+';
        const regex = new RegExp(replace,"g");
        const inner = this.html_template.replaceAll(
            regex,
            this.parent_id + '-' + this.id_number
        );

        let li = document.createElement('li');
        li.innerHTML = inner;

        parent.appendChild(li);

        this.id_number = (Number(this.id_number) + 1).toString();
    }

}