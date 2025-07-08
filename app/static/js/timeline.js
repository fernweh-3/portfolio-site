/* Selecting the HTML form and adding a 'submit' event listener */

const form = document.getElementById('timelineForm');
const timelinePosts = document.getElementById("timelinePosts");


function formatToPythonDateUTC(datetimeStr) {
    const date = new Date(datetimeStr);
    const pad = (n) => n.toString().padStart(2, '0');

    const year = date.getUTCFullYear();
    const month = pad(date.getUTCMonth() + 1);
    const day = pad(date.getUTCDate());
    const hour = pad(date.getUTCHours());
    const minute = pad(date.getUTCMinutes());
    const second = pad(date.getUTCSeconds());

    return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}


function createPostCard(data) {
    const emailHash = CryptoJS.SHA256(data.email.trim().toLowerCase()).toString();
    const avatarUrl = `https://www.gravatar.com/avatar/${emailHash}?d=identicon`;
    const formattedDate = formatToPythonDateUTC(data.created_at);

    const post = document.createElement('div');
    post.className = 'card shadow-sm';
    post.id = `post-${data.id}`;
    post.innerHTML = `
        <div class="card-body d-flex align-items-start">
            <img src="${avatarUrl}" alt="Avatar" class="rounded-circle me-3 mt-1" width="50" height="50">
            <div class="flex-grow-1">
                <h5 class="card-title mb-1">${data.name}</h5>
                <small class="text-muted">${data.email}</small>
                <p class="card-text mt-2">${data.content}</p>
                <small class="text-muted">Posted on ${formattedDate}</small>
            </div>
            <button class="btn btn-outline-danger btn-sm ms-3 delete-post" data-id="${data.id}">Delete</button>
        </div>
    `;
    return post;
}


document.addEventListener("DOMContentLoaded", function () {
    // setting up the Gravatar images for existing posts
    const avatarImgs = document.querySelectorAll('img[data-email]');
    avatarImgs.forEach(img => {
        const email = img.getAttribute('data-email').trim().toLowerCase();
        const hash = CryptoJS.SHA256(email).toString();
        img.src = `https://www.gravatar.com/avatar/${hash}?d=identicon`;
    });
});

form.addEventListener('submit', function(e) {
    e.preventDefault()

    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.disabled = true; // Disable the button to prevent multiple submissions
    submitBtn.textContent = 'Submitting...'; // Change button text

    // Create payload as new FormData object:
    const payload = new FormData(form);

    // Post the payload using Fetch:
    fetch('/api/timeline_post', {
    method: 'POST',
    body: payload,
    })
    .then(res => res.json())
    .then(data => {
        if (!data || !data.id) {
            alert("Failed to create post. Please try again.");
            return;
        }
        submitBtn.disabled = false; // Re-enable the button
        submitBtn.textContent = 'Submit'; // Reset button text

        let newPost = createPostCard(data);
        timelinePosts.prepend(newPost);
        form.reset(); // Reset the form after submission
    })
})


document.addEventListener('click', function (e) {
    if (e.target.classList.contains('delete-post')) {
        const postId = e.target.getAttribute('data-id');
        if (!postId) return;

        // delete the post by sending a DELETE request to the server
        fetch(`/api/timeline_post/${postId}`, {
            method: 'DELETE',
        })
        .then(res => {
            if (res.ok) {
                const postElement = document.getElementById(`post-${postId}`);
                console.log("Post deleted:", postElement);
                if (postElement) {
                    postElement.remove();
                }
            } else {
                alert("Failed to delete post.");
            }
        })
        .catch(err => {
            console.error("Delete failed:", err);
            alert("Error occurred while deleting post.");
        });
    }
});


