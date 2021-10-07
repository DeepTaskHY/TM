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

        // Set message
        const header = message['header']
        const contentName = header['content']
        const content = message[contentName]

        if (mine)
            $dialogOutput
                .text(content['human_speech'])
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


    const addBGR8toCanvas = (canvas, bgr8) => {
        canvas.width = bgr8.width
        canvas.height = bgr8.height

        const ctx = canvas.getContext('2d')
        const imgData = ctx.createImageData(bgr8.width, bgr8.height)
        const inData = atob(bgr8.data)
        const rawData = imgData.data

        var i = 4, j = 0

        while (j < inData.length) {
            let w1 = inData.charCodeAt(j++)
            let w2 = inData.charCodeAt(j++)
            let w3 = inData.charCodeAt(j++)

            if (!bgr8.is_bigendian) {
                rawData[i++] = w3  // blue
                rawData[i++] = w2  // green
                rawData[i++] = w1  // red
            }
            else {
                rawData[i++] = (w1 >> 8) + ((w1 & 0xFF) << 8)
                rawData[i++] = (w2 >> 8) + ((w2 & 0xFF) << 8)
                rawData[i++] = (w3 >> 8) + ((w3 & 0xFF) << 8)
            }

            rawData[i++] = 255  // alpha
        }

        ctx.putImageData(imgData, 0, 0)
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

    visionNamespace.on('image_raw', (data) => {
        const canvas = $('#face')[0]
        addBGR8toCanvas(canvas, data)
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
