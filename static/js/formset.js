$(document).ready(function () {
    $('.add-form').click(function () {
        cloneForm($(this).data('form-prefix'));
    });

    $('.remove-form').click(function () {
        removeForm($(this).data('form-prefix'));
    });

    function cloneForm(formPrefix) {
        const formContainer = $('.form-container').last();
        const totalForms = parseInt($('#id_' + formPrefix + '-TOTAL_FORMS').val());
        const newForm = formContainer.clone();

        newForm.find('input').val('');
        newForm.find('select').val('');
        newForm.find('input[type="hidden"]').remove();
        newForm.find('label.error').remove();

        formContainer.after(newForm);

        newForm.find('input, select').each(function () {
            updateFormElementIndex($(this), formPrefix, totalForms);
        });

        $('#id_' + formPrefix + '-TOTAL_FORMS').val(totalForms + 1);
    }

    function removeForm(formPrefix) {
        const formContainer = $('.form-container');
        if (formContainer.length > 1) {
            formContainer.last().remove();
            updateFormIndex(formPrefix);
        }
    }

    function updateFormElementIndex(elem, formPrefix, formIndex) {
        const idRegex = new RegExp(formPrefix + '-(\\d+|__prefix__)-');
        const replacement = formPrefix + '-' + formIndex + '-';
        elem.attr('id', elem.attr('id').replace(idRegex, replacement));
        elem.attr('name', elem.attr('name').replace(idRegex, replacement));
        elem.attr('for', elem.attr('for').replace(idRegex, replacement));
    }

    function updateFormIndex(formPrefix) {
        const formContainer = $('.form-container');
        formContainer.each(function (index) {
            $(this).find('input, select').each(function () {
                updateFormElementIndex($(this), formPrefix, index);
            });
        });
        $('#id_' + formPrefix + '-TOTAL_FORMS').val(formContainer.length);
    }
});