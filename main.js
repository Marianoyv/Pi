

// const menuToggle = document.querySelector('.toggle');
// const showcase = document.querySelector('.showcase');
// menuToggle.addEventListener('click', () => {
//   menuToggle.classList.toggle('active');
//   showcase.classList.toggle('active');// })
// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

  const app = initializeApp(firebaseConfig);
  import { initializeApp } from 'firebase/app';
  const firebaseConfig = {
  apiKey: "AIzaSyBzH4z4eTW0JKavCw_ZcAYzX1n0RGcx2xE",
  authDomain: "pidevelopment.firebaseapp.com",
  databaseURL: "https://pidevelopment-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "pidevelopment",
  storageBucket: "pidevelopment.appspot.com",
  messagingSenderId: "794676722903",
  appId: "1:794676722903:web:ba49378fbced6c77c8c492",
  measurementId: "G-ZD7XRCLYLB"
};

function myFunction() {
  var x = document.getElementById("Topnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}


document.querySelectorAll("[data-img-to-show]").forEach(section => {
  observer.observe(section)
})
const text = document.querySelector(".tsecond");
    
const textLoad = () => {
    setTimeout(() => {
        text.textContent = "Web Developer";
    }, 0);
    setTimeout(() => {
        text.textContent = "Web Designer";
    }, 3000);
    setTimeout(() => {
        text.textContent = "Marketing Analyst";
    }, 6000);
    setTimeout(() => {
        text.textContent = "Search Engine Optimization";
    }, 9000); //1s = 1000 milliseconds
}

textLoad();
setInterval(textLoad, 12000);


// Reference messages collection
var messagesRef = firebase.database().ref('messages');

// Listen for form submit
document.getElementById('contactForm').addEventListener('submit', submitForm);

// Submit form
function submitForm(e){
  e.preventDefault();

  // Get values
  var name = getInputVal('name');
  var company = getInputVal('company');
  var email = getInputVal('email');
  var phone = getInputVal('phone');
  var message = getInputVal('message');

  // Save message
  saveMessage(name, company, email, phone, message);

  // Show alert
  document.querySelector('.alert').style.display = 'block';

  // Hide alert after 3 seconds
  setTimeout(function(){
    document.querySelector('.alert').style.display = 'none';
  },3000);

  // Clear form
  document.getElementById('contactForm').reset();
}

// Function to get get form values
function getInputVal(id){
  return document.getElementById(id).value;
}

// Save message to firebase
function saveMessage(name, company, email, phone, message){
  var newMessageRef = messagesRef.push();
  newMessageRef.set({
    name: name,
    company:company,
    email:email,
    phone:phone,
    message:message
  });
}