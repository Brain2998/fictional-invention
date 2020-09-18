$(document).ready(function() {
    var booksList=$('#books_list tbody');
    getBooksList();
    $('#addBook').submit(function(e){
        booksList.empty()
        e.preventDefault()
        var form=$(this)
        $.ajax({
            async: true,
            type: "POST",
            url: "/addNewBook",
            data: form.serialize(),
            cache: false,
            processData: false,
            success: function(data){
                getBooksList()
            },
            error: function(err){
                showResult(`ajax err: ${JSON.stringify(err,null,2)}`);    
            }
        })
    });
    function getBooksList(){
        booksList.empty();
        $.ajax({
            async: true,
            type: "GET",
            url: "/getBooksList",
            success: function(data){
                var result = JSON.parse(data);
                var htmlResult='';
                for (var i=0; i<result.length; ++i){
                    htmlResult+='<tr>';
                    htmlResult+='<td>'+result[i].id+'</td>';
                    htmlResult+='<td>'+result[i].name+'</td>';
                    htmlResult+='<td>'+result[i].author+'</td>';
                    htmlResult+='<td>'+result[i].genre+'</td>';
                    htmlResult+="<td><a href=\"/getTaskDetails?id="+result[i].name+'_'+result[i].started_at+"&getDbData=false\" class=\"btn btn-default\">Details</a></td>";
                    htmlResult+='</tr>';
                }
                $("#books_list").DataTable().clear().destroy();
                showResult(htmlResult);
                $("#books_list").dataTable({"bDestroy": true});
            },
            error: function(err){
                showResult(`ajax err: ${JSON.stringify(err,null,2)}`);    
            }
        });
    }
    function showResult(data){
        booksList.html(data);
    }
});