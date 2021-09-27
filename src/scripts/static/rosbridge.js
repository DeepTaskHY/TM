'use strict'

$(document).ready(() => {
    var submitMessage = (message = {}, mine = true) => {
        var $wrap = $('#dialog-wrap')

        var $example = $wrap
            .find('.dialog-example')

        var $dialog = $example.clone()
            .removeClass('dialog-example visually-hidden')
            .appendTo($wrap)

        var $dialogOutputWrap = $dialog
            .children('.dialog-output')

        var $dialogOutput = $dialogOutputWrap
            .children('button')

        var $dialogDetailWrap = $dialog
            .children('.dialog-detail')

        var $dialogDetail = $dialogDetailWrap
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
        var id = $wrap.children('.dialog').length - 1
        var detailName = $dialogOutput.attr('aria-controls')
        var detailId = `${detailName}-${id}`

        $dialogOutput
            .attr('data-bs-target', `#${detailId}`)
            .attr('aria-controls', detailId)

        $dialogDetailWrap
            .attr('id', detailId)

        // Set message
        var header = message['header']
        var contentName = header['content']
        var content = message[contentName]

        if (mine)
            $dialogOutput
                .text(content['human_speech'])
        else
            $dialogOutput
                .text(content['dialog'])

        var $messageWrap = $('<pre/>')
            .text(JSON.stringify(message, null, 2))

        $dialogDetail.append($messageWrap)

        // Set scroll position
        $wrap.scrollTop($wrap.prop('scrollHeight'))

        return $dialog
    }


    var dialogNamespace = io('/dialog')

    $('#input-form').on('submit', (e) => {
        e.preventDefault()

        var data = $(e.currentTarget).serializeObject()
        var header = data['header']
        var contentName = header['content']
        delete data['header']

        var message = {
            'header': header,
            [contentName]: data
        }

        // Publish
        dialogNamespace.emit('publish', {'data': JSON.stringify(message)})
        submitMessage(message, true)
    })

    dialogNamespace.on('subscribe', (data) => {
        var message = JSON.parse(data['data'])

        // Print message
        submitMessage(message, false)

        // Increase message ID
        $('#id').val((i, val) => { return ++val })
    })


    var recognitionNamespace = io('/recognition')

    recognitionNamespace.on('face_id', (data) => {
        console.log(data)
    })

    recognitionNamespace.on('image_raw', (data) => {
        const can = $('#face')[0]
        can.width = data.width
        can.height = data.height
        const ctx = can.getContext('2d')

        const imgData = ctx.createImageData(data.width, data.height)
        const inData = atob(data.data)
        const rawData = data.data

        var i = 4, j = 0

        while (j < inData.length) {
            const w1 = inData.charCodeAt(j++)
            const w2 = inData.charCodeAt(j++)
            const w3 = inData.charCodeAt(j++)

            if (!imgMes.is_bigendian) {
                rawData[i++] = w3 // blue
                rawData[i++] = w2 // green
                rawData[i++] = w1 // red
            }
            else {
                rawData[i++] = (w1 >> 8) + ((w1 & 0xFF) << 8)
                rawData[i++] = (w2 >> 8) + ((w2 & 0xFF) << 8)
                rawData[i++] = (w3 >> 8) + ((w3 & 0xFF) << 8)
            }

            rawData[i++] = 255  // alpha
        }

        ctx.putImageData(imgData, 0, 0)
    })
})
