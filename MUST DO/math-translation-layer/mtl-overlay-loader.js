/**
 * MTL Overlay Loader
 * Fetches reviewed translations from /shared/data/mtl-overlay-translations.json
 * and exposes them as window.MATH_TRANSLATION_TABLE_V2 before the overlay runs.
 */
(function(){
  function load(){
    fetch('/shared/data/mtl-overlay-translations.json')
      .then(function(res){ return res.json(); })
      .then(function(data){
        if(Array.isArray(data)){
          window.MATH_TRANSLATION_TABLE_V2 = data;
        }
      })
      .catch(function(err){
        // No reviewed table is fine; the overlay will fall back to heuristic translation.
        console.warn('[MTL] Could not load reviewed translations:', err);
      });
  }

  if(document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', load);
  } else {
    load();
  }
})();
