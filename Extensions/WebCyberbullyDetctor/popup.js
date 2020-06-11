
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("hideButton").addEventListener("click", hideStuff);
    document.getElementById("redactButton").addEventListener("click", redactStuff);
    document.getElementById("restoreButton").addEventListener("click", restoreStuff);
    document.getElementById("imageButton").addEventListener("click", hideImages);
  });

function hideStuff(){
    document.getElementById("hideButton").style.backgroundColor = 'red';
    document.getElementById("redactButton").style.backgroundColor = 'white';
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        var activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, {"message": "hide"});
       });
}

function redactStuff(){
    document.getElementById("redactButton").style.backgroundColor = 'red';
    document.getElementById("hideButton").style.backgroundColor = 'white';
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        var activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, {"message": "redact"});
       });
}

function restoreStuff(){
    document.getElementById("hideButton").style.backgroundColor = 'white';
    document.getElementById("imageButton").style.backgroundColor = 'white';
    document.getElementById("redactButton").style.backgroundColor = 'white';
    document.getElementById("restoreButton").style.backgroundColor = 'white';
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        var activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, {"message": "restore"});
       });
}

function hideImages(){
    
    document.getElementById("imageButton").style.backgroundColor = 'red';
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        var activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, {"message": "image"});
       });
}