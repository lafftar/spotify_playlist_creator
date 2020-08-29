chrome.extension.sendMessage({}, function (response) {
    var readyStateCheckInterval = setInterval(function () {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);

            // ----------------------------------------------------------
            // This part of the script triggers when page is done loading
            async function start() {
                console.log("Hello. This message was sent from scripts/inject.js");
                $('ytd-menu-renderer.ytd-playlist-sidebar-primary-info-renderer > yt-icon-button:nth-child(2)').click();
                await this.sleep(500);
                $('#items > ytd-menu-service-item-renderer:nth-child(1) > paper-item > yt-formatted-string').click();
                await this.sleep(1500)
                var i_frame = $('.picker-frame').contentWindow.document;
                var theButton = i_frame.querySelector("#\\:6 > div");
                var box = theButton.getBoundingClientRect(),
                    coordX = box.left + (box.right - box.left) / 2,
                    coordY = box.top + (box.bottom - box.top) / 2;
                simulateMouseEvent(theButton, "mousedown", coordX, coordY);
                simulateMouseEvent(theButton, "mouseup", coordX, coordY);
                simulateMouseEvent(theButton, "click", coordX, coordY);
                var url_box = i_frame.getElementsByTagName('input')[0];
                url_box.sendkeys('https://youtube.com/watch?v=M94bXPxpAes{enter}')
                console.log("Done!");
            }

            start();
            // ----------------------------------------------------------

        }
    }, 10);
});

function getElementByXpath(path) {
    return document.evaluate(path, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function simulateMouseEvent(element, eventName, coordX, coordY) {
    element.dispatchEvent(new MouseEvent(eventName, {
        view: window,
        bubbles: true,
        cancelable: true,
        clientX: coordX,
        clientY: coordY,
        button: 0
    }));
}
