// 定义长连接
var conn =  null;

// 定义连接函数
function connect() {
    disconnect();
    var transports = ["websocket"];
    // 创建连接对象
    conn = new SockJS("http://" + window.location.host+"/real_time",transports);
    // 建立连接
    conn.onopen=function () {
        console.log("连接成功")
    };
    // 建立发送消息
    conn.onmessage = function (e) {
        console.log(e.data)
    };
    // 建立关闭连接
    conn.onclose=function () {
        console.log("断开连接")
    };
     //每隔几秒触发一个事件
    setInterval(function () {
        conn.send("system");
    }, 500);
}

//定义断开连接的函数
function disconnect() {
    if(conn!=null){
        conn.close();
        conn=null;
    }
}

//刷新页面断开连接,重新连接,短信年重连判断
if(conn==null){
    connect();
}else {
  disconnect();
}