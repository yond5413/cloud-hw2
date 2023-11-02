function callPutPhotoApi(filename,labels) {
    // filename, labels, file?
    return sdk.Post({},{})
    /*return sdk.chatbotPost({}, {
      messages: [{
        type: 'unstructured',
        unstructured: {
          text: message
        }
      }]
    }, {});*/
  }

/////////event-stuff///////////
document.addEventListener('DOMContentLoaded', function () {
    const imageForm = document.getElementById('image-form');
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');
    const uploadedImage = document.getElementById('uploaded-image');

    // Handle image upload form submission
    imageForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const imageInput = document.getElementById('image-input');
        const labelInput = document.getElementById('label-input');

        const formData = new FormData(imageForm);

        // You can send the form data to the server for processing here
        // For now, we'll just display the selected image
        const selectedImage = imageInput.files[0];
        uploadedImage.src = URL.createObjectURL(selectedImage);
    });

    // Handle search form submission
    searchForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const searchKeyword = document.getElementById('search-keyword').value;

        // You can implement the search functionality here
        // For now, let's just display the search keyword in the results
        searchResults.innerHTML = `Search results for: ${searchKeyword}`;
    });
});
