$(document).ready(function(){
    updateClock();
    updateWeather();
    setInterval('updateClock()', 1 * 1000); 
    setInterval('updateWeather()', 5 * 60 * 1000); 
    $('#reload').click(function(){
        window.location.reload();
    });
    // Default images
    $('#today-image, #tomorrow-image, #aftertomorrow-image').error(function(){
        console.log($(this).attr('id'));
        $(this).attr('src', 'img/not_available.png');
    });
});

var api_url = 'http://ec2-54-226-139-147.compute-1.amazonaws.com/';

function new_updateClock() {
    $.getJSON(api_url, function(data) {
        $('#clock').html(data.time); 
    });
}

function updateWeather() {
    $.getJSON(api_url, function(data) {
        var tu = ' &deg;' + data.weather.temperature_unit;
        // Today
        $('#current-temperature').html('Now: ' + Math.round(data.weather.today.temperature) + tu); 
        $('#today-image').attr('src', data.weather.today.image);
        $('#today-condition').html(data.weather.today.condition);
        $('#today-high').html("High: " + data.weather.today.high + tu);
        $('#today-low').html("Low: " + data.weather.today.low + tu);

        // Tomorrow
        $('#tomorrow-title').html(get_day_name(1));
        $('#tomorrow-image').attr('src', data.weather.tomorrow.image);
        $('#tomorrow-condition').html(data.weather.tomorrow.condition);
        $('#tomorrow-low').html("Low: " + data.weather.tomorrow.low + tu);
        $('#tomorrow-high').html("High: " + data.weather.tomorrow.high + tu);
        // After tomorrow
        $('#aftertomorrow-title').html(get_day_name(2));
        $('#aftertomorrow-image').attr('src', data.weather.after_tomorrow.image);
        $('#aftertomorrow-condition').html(data.weather.after_tomorrow.condition);
        $('#aftertomorrow-low').html("Low: " + data.weather.after_tomorrow.low + tu);
        $('#aftertomorrow-high').html("High: " + data.weather.after_tomorrow.high + tu);
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

function get_day_name(delta){
    if (delta == 'undefined') delta = 0;
    var d = new Date();
    day = d.getDay();
    day += delta;
    if (day > 7) {
        day -= 7;
    }
    var weekday=new Array(7);
    weekday[0]="Sunday";
    weekday[1]="Monday";
    weekday[2]="Tuesday";
    weekday[3]="Wednesday";
    weekday[4]="Thursday";
    weekday[5]="Friday";
    weekday[6]="Saturday";
    return weekday[day];
}
