$(document).ready(function () {
    $('#autor_select').select2({
        tags: true,
        placeholder: "-- Busca o escribe un autor --",
        createTag: function (parametros) {
            var termino = $.trim(parametros.term);
            if (termino === '') { return null; }
            return { id: 'NUEVO_' + termino, text: termino, newTag: true }
        }
    });

    $('#autor_select').on('select2:select', function (evento) {
        var datos = evento.params.data;
        if (datos.id.startsWith('NUEVO_')) {
            var nombreAutor = datos.text;
            $.ajax({
                url: "/autores/crear_ajax",
                method: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ nombre: nombreAutor }),
                success: function (respuesta) {
                    var nuevaOpcion = new Option(respuesta.nombre, respuesta.id, true, true);
                    $('#autor_select').find('option[value="' + datos.id + '"]').remove();
                    $('#autor_select').append(nuevaOpcion).trigger('change');
                }
            });
        }
    });
});
