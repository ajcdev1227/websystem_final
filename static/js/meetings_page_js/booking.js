"use strict";

// booking page

// booking buttons add and remove active class

const bookingBtns = document.querySelectorAll(".booking-tabs .tab-btn");
const bookings = document.querySelectorAll(".bookings");

// Show the "Upcoming" tab content by default
//document.getElementById(".tab-btn[data-tab='upcoming']").classList.add("active");

bookingBtns.forEach((btn) => {
  btn.addEventListener("click", function () {
    const tab = this.getAttribute("data-tab");

    // Hide all bookings
    bookings.forEach((booking) => {
      booking.style.display = "none";
    });

    // Show the selected booking tab
    document.getElementById(tab).style.display = "block";

    // Remove active class from all buttons
    bookingBtns.forEach((btn) => {
      btn.classList.remove("active");
    });

    // Add active class to the clicked button
    this.classList.add("active");
  });
});

