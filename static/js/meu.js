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

function verDescricao(txt){
        if(txt == 'None' || txt == ''){
			txt = 'Sem Descrição'
        }
        $('#descricao').html(txt)
}

function verResultado(txt){
	let pai = $('#resultado')
	let area = document.getElementById('areaResultado')
	if(area === null){
		$('<textarea>', {
			id: 'areaResultado',
			class: 'textDesc2 conteudo-animado',
			disabled: true,
			rows: '15'
		}).appendTo(pai);
		$('#resultado textarea').val(txt)
	}
}

function carregarEdit(id){
	$.ajax({
        url : `http://localhost:5000/editar_tarefa/${id}`,
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

function editarTarefa(){
	id_tarefa = $('textarea').attr('id')
	valor = $('textarea').val()
	valor = valor.trim()
	
	$.ajax({
		url : "http://localhost:5000/editar_tarefa",
		type : 'put',
		data : {id : id_tarefa, desc: valor}
   })
   .done(function(msg){
		alert(msg)
   })
   .fail(function(jqXHR, textStatus, msg){
		alert(msg);
   });
}

function infosGrupo(id){
	$.ajax({
        url : `http://localhost:5000/grupos/${id}`,
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

function listarTarefas(){
	$.ajax({
        url : 'http://localhost:5000/ver_tarefas',
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

function perfil(){
	$.ajax({
        url : 'http://localhost:5000/perfil',
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

function acoesGrupo(id_grupo){
	$.ajax({
        url : `http://localhost:5000/acoes_grupo/${id_grupo}`,
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

function criarGrupo(){
    $.ajax({
    url : 'http://localhost:5000/carrega_tela_criar',
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

var slide_wrp 		= ".side-menu-wrapper"; //Menu Wrapper
var open_button 	= ".menu-open"; //Menu Open Button
var close_button 	= ".menu-close"; //Menu Close Button
var overlay 		= ".menu-overlay"; //Overlay

//Initial menu position
$(slide_wrp).hide().css( {"right": -$(slide_wrp).outerWidth()+'px'}).delay(50).queue(function(){$(slide_wrp).show()}); 

$(open_button).click(function(e){ //On menu open button click
	e.preventDefault();
	$(slide_wrp).css( {"right": "0px"}); //move menu right position to 0
	setTimeout(function(){
		$(slide_wrp).addClass('active'); //add active class
	},50);
	$(overlay).css({"opacity":"1", "width":"100%"});
});

$(close_button).click(function(e){ //on menu close button click
	e.preventDefault();
	$(slide_wrp).css( {"right": -$(slide_wrp).outerWidth()+'px'}); //hide menu by setting right position 
	setTimeout(function(){
		$(slide_wrp).removeClass('active'); // remove active class
	},50);
	$(overlay).css({"opacity":"0", "width":"0"});
});

$(document).on('click', function(e) { //Hide menu when clicked outside menu area
	if (!e.target.closest(slide_wrp) && $(slide_wrp).hasClass("active")){ // check menu condition
		$(slide_wrp).css( {"right": -$(slide_wrp).outerWidth()+'px'}).removeClass('active');
		$(overlay).css({"opacity":"0", "width":"0"});
	}
});