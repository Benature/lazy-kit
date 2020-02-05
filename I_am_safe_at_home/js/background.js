chrome.runtime.onInstalled.addListener(function () {
    chrome.storage.sync.set({ color: '#3aa757' }, function () {
        console.log("The color is green.");
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function () {
        chrome.declarativeContent.onPageChanged.addRules([{
            conditions: [
                new chrome.declarativeContent.PageStateMatcher({
                    pageUrl: { urlContains: 'wjx.cn' },
                })
            ],
            actions: [new chrome.declarativeContent.ShowPageAction()]
        }]);
    });
});


// default setting
var config_default = [
    {
        type: 'text',
        label: '姓名',
        content: '张三',
    },
    {
        type: 'text',
        label: '学号',
        content: '99999999'
    },
    {
        type: 'text',
        label: '年级、班级',
        content: '2017级‐2班'
    },
    {
        type: 'select',
        label: '有无异样',
        content: '无'
    },
    {
        type: 'select',
        label: '居住地',
        content: '家'
    },
];