window.addElement = function(type) {
    const container = document.getElementById('plan-container');

    const element = document.createElement('div');
    element.classList.add('element');
    element.style.position = 'absolute';
    element.style.top = '50px';
    element.style.left = '50px';
    element.style.display = 'flex';
    element.style.alignItems = 'center';
    element.style.justifyContent = 'center';
    element.style.cursor = 'move';
    element.setAttribute('data-type', type);

    switch (type) {
        case 'table-carree':
            element.style.width = '80px';
            element.style.height = '80px';
            element.style.background = 'white';
            element.style.border = '2px solid #000';
            element.innerText = '⬛';
            break;

        case 'table-ronde':
            element.style.width = '80px';
            element.style.height = '80px';
            element.style.background = 'white';
            element.style.border = '2px solid #000';
            element.style.borderRadius = '50%';
            element.innerText = '⚪';
            break;

        case 'tabouret':
            element.style.width = '40px';
            element.style.height = '40px';
            element.style.background = '#ccc';
            element.style.border = '2px solid #555';
            element.style.borderRadius = '50%';
            element.innerText = '🪑';
            break;

        case 'matelas':
            element.style.width = '100px';
            element.style.height = '60px';
            element.style.background = '#e0e0e0';
            element.style.border = '2px solid #555';
            element.innerText = '🛏️';
            break;

        case 'mur':
            element.style.width = '200px';
            element.style.height = '20px';
            element.style.background = '#444';
            break;

        case 'plante':
            element.style.width = '50px';
            element.style.height = '50px';
            element.style.background = '#6ab04c';
            element.style.border = '2px solid #2f3640';
            element.style.borderRadius = '50%';
            element.innerText = '🪴';
            break;

        case 'bar':
            element.style.width = '200px';
            element.style.height = '60px';
            element.style.background = '#8e44ad';
            element.style.color = 'white';
            element.style.fontWeight = 'bold';
            element.innerText = 'BAR';
            break;

        default:
            element.style.width = '60px';
            element.style.height = '60px';
            element.style.background = 'grey';
            element.innerText = '?';
    }

    container.appendChild(element);
};
