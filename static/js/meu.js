function carregarGrupos(){    
    $.ajax({
        url : "http://localhost:5000/grupos",
        type : 'get',
        beforeSend : function(){
            $("#cont").html('carregando...')
            }
    })
    .done(function(msg){
            $("#cont").html(msg);
    })
    .fail(function(jqXHR, textStatus, msg){
            alert(msg);
    }); 
}


function carregarTarefasGrupo(idGrupo){
    $.ajax({
        url : `http://localhost:5000/tarefas_gp/${idGrupo}`,
        type : 'get',
        beforeSend : function(){
            $("#cont").html('carregando...')
            }
    })
    .done(function(msg){
            $("#cont").html(msg);
    })
    .fail(function(jqXHR, textStatus, msg){
            alert(msg);
    }); 
}


function apagarTarefa(id){
        $.ajax({
                url : "http://localhost:5000/remover_tarefa",
                type : 'post',
                data : {id_tarefa : id},
           })
           .done(function(msg){
                alert(msg)
                $(`#${id}`).remove()
           })
           .fail(function(jqXHR, textStatus, msg){
                alert(msg);
           });
}