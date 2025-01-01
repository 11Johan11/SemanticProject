let searchTimeout;

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const type = searchInput.dataset.type; //determine if searching for actors/movies based on data attribute
    const placeholderText = type === 'movies' 
        ? 'Search for a movie to get started!' 
        : 'Search for an actor to get started!';
    setupSearch(type, placeholderText);
});

function setupSearch(type, placeholderText) {
    const searchInput = document.getElementById('search-input');
    showInfoText(placeholderText);

    searchInput.addEventListener('input', function () {
        clearTimeout(searchTimeout);
        const query = searchInput.value.trim();
        console.log(query);
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
    if (type=="movies") {
        results.forEach((item) => {
            const widgetHTML = `
              <div class="col-6">
                <div class="grid-stack-item draggable-widget newWidget" style="background-image: url('${item.poster}'); background-size: cover; background-position: center;" 
                  gs-w="3" gs-h="2"
                  data-meta='${JSON.stringify(item)}'>
                  <div class="widget-title-bar">
                    ${item.title}
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
