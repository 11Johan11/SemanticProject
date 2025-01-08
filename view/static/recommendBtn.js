  //recommend
  document.addEventListener('DOMContentLoaded', function () {
  const recommendBtn = document.getElementById('recommendBtn');

  recommendBtn.addEventListener('click', function () {
    //gather all widgets in the dashboard
    const widgets = document.querySelectorAll('#advanced-grid .grid-stack-item');

    //extract metadata from each widget
    const allMetadata = Array.from(widgets).map(widget => {
      return JSON.parse(widget.getAttribute('data-meta'));
    });

    //send data to the server
    fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ movies: allMetadata }),
    })
      .then(response => response.json())
      .then(data => {
        console.log('Recommendation Response:', data);

       

// Limit the data to the first 100 entries
const limitedData = data.slice(0, 100);

// Define the parent container for widgets
const recommendationContent = document.getElementById('recommendationContent');
recommendationContent.innerHTML = ''; // Clear existing content if any

// Create movie widgets for each entry
limitedData.forEach((movie) => {
    // Generate a rating banner if points are available
    const ratingHTML = movie.points
        ? `
        <div style="
            position: absolute;
            top: 0;
            right: 0;
            width: 50px;
            height: 50px;
            background-color: #f1c40f;
            color: black;
            display: flex;
            align-items: flex-start;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
            clip-path: polygon(
                0% 0%, 100% 0%, 100% 100%, 
                85% 100%, 50% 75%, 15% 100%, 0% 100%
            );
            z-index: 5;"
            title="Recommendation Points">
            ${Math.round(movie.points)}
        </div>
        `
        : '';

            // Generate the widget HTML
            const widgetHTML = `
                <div class="col-md-4 mb-4">
                    <div class="position-relative" style="
                        background-image: url('https://via.placeholder.com/300'); /* Fallback image */
                        background-image: url('${movie.movie_uri.replace(
                            'http://www.wikidata.org/entity/',
                            'https://image.tmdb.org/t/p/w500/'
                        )}');
                        background-size: cover; 
                        background-position: center; 
                        border-radius: 8px;
                        height: 250px; /* Adjust height for widgets */
                        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        overflow: hidden;">
                        ${ratingHTML}
                        <div class="position-absolute bottom-0 w-100 text-center text-white" style="
                            background: rgba(0, 0, 0, 0.7);
                            padding: 8px 0;">
                            <strong>${movie.genres[0] || 'Genre Unknown'}</strong>
                        </div>
                    </div>
                </div>`;
            
            // Inject the widget into the modal content
            recommendationContent.innerHTML += widgetHTML;
        });

        // Initialize and show the modal
        const recommendModal = new bootstrap.Modal(document.getElementById('recommendModal'), {});
        recommendModal.show();


        alert(`Server Response: ${data.message}`);
      })
      .catch(err => console.error('Error in /recommend request:', err));
  });
});