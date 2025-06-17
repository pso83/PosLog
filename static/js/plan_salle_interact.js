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

  if (type === 'table') {
    const numero = prompt("Numéro de table ?");
    const forme = document.getElementById("planType").value === 'restaurant'
      ? prompt("Forme ? ronde / carree", "ronde") : 'ronde';
    const cv = parseInt(prompt("Nombre de couverts ?", "4"));
    element.dataset.numero = numero;
    element.dataset.forme = forme;
    element.dataset.couverts = cv;

    const img = document.createElement("img");
    img.src = "/static/images/plan/table_" + forme + ".png";
    img.style.width = forme === 'ronde' ? '100px' : '50px';
    img.style.height = forme === 'ronde' ? '100px' : '50px';
    element.appendChild(img);

    const label = document.createElement("div");
    label.innerHTML = `<strong>${numero}</strong><br/>(${cv} cv)`;
    label.style.position = "absolute";
    label.style.top = "35%";
    label.style.left = "0";
    label.style.width = "100%";
    label.style.textAlign = "center";
    label.style.fontWeight = "bold";
    element.appendChild(label);

    for (let i = 0; i < cv; i++) {
      const angle = (2 * Math.PI / cv) * i;
      const rayon = forme === 'ronde' ? 60 : 40;
      const x = 30 + rayon * Math.cos(angle);
      const y = 30 + rayon * Math.sin(angle);
      const chaise = document.createElement("img");
      chaise.src = "/static/images/plan/chaise.png";
      chaise.className = "chaise";
      chaise.style.position = "absolute";
      chaise.style.left = x + "px";
      chaise.style.top = y + "px";
      chaise.style.width = "20px";
      chaise.style.height = "20px";
      element.appendChild(chaise);
    }

  } else {
    const img = document.createElement("img");
    img.src = "/static/images/plan/" + type + ".png";
    img.style.width = type === "bar" ? "100px" : "60px";
    img.style.height = type === "bar" ? "40px" : "60px";
    element.appendChild(img);
  }

  container.appendChild(element);

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
      type: el.dataset.type,
      numero: el.dataset.numero || null,
      forme: el.dataset.forme || null,
      nb_places: el.dataset.couverts ? parseInt(el.dataset.couverts) : null,
      x: parseFloat(el.getAttribute('data-x')) || 0,
      y: parseFloat(el.getAttribute('data-y')) || 0
    };
  });

  fetch("/configuration/plan_salle", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ tables: elements })
  })
  .then(res => res.json())
  .then(data => alert("Plan sauvegardé avec succès."))
  .catch(err => alert("Erreur sauvegarde: " + err));
}
</script>