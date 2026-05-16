document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('invoiceFile');
    const fileMsg = document.querySelector('.file-msg');
    const submitBtn = document.getElementById('submitBtn');
    
    const loader = document.getElementById('loader');
    const resultsSection = document.getElementById('resultsSection');
    const errorMessage = document.getElementById('errorMessage');

    // Cambiar texto cuando se selecciona un archivo
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileMsg.textContent = `Archivo seleccionado: ${e.target.files[0].name}`;
            fileMsg.style.color = 'var(--pwc-orange)';
        } else {
            fileMsg.textContent = 'Arrastra tu archivo aquí o haz clic para buscar';
            fileMsg.style.color = 'var(--pwc-dark-gray)';
        }
    });

    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const file = fileInput.files[0];
        if (!file) return;

        // Preparar UI para la carga
        loader.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        errorMessage.classList.add('hidden');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Procesando...';

        // Crear FormData para enviar el archivo
        const formData = new FormData();
        formData.append('file', file);

        try {
            // Llamada al backend de FastAPI
            const response = await fetch('/api/upload-invoice/', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Error procesando la factura');
            }

            const data = await response.json();
            
            // Pintar resultados en el HTML
            renderResults(data);
            
            // Mostrar sección de resultados
            resultsSection.classList.remove('hidden');

        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.classList.remove('hidden');
        } finally {
            // Restaurar UI
            loader.classList.add('hidden');
            submitBtn.disabled = false;
            submitBtn.textContent = 'Procesar Factura';
        }
    });

    function renderResults(data) {
        // Datos del Cliente
        document.getElementById('resNombre').textContent = data.cliente.nombre_completo;
        document.getElementById('resDireccion').textContent = data.cliente.direccion || 'N/A';
        document.getElementById('resCelular').textContent = data.cliente.celular || 'N/A';

        // Datos de Factura
        document.getElementById('resFecha').textContent = data.fecha;
        // Formatear el total como moneda
        const totalFormateado = new Intl.NumberFormat('es-CO', { 
            minimumFractionDigits: 2, maximumFractionDigits: 2 
        }).format(data.valor_total);
        document.getElementById('resTotal').textContent = totalFormateado;

        // Detalle de productos
        const tbody = document.querySelector('#detailsTable tbody');
        tbody.innerHTML = ''; // Limpiar tabla anterior

        data.detalles.forEach(detalle => {
            const tr = document.createElement('tr');
            
            const subtotal = detalle.cantidad * detalle.valor_unitario;
            const subtotalFormateado = new Intl.NumberFormat('es-CO', { 
                minimumFractionDigits: 2 
            }).format(subtotal);
            
            const valorUnitarioFormateado = new Intl.NumberFormat('es-CO', { 
                minimumFractionDigits: 2 
            }).format(detalle.valor_unitario);

            tr.innerHTML = `
                <td>${detalle.producto}</td>
                <td>${detalle.cantidad}</td>
                <td>$${valorUnitarioFormateado}</td>
                <td>$${subtotalFormateado}</td>
            `;
            tbody.appendChild(tr);
        });
    }
});