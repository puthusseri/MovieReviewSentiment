const counter = document.querySelector(".counter");
let count = 0;
setInterval(() => {
 if(count == 92) {
  clearInterval(count);
 }else {
  count+=1;
  counter.textContent = count + "%";
 }
}, 42);

function getCookie(name) {
    // Add the = sign
    name = name + '=';
    // Get the decoded cookie
    var decodedCookie = decodeURIComponent(document.cookie);
  
    // Get all cookies, split on ; sign
    var cookies = decodedCookie.split(';');
  
    // Loop over the cookies
    for (var i = 0; i < cookies.length; i++) {
      // Define the single cookie, and remove whitespace
      var cookie = cookies[i].trim();
  
      // If this cookie has the name of what we are searching
      if (cookie.indexOf(name) == 0) {
        // Return everything after the cookies name
        return cookie.substring(name.length, cookie.length);
      }
    }
  }

// function findByName(name){
//     alert(name);
// }
