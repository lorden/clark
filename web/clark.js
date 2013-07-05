$(document).ready(function(){
    updateClock();
    updateWeather();
    setInterval('updateClock()', 1 * 1000); 
    setInterval('updateWeather()', 5 * 60 * 1000); 
    $('#reload').click(function(){
        window.location.reload();
    });
});

function new_updateClock() {
    $.getJSON('http://127.0.0.1:5000', function(data) {
        $('#clock').html(data.time); 
    });
}

function updateWeather() {
    $.getJSON('http://127.0.0.1:5000', function(data) {
        $('#current-temperature').html(
            Math.round(data.weather.current_temperature) +
            ' &deg;' +
            data.weather.temperature_unit); 
        $('#weather-image').attr('src', data.weather.image);
    });
}

function updateClock ( ) {
  var currentTime = new Date ( );

  var currentHours = currentTime.getHours ( );
  var currentMinutes = currentTime.getMinutes ( );
  var currentSeconds = currentTime.getSeconds ( );

  // Pad the minutes and seconds with leading zeros, if required
  currentMinutes = ( currentMinutes < 10 ? "0" : "" ) + currentMinutes;
  currentSeconds = ( currentSeconds < 10 ? "0" : "" ) + currentSeconds;

  // Choose either "AM" or "PM" as appropriate
  var timeOfDay = ( currentHours < 12 ) ? "AM" : "PM";

  // Convert the hours component to 12-hour format if needed
  currentHours = ( currentHours > 12 ) ? currentHours - 12 : currentHours;

  // Convert an hours component of "0" to "12"
  currentHours = ( currentHours == 0 ) ? 12 : currentHours;

  // Compose the string for display
  var currentTimeString = currentHours + ":" + currentMinutes + ":" + currentSeconds + " " + timeOfDay;

  // Update the time display
  $('#clock').html(currentTimeString);
}
