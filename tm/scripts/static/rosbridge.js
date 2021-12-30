'use strict'


$(document).ready(() => {
    const printDialogDetails = (message = {}) => {
        // Get jQuery objects
        const $id = $('#id')
        const $intent = $('#intent')
        const $human_speech = $('#human_speech')
        const $sc = $('#social_context')

        // Get message details
        const header = message['header']
        const contentName = header['content']
        const content = message[contentName]
        const sc = JSON.stringify(content['social_context'], null, 2)

        // Set message details
        $id.val(header['id'])
        $intent.val(content['intent'])
        $human_speech.val(content['human_speech'])
        $sc.val(sc)
    }


    const printDialog = (message = {}, mine = true) => {
        // Set message
        const header = message['header']
        const contentName = header['content']
        const content = message[contentName]

        if (!content[mine && 'human_speech' || 'dialog'])
            return null

        console.log(message)

        const $wrap = $('#dialog-wrap')

        const $example = $wrap
            .find('.dialog-example')

        const $dialog = $example.clone()
            .removeClass('dialog-example visually-hidden')
            .appendTo($wrap)

        const $dialogOutputWrap = $dialog
            .children('.dialog-output')

        const $dialogOutput = $dialogOutputWrap
            .children('button')

        const $dialogDetailWrap = $dialog
            .children('.dialog-detail')

        const $dialogDetail = $dialogDetailWrap
            .children('.card')

        const $humanSpeech = $('#human_speech')

        // Set class style
        if (mine) {
            $dialogOutputWrap
                .addClass('justify-content-start')

            $dialogOutput
                .addClass('btn-primary')
        }
        else {
            $dialogOutputWrap
                .addClass('justify-content-end')

            $dialogOutput
                .addClass('btn-dark')
        }

        // Set dialog detail ID
        const id = $wrap.children('.dialog').length - 1
        const detailName = $dialogOutput.attr('aria-controls')
        const detailId = `${detailName}-${id}`

        $dialogOutput
            .attr('data-bs-target', `#${detailId}`)
            .attr('aria-controls', detailId)

        $dialogDetailWrap
            .attr('id', detailId)

        if (mine) {
            $humanSpeech
                .val('')

            $dialogOutput
                .text(content['human_speech'])
        }
        else
            $dialogOutput
                .text(content['dialog'])

        const $messageWrap = $('<pre/>')
            .text(JSON.stringify(message, null, 2))

        $dialogDetail.append($messageWrap)

        // Set scroll position
        $wrap.scrollTop($wrap.prop('scrollHeight'))

        return $dialog
    }


    const getCompressedImage = (data) => {
        return `data:image/${data['format']};base64,${data['data']}`
    }


    const planningNamespace = io('/planning')

    planningNamespace.on('dialog_generation', (data) => {
        const message = data['data']

        // Print message details
        printDialogDetails(message)

        // Print message
        printDialog(message, true)
    })


    const dialogNamespace = io('/dialog')

    dialogNamespace.on('subscribe', (data) => {
        const message = data['data']

        // Print message
        printDialog(message, false)
    })


    const visionNamespace = io('/vision')

    visionNamespace.on('image', (data) => {
        $('#face').attr('src', getCompressedImage(data))
    })


    const speechNamespace = io('/speech')

    $('#input-form').on('submit', (e) => {
        e.preventDefault()

        // Increase message ID
        $('#id').val((i, val) => { return ++val })

        // Get form data
        const data = $(e.currentTarget).serializeObject()
        const message = {id: parseInt(data['id']), stt: data['human_speech']}

        // Publish to speech
        speechNamespace.emit('speech', {data: message})
    })

    $('#recorder-on').on('click', () => {
        speechNamespace.emit('record', {data: true})
    })

    $('#recorder-off').on('click', () => {
        speechNamespace.emit('record', {data: false})
    })
})
