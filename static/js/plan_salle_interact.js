<script>
let id = 0;

function ajouterElement(type) {
  const container = document.getElementById("plan-container");
  const element = document.createElement("div");
  element.className = "element";
  element.style.position = "absolute";
  element.style.left = "100px";
  element.style.top = "100px";
  element.dataset.type = type;

  const planType = document.getElementById("planType")?.value || 'restaurant';

  // Gestion des éléments avec numéro et couverts
  if (["tables", "plage"].includes(type)) {
    const numero = prompt("Numéro ?");
    if (!numero) return;

    const nbPlaces = (type !== "tabouret" && type !== "plage")
      ? parseInt(prompt("Nombre de couverts ?", "2")) : null;

    element.dataset.numero = numero;
    element.dataset.nb_places = nbPlaces;

    // Image selon l'élément
    const img = document.createElement("img");
    img.src = `/static/images/elements/${type}/${type === "tables" ? "table_2cv.png" : "objet.png"}`;
    img.style.width = "auto";
    img.style.height = "auto";
    img.style.maxWidth = "100px";
    img.style.maxHeight = "100px";
    element.appendChild(img);

    // Label
    const label = document.createElement("div");
    label.innerHTML = `<strong>${numero}</strong>${nbPlaces ? `<br/>(${nbPlaces} cv)` : ""}`;
    label.style.position = "absolute";
    label.style.top = "35%";
    label.style.left = "0";
    label.style.width = "100%";
    label.style.textAlign = "center";
    label.style.fontWeight = "bold";
    element.appendChild(label);

  } else {
    // Éléments sans numéro
    const img = document.createElement("img");
    img.src = `/static/images/elements/${type}/${type}.png`;
    img.style.width = "auto";
    img.style.height = "auto";
    img.style.maxWidth = "100px";
    img.style.maxHeight = "100px";
    element.appendChild(img);
  }

  container.appendChild(element);

  // Activation du drag
  interact(element).draggable({
    listeners: {
      move (event) {
        const target = event.target;
        const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
        const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;
        target.style.transform = `translate(${x}px, ${y}px)`;
        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);
      }
    }
  });
}

function sauvegarderPlan() {
  const elements = Array.from(document.querySelectorAll('#plan-container .element')).map(el => {
    return {
      type_element: el.dataset.type,
      numero: el.dataset.numero || null,
      nb_places: el.dataset.nb_places ? parseInt(el.dataset.nb_places) : null,
      x: parseFloat(el.getAttribute('data-x')) || 0,
      y: parseFloat(el.getAttribute('data-y')) || 0,
      rotation: 0,  // Tu peux gérer cela dynamiquement si tu le souhaites
      image: el.querySelector('img')?.getAttribute('src') || ''
    };
  });

  fetch("/configuration/plan/save", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ elements: elements, salle_id: selectedSalleId })
  })
  .then(res => {
    if (!res.ok) throw new Error("Erreur API");
    return res.json();
  })
  .then(data => alert("Plan sauvegardé avec succès."))
  .catch(err => alert("Erreur sauvegarde: " + err));
}

function getNextNumeroDisponible() {
  const usedNumbers = Array.from(document.querySelectorAll('#plan-container .element'))
    .map(el => parseInt(el.dataset.numero))
    .filter(n => !isNaN(n));
  let numero = 1;
  while (usedNumbers.includes(numero)) {
    numero++;
  }
  return numero;
}

function onElementTypeSelect(type) {
  const numeroInput = document.getElementById("element-numero");
  const cvInput = document.getElementById("element-couverts");

  if (type === 'objets') {
    numeroInput.disabled = true;
    cvInput.disabled = true;
  } else if (type === 'tabouret') {
    numeroInput.disabled = false;
    cvInput.disabled = true;
    numeroInput.value = getNextNumeroDisponible();
    cvInput.value = '';
  } else {
    numeroInput.disabled = false;
    cvInput.disabled = false;
    numeroInput.value = getNextNumeroDisponible();
    cvInput.value = 4;
  }
}

</script>
