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
        alert(`Server Response: ${data.message}`);
      })
      .catch(err => console.error('Error in /recommend request:', err));
  });
});