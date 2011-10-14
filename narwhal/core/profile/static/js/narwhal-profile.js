$(document).ready(function (){
    function get_user_card() {
        var res = $.ajax({url: "{% url profile:user-card %}"+$(this).data('user'),
                          async: false,
                          datatype: 'html',
                          timeout: 500 });
        if (res.status == 200) { return res.responseText; }
        else { return "Could not retrieve User Card";}
    }
    $('#usertools a .avatar').popover({animate:true, title:'data-user', placement:'below',
                                     html:true,  trigger:'hover', content: get_user_card})
    $('#content .avatar').popover({animate:true, title:'data-user', placement:'right',
                                     html:true,  trigger:'hover', content: get_user_card})
})