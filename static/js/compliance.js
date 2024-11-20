// @ts-check

;(function () {
    'use strict'

    /** @type {HTMLFormElement} */
    const rejectForm = document.getElementById('reject-form')
    /** @type {HTMLInputElement} */
    const rejectFormCaseUuid = document.getElementById('reject-form-case-uuid')
    /** @type {HTMLButtonElement} */
    const rejectFormClose = document.getElementById('reject-form-close')
    /** @type {HTMLInputElement} */
    const rejectFormSubmit = document.getElementById('reject-form-submit')

    // Reset form state
    rejectFormClose.disabled = false
    rejectFormSubmit.disabled = false
    rejectFormSubmit.value = rejectFormSubmit.dataset.labelDefault

    // Hook up form handlers
    rejectForm.addEventListener('submit', function () {
        rejectFormClose.disabled = true
        // Prevent double-clicking
        rejectFormSubmit.disabled = true

        rejectFormSubmit.value = rejectFormSubmit.dataset.labelSubmitting
    })

    /**
     * Opens the reject modal and sets it up for a specific case UUID
     * @param {string} caseUuid The case's UUID
     * @returns {void}
     */
    function openRejectModal(caseUuid) {
        rejectFormCaseUuid.value = caseUuid

        $('#reject-modal').modal('show')
    }

    window.openRejectModal = openRejectModal
})()

;(function () {
    'use strict'

    /** @type {HTMLPreElement} */
    const rejectReasonText = document.getElementById('reject-reason-text')
    /** @type {HTMLElement} */
    const rejectReasonPlaceholder = document.getElementById('reject-reason-placeholder')

    /**
     * Opens the reject reason modal and displays the provided text.
     * If the text is empty, a placeholder message will be shown.
     *
     * The text must be URL-encoded.
     * @param {string | ''} text The URL-encoded text, or empty to show a default message
     * @returns {void}
     */
    function openRejectReasonModal(text) {
        if (text) {
            rejectReasonText.innerText = decodeURIComponent(text)
            rejectReasonText.style.display = 'block'
            rejectReasonPlaceholder.style.display = 'none'
        } else {
            rejectReasonText.innerText = ''
            rejectReasonText.style.display = 'none'
            rejectReasonPlaceholder.style.display = 'block'
        }

        $('#reject-reason-modal').modal('show')
    }

    window.openRejectReasonModal = openRejectReasonModal
})()
