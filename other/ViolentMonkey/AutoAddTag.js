// ==UserScript==
// @name        auto add tag
// @namespace   Violentmonkey Scripts
// @match       https://www.notion.so/*
// @grant       none
// @version     1.0
// @author      Benature
// @description 2/29/2020, 5:28:43 PM
// ==/UserScript==


var i, j;

window.addEventListener('keydown', function (e) {
    if (13 == e.keyCode) {
        var table = document.getElementsByClassName('notion-table-view')[0].childNodes[0]
        if (table != null) {
            // 取得 tag 的 index
            var theads = table.childNodes[0].childNodes[0].childNodes;
            for (i = 0; i < theads.length; i++) {
                let text = theads[i].innerText
                switch (text) {
                    case 'Tags':
                        var Tags_i = i;
                        break
                    case 'Tag':
                        var linkTag_i = i;
                        break;
                }
            }
            // console.log(Tags_i, linkTag_i)
            var tbodys = table.childNodes[2].childNodes;
            // console.log(tbodys)

            for (i = 1; i < tbodys.length; i++) {
                // 每一行
                let trs = tbodys[i].childNodes;
                let tag = trs[Tags_i].innerText
                let linkTag = trs[linkTag_i].innerText
                if (tag == '' || tag == linkTag) {
                    continue;
                }
                console.log(tbodys[i])
                trs[linkTag_i].click();
                setTimeout(function () {
                    let input = document.getElementsByTagName('input')[0];
                    input.value = tag; // 假的

                    let select = document.getElementsByClassName('notion-scroller horizontal')[2];
                    select = select.childNodes[0].childNodes[0].childNodes
                    for (j = 0; j < select.length; j++) {
                        let select_text = select[j].innerText;
                        select_text = select_text.split('\n')[0]
                        if (select_text == tag) {
                            select[j].click();
                            trs[1].click()
                            break;
                        }
                    }
                }, 1000);

                // break
            }
        }


    }
}, true)