/*
* TODO: 
* - add translation function
* - add edit function
* ref: idk.js
*/

async function getAllProducts() {
    try {
        const response = await fetch(`/api/getAllProducts`);
        const data = await response.json();

        data.forEach(product => {
            barcode = product[0];
            name = product[1];
            translation = product[2]

            productElement = document.createElement('div');
            productElement.className = 'product';
            productElement.id = barcode;

            editButtonElement = document.createElement('button');
            editButtonElement.textContent = '✏️';
            editButtonElement.id = 'editButton';
            productElement.appendChild(editButtonElement);

            codeElement = document.createElement('div');
            codeElement.textContent = barcode;
            codeElement.className = 'code';
            productElement.appendChild(codeElement);

            nameElement = document.createElement('div');
            nameElement.textContent = name;
            nameElement.className = 'name';
            productElement.appendChild(nameElement);

            arrowElement = document.createElement('div');
            arrowElement.innerHTML = '→';
            arrowElement.className = 'arrow';
            productElement.appendChild(arrowElement);

            translationElement = document.createElement('div');
            translationElement.textContent = translation;
            translationElement.className = 'translation';
            productElement.appendChild(translationElement);

            empties.appendChild(productElement);
        });
    } catch (error) {
        console.error(error);
    }
}

getAllProducts();
