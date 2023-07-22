// verificar se o input é maior que 10

const buttonElement = document.getElementById('checkButton');
buttonElement.addEventListener('click', 
    function() { 
        var inputValue = document.getElementById('numeroInput').value; 
        if (inputValue > 10) {   
            buttonElement.classList.remove('button-red');  
            buttonElement.classList.add('button-green');  
            buttonElement.innerHTML = 'O valor  ' + inputValue + '  é maior que 10!'; 
            
        } 
        else { 
            buttonElement.classList.remove('button-green');  
            buttonElement.classList.add('button-red');  
            buttonElement.innerHTML = 'O valor ' + inputValue + ' é menor que 10!';  
            
        }
    });
