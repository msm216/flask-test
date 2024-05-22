// 该函数在页面DOM加载完毕后执行，$ 符号是jQuery的简写，
$(function() {
    // 根据id选择 load 对象并为单击事件注册回调函数
    $('#load').click(function() {
        // 发送一个URL为"/more"请求类型为GET的AJAX请求到服务器
        $.ajax({
            url: '/more',
            type: 'get',
            // data为服务器返回的响应主体
            // load_post视图的返回响应为一段随机文本
            success: function(data) {
                // 选择 body 类并使用 append() 方法插入data
                $('.body').append(data);
            }
        })
    })
})
