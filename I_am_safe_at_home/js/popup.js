let fillForm = document.getElementById('fillForm');

chrome.tabs.getSelected(null, function (tab) {
    console.log(tab.url);
});

fillForm.onclick = function (element) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { wjx: "fillIt" }, function (response) {
            if (response.status == 'done') {
                fillForm.innerText = '武汉加油 大家要乖';
            }
        });
    });
};