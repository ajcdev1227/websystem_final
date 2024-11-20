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

// availability page

// show and hide the new schedule box

const availabilityNewBtn = document.querySelector(".availability-new");
const newScheduleBox = document.querySelector(".new-schedule");
const closeScheduleBox = document.querySelector(".close-schedule");

availabilityNewBtn.addEventListener("click", () => {
  newScheduleBox.classList.add("active");
});

closeScheduleBox.addEventListener("click", () => {
  newScheduleBox.classList.remove("active");
});

const allOptionsBtns = document.querySelectorAll(
  ".availability-edit .availability-options"
);

allOptionsBtns.forEach((button) => {
  button.addEventListener("click", () => {
    const editBtns = button
      .closest(".availability-edit")
      .querySelector(".availability-edit-btns");
    editBtns.classList.toggle("active");
  });
});
