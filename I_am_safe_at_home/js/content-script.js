console.log('武汉加油')

chrome.extension.onMessage.addListener(function (request, sender, sendMessage) {
    if (request.wjx == "fillIt") {
        var config = request.data;
        let fields = document.getElementsByClassName('field');
        for (let i = 0; i < fields.length; i++) {
            let label = fields[i].getElementsByClassName('field-label')[0].innerText;
            let input = fields[i].getElementsByTagName('input');
            for (let j = 0; j < config.length; j++) {
                let cf = config[j];
                if (label.indexOf(cf.label) != -1) {
                    // 找到对应配置
                    if (cf.type == 'text') {
                        input[0].value = cf.content;
                    } else if (cf.type == 'select') {
                        let a = fields[i].getElementsByTagName('a');
                        for (let k = 0; k < input.length; k++) {
                            if (input[k].innerText.indexOf(cf.content)) {
                                // 勾选
                                input[k].checked = true;
                                // 样式显示勾选状态（免得心慌）
                                a[k].setAttribute('class', 'jqradio jqchecked')
                                break;
                            }
                        }
                    }
                }
            }
        }
        console.log('武汉加油 ヾ(◍°∇°◍)ﾉﾞ')
        sendMessage({ status: 'done' });
    } else if (request.mwg == "jump2github") {
        let url = 'https://github.com/Benature/lazy-kit/tree/master/I_am_safe_at_home';
        console.log(url)
        window.location.href = url
        sendMessage({ status: 'done' });
    }
    else {
        sendMessage("failed");
    }
});
