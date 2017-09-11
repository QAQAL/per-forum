var log = function() {
    console.log.bind(console, arguments)
}

var e = function(sel) {
    return document.querySelector(sel)
}

var timeString = function(timestamp) {
    var d = new Date(timestamp*1000)
    return d.toLocaleString()
}


var loadcontent = function() {
    // 调用 ajax api 来载入数据
    var topic = e('.markdown-text').innerHTML
    var topic_content = marked(topic)
    e('.markdown-text').innerHTML = topic_content
}

var __main = function() {
    loadcontent()
}

__main()
