let searchTimeout;

document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const searchSwitchButtons = document.querySelectorAll('#search-switch');
    const searchButton = document.getElementById('search-button');

    let type = searchInput.dataset.type;
    let placeholderText = "Search for " + type + "...";

    //init search
    setupSearch(type, placeholderText);

    //listen for button click to switch type
    searchSwitchButtons.forEach((button) => {
        button.addEventListener('click', function () {
            const newType = button.title.toLowerCase();
            if (type !== newType) {
                type = newType; // Update the global `type`
                searchInput.setAttribute('data-type', newType);
                console.log('Switched to type:', type);
                setupSearch(newType, "Search for " + newType + "...");
                updateButtonStyles(button);
            }
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

    function setupSearch(type, placeholderText) {
        console.log('Setting up search for type:', type);

        //clean up previous event listeners
        searchInput.removeEventListener('input', handleInput);
        searchInput.removeEventListener('keydown', handleKeydown);
        searchButton.removeEventListener('click', handleClick);

        //update placeholder text
        showInfoText(placeholderText);

        //add new event listeners
        searchInput.addEventListener('input', handleInput);
        searchInput.addEventListener('keydown', handleKeydown);
        searchButton.addEventListener('click', handleClick);
    }

    function handleInput() {
        clearTimeout(searchTimeout);
        const query = searchInput.value.trim();
        if (query.length >= 3) {
            searchTimeout = setTimeout(() => {
                clearScrollContainer();
                showLoadingIndicator();
                performSearch(query, type);
            }, 2000); //debounce for 2 seconds (delay for auto search when not clicking search or enter)
        }
    }

    function handleKeydown(event) {
        if (event.key === 'Enter') {
            clearTimeout(searchTimeout);
            const query = searchInput.value.trim();
            if (query.length >= 3) {
                clearScrollContainer();
                showLoadingIndicator();
                performSearch(query, type);
            }
        }
    }

    function handleClick() {
        clearTimeout(searchTimeout);
        const query = searchInput.value.trim();
        if (query.length >= 3) {
            clearScrollContainer();
            showLoadingIndicator();
            performSearch(query, type);
        }
    }

    function clearScrollContainer() {
        const row = document.getElementById('replace');
        row.innerHTML = ''; //clear the scrollable container
    }

    function showInfoText(placeholderText) {
        const row = document.getElementById('replace');
        const infoHTML = `
        <div class="d-flex flex-column justify-content-center align-items-center" style="height: 100px; color: #6c757d; text-align: center;">
          <i class="bi bi-search" style="font-size: 2rem; margin-bottom: 10px;"></i>
          <div style="font-size: 1.2rem; font-weight: bold;">${placeholderText}</div>
        </div>`;
        row.innerHTML = infoHTML;
    }

    function showLoadingIndicator() {
        const row = document.getElementById('replace');
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
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query, type }),
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Search Results:', data);
                updateDraggableWidgets(data.results, type);
            })
            .catch((error) => console.error('Search Error:', error));
    }

function updateDraggableWidgets(results, type) {
  const row = document.getElementById('replace');
  row.innerHTML = ''; //clear previous widgets

  //avoid adding multiple click listeners if called multiple times:
  if (row._rowClickHandler) {
    row.removeEventListener('click', row._rowClickHandler);
  }

  //CONFIG for types and future types
  const typeConfig = {
    movie:    { gsWidth: 3, gsHeight: 5, imageKey: 'poster' },
    actor:    { gsWidth: 2, gsHeight: 2, imageKey: 'profile' },
    director: { gsWidth: 2, gsHeight: 2, imageKey: 'poster' }, //add more here
  };

  //fallback
  const config = typeConfig[type] || { gsWidth: 2, gsHeight: 3, imageKey: 'poster' };


  //populate with the new widgets from the search results
  results.forEach((item) => {
    const widgetHTML = `
      <div class="col-6">
        <div class="grid-stack-item draggable-widget newWidget"
             style="background-image: url('${item[config.imageKey]}');
                    background-size: cover; 
                    background-position: center;"
             gs-w="${config.gsWidth}"
             gs-h="${config.gsHeight}"
             data-meta='${JSON.stringify(item)}'>
          <div class="widget-title-bar">${item.name}</div>
        </div>
      </div>`;
    row.innerHTML += widgetHTML;
  });

  //allow them to be dragged in
  GridStack.setupDragIn(`.scroll-container > .row > .col-6 > .grid-stack-item`, {
    width:  config.gsWidth,
    height: config.gsHeight,
  });

  //function to add a widget when clicked
  function addWidgetToGrid(item) {
    const metadata = JSON.parse(item.getAttribute('data-meta'));

    //build the widget HTML
    const widgetHTML = `
      <div class="grid-stack-item" data-meta='${JSON.stringify(metadata)}'
           gs-w="${config.gsWidth}"
           gs-h="${config.gsHeight}">
        <div class="grid-stack-item-content"
             style="background-image: url('${metadata[config.imageKey]}');
                    background-size: cover; 
                    background-position: center;">
          <div class="widget-title-bar">${metadata.name}</div>
        </div>
      </div>`;

    //parse the html (makeWidget function demanded this)
    const template = document.createElement('template');
    template.innerHTML = widgetHTML.trim();
    const widgetElement = template.content.firstChild;

    //add the widget to the grid / the grid is defined globally in window.grid  :)
    grid.makeWidget(widgetElement);
  }

  //create a single click handler and store it in row, so it can be removed later to avoid strange glitches
  row._rowClickHandler = function(event) {
    const target = event.target.closest('.draggable-widget');
    if (target) {
      addWidgetToGrid(target);
      const metadata = JSON.parse(target.getAttribute('data-meta'));
      console.log('Widget clicked:', metadata);
    }
  };

  //attach
  row.addEventListener('click', row._rowClickHandler);
}

});
