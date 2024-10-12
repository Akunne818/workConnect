(function ($) {
  "use strict";

  // spiner
  var spinner = function () {
    setTimeout(function () {
      if ($("#spinner").length > 0) {
        $("#spinner").removeClass("show");
      }
    }, 1);
  };
  spinner();

  new WOW().init();

  // sticky navigation
  $(window).scroll(function () {
    if ($("this").scrollTop() > 300) {
      $(".sticky-top").css("top", "0px");
    } else {
      $(".sticky-top").css("top", "-100px");
    }
  });

  // back to top buttton
  $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
      $(".back-to-top").fadeIn("slow");
    } else {
      $(".back-to-top").fadeOut("slow");
    }
  });
  $(".back-to-top").click(function () {
    $("html, body").animate({ scrollTop: 0 }, 1500, "easeInOutExpo");
    return false;
  });

  // Header carousel
  $(".header-carousel").owlCarousel({
    autoplay: true,
    smartSpeed: 1500,
    items: 1,
    dots: true,
    loop: true,
    nav: true,
    navText: [
      '<i class="bi bi-chevron-left"></i>',
      '<i class="bi bi-chevron-right"></i>',
    ],
  });

  // Testimonial carousel
  $(".testimonial-carousel").owlCarousel({
    autoplay: true,
    smartSpeed: 1000,
    center: true,
    margin: 24,
    dots: true,
    loop: true,
    nav: false,
    responsive: {
      0: {
        items: 1,
      },
      768: {
        items: 2,
      },
      992: {
        items: 3,
      },
    },
  });
})(jQuery);

// Modal

var x = document.getElementById("login");
var y = document.getElementById("register");
var z = document.getElementById("btna");
var form_size = document.getElementsByClassName("forma-box");

function register() {
  x.style.left = "-400px";
  y.style.left = "50px";
  z.style.left = "110px";
  form_size[0].style.height = "528px";
}

function login() {
  x.style.left = "50px";
  y.style.left = "450px";
  z.style.left = "0px";
  form_size[0].style.height = "430px";
}

let currentPage = 1;
const paginationData = document.getElementById("pagination-data");
const totalPages = paginationData.getAttribute("data-total-pages");
// Function to load jobs via AJAX
function loadJobs(direction) {
  // Calculate new page number
  let startIndex = 0;
  if (direction === "next") {
    currentPage++;
    startIndex = (currentPage - 1) * 10;
    updateJobDescription(startIndex);
  } else if (direction === "prev") {
    currentPage--;
    startIndex = (currentPage - 1) * 10;
    updateJobDescription(startIndex);
  }

  // Fetch jobs via AJAX
  fetch(`/fetch_jobs?page=${currentPage}`)
    .then((response) => response.json())
    .then((jobs) => {
      // Update job listings
      const jobListingsDiv = document.getElementById("job-listings");
      jobListingsDiv.innerHTML = ``;

      jobs.slice(startIndex, startIndex + 10).forEach((job, index) => {
        const jobHtml = `
                    <div class="job-item p-4 mb-4" data-job-id="${startIndex + index}" onclick="updateJobDescription('${startIndex + index}')">
                        <div class="row g-4">
                            <div class="col-sm-12 col-md-8 d-flex align-items-center">
                                <img class="flex-shrink-0 img-fluid border rounded"
                                      src="${job.company_logo}" alt="Company Logo"
                                      style="width: 80px; height: 80px" />
                                <div class="text-start ps-4">
                                    <h5 class="mb-3">${job.title}</h5>
                                    <span class="text-truncate me-3">
                                        <i class="fa fa-map-marker-alt text-primary me-2"></i>${job.location}
                                    </span>
                                    <span class="text-truncate me-3">
                                        <i class="fa fa-building text-primary me-2"></i>${job.company}
                                    </span>
                                    <span class="text-truncate me-0">
                                        <i class="far fa-money-bill-alt text-primary me-2"></i>$123 - $321
                                    </span>
                                </div>
                            </div>
                            <div class="col-sm-12 col-md-4 d-flex flex-column align-items-start align-items-md-end justify-content-center">
                                <div class="d-flex mb-3">
                                    <a class="btn btn-light btn-square me-3" href="">
                                        <i class="far fa-heart text-primary"></i>
                                    </a>
                                    <a class="btn btn-primary" href="${job.apply_url}">Apply Now</a>
                                </div>
                                <small class="text-truncate">
                                    <i class="far fa-calendar-alt text-primary me-2"></i>${job.date}
                                </small>
                            </div>
                        </div>
                    </div>`;
        jobListingsDiv.innerHTML += jobHtml;
      });

      // Update button states
      document.getElementById("prev-btn").disabled = currentPage === 1;
      document.getElementById("next-btn").disabled = currentPage === totalPages;
    });
}

document.getElementById("next-btn").addEventListener("click", function (event) {
  event.preventDefault(); // Prevent default page reload

  loadJobs("next");

  // After loading the new jobs, scroll to the top of the container
  document
    .getElementById("job-container")
    .scrollIntoView({ behavior: "smooth" });
});

document.getElementById("prev-btn").addEventListener("click", function (event) {
  event.preventDefault(); // Prevent default page reload

  loadJobs("prev");

  // After loading the previous jobs, scroll to the top of the container
  document
    .getElementById("job-container")
    .scrollIntoView({ behavior: "smooth" });
});

let jobDescriptions = null;

fetch(`/fetch_jobs`)
  .then((response) => response.json())
  .then((All_jobs) => {
    
    jobDescriptions = All_jobs;
    console.log(jobDescriptions);

    // Add event listeners to each job item
    // const jobItems = document.getElementsByClassName("job-item");
    // for (let i = 0; i < jobItems.length; i++) {
    //   jobItems[i].addEventListener("click", function (event) {
    //     // Get the job ID from the clicked item
    //     const jobId = parseInt(event.target.getAttribute("data-job-id"));

    //     // Update the job description
    //     updateJobDescription(jobId);
    //   });
    // }
  });

function updateJobDescription(jobId) {
  console.log(jobId);
  if (jobDescriptions) {
    const jobDescription = jobDescriptions[jobId].description;
    document.getElementById("job-desc-content").innerText = jobDescription;

    // Scroll to the job description section if necessary
    document
      .getElementById("job-description")
      .scrollIntoView({ behavior: "smooth" });
  }
}
window.onload = function() {
  updateJobDescription(0);  // Display the first job's description on page load
}