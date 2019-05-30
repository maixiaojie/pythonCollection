const path = require('path')
const fs = require('fs')
const mysql = require('mysql')
const squel = require('squel').useFlavour('postgres');

const dbconfig = {
	host: '140.143.163.52',
	port: '3306',
    user: 'root',
    password: 'wenyujie@123',
    database: 'mdblog'
 //    host: 'localhost',
	// port: '3303',
 //    user: 'root',
 //    password: '123456',
 //    database: 'mydb'
}
const pool = mysql.createPool(dbconfig);


const file = path.join(__dirname, './articles154.json')
const tableName = 'article'
fs.readFile(file, 'utf-8', function(err, data) {
	// data = data.replace(/\n/g, '')
	const json = JSON.parse(data)
	// console.log(json[0].mdhtml)
	pool.getConnection(function(err, connection) {
		// var sql = squel.insert()
		// 				.into('article')
		// 				.setFieldsRows(json, {ignorePeriodsForFieldNameQuotes: true})
		// 				.toParam()
		// console.log(sql)
		var sql = `INSERT INTO article (article_title, audio_time, audio_size, pid, audio_url, audio_download_url, mdhtml, ctime, id, article_cover) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;

		for(let i=0; i<json.length; i++) {
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
			json[i].article_cover]
			connection.query(sql, values, function (error, results, fields) {
		    // When done with the connection, release it.
		    // Handle error after the release.
		    if (error) throw error;
		    // Don't use the connection here, it has been returned to the pool.
		  });
		}
		pool.end();
		// connection.release();
		 // connection.query(sql, arr, function (error, results, fields) {
		 //    // When done with the connection, release it.
		 //    connection.on('error', function(err) {
		 //    	console.log(err.code)
		 //    })
		 //    connection.release();
			
		 //    // Handle error after the release.
		 //    if (error) throw error;
		 //    connection.end(function(err) {

		 // 	})
		 //    // Don't use the connection here, it has been returned to the pool.
		 //  });
		 
	})
	
})