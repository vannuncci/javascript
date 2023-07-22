// verificar se o input é maior que 10

const buttonElement = document.getElementById('checkButton');
const resultadoMensagemElement = document.getElementById('resultadoMensagem');
buttonElement.addEventListener('click', 
    function() { 
        var inputValue = document.getElementById('numeroInput').value; 

        if (inputValue == '' || isNaN(inputValue)) {
            alert('O valor digitado não é um número válido!');
            resultadoMensagemElement.classList.remove('button-red');
            resultadoMensagemElement.classList.remove('button-green');  
            resultadoMensagemElement.innerHTML = '';
            return;
        } else if (inputValue > 10) {   
            resultadoMensagemElement.classList.remove('button-red');  
            resultadoMensagemElement.classList.add('button-green');  
            resultadoMensagemElement.innerHTML = 'O valor  ' + inputValue + '  é maior que 10!'; 
            
        } else { 
            resultadoMensagemElement.classList.remove('button-green');  
            resultadoMensagemElement.classList.add('button-red');  
            resultadoMensagemElement.innerHTML = 'O valor ' + inputValue + ' é menor que 10!';  
            
        }
    });
