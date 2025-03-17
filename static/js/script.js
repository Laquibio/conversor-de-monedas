document.getElementById('conversionForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Evitar que el formulario se envíe normalmente

    // Obtener los datos del formulario
    const formData = new FormData(this);

    // Enviar los datos al servidor usando Fetch API
    fetch('/convertir', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            // Mostrar el resultado en la misma tarjeta
            document.getElementById('amountResult').textContent = data.amount;
            document.getElementById('fromCurrencyResult').textContent = data.from_currency;
            document.getElementById('convertedAmountResult').textContent = data.converted_amount;
            document.getElementById('toCurrencyResult').textContent = data.to_currency;
            document.getElementById('resultado').classList.remove('hidden');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});