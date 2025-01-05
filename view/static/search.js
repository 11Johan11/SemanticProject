let searchTimeout;



document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const searchSwitchButtons = document.querySelectorAll('#search-switch');

    let type = searchInput.dataset.type; //determine if searching for actors/movies based on data attribute
    let placeholderText = "Search for " + type + "...";


    setupSearch(type, placeholderText);

 //listen for button click, setupSearch again
  searchSwitchButtons.forEach((button) => {
    button.addEventListener('click', function () {
      newType = button.title.toLowerCase(); //use buttons title to assign data-type to the searchInput
      let type = newType;
      console.log(type);
      searchInput.setAttribute('data-type', newType);
      setupSearch(newType, "Search for " + newType + "...");
      updateButtonStyles(button);
    });
  });

function updateButtonStyles(activeButton) {
searchSwitchButtons.forEach((button) => {
  if (button === activeButton) {
    button.classList.add('btn-primary');
    button.classList.remove('btn-outline-secondary');
  } else {
    button.classList.add('btn-outline-secondary');
    button.classList.remove('btn-primary');
  }
});
}

});

function setupSearch(type, placeholderText) {
    const searchInput = document.getElementById('search-input');
    console.log(type);
    showInfoText(placeholderText);

    searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        const query = searchInput.value.trim();
        //console.log(query);
        if (query.length >= 3) {
            clearScrollContainer();
            showLoadingIndicator();
            searchTimeout = setTimeout(() => {
                performSearch(query, type);
            }, 2000); //debounce for 2 seconds
        } else {
            clearScrollContainer(type);
            showInfoText(placeholderText);
        }
    });
}

function clearScrollContainer() {
    const row = document.getElementById(`replace`);
    row.innerHTML = ''; //clear the scrollable container
}

function showInfoText(placeholderText) {
    const row = document.getElementById(`replace`);
    const infoHTML = `
    <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100px; color: #6c757d; text-align: center;">
      <i class="bi bi-search" style="font-size: 2rem; margin-bottom: 10px;"></i>
      <div style="font-size: 1.2rem; font-weight: bold;">${placeholderText}</div>
    </div>`;
    row.innerHTML = infoHTML;
}

function showLoadingIndicator() {
    const row = document.getElementById(`replace`);
    const loadingHTML = `
      <div class="d-flex justify-content-center align-items-center" style="height: 100px;">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>`;
    row.innerHTML = loadingHTML;
}

function performSearch(query, type) {
    fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                query
            }),
        })
        .then((response) => response.json())
        .then((data) => {
            console.log('Search Results:', data);
            updateDraggableWidgets(data.results, type);
        })
        .catch((error) => console.error('Search Error:', error));
}

function updateDraggableWidgets(results, type) {
    const row = document.getElementById(`replace`);
    row.innerHTML = '';

    console.log(results);
    console.log(type);
    if (type=="movie") {
        results.forEach((item) => {
            const widgetHTML = `
              <div class="col-6">
                <div class="grid-stack-item draggable-widget newWidget" style="background-image: url('${item.poster}'); background-size: cover; background-position: center;" 
                  gs-w="3" gs-h="2"
                  data-meta='${JSON.stringify(item)}'>
                  <div class="widget-title-bar">
                    ${item.name}
                  </div>
                </div>
              </div>`;
            row.innerHTML += widgetHTML;
        });
    }//TODO: add specific widgets for actors

    // Setup drag-in for draggable widgets
    GridStack.setupDragIn(`.scroll-container > .row > .col-6 > .grid-stack-item`, {
        width: 3, //grid columns
        height: 2, //grid rows
    });
}
