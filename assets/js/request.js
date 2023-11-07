function callPutPhotoApi(file,filename,labels) {
    // filename, labels, file?
    //file-> currently encoded base64
    var params = {
        'bucket': "my-photo-bucket-cc-bd",
        'object': filename,
        'x-amz-meta-customLabels': labels,
        'Content-Type': 'text/base64'

    };
    var body = {file}
    /*- in method reques add Content-Type: text/base64;
     custom label too
     file co
    integration request
     add stuff from headers 
     need to encode file into base64 via some built in javascript 
    */
   // first param: params, second body, third-> other
    return sdk.uploadBucketObjectPut(params,body,{})
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

  function callSearchPhotosApi(q) {
  //// have not implemented yet!
    return sdk.searchGet({},{},{})
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
///////////////////////////////
/////////event-stuff///////////
document.addEventListener('DOMContentLoaded', function () {
    const imageForm = document.getElementById('image-form');
    const searchForm = document.getElementById('search-form');
    const searchResults = document.getElementById('search-results');
    const uploadedImage = document.getElementById('uploaded-image');
    var base64String = null;
    // Handle image upload form submission
    imageForm.addEventListener('submit', function (event) {
        event.preventDefault();
        console.log(event)
        const imageInput = document.getElementById('image-input');
        const labelInput = document.getElementById('label-input');
        const formData = new FormData(imageForm);
        console.log(labelInput.value);
        const selectedImage = imageInput.files[0];
        var reader = new FileReader();
        reader.onload = function() {
            //console.log("reader.result: "+reader.result)
            base64String = btoa(reader.result);
            var filename = selectedImage.name;
            uploadedImage.src = URL.createObjectURL(selectedImage);
            //console.log("hello: "+base64String)
            callPutPhotoApi(base64String,filename,labelInput.value);
        };
        reader.readAsBinaryString(selectedImage);
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
