let fillForm = document.getElementById('fillForm');

chrome.tabs.getSelected(null, function (tab) {
    console.log(tab.url);
});

// var config;
fillForm.onclick = function (element) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.storage.sync.get('config', function (data) {
            var config = data.config;
            console.log(config)
            chrome.tabs.sendMessage(tabs[0].id, {
                wjx: "fillIt",
                data: config,
            }, function (response) {
                if (response.status == 'done') {
                    fillForm.innerText = '武汉加油💪';
                }
            });
        });
    });
};