document.addEventListener('DOMContentLoaded', function () {

    // Comprobar que la URL es la pestaña de /todo/list
    if (window.location.pathname === '/todo/list') {

        // Seleccionar el enlace con el id "delete-todo"
        var element = document.getElementById('delete-todo');

        if (element) { // Verificar si el elemento existe
            element.addEventListener('click', function (event) {
                event.preventDefault(); // Prevenir la acción predeterminada del enlace

                // Obtener la URL del atributo data-url
                const deleteUrl = this.getAttribute('data-url');

                // Mostrar el modal de confirmación
                Swal.fire({
                    title: '¿Estás seguro de que deseas eliminar esta tarea?',
                    text: "¡No podrás revertir esta acción!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Sí, eliminar',
                    cancelButtonText: 'Cancelar'
                }).then((result) => {
                    if (result.isConfirmed) {
                        // Redirigir a la URL de eliminación si se confirma
                        window.location.href = deleteUrl;
                    }
                });
            });
        }

    }

});
