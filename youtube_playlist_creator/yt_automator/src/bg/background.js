// if you checked "fancy-settings" in extensionizr.com, uncomment this lines

// var settings = new Store("settings", {
//     "sample_setting": "This is how you use Store.js to remember values"
// });


//example of using a message handler from the inject scripts
chrome.extension.onMessage.addListener(
  function(request, sender, sendResponse) {
  	chrome.pageAction.show(sender.tab.id);
    sendResponse();
  });

injectScripts(["src/bg/jquery.js", "src/bg/billiteRange.js", "src/bg/sendkeys.js"]);

function injectScripts(scripts, callback) {
  if(scripts.length) {
    var script = scripts.shift();
    chrome.tabs.executeScript({file: script}, function() {
      if(chrome.runtime.lastError && typeof callback === "function") {
        callback(false); // Injection failed
      }
      injectScripts(scripts, callback);
    });
  } else {
    if(typeof callback === "function") {
      callback(true);
    }
  }
}