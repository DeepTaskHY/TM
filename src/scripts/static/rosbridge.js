'use strict'

$(document).ready(() => {
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


    const planningNamespace = io('/planning')

    planningNamespace.on('dialog_generation', (data) => {
        const message = data['data']

        // Print message
        printDialog(message, true)
    })


    const dialogNamespace = io('/dialog')

    dialogNamespace.on('subscribe', (data) => {
        const message = data['data']

        // Print message
        printDialog(message, false)

        // Increase message ID
        $('#id').val((i, val) => { return ++val })
    })


    const visionNamespace = io('/vision')

    visionNamespace.on('image_raw', (data) => {
        const can = $('#face')[0]
        can.width = data.width
        can.height = data.height
        const ctx = can.getContext('2d')

        const imgData = ctx.createImageData(data.width, data.height)
        const inData = atob(data.data)
        const rawData = imgData.data

        var i = 4, j = 0

        while (j < inData.length) {
            let w1 = inData.charCodeAt(j++)
            let w2 = inData.charCodeAt(j++)
            let w3 = inData.charCodeAt(j++)

            if (!data.is_bigendian) {
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


    const speechNamespace = io('/speech')

    $('#recorder-on').on('click', () => {
        speechNamespace.emit('record', {data: true})
    })

    $('#recorder-off').on('click', () => {
        speechNamespace.emit('record', {data: false})
    })
})
