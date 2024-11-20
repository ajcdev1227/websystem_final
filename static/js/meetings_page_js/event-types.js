(function () {
    'use strict'

    /**
     * Creates a slug from text
     * @param {string} str The text
     * @returns {string} The slug
     */
    function slugify(str) {
      return String(str)
        .normalize('NFKD') // split accented characters into their base characters and diacritical marks
        .replace(/[\u0300-\u036f]/g, '') // remove all the accents, which happen to be all in the \u03xx UNICODE block.
        .trim() // trim leading or trailing whitespace
        .toLowerCase() // convert to lowercase
        .replace(/[^a-z0-9 -]/g, '') // remove non-alphanumeric characters
        .replace(/\s+/g, '-') // replace spaces with hyphens
        .replace(/-+/g, '-'); // remove consecutive hyphens
    }

    PetiteVue.createApp({
        createEventTypeError: undefined,
        isCreatingEventType: false,
        newEventTypeTitle: '',
        newEventTypeSlug: '', // TODO Autogenerate slug as title is typed
        newEventTypeLocation: '',
        newEventTypeDescription: '',
        newEventTypeDuration: 15,

        async createEventType() {
            try {
                console.log("trying to create event")
                this.createEventTypeError = undefined
                this.isCreatingEventType = true

                const {slug} = await apiPost('/meetings/api/event-type', undefined, {
                    title: this.newEventTypeTitle,
                    slug: this.newEventTypeSlug,
                    location: this.newEventTypeLocation,
                    description: this.newEventTypeDescription,
                    duration: parseInt(this.newEventTypeDuration),
                })

                window.location.assign('/meetings/type/' + slug + '/')
            } catch (err) {
                console.error('Failed to create event type:', err)
                this.createEventTypeError = err.apiMessage ?? err.message ?? String(err)
            } finally {
                this.isCreatingEventType = false
            }
        },

        /**
         * @param {InputEvent} event
         */
        handleNewEventTypeTitleInput(event) {
            this.newEventTypeTitle = event.target.value
            this.newEventTypeSlug = slugify(this.newEventTypeTitle)
        },

        mounted() {

        }
    }).mount('body')
})()
