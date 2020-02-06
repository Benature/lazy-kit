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
        content: '9999'
    },
    {
        type: 'text',
        label: '年级、班级',
        content: '2017级‐2班'
    },
    // {
    //     type: 'select',
    //     label: '有无异样',
    //     content: '无'
    // },
    // {
    //     type: 'select',
    //     label: '居住地',
    //     content: '家'
    // },
];

// Saves options to chrome.storage
function save_options() {
    // 收集数据
    var trs = document.getElementsByTagName('tr');
    var configs = new Array();
    // 从 1 开始，跳过 th
    for (var i = 1; i < trs.length; i++) {
        let tds = trs[i].getElementsByTagName('td');
        configs.push({
            type: tds[0].innerText,
            label: tds[1].innerText,
            content: tds[2].getElementsByTagName('input')[0].value,
        })
    }
    console.log(configs)
    // var color = document.getElementById('color').value;
    // var likesColor = document.getElementById('like').checked;
    chrome.storage.sync.set({
        config: configs,
    }, function () {
        // Update status to let user know options were saved.
        var status = document.getElementById('status');
        status.textContent = '配置已更新👌';
        setTimeout(function () {
            status.textContent = '';
        }, 750);
    });
}

document.getElementById('save').addEventListener('click', save_options);

function drawTable() {
    chrome.storage.sync.get({
        config: config_default,
    }, function (items) {
        var conf = items.config;
        var tbody = document.getElementById('tbMain');
        tbody.appendChild(getDataRow({ label: '关键词', content: '自动填充内容', type: null }, 'th'));

        for (var i = 0; i < conf.length; i++) {
            var trow = getDataRow(conf[i]);
            tbody.appendChild(trow);
        }
    });
    chrome.storage.sync.get('config', function (data) {
        config = data.config;
        console.log(config)
        console.log(data)
    });
}


function getDataRow(data, tag = 'td') {
    var row = document.createElement('tr'); //创建行

    // TODO: 选择输入类型
    var cell1 = document.createElement('td');
    cell1.innerHTML = data.type;
    cell1.setAttribute('hidden', true);
    row.appendChild(cell1);

    // label
    let cell2 = document.createElement(tag);
    cell2.innerHTML = data.label;
    row.appendChild(cell2);

    // input
    let cell3 = document.createElement(tag);
    if (tag == 'th') {
        cell3.innerText = data.content;
    } else {
        let input = document.createElement('input');
        input.setAttribute('type', 'text');
        input.setAttribute('value', data.content);
        cell3.appendChild(input);
    }
    row.appendChild(cell3);



    // TODO: 删除按钮
    // var delCell = document.createElement('td');//创建第四列，操作列
    // row.appendChild(delCell);
    // var btnDel = document.createElement('input'); //创建一个input控件
    // btnDel.setAttribute('type', 'button'); //type="button"
    // btnDel.setAttribute('value', '删除');

    // //删除操作
    // btnDel.οnclick = function () {
    //     if (confirm("确定删除这一行嘛？")) {
    //         //找到按钮所在行的节点，然后删掉这一行
    //         this.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode);
    //         //btnDel - td - tr - tbody - 删除(tr)
    //         //刷新网页还原。实际操作中，还要删除数据库中数据，实现真正删除
    //     }
    // }
    // delCell.appendChild(btnDel);  //把删除按钮加入td，别忘了

    return row; //返回tr数据	 
}

document.addEventListener('DOMContentLoaded', drawTable);



