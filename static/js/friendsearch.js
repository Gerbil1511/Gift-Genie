// Wait until the document is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Get the search usernames URL from the template
    var searchUsernamesUrl = "{% url 'search_usernames' %}";
    
    // Attach an event listener to the search button
    document.getElementById('search-button').addEventListener('click', function () {
        // Get the current value of the search query
        var query = document.getElementById('search_query').value;
        
        // Check if the input length is greater than 2 characters
        if (query.length > 2) {
            // Make a Fetch request to the search usernames endpoint
            fetch(searchUsernamesUrl + '?term=' + query)
                .then(response => response.json())
                .then(data => {
                    // Get the search results div in the template
                    var searchResults = document.getElementById('search-results');
                    
                    // Clear any existing results
                    searchResults.innerHTML = '';

                    // Check if any users were found
                    if (data.length > 0) {
                        // Iterate over the returned data (list of users)
                        data.forEach(function (user) {
                            // Create a div for each user
                            var resultItem = document.createElement('div');
                            resultItem.className = 'search-result-item';
                            
                            // Create an image element for the user's profile image
                            var img = document.createElement('img');
                            img.src = user.profile_image || 'https://res.cloudinary.com/dqm93egis/image/upload/v1738488445/nobody_l7bbqh.jpg';
                            img.className = 'rounded-circle';
                            img.style.width = '50px';
                            img.style.height = '50px';
                            img.style.objectFit = 'cover';
                            img.style.marginRight = '10px';
                            
                            // Create a span element for the user's username
                            var span = document.createElement('span');
                            span.textContent = user.username;
                            
                            // Append the image and span to the result item
                            resultItem.appendChild(img);
                            resultItem.appendChild(span);
                            
                            // Append the result item to the search results div
                            searchResults.appendChild(resultItem);
                        });
                    } else {
                        // If no users found, show a message
                        var noResults = document.createElement('div');
                        noResults.textContent = 'No registered user found with that username.';
                        searchResults.appendChild(noResults);
                    }
                })
                .catch(error => console.error('Error fetching usernames:', error));
        }
    });
});