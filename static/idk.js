let empties = document.getElementById("empties");
let database = document.getElementById("db").innerHTML;
let user = document.getElementById("user").innerHTML;
let password = document.getElementById("password").innerHTML;

console.log(database, user, password);
var edit = false;


(async () => {
  try {
    const response = await fetch(`/api/empty?database=${database}&user=${user}&password=${password}`);
    const data = await response.json();
    for (const [barcode, name] of data) {
      const productElement = document.createElement('div');
      productElement.className = 'product';
      productElement.id = barcode;

      const arrowElement = document.createElement('div');
      arrowElement.innerHTML = '→';
      arrowElement.className = 'arrow';

      const codeElement = document.createElement('div');
      codeElement.textContent = barcode;
      codeElement.className = 'code';

      const nameElement = document.createElement('div');
      nameElement.textContent = name;
      nameElement.className = 'name';

      const translatedElement = document.createElement('div');
      translatedElement.textContent = '...';
      translatedElement.className = 'translated';

      const responseTranslate = await fetch(`/api/translate?text=${encodeURIComponent(name)}`);
      const translatedName = await responseTranslate.json();
      translatedElement.textContent = translatedName;

      const originalButtonElement = document.createElement('button');
      originalButtonElement.textContent = '✏️';
      originalButtonElement.id = 'fixOriginal';

      productElement.appendChild(codeElement);
      productElement.appendChild(originalButtonElement);
      productElement.appendChild(nameElement);
      productElement.appendChild(arrowElement);
      productElement.appendChild(translatedElement);

      empties.appendChild(productElement);
      await fetch(`/api/appendLocal?barcode=${barcode}&name=${name}&translation=${translatedName}`);

      originalButtonElement.addEventListener('click', async () => {
        const { 0: code, 1: name, 2: translation } = await (await fetch(`/api/getProduct?&barcode=${barcode}`)).json();

        //todo: create floating panel with fields to edit original name and translation
        createEditBox(barcode, name, translation);

      });
    }
  } catch (error) {
    console.error(error);
  }
})();


function createEditBox(barcode, name, translation) {
  if (edit) {
    return;
  }

  overlay = document.createElement('div');
  overlay.id = 'overlay';
  document.body.appendChild(overlay);
  edit = true;

  box = document.createElement('div');
  box.id = 'editbox';

  let barcodeLabel = document.createElement('h1');
  barcodeLabel.innerHTML=barcode;
  document.body.appendChild(box);

  let nameFieldWrapper = document.createElement('div');
  nameFieldWrapper.className = 'editField';

  let nameField = document.createElement('input');
  nameField.type = 'text';
  nameField.value = name;
  nameField.id = 'nameField';
  nameField.className = 'editField';


  nameFieldWrapper.appendChild(nameField);

  let translationFieldWrapper = document.createElement('div');
  translationFieldWrapper.className = 'editField';

  let translationField = document.createElement('input');
  translationField.type = 'text';
  translationField.value = translation;
  translationField.id = 'translationField';
  translationField.className = 'editField';


  translationFieldWrapper.appendChild(translationField);

  box.appendChild(barcodeLabel);
  box.appendChild(nameFieldWrapper);
  box.appendChild(document.createElement('br'));
  box.appendChild(translationFieldWrapper);
  box.appendChild(document.createElement('br'));

  let saveButton = document.createElement('button');
  saveButton.textContent = "Save";
  saveButton.addEventListener('click', async () => {
    const name = document.getElementById('nameField').value;
    const translation = document.getElementById('translationField').value;
    const response = await fetch(`/api/updateName?barcode=${barcode}&name=${name}`);
    const response2 = await fetch(`/api/updateTranslation?barcode=${barcode}&translation=${translation}`);
    if (response.ok && response2.ok) {
      console.log("Changes saved!");
    } else {
      console.log("Error saving changes");
    }
    document.getElementById('overlay').remove();
    document.getElementById('editbox').remove();
    edit = false;

    name = document.getElementById('nameField').value;
    translation = document.getElementById('translationField').value;
    document.getElementById(barcode).children[2].textContent = name;
    document.getElementById(barcode).children[4].textContent = translation;
  });
  box.appendChild(saveButton);
  document.body.appendChild(box);
}