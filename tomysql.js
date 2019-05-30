const path = require('path')
const fs = require('fs')
const mysql = require('mysql')

// 数据库配置
const dbconfig = {
    host: 'your mysql host',
    port: 'your mysql port',
    user: 'your mysql username',
    password: 'your mysql password',
    database: 'your mysql database'
}
const pool = mysql.createPool(dbconfig);

// 读取json文件
const file = path.join(__dirname, './articles154.json')
// 数据表名
const tableName = 'article'
fs.readFile(file, 'utf-8', function(err, data) {
    const json = JSON.parse(data)
    pool.getConnection(function(err, connection) {
    	// sql  下面的逻辑可以根据自己的需要去写
        var sql = `INSERT INTO article (article_title, audio_time, audio_size, pid, audio_url, audio_download_url, mdhtml, ctime, id, article_cover) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;
        for (let i = 0; i < json.length; i++) {
            console.log(json[i].article_title)
            var values = [
                json[i].article_title,
                json[i].audio_time,
                json[i].audio_size,
                json[i].pid,
                json[i].audio_url,
                json[i].audio_download_url,
                json[i].article_content,
                json[i].ctime,
                json[i].id,
                json[i].article_cover
            ]
            connection.query(sql, values, function(error, results, fields) {
                // When done with the connection, release it.
                // Handle error after the release.
                if (error) throw error;
                // Don't use the connection here, it has been returned to the pool.
            });
        }
        pool.end();
    })
})