const products = [
  {id:1,title:"Profi Allzweckreiniger Konzentrat",category:"Reinigungsmittel",detail:"Für robuste und abwaschbare Oberflächen",icon:"spray-can",badge:"Bestseller"},
  {id:2,title:"Sanitärreiniger Daily",category:"Reinigungsmittel",detail:"Für Bad, WC und säurebeständige Flächen",icon:"droplets",badge:"Profi"},
  {id:3,title:"Glas und Oberflächenreiniger",category:"Reinigungsmittel",detail:"Für streifenfreie Glas und Spiegelreinigung",icon:"sparkles",badge:"Schnell"},
  {id:4,title:"Mikrofasertuch Universal",category:"Tücher und Mopps",detail:"Für tägliche Unterhaltsreinigung",icon:"scan-line",badge:"Set"},
  {id:5,title:"Moppbezug Professional 40 cm",category:"Tücher und Mopps",detail:"Für effiziente Bodenreinigung im Objekt",icon:"waves",badge:"Objekt"},
  {id:6,title:"Papierhandtücher Z Falzung",category:"Hygiene und Papier",detail:"Für Spendersysteme in Waschräumen",icon:"scroll",badge:"Karton"},
  {id:7,title:"Müllsäcke Extra Stark 120 L",category:"Müllentsorgung",detail:"Robuste Säcke für Gewerbe und Objektservice",icon:"trash-2",badge:"Stark"},
  {id:8,title:"Nitril Handschuhe 100 Stück",category:"Arbeitsschutz",detail:"Einmalhandschuhe für Reinigung und Hygiene",icon:"shield-check",badge:"Schutz"},
  {id:9,title:"Reinigungswagen Compact",category:"Reinigungswagen",detail:"Kompakte Lösung für tägliche Objektpflege",icon:"shopping-cart",badge:"System"},
  {id:10,title:"Seifenspender Professional",category:"Spendersysteme",detail:"Für Waschräume und stark frequentierte Bereiche",icon:"hand",badge:"Hygiene"},
  {id:11,title:"Nass und Trockensauger Pro",category:"Maschinen und Geräte",detail:"Leistungsstark für professionelle Anwendungen",icon:"settings",badge:"Gerät"},
  {id:12,title:"Bodenpad Universal",category:"Maschinen und Geräte",detail:"Passend für viele maschinelle Bodenarbeiten",icon:"disc-3",badge:"Zubehör"}
];

let activeFilter = "Alle";
let currentSearch = "";
let cart = JSON.parse(localStorage.getItem("perfectSolutionCart") || "{}");

const productGrid = document.getElementById("productGrid");
const emptyState = document.getElementById("emptyState");
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const categoryPanel = document.getElementById("categoryPanel");
const categoryTrigger = document.getElementById("categoryTrigger");
const cartDrawer = document.getElementById("cartDrawer");
const backdrop = document.getElementById("backdrop");
const accountModal = document.getElementById("accountModal");
const toast = document.getElementById("toast");

function icon(name){
  return '<i data-lucide="' + name + '"></i>';
}

function renderProducts(){
  const query = currentSearch.trim().toLowerCase();
  const filtered = products.filter(p => {
    const categoryMatch = activeFilter === "Alle" || p.category === activeFilter;
    const searchMatch = !query || [p.title,p.category,p.detail].some(v => v.toLowerCase().includes(query));
    return categoryMatch && searchMatch;
  });

  productGrid.innerHTML = filtered.map(p => `
    <article class="product-card">
      <div class="product-art">
        <span class="product-badge">${p.badge}</span>
        ${icon(p.icon)}
      </div>
      <div class="product-body">
        <div class="product-meta">${p.category}</div>
        <h3 class="product-title">${p.title}</h3>
        <div class="product-copy">${p.detail}</div>
        <div class="product-buy">
          <div class="product-price"><small>Geschäftskundenpreis</small><strong>nach Anmeldung</strong></div>
          <button class="add-button" type="button" data-add="${p.id}" aria-label="${p.title} hinzufügen">${icon("plus")}</button>
        </div>
      </div>
    </article>
  `).join("");

  emptyState.classList.toggle("visible", filtered.length === 0);
  lucide.createIcons();

  productGrid.querySelectorAll("[data-add]").forEach(button => {
    button.addEventListener("click", () => addToCart(Number(button.dataset.add)));
  });
}

function setFilter(category){
  activeFilter = category;
  document.querySelectorAll(".filter").forEach(button => {
    button.classList.toggle("active", button.dataset.filter === category);
  });
  if(!document.querySelector('.filter[data-filter="' + category + '"]')){
    document.querySelectorAll(".filter").forEach(button => button.classList.remove("active"));
  }
  renderProducts();
  document.getElementById("produkte").scrollIntoView({behavior:"smooth",block:"start"});
}

function addToCart(id){
  cart[id] = (cart[id] || 0) + 1;
  persistCart();
  renderCart();
  showToast("Produkt zum Anfragekorb hinzugefügt");
}

function persistCart(){
  localStorage.setItem("perfectSolutionCart", JSON.stringify(cart));
}

function cartQuantity(){
  return Object.values(cart).reduce((sum,value) => sum + value,0);
}

function renderCart(){
  const ids = Object.keys(cart).filter(id => cart[id] > 0);
  const items = ids.map(id => {
    const p = products.find(item => item.id === Number(id));
    if(!p) return "";
    return `
      <div class="drawer-item">
        <span class="drawer-item-icon">${icon(p.icon)}</span>
        <div><strong>${p.title}</strong><small>${p.category}</small></div>
        <div class="drawer-item-controls">
          <button type="button" data-minus="${p.id}" aria-label="Menge reduzieren">−</button>
          <span>${cart[id]}</span>
          <button type="button" data-plus="${p.id}" aria-label="Menge erhöhen">+</button>
        </div>
      </div>
    `;
  }).join("");

  document.getElementById("cartItems").innerHTML = items;
  document.getElementById("cartCount").textContent = cartQuantity();
  document.getElementById("cartTotalItems").textContent = cartQuantity();
  document.getElementById("cartEmpty").style.display = ids.length ? "none" : "block";
  document.getElementById("cartFooter").style.display = ids.length ? "block" : "none";

  document.querySelectorAll("[data-minus]").forEach(button => button.addEventListener("click", () => changeQty(Number(button.dataset.minus),-1)));
  document.querySelectorAll("[data-plus]").forEach(button => button.addEventListener("click", () => changeQty(Number(button.dataset.plus),1)));
  lucide.createIcons();
}

function changeQty(id,delta){
  cart[id] = (cart[id] || 0) + delta;
  if(cart[id] <= 0) delete cart[id];
  persistCart();
  renderCart();
}

function openOverlay(type){
  backdrop.classList.add("visible");
  document.body.classList.add("locked");
  if(type === "cart"){
    cartDrawer.classList.add("open");
    cartDrawer.setAttribute("aria-hidden","false");
  }else{
    accountModal.classList.add("open");
    accountModal.setAttribute("aria-hidden","false");
  }
}

function closeOverlays(){
  cartDrawer.classList.remove("open");
  accountModal.classList.remove("open");
  backdrop.classList.remove("visible");
  document.body.classList.remove("locked");
  cartDrawer.setAttribute("aria-hidden","true");
  accountModal.setAttribute("aria-hidden","true");
}

function showToast(message){
  toast.querySelector("span").textContent = message;
  toast.classList.add("show");
  clearTimeout(window.toastTimer);
  window.toastTimer = setTimeout(() => toast.classList.remove("show"),2600);
}

searchForm.addEventListener("submit", event => {
  event.preventDefault();
  currentSearch = searchInput.value;
  activeFilter = "Alle";
  document.querySelectorAll(".filter").forEach(button => button.classList.toggle("active",button.dataset.filter === "Alle"));
  renderProducts();
  document.getElementById("produkte").scrollIntoView({behavior:"smooth",block:"start"});
});

searchInput.addEventListener("input", () => {
  if(searchInput.value === ""){
    currentSearch = "";
    renderProducts();
  }
});

document.querySelectorAll(".filter").forEach(button => button.addEventListener("click", () => setFilter(button.dataset.filter)));
document.querySelectorAll("[data-category]").forEach(button => button.addEventListener("click", () => {
  categoryPanel.classList.remove("open");
  setFilter(button.dataset.category);
}));

categoryTrigger.addEventListener("click", () => categoryPanel.classList.toggle("open"));
document.addEventListener("click", event => {
  if(!categoryPanel.contains(event.target) && !categoryTrigger.contains(event.target)) categoryPanel.classList.remove("open");
});

document.getElementById("cartButton").addEventListener("click", () => openOverlay("cart"));
document.getElementById("closeCart").addEventListener("click", closeOverlays);
document.getElementById("accountButton").addEventListener("click", () => openOverlay("account"));
document.getElementById("closeAccount").addEventListener("click", closeOverlays);
document.getElementById("accountCta").addEventListener("click", closeOverlays);
backdrop.addEventListener("click", closeOverlays);

document.getElementById("requestButton").addEventListener("click", () => {
  const selected = Object.keys(cart).filter(id => cart[id] > 0).map(id => {
    const p = products.find(item => item.id === Number(id));
    return cart[id] + " × " + p.title;
  }).join("\n");
  closeOverlays();
  document.getElementById("kontakt").scrollIntoView({behavior:"smooth"});
  showToast("Auswahl vorbereitet. Kontaktdaten können als Nächstes ergänzt werden.");
  console.info("Anfragekorb:\n" + selected);
});

document.getElementById("resetSearch").addEventListener("click", () => {
  currentSearch = "";
  activeFilter = "Alle";
  searchInput.value = "";
  document.querySelectorAll(".filter").forEach(button => button.classList.toggle("active",button.dataset.filter === "Alle"));
  renderProducts();
});

document.getElementById("businessForm").addEventListener("submit", event => {
  event.preventDefault();
  const status = document.getElementById("businessStatus");
  status.textContent = "Vielen Dank. Die Demo Anfrage wurde erfolgreich erfasst.";
  event.target.reset();
  showToast("Geschäftskonto Anfrage erfasst");
});

document.getElementById("menuButton").addEventListener("click", () => categoryPanel.classList.toggle("open"));
document.getElementById("year").textContent = new Date().getFullYear();

renderProducts();
renderCart();
lucide.createIcons();
