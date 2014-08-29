function load_jQuery() {
    var jquery = document.createElement('script');
    jquery.src = "http://code.jquery.com/jquery-2.1.1.min.js";
    jquery.type = "text/javascript"
    document.body.appendChild(jquery);
    var div = document.createElement('div');
    div.id = "search_real_url";
    div.style.display = "none";
    document.body.appendChild(div);
}
load_jQuery();
var jquery_ready = setTimeout(function() {
    var result = {};
    var pl_weibo_directtop = $('#pl_weibo_directtop');
    if (pl_weibo_directtop.text().trim().length() == 0) {
        result.msg = "没有数据"
        alert(result.msg);
    } else {
        real_url = pl_weibo_directtop.find('div.pl_directarea div.search_directarea.per_dir div.list_person.clearfix div.person_detail p.person_name a').attr('href')
        alert(real_url);
    }
}, 1000);
