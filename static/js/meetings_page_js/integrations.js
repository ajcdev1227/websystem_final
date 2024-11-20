"use strict";

// show and hide sidebar

const body = document.querySelector("body");
const sidebarShowBtn = document.querySelector(".sidebar-header .sidebar-btn");
const sidebar = document.querySelector(".sidebar-wrapper");
const bodyGrid = document.querySelector(".body-grid");

bodyGrid.style.gridTemplateColumns = `${sidebar.offsetWidth}px 1fr`;

sidebarShowBtn.addEventListener("click", () => {
  sidebar.classList.toggle("active");
  sidebarShowBtn.classList.toggle("active");
  const icon = sidebarShowBtn.querySelector("i");
  if (sidebarShowBtn.classList.contains("active")) {
    icon.className = "bx bxs-chevrons-left";
    body.style.overflow = "hidden";
    
    // get sidebar width dynamically

    sidebarShowBtn.style.left = `calc(${sidebar.offsetWidth}px - 5px)`;
  } else {
    icon.className = "bx bxs-chevrons-right";
    sidebarShowBtn.style.left = "5px";
    body.style.overflow = "auto";
  }
});

// sidebar links add and remove active class

const sidebarLinks = document.querySelectorAll(".sidebar ul li a");

sidebarLinks.forEach((links) => {
  links.addEventListener("click", function () {
    sidebarLinks.forEach((link) => link.classList.remove("active"));
    this.classList.add("active");
  });
});
