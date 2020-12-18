window.alert("hello!")

function processForm(evt){
    evt.preventDefault();
 

        method: "POST",
    url: "/api/search",
    contentType: "application/json",
    data: JSON.stringify({
      //brand: $("#brand").val(),
      productname: $("#productname").val(),
      //version: $("#version").val(),
    }),
    success: handleResponse // if success call handleResponse function

    })
}

function handleResponse(resp){
    if ("errors" in resp) {
        // received errors from API:
        //   for each error, put message next to corresponding field
    
        for (let fld in resp.errors) {
          $(`#${fld}-err`).text(resp.errors[fld]);
        }
      }
    
      else {
    
        $("#result").text(resp);
      }
  
} 



$("#search-form").on("submit",processForm)



