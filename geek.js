/**
 * 运行在浏览器控制台中
 * @type {Array}
 */

// 要爬取的文章id集合  geek网站做了限流，所以分两次请求。当然你也可以用代理什么的
var ids = [77345, 77749, 77804, 78158, 78168, 78884, 79319, 79539, 80011, 80021, 80042, 80240, 80260, 80311, 81730, 82397, 82711, 82764, 83302, 83719, 83860, 84365, 84633, 85031, 85341, 85745, 86117];
var ids2 = [86400, 86823, 87179, 87234, 87808, 88275, 88538, 88827, 89151, 89491, 89832, 90148, 90485, 90998, 91325, 91644, 92227, 92663, 93110, 93216, 93289, 93777, 94156, 94644, 94979, 95469, 95833, 96269, 96809, 97144];
// 最后获得的数据
var rs = []
/**
 * 初始化   文档中注入FileSaver.js 并执行请求开始的方法
 * @return {[type]} [description]
 */
function init() {
    var src = 'https://cdn.bootcss.com/FileSaver.js/2014-11-29/FileSaver.js';
    var script = document.createElement('script');
    script.src = src;
    var heads = document.getElementsByTagName("head");
    if (heads.length)
        heads[0].appendChild(script);
    else
        document.documentElement.appendChild(script);
    script.onload = function() {
        console.log('script loaded')
        start()
    }
}
// 将数据转存为json文件
function downloadJson(data) {
    var blob = new Blob([JSON.stringify(data)], { type: "" });
    saveAs(blob, "data.json");
}

// 爬取一篇文章 就是一个ajax请求
function fetch(id) {
    var data = JSON.stringify({
        "include_neighbors": "false",
        "id": id
    });
    var xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.addEventListener("readystatechange", function() {
        if (this.readyState === 4) {
            var res = JSON.parse(this.responseText);
            if (res.code == 0) {
                var data = res.data;
                var item = {
                    id: data.id,
                    pid: data.cid,
                    article_content: data.article_content,
                    article_cover: data.article_cover,
                    article_ctime: data.article_ctime,
                    article_title: data.article_title,
                    audio_download_url: data.audio_download_url,
                    audio_size: data.audio_size,
                    audio_time: data.audio_time,
                    audio_url: data.audio_url
                }
                rs.push(item);
                // 如果当前是最后一个就下载文件
                if (id == ids2[ids2.length - 1]) {
                    downloadJson(rs)
                }
            }
        }
    });

    xhr.open("POST", "https://time.geekbang.org/serv/v1/article");
    xhr.setRequestHeader("content-type", "application/json");
    xhr.send(data);
}

function start() {
    // 依次请求
    for (var i = 0; i < ids2.length; i++) {
        (function(i) {
            setInterval(fetch(ids2[i]), 3000)
        })(i)
    }
}
init()
