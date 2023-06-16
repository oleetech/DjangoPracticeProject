$(document).ready(function() {
    updateExtraValue();

    $('.add-form').click(function() {
        cloneForm($(this).data('form-prefix'));
        updateExtraValue();
    });

    $('.remove-form').click(function() {
        removeForm($(this).data('form-prefix'));
        updateExtraValue();
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

        newForm.find('input, select').each(function() {
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
        formContainer.each(function(index) {
            $(this).find('input, select').each(function() {
                updateFormElementIndex($(this), formPrefix, index);
            });
        });
        $('#id_' + formPrefix + '-TOTAL_FORMS').val(formContainer.length);
    }
    
    function updateExtraValue() {
        const formContainer = $('.form-container');
        const extraValue = Math.max(formContainer.length - 1, 1); // Calculate the new extra value
        const formPrefix = formContainer.first().find('input, select').first().attr('name').split('-')[0];
        $('#id_' + formPrefix + '-TOTAL_FORMS').val(extraValue);
    }
});


$(document).ready(function() {
    // Update the extra value based on the initial form count
    var extraValue = Math.max($('#formset-container .form-container').length - 1, 0);
    $('#id_extra_value').val(extraValue);
    
    // Rest of your JavaScript code
    // ...
  });