$(document).ready(function () {
    function fetchPosterURL(obj) {
        var posterURL = null;
        $.ajax({
            type: "GET",
            url: "/getPosterURL", 
            dataType: "json",
            data: { imdbID: obj.innerHTML },
            async: false, 
            success: function (response) {
                posterURL = response.posterURL;
                var poster = `<img src=${response.posterURL} alt="Movie Poster" 
                    class="poster-image" style="width: 75%; height: auto; margin: 0;"></img>`
                obj.innerHTML += poster;        
            },
            error: function (error) {
                console.log("Error fetching poster URL: " + error);
            },
        });
        return posterURL;
    };

    $('.imdbId').map((index, obj) => {
        fetchPosterURL(obj);
    });
    
    
});
  

document.addEventListener("DOMContentLoaded", function () {
    // Open Edit Profile Modal
    document.getElementById("editProfileBtn").addEventListener("click", () => {
      document.getElementById("editProfileModal").style.display = "block";
    });

    // Close Modal
    document.querySelector(".close").addEventListener("click", () => {
      document.getElementById("editProfileModal").style.display = "none";
    });

    // Profile Update Form Submission
    document.getElementById("updateProfileForm").addEventListener("submit", async (e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      const response = await fetch("/update_profile", {
        method: "POST",
        body: formData
      });
      if (response.ok) {
        alert("Profile updated successfully!");
        location.reload();
      } else {
        alert("Error updating profile!");
      }
    });
  });

  $(document).ready(function () {
// Load messages as soon as the page loads
loadMessages();

// Send Message
$('#sendMessageForm').submit(function (e) {
  e.preventDefault();

  const recipientUsername = $('#recipientUsername').val().trim();
  const content = $('#messageContent').val().trim();

  if (!recipientUsername || !content) {
    alert('Please fill in all fields.');
    return;
  }

  $.ajax({
    url: '/send_message',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({
      recipient_username: recipientUsername,
      content: content
    }),
    success: function (response) {
      alert('Message sent successfully!');
      $('#sendMessageForm')[0].reset();
      loadMessages(); // Reload messages after sending
    },
    error: function (xhr) {
      alert(`Error: ${xhr.responseJSON.error}`);
    }
  });
});

// Function to load messages
function loadMessages() {
  $.ajax({
    url: '/get_messages',
    type: 'GET',
    success: function (response) {
      const { received, sent } = response;

      // Populate received messages
      const receivedList = received.map(msg => `
        <li class="received" data-id="${msg.id}">
          <strong>${msg.sender}:</strong> ${msg.content} <small>(${msg.timestamp})</small>
          <button class="btn btn-danger delete-btn" data-id="${msg.id}">Read</button>
        </li>
      `).join('');
      $('#receivedMessages').html(receivedList || '<li>No received messages.</li>');

      // Populate sent messages
      const sentList = sent.map(msg => `
        <li class="sent" data-id="${msg.id}">
          <strong>To ${msg.recipient}:</strong> ${msg.content} <small>(${msg.timestamp})</small>
          <button class="btn btn-danger delete-btn" data-id="${msg.id}">Delete</button>
        </li>
      `).join('');
      $('#sentMessages').html(sentList || '<li>No sent messages.</li>');

      // Attach event listeners to delete buttons
      $('.delete-btn').on('click', function () {
        const messageId = $(this).data('id');
        console.log('Message ID:', messageId); // Check the message ID being passed
        if (messageId !== undefined) {
          deleteMessage(messageId);
        } else {
          console.error('No message ID found.');
        }
      });
    },
    error: function () {
      alert('Failed to load messages.');
    }
  });
}

// Function to delete message
function deleteMessage(messageId) {
  $.ajax({
    url: `/delete_message/${messageId}`,
    type: 'DELETE',
    success: function (response) {
      alert('Message deleted successfully!');
      loadMessages(); // Reload the messages after deletion
    },
    error: function (xhr) {
      alert(`Error: ${xhr.responseJSON.error}`);
    }
  });
}

});
