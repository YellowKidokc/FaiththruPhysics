(function(){
  if(document.querySelector("[data-site-shell]")) return;

  const sections = [
    {label:"Start", href:"#start"},
    {label:"Story", href:"#master-story"},
    {label:"Ladder", href:"#ladder"},
    {label:"Series", href:"#all"}
  ];

  const subdomains = [
    {label:"Home", href:"/"},
    {label:"Rigor", href:"/rigor/"},
    {label:"Lexicon", href:"/glossary/"},
    {label:"Equation", href:"/equation/"},
    {label:"Proof Explorer", href:"/proof-explorer/"},
    {label:"Isomorphisms", href:"/isomorphism/"},
    {label:"Master Equation", href:"/master-equation/"},
    {label:"GTQ", href:"/genesis-to-quantum/"},
    {label:"MDA", href:"/mda/"},
    {label:"Moral Decline", href:"/moral-decline/"},
    {label:"Media", href:"/media/"},
    {label:"Audio", href:"/audio/"},
    {label:"Podcast", href:"/podcast/"}
  ];

  function iconHome(){
    return '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>';
  }

  function iconSeries(){
    return '<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>';
  }

  function currentSection(){
    const hash = window.location.hash || "#start";
    return sections.find(section => section.href === hash) || sections[0];
  }

  function renderTop(){
    const current = currentSection();
    const tabs = sections.map(section => {
      const active = section.label === current.label ? " is-active" : "";
      return `<a class="site-shell-tab${active}" href="${section.href}">${section.label}</a>`;
    }).join("");

    const top = document.createElement("nav");
    top.className = "site-shell-top";
    top.setAttribute("data-site-shell", "top");
    top.setAttribute("aria-label", "Site frame");
    top.innerHTML = `
      <a class="site-shell-home" href="/">${iconHome()}<span>Home</span></a>
      <div class="site-shell-center">
        <span class="site-shell-side-label">Prev</span>
        <div class="site-shell-tabs" aria-label="Homepage sections">${tabs}</div>
        <span class="site-shell-side-label">Next</span>
      </div>
      <a class="site-shell-series" href="#all">${iconSeries()}<span>Series</span></a>
    `;
    document.body.prepend(top);
  }

  function renderBottom(){
    const nav = document.createElement("nav");
    nav.className = "site-shell-subdomains";
    nav.setAttribute("data-site-shell", "bottom");
    nav.setAttribute("aria-label", "Faith Through Physics network");
    nav.innerHTML = `
      <div class="site-shell-subdomain-inner">
        ${subdomains.map(item => `<a class="site-shell-subdomain-link" href="${item.href}"><span class="site-shell-dot"></span>${item.label}</a>`).join("")}
      </div>
    `;

    const credit = document.createElement("div");
    credit.className = "site-shell-credit";
    credit.setAttribute("data-site-shell", "credit");
    credit.textContent = "© 2024-2026 David Lowe · Faith Through Physics";

    const footer = document.querySelector("footer");
    if(footer){
      footer.parentNode.insertBefore(nav, footer);
      footer.insertAdjacentElement("afterend", credit);
    }else{
      document.body.append(nav, credit);
    }
  }

  function markActiveTab(){
    const current = currentSection();
    document.querySelectorAll(".site-shell-tab").forEach(tab => {
      tab.classList.toggle("is-active", tab.textContent.trim() === current.label);
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.body.classList.add("site-shell-enabled");
    renderTop();
    renderBottom();
    window.addEventListener("hashchange", markActiveTab);
  });
})();
