chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log(request.options.message);
    var data = 'urls='+request.options.message+'&modelId=4df5e7ba-e1e4-4e5b-9eb2-10ea96c465f3';
    postData("https://app.nanonets.com/api/v2/ImageCategorization/LabelUrls/", data)
    .then((responseText)=>{
        chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
            var activeTab = tabs[0];
            chrome.tabs.sendMessage(activeTab.id, {
            "message": "imagesent",
            "image": request.options.message, 
            "state": responseText["result"][0]["prediction"][0]["label"],
            "i": request.options.i
        });
           })
        
        
        })
});

async function postData(url = '', data) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: 'POST', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'authorization': "Basic " + btoa("3lWlxT6SbjLIm-60Jxvb-tjPCICer6UM:"),
      },
      redirect: 'follow', // manual, *follow, error
      referrerPolicy: 'no-referrer', // no-referrer, *client
      body: data // body data type must match "Content-Type" header
    });
    return await response.json(); // parses JSON response into native JavaScript objects
  }
  
console.log('background running') 