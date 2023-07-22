const pageTitleElement = document.getElementById('pageTitle');
console.log(pageTitleElement.textContent); //Saída: "Título da página"

const paragraphElements = document.getElementById('paragraph');
paragraphElements.textContent = 'Novo Parágrado'; 




const firstListItem = document.querySelector('li');
console.log(firstListItem.textContent); //Saída: "Item 1"

const listItems = document.querySelectorAll('li');
listItems.forEach((item) => console.log(item.textContent)); //Saída: "Item 1", "Item 2", "Item 3"




const buttonElement = document.getElementById('btnClick');
console.log(buttonElement.getAttribute('id')); //Saída: "btnClick"

buttonElement.setAttribute('disabled', true); //Desabilita o botão



const pageTitleElement = document.getElementById('pageTitle');
console.log(pageTitleElement.textContent); //Saída: "Título da página"

pageTitleElement.classList.add('red'); //Adiciona a classe "red" ao elemento

pageTitleElement.classList.remove('red'); //Remove a classe "red" do elemento

pageTitleElement.classList.add('green'); //Adiciona a classe "green" ao elemento 




const listElement = document.getElementById('list');
listElement.innerHTML += '<li>Item 4</li>'; //Adiciona um novo item à lista

const paragraphElement = document.getElementById('paragraph');
paragraphElement.innerHTML = '<br>Novo <strong>parágrafo</strong>'; //Altera o  parágrafo ao elemento


const listElement = document.getElementById('list');
const newListItem = document.createElement('li');
newListItem.textContent = 'Item 5';
listElement.appendChild(newListItem); //Adiciona o novo item à lista

const firstListItem = document.querySelector('li');
listElement.removeChild(firstListItem); //Remove o primeiro item da lista

const buttonElement = document.getElementById('btnClick');
buttonElement.addEventListener('click', function() {
    alert('Você clicou no botão!');
}); //Adiciona um evento de clique ao botão