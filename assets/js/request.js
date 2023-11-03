function callPutPhotoApi(file,filename,labels) {
    // filename, labels, file?
    var other_headers = {
      headers:{
        'filename': filename,
        'x-amz-meta-customLabels': labels
      }
    };
    return sdk.upload.post({},file,other_headers)
    .then(function (result) {
      // Handle the successful response
      console.log("API response:", result);
      return result;
  })
  .catch(function (error) {
      // Handle errors
      console.error("API error:", error);
      throw error; // Propagate the error for further handling if needed
  });
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
        console.log(labelInput.value);
        // You can send the form data to the server for processing here
        // For now, we'll just display the selected image
        const selectedImage = imageInput.files[0];
        console.log(selectedImage);
        console.log(selectedImage.name);
        var filename = selectedImage.name;
        uploadedImage.src = URL.createObjectURL(selectedImage);
        callPutPhotoApi(selectedImage,filename,labelInput.value);
        
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
