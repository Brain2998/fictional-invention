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
    $(this).on('click', 'button[name="deleteBook"]', function(e){
        booksList.empty()
        e.preventDefault()
        var row=$(this).parent().parent();
        $.ajax({
            async: true,
            type: "POST",
            url: "/deleteBook",
            data: "id="+row.find("[name='id']").html(),
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
    $(this).on('click', 'button[name="editBook"]', function(e){
        booksList.empty()
        e.preventDefault()
        var row=$(this).parent().parent();
        $.ajax({
            async: true,
            type: "POST",
            url: "/editBook",
            data: "id="+row.find("[name='id']").html()+"&name="+row.find("[name='name']").val()+"&author="+row.find("[name='author']").val()+"&genre="+row.find("[name='genre']").val(),
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
                    htmlResult+='<td name="id">'+result[i].id+'</td>';
                    htmlResult+='<td><input type="text" class="form-control" name="name" placeholder="Name" value="'+result[i].name+'"></td>';
                    htmlResult+='<td><input type="text" class="form-control" name="author" placeholder="Author" value="'+result[i].author+'"></td>';
                    htmlResult+='<td><input type="text" class="form-control" name="genre" placeholder="Genre" value="'+result[i].genre+'"></td>';
                    htmlResult+='<td><button name="editBook"  class="btn btn-primary">Edit</button></td>';
                    htmlResult+='<td><button name="deleteBook" class="btn btn-primary">Delete</button></td>';
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