$(document).ready(function() {
    var serversList=$('#servers_list tbody');
    getServersList();
    $('#addServer').submit(function(e){
        serversList.empty()
        e.preventDefault()
        var form=$(this)
        $.ajax({
            async: true,
            type: "POST",
            url: "/addNewServer",
            data: form.serialize(),
            cache: false,
            processData: false,
            success: function(data){
                getServersList()
            },
            error: function(err){
                showResult(`ajax err: ${JSON.stringify(err,null,2)}`);    
            }
        })
    });
    $(this).on('click', 'button[name="deleteServer"]', function(e){
        serversList.empty()
        e.preventDefault()
        var row=$(this).parent().parent();
        $.ajax({
            async: true,
            type: "POST",
            url: "/deleteServer",
            data: "id="+row.find("[name='id']").html(),
            cache: false,
            processData: false,
            success: function(data){
                getServersList()
            },
            error: function(err){
                showResult(`ajax err: ${JSON.stringify(err,null,2)}`);    
            }
        })
    });
    $(this).on('click', 'button[name="editServer"]', function(e){
        serversList.empty()
        e.preventDefault()
        var row=$(this).parent().parent();
        console.log()
        $.ajax({
            async: true,
            type: "POST",
            url: "/editServer",
            data: "id="+row.find("[name='id']").html()+"&name="+row.find("[name='name']").val()+"&processor="+row.find("[name='processor']").val()+"&ram="+row.find("[name='ram']").val()+"&system="+row.find("[name='system']").val(),
            cache: false,
            processData: false,
            success: function(data){
                getServersList()
            },
            error: function(err){
                showResult(`ajax err: ${JSON.stringify(err,null,2)}`);    
            }
        })
    });
    function getServersList(){
        serversList.empty();
        $.ajax({
            async: true,
            type: "GET",
            url: "/getServersList",
            success: function(data){
                var result = JSON.parse(data);
                var htmlResult='';
                for (var i=0; i<result.length; ++i){
                    htmlResult+='<tr>';
                    htmlResult+='<td name="id">'+result[i].id+'</td>';
                    htmlResult+='<td><input type="text" class="form-control" name="name" placeholder="Name" value="'+result[i].name+'"></td>';
                    htmlResult+='<td><input type="text" class="form-control" name="processor" placeholder="Processor" value="'+result[i].processor+'"></td>';
                    htmlResult+='<td><input type="text" class="form-control" name="ram" placeholder="RAM" value="'+result[i].ram+'"></td>';
                    htmlResult+='<td><input type="text" class="form-control" name="system" placeholder="System" value="'+result[i].system+'"></td>';
                    htmlResult+='<td><button name="editServer"  class="btn btn-primary">Edit</button></td>';
                    htmlResult+='<td><button name="deleteServer" class="btn btn-primary">Delete</button></td>';
                    htmlResult+='</tr>';
                }
                $("#servers_list").DataTable().clear().destroy();
                showResult(htmlResult);
                $("#servers_list").dataTable({"bDestroy": true});
            },
            error: function(err){
                showResult(`ajax err: ${JSON.stringify(err,null,2)}`);    
            }
        });
    }
    function showResult(data){
        serversList.html(data);
    }
});