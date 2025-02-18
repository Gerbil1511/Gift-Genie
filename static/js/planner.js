document.addEventListener('DOMContentLoaded', function() {
    // Declare calendar variable outside the fetch scope
    let calendar;
    const calendarEl = document.getElementById('calendar');

    // Get modal and form elements
    const eventModal = new bootstrap.Modal(document.getElementById('eventModal'));
    const eventForm = document.getElementById('eventForm');
    const eventTitle = document.getElementById('eventTitle');
    const eventStart = document.getElementById('eventStart');
    const eventEnd = document.getElementById('eventEnd');
    const eventDescription = document.getElementById('eventDescription');
    const eventId = document.getElementById('eventId');
    const saveEventButton = document.getElementById('saveEvent');
    const deleteEventButton = document.getElementById('deleteEvent');

    // Initialize calendar and load events
    fetch('/planner/get-events/')  // Match the URL in your Django urls.py
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            calendar = new FullCalendar.Calendar(calendarEl, {
                initialView: 'dayGridMonth',
                editable: true,
                selectable: true,
                events: data.events.map(event => ({
                    id: event.id,
                    title: event.title,
                    start: event.start,
                    end: event.end,
                    color: event.user === event.is_friend ? '#3788d8' : '#6c757d', // Color coding
                    extendedProps: {
                        description: event.description || '' // Store description for later use
                    }
                })),
                dateClick: function(info) {
                    openModal(null, info.dateStr);
                },
                eventClick: function(info) {
                    console.log("event clicked:", info.event);
                    openModal(info.event);
                }
            });
            calendar.render();
        })
        .catch(error => {
            console.error('Error fetching events:', error);
        });

    const allDayCheckbox = document.getElementById('allDayCheckbox');

    // Function to open the modal
    function openModal(event, dateStr) {
        if (event) {
            // Editing an existing event
            eventId.value = event.id;
            eventTitle.value = event.title;
            eventStart.value = event.start ? new Date(event.start).toISOString().slice(0, 16) : '';
            eventEnd.value = event.end ? new Date(event.end).toISOString().slice(0, 16) : '';
            eventDescription.value = event.extendedProps.description || '';
            allDayCheckbox.checked = event.allDay || false;
            deleteEventButton.style.display = 'inline-block';
        } else {
            // Adding a new event
            eventId.value = '';
            eventTitle.value = '';
            eventStart.value = dateStr ? new Date(dateStr).toISOString().slice(0, 16) : '';
            eventEnd.value = '';
            eventDescription.value = '';
            allDayCheckbox.checked = false;
            deleteEventButton.style.display = 'none';
        }
        eventModal.show();
    }

    // auto-disable time fields when "All-Day" is checked
    allDayCheckbox.addEventListener('change', function() {
        if (this.checked) {
            eventStart.type = 'date';
            eventEnd.type = 'date';
        } else {
            eventStart.type = 'datetime-local';
            eventEnd.type = 'datetime-local';
        }
    });


    // Save event (Create/Update)
    saveEventButton.addEventListener('click', function() {
        const eventData = {
            id: eventId.value,
            title: eventTitle.value,
            start: eventStart.value,
            end: eventEnd.value || null,
            description: eventDescription.trim || ''
        };

        // Determine endpoint (add or edit)
        const url = eventData.id 
            ? `/planner/edit/${eventData.id}/`  // Match Django URL pattern
            : '/planner/add/';

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(eventData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                console.log("Event saved successfully!");
                calendar.removeAllEvents();
                calendar.refetchEvents();  // Force refresh events from the server
                eventModal.hide();
            } else {
                console.error('Server error:', data.errors || data.error); // Log form errors
            }
        })
        .catch(error => {
            console.error('Fetch error:', error); // Log network/parsing errors
        });
    });

    // Delete event
    deleteEventButton.addEventListener('click', function() {
        if (confirm('Are you sure?')) {
            fetch(`/planner/delete/${eventId.value}/`, {  // Match Django URL pattern
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    calendar.removeAllEvents();
                    calendar.refetchEvents();  // Force refresh events from server
                    eventModal.hide();
                } else {
                    console.error('Server error:', data.errors || data.error); // Log form errors
                }
            })
            .catch(error => {
                console.error('Fetch error:', error); // Log network/parsing errors
            });
        }
    });

    // CSRF token function
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

