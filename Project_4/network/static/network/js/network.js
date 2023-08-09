function editPost(id) {
    contentdiv = document.querySelector("#postcontent_" + id);
    initialContent = contentdiv.innerHTML;
    contentdiv.innerHTML = '';
    document.querySelector("#edit_" + id).style.display = "none";

    // Replaces the div innerHTML with the textarea component
    var textarea = document.createElement('textarea');
    textarea.value = initialContent;
    textarea.style.width = "100%";

    // Renders the button for saving post
    var saveBtn = document.createElement('button');
    saveBtn.innerText = 'Save';
    saveBtn.onclick = function () {
        saveEditedPost(id, contentdiv, textarea);
    };

    // Renders the button if user cancels edit
    var cancelBtn = document.createElement('button');
    cancelBtn.innerText = 'Cancel';
    cancelBtn.onclick = function () {
        contentdiv.innerHTML = initialContent;
        document.querySelector("#edit_" + id).style.display = "block";
    };

    contentdiv.append(textarea);
    contentdiv.appendChild(saveBtn);
    contentdiv.appendChild(cancelBtn);
}

function saveEditedPost(id, contentdiv, textarea) {
    contentdiv.innerHTML = textarea.value;
    document.querySelector("#edit_" + id).style.display = "block";

    // Fetch request
    fetch("/saveEditedPost", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "id": id,
            "data": contentdiv.innerHTML
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(JSON.stringify({
            "id": id,
            "data": contentdiv.innerHTML
        }));
        console.log("Response from server:", data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

let isLikePost = true;

function updateLikes(likeElm) {
    if (likeElm.disabled) return;
    
    likeElm.disabled = true;
    id = likeElm.id.match(/\d+/)[0]

    dict_data = {"id": id}

    //  Add a like
    if (isLikePost) {
        // console.log("Add a like for " + likeElm.id);
        dict_data["like_post"] = true
    } 
    // Remove a like
    else {
        // console.log("Remove a like for " + likeElm.id);
        dict_data["like_post"] = false
    }

    // console.log(dict_data);

    // Fetch and update request
    fetch("/updateLikes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dict_data)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response from server:", data);

        // Update the like count
        document.querySelector("#likecount_" + id).textContent = data.data.likes; 
    })
    .catch(error => {
        console.error("Error:", error);
    });

    isLikePost = !isLikePost;
    likeElm.disabled = false;
}

// If onclick="likePost('{{post.id}}')" is used on the Div, it means that the first click 
// event triggers the likePost function and attaches the event listener, but it doesn't 
// actually execute the toggleFunctions logic for the first click.
document.addEventListener('DOMContentLoaded', function() {
    const likeElms = document.querySelectorAll('[id^="like_"]');
    likeElms.forEach(elm => {
        elm.addEventListener('click', function () {
            updateLikes(elm);
        });
    });
});
