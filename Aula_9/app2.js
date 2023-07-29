// Um jogo de Adivinhação, nesse jogo terá um campo, onde o usuário digitara um número, esse número deve ser entre 1 e 100.
const buttonElement = document.getElementById('checkButton');
const resultadoMensagemElement = document.getElementById('resultMessage');
const numeroAleatorio = Math.floor(Math.random() * 100) + 1; 

// contar quantas tentativas o usuario fez
var tentativas = 1;

buttonElement.addEventListener('click', 
    function() { 
        var inputValue = document.getElementById('tentativaInput').value;
        removeClass(); 

        // criar numero aleatorio de 1 a 100 
        console.log(numeroAleatorio);
        tentativas++;
        if (inputValue == '' || isNaN(inputValue)) { 
            resultadoMensagemElement.classList.add('result-error');
            resultadoMensagemElement.innerHTML = 'O valor digitado não é um número válido!';
            return;
        } else {
            // se o numero for maior que 100 ou menor que 1 mostrar mensagem de numero invalido em vermelho.
            if (inputValue > 100 || inputValue < 1) { 
                resultadoMensagemElement.classList.add('result-error');
                resultadoMensagemElement.innerHTML = 'O valor digitado não é um <strong> número </strong> válido! <br> Tentativa ' + tentativas + '.';
                // verificar se o numero digitado é igual ao numero sorteado
            } else if (inputValue == numeroAleatorio) {
                    resultadoMensagemElement.classList.add('result-success');
                    resultadoMensagemElement.innerHTML = '<strong> Parabéns!</strong>  Você acertou o número sorteado! <br> Tentativa ' + tentativas + '.'
                    saveTextAsFile();
                } else if (inputValue > numeroAleatorio) {
                    // verificar se o numero digitado é maior ou menor que o numero sorteado 
                    resultadoMensagemElement.classList.add('result-fail');  
                    resultadoMensagemElement.innerHTML = 'O valor  ' + inputValue + '  é <strong> maior </strong> que o número sorteado! <br> Tentativa ' + tentativas + '.' 
                } else if (inputValue < numeroAleatorio) {
                    resultadoMensagemElement.classList.add('result-fail');  
                    resultadoMensagemElement.innerHTML = 'O valor  ' + inputValue + '  é <strong> menor </strong> que o número sorteado! <br> Tentativa ' + tentativas + '.'
                }
        } 
    });

    // criar funcao para salvar txt com a mensagem usando CreateTextFile
    function saveTextAsFile() { 
        var title = "Resultado do Jogo de Adivinhação as " + new Date() + "\r\n";
        var texto = "Você Acertou na Tentativa " + tentativas + " o número sorteado foi " + numeroAleatorio + "\r\n"; 
        let blob = new Blob([texto], 
                        {
                            type: "text/plain;charset=utf-8"
                        });   
        saveAs(blob,  title + ".txt");
    }        

    // cria funcao para remover a classe result-success e result-fail e result-error
    function removeClass() {
        resultadoMensagemElement.classList.remove('result-success');
        resultadoMensagemElement.classList.remove('result-error');
        resultadoMensagemElement.classList.remove('result-fail');
    }
