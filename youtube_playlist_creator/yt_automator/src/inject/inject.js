chrome.extension.sendMessage({}, function (response) {
    var readyStateCheckInterval = setInterval(function () {
        if (document.readyState === "complete") {
            clearInterval(readyStateCheckInterval);

            // ----------------------------------------------------------
            // This part of the script triggers when page is done loading
            async function start() {
                var simulateMouseEvent = function (element, eventName, coordX, coordY) {
                    element.dispatchEvent(new MouseEvent(eventName, {
                        view: window,
                        bubbles: true,
                        cancelable: true,
                        clientX: coordX,
                        clientY: coordY,
                        button: 0
                    }));
                };
                console.log("Hello. This message was sent from scripts/inject.js");
                document.querySelector('ytd-menu-renderer.ytd-playlist-sidebar-primary-info-renderer > yt-icon-button:nth-child(2)').click();
                await this.sleep(500);
                document.querySelector('#items > ytd-menu-service-item-renderer:nth-child(1) > paper-item > yt-formatted-string').click();
                var iframe = document.getElementsByTagName('iframe')[1];
                var theButton = document.querySelector("#\\:6 > div");
                var box = theButton.getBoundingClientRect(),
                    coordX = box.left + (box.right - box.left) / 2,
                    coordY = box.top + (box.bottom - box.top) / 2;
                simulateMouseEvent(theButton, "mousedown", coordX, coordY);
                simulateMouseEvent(theButton, "mouseup", coordX, coordY);
                simulateMouseEvent(theButton, "click", coordX, coordY);
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