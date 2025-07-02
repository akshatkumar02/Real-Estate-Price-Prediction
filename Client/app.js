function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (let i = 0; i < uiBathrooms.length; i++) {
    if (uiBathrooms[i].checked) {
      return i + 1;
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (let i = 0; i < uiBHK.length; i++) {
    if (uiBHK[i].checked) {
      return i + 1;
    }
  }
  return -1; // Invalid Value
}

// ✅ Use Render backend URL here
const BASE_URL = "https://real-estate-price-prediction-api-67t8.onrender.com";

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");

  var url = `${BASE_URL}/predict_home_price`;

  $.ajax({
    url: url,
    type: "POST",
    data: {
      total_sqft: parseFloat(sqft.value),
      bhk: bhk,
      bath: bathrooms,
      location: location.value
    },
    success: function(data) {
      console.log(data.estimated_price);
      estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
    },
    error: function(xhr, status, error) {
      console.error("Error occurred:", status, error);
      estPrice.innerHTML = "<h2>Error fetching price</h2>";
    }
  });
}

function onPageLoad() {
  console.log("document loaded");
  var url = `${BASE_URL}/get_location_names`;

  $.get(url, function(data, status) {
    console.log("got response for get_location_names request");
    if (data) {
      var locations = data.locations;
      var uiLocations = document.getElementById("uiLocations");
      $('#uiLocations').empty();
      for (var i in locations) {
        var opt = new Option(locations[i]);
        $('#uiLocations').append(opt);
      }
    }
  });
}

window.onload = onPageLoad;
