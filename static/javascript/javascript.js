// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Menu toggle functionality - fixed to avoid the hamburger being covered
    const menuButton = document.querySelector('.menu-button');
    const menu = document.getElementById('sideMenu');
    
    function toggleMenu() {
        menu.classList.toggle('active');
    }
    
    menuButton.addEventListener('click', toggleMenu);
    
    // Close menu when clicking outside, but not when clicking the menu button
    document.addEventListener('click', function(event) {
        const isClickInsideMenu = menu.contains(event.target);
        const isClickOnMenuButton = menuButton.contains(event.target);
        
        if (!isClickInsideMenu && !isClickOnMenuButton && menu.classList.contains('active')) {
            toggleMenu();
        }
    });
    
    // Profile menu toggle with improved event handling
    const profileButton = document.getElementById('profileButton');
    const profileMenu = document.getElementById('profile-icon-menu');
    
    profileButton.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent document click from immediately closing the menu
        profileMenu.style.display = profileMenu.style.display === 'block' ? 'none' : 'block';
    });
    
    // Close profile menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideProfileMenu = profileMenu.contains(event.target);
        const isClickOnProfileButton = profileButton.contains(event.target);
        
        if (!isClickInsideProfileMenu && !isClickOnProfileButton && profileMenu.style.display === 'block') {
            profileMenu.style.display = 'none';
        }
    });
    
    // Enhanced search functionality with proper focus handling
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    let searchTimeout;
    
    searchInput.addEventListener('focus', function() {
        if (this.value.length > 0) {
            searchResults.style.display = 'block';
        }
    });
    
    searchInput.addEventListener('blur', function(e) {
        // Small delay to allow for clicking on results
        searchTimeout = setTimeout(() => {
            if (!searchResults.contains(document.activeElement)) {
                searchResults.style.display = 'none';
            }
        }, 150);
    });
    
    searchInput.addEventListener('input', debounce(function() {
        // Clear existing timeout to prevent race conditions
        if (searchTimeout) {
            clearTimeout(searchTimeout);
        }
        
        // Improved search results handling
        if (this.value.length > 0) {
            searchResults.innerHTML = '';
            
            // Sample results - replace with actual API call in production
            const mockResults = [
                'Astronomy',
                'Space Exploration',
                'Black Holes',
                'NASA News',
                'Exoplanets',
                'Solar System',
                'Nebulae',
                'Space Telescopes',
                'Cosmic Events'
            ];
            
            const query = searchInput.value.toLowerCase();
            const filteredResults = mockResults.filter(result => 
                result.toLowerCase().includes(query)
            );
            
            if (filteredResults.length > 0) {
                filteredResults.forEach(result => {
                    const li = document.createElement('li');
                    li.textContent = result;
                    li.addEventListener('click', function() {
                        searchInput.value = result;
                        searchResults.style.display = 'none';
                    });
                    searchResults.appendChild(li);
                });
                searchResults.style.display = 'block';
            } else {
                const li = document.createElement('li');
                li.textContent = 'No results found';
                li.style.opacity = '0.7';
                li.style.fontStyle = 'italic';
                searchResults.appendChild(li);
                searchResults.style.display = 'block';
            }
        } else {
            searchResults.style.display = 'none';
        }
    }, 250)); // Debounce to prevent excessive calculations
    
    // Space quotes with better animation
    const quotes = [
        "The Earth is the cradle of humanity, but mankind cannot stay in the cradle forever. - Konstantin Tsiolkovsky",
        "Space is for everybody. It's not just for a few people in science or math, or for a select group of astronauts. That's our new frontier out there, and it's everybody's business to know about space. - Christa McAuliffe",
        "Somewhere, something incredible is waiting to be known. - Carl Sagan",
        "The important achievement of Apollo was demonstrating that humanity is not forever chained to this planet and our visions go rather further than that and our opportunities are unlimited. - Neil Armstrong",
        "Space, the final frontier. - Gene Roddenberry",
        "There are no constraints on the human mind, no walls around the human spirit, no barriers to our progress except those we ourselves erect. - Ronald Reagan",
        "Exploration is really the essence of the human spirit. - Frank Borman",
        "We choose to go to the moon in this decade and do the other things, not because they are easy, but because they are hard. - John F. Kennedy",
        "The cosmos is within us. We are made of star-stuff. We are a way for the universe to know itself. - Carl Sagan",
        "The most beautiful experience we can have is the mysterious. It is the fundamental emotion that stands at the cradle of true art and true science. - Albert Einstein",
        "We are all connected; To each other, biologically. To the earth, chemically. To the rest of the universe, atomically. - Neil deGrasse Tyson",
        "The Earth is a very small stage in a vast cosmic arena. - Carl Sagan",
        "Space exploration is a force of nature unto itself that no other force in society can rival. - Neil deGrasse Tyson",
        "We are an impossibility in an impossible universe. - Ray Bradbury",
        "Once we get to the moon, we will have learned so much more about the universe and about Earth. - Jim Lovell",
        "To confine our attention to terrestrial matters would be to limit the human spirit. - Stephen Hawking",
        "We are stardust brought to life, then empowered by the universe to figure itself out — and we have only just begun. - Neil deGrasse Tyson",
        "The universe is under no obligation to make sense to you. - Neil deGrasse Tyson",
    ];
    
    const quoteElement = document.getElementById('quote');
    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
    
    quoteElement.textContent = randomQuote;
    
    // Fade in the quote with a slight delay for better UX
    setTimeout(() => {
        quoteElement.style.opacity = 1;
    }, 1200);
    
    // Create star particles for background with improved rendering performance
    //createStars();
    
    // Improved parallax effect with throttling for performance
    document.addEventListener('mousemove', throttle(function(e) {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        document.body.style.backgroundPosition = `${50 + (x - 0.5) * 10}% ${50 + (y - 0.5) * 10}%`;
    }, 50));
    
    // Add smooth scroll for buttons
    document.getElementById('getStartedBtn').addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector('.quote-container').scrollIntoView({
            behavior: 'smooth'
        });
    });
    
    // Initialize animation for hero content
    animateHeroContent();
});

// Create star particles with better performance
function createStars() {
    const starsContainer = document.createElement('div');
    starsContainer.className = 'stars';
    document.body.appendChild(starsContainer);
    
    // Use document fragment for better performance
    const fragment = document.createDocumentFragment();
    
    for (let i = 0; i < 150; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.top = `${Math.random() * 100}%`;
        star.style.left = `${Math.random() * 100}%`;
        
        // Vary star sizes for more realistic effect
        const size = Math.random() * 2 + 1;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        
        // Add variable animation for more natural twinkling
        star.style.animationDelay = `${Math.random() * 3}s`;
        star.style.animationDuration = `${Math.random() * 3 + 1}s`;
        
        fragment.appendChild(star);
    }
    
    starsContainer.appendChild(fragment);
    
    // Add cosmic dust effect - positioned behind the Earth background
    const cosmicDust = document.createElement('div');
    cosmicDust.className = 'cosmic-dust';
    document.body.appendChild(cosmicDust);
}

// Search page redirection with query handling
function redirectToPage() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput.value.trim() !== '') {
        // Replace with actual search page URL
        window.location.href = `search.html?q=${encodeURIComponent(searchInput.value)}`;
    }
}

// Animation for hero content
function animateHeroContent() {
    const heroContent = document.querySelector('.hero-content');
    
    // Animate hero content on page load
    heroContent.style.opacity = '0';
    heroContent.style.transform = 'translateY(30px)';
    
    setTimeout(() => {
        heroContent.style.transition = 'opacity 1s ease-out, transform 1s ease-out';
        heroContent.style.opacity = '1';
        heroContent.style.transform = 'translateY(0)';
    }, 300);
}

// Utility function to debounce frequent events
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

// Utility function to throttle frequent events
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}



document.getElementById('image-upload').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const previewContainer = document.getElementById('image-preview-container');
    const previewImage = document.getElementById('image-preview');

    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewContainer.style.display = 'block';
        }
        reader.readAsDataURL(file);
    } else {
        previewContainer.style.display = 'none';
        previewImage.src = '#';
    }
});

// Add this code for the cancel button functionality
document.addEventListener('DOMContentLoaded', function() {
    const cancelButton = document.getElementById('cancel-image-upload');
    const imageInput = document.getElementById('image-upload');
    const previewContainer = document.getElementById('image-preview-container');
    const previewImage = document.getElementById('image-preview');
    
    // Cancel image upload when button is clicked
    cancelButton.addEventListener('click', function() {
        // Clear the file input
        imageInput.value = '';
        
        // Hide the preview
        previewContainer.style.display = 'none';
        
        // Clear the preview image src
        previewImage.src = '#';
    });
});


// Notification dropdown toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const notificationBtn = document.getElementById('uplnotificationButton');
    const notificationsDropdown = document.getElementById('notifications-dropdown');
    const profileButton = document.getElementById('profileButton');
    const profileIconMenu = document.getElementById('profile-icon-menu');
    
    // Toggle notification dropdown
    notificationBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        
        // Close profile menu if open
        if (profileIconMenu.style.display === 'block') {
            profileIconMenu.style.display = 'none';
        }
        
        // Toggle notification dropdown
        if (notificationsDropdown.style.display === 'block') {
            notificationsDropdown.style.display = 'none';
        } else {
            notificationsDropdown.style.display = 'block';
        }
    });
    
    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!notificationBtn.contains(e.target) && !notificationsDropdown.contains(e.target)) {
            notificationsDropdown.style.display = 'none';
        }
        
        if (!profileButton.contains(e.target) && !profileIconMenu.contains(e.target)) {
            profileIconMenu.style.display = 'none';
        }
    });
    
    // Add animation to notification bell
    notificationBtn.querySelector('i').classList.add('fa-beat');
    setTimeout(() => {
        notificationBtn.querySelector('i').classList.remove('fa-beat');
    }, 2000);
});
        // Post Settings functionality
        document.addEventListener('DOMContentLoaded', function() {
            // Add click event listeners for all post settings buttons
            const settingsButtons = document.querySelectorAll('.post-settings-button');
            
            settingsButtons.forEach(button => {
                button.addEventListener('click', function(e) {
                    e.stopPropagation(); // Prevent event bubbling
                    const postId = this.getAttribute('data-post-id');
                    const dropdown = document.getElementById(`post-settings-${postId}`);
                    
                    // Close all other dropdowns
                    document.querySelectorAll('.post-settings-dropdown.active').forEach(activeDropdown => {
                        if (activeDropdown !== dropdown) {
                            activeDropdown.classList.remove('active');
                        }
                    });
                    
                    // Toggle current dropdown
                    dropdown.classList.toggle('active');
                });
            });
            
            // Delete post functionality
            document.querySelectorAll('.delete-post').forEach(item => {
                item.addEventListener('click', function() {
                    const postId = this.getAttribute('data-post-id');
                    if (confirm('Are you sure you want to delete this post? This action cannot be undone.')) {
                        window.location.href = `/delete-post/${postId}`;
                    }
                });
            });
            
            // Edit post functionality
            document.querySelectorAll('.edit-post').forEach(item => {
                item.addEventListener('click', function() {
                    const postId = this.getAttribute('data-post-id');
                    window.location.href = `/edit-post/${postId}`;
                });
            });
            
            // Save post functionality
            document.querySelectorAll('.save-post').forEach(item => {
                item.addEventListener('click', function() {
                    const postId = this.getAttribute('data-post-id');
                    // Call the save post functionality - this would be an AJAX call to your backend
                    savePost(postId);
                });
            });
            
            // Copy link functionality
            document.querySelectorAll('.copy-link').forEach(item => {
                item.addEventListener('click', function() {
                    const postId = this.getAttribute('data-post-id');
                    const postLink = `${window.location.origin}/post/${postId}`;
                    navigator.clipboard.writeText(postLink).then(() => {
                        alert('Post link copied to clipboard!');
                    });
                });
            });
            
            // Report post functionality
            document.querySelectorAll('.report-post').forEach(item => {
                item.addEventListener('click', function() {
                    const postId = this.getAttribute('data-post-id');
                    // You could redirect to a form or open a modal
                    window.location.href = `/report-post/${postId}`;
                });
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.post-settings-dropdown') && !e.target.closest('.post-settings-button')) {
                    document.querySelectorAll('.post-settings-dropdown.active').forEach(dropdown => {
                        dropdown.classList.remove('active');
                    });
                }
            });
            
            // Function to save a post (would call your backend API)
            function savePost(postId) {
                // This would be an AJAX call to your backend
                fetch(`/save-post/${postId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Post saved successfully!');
                    } else {
                        alert('Error saving post: ' + data.error);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred while saving the post.');
                });
            }
            
            // Function to get CSRF token from cookies
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
        });