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

function search(){
  var searchValue = document.getElementById("keyword").value.toLowerCase();
  document.getElementById("keyword").value = "";
  console.log(searchValue);
}


// search job section
let searchCurrentPage = 1;
let searchTotalPages = 1;
let searchJobs = []; // Store search jobs for pagination

// Function to search jobs dynamically
function searchJobsAPI() {
  const searchValue = document.getElementById("keyword").value.trim().toLowerCase();
  if (!searchValue) return;

  // Fetch jobs using AJAX with the search keyword
  fetch(`/fetch_search_jobs?keywords=${searchValue}`)
    .then(response => response.json())
    .then(jobs => {
      searchJobs = jobs; // Store the search results for pagination
      searchTotalPages = Math.ceil(jobs.length / 10); // Calculate total pages
      searchCurrentPage = 1; // Reset to the first page
      renderSearchTab(0); // Render the first set of jobs and pagination
    })
    .catch(error => console.error('Error fetching jobs:', error));
}

// Function to render the entire tab-1 content with jobs and pagination
function renderSearchTab(startIndex) {
  const tabDiv = document.getElementById("tab-1");
  tabDiv.innerHTML = ""; // Clear the entire tab-1 content

  // Render the search jobs
  const jobsToShow = searchJobs.slice(startIndex, startIndex + 10);
  let jobsHtml = jobsToShow.map((job, index) => `
    <div class="job-item p-4 mb-4" data-job-id="${startIndex + index}" onclick="updateJobDescription('${startIndex + index}')">
      <div class="row g-4">
        <div class="col-sm-12 col-md-8 d-flex align-items-center">
          <img class="flex-shrink-0 img-fluid border rounded" 
               src="${job.company_logo || ''}" 
               alt="Company Logo" 
               style="width: 80px; height: 80px" />
          <div class="text-start ps-4">
            <h5 class="mb-3">${job.position || "N/A"}</h5>
            <span class="text-truncate me-3">
              <i class="fa fa-map-marker-alt text-primary me-2"></i>${job.location || "N/A"}
            </span>
            <span class="text-truncate me-3">
              <i class="fa fa-building text-primary me-2"></i>${job.company || "N/A"}
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
            <a class="btn btn-primary" href="${job.url || '#'}">Apply Now</a>
          </div>
          <small class="text-truncate">
            <i class="far fa-calendar-alt text-primary me-2"></i>${job.date || "N/A"}
          </small>
        </div>
      </div>
    </div>`).join('');

  // Add pagination controls below the jobs
  const paginationHtml = `
    <div class="text-center mt-5">
      <button id="search-prev-btn" class="btn btn-outline-primary me-3" 
              onclick="handleSearchPagination('prev')" ${searchCurrentPage === 1 ? 'disabled' : ''}>Previous</button>
      <button id="search-next-btn" class="btn btn-primary" 
              onclick="handleSearchPagination('next')" ${searchCurrentPage === searchTotalPages ? 'disabled' : ''}>Next</button>
    </div>`;

  // Combine jobs and pagination into the full tab content
  tabDiv.innerHTML = `
    <div id="job-listings">
      ${jobsHtml}
    </div>
    ${paginationHtml}`;
}

// Function to handle search pagination
function handleSearchPagination(direction) {
  let startIndex = 0;
  if (direction === "next" && searchCurrentPage < searchTotalPages) {
    searchCurrentPage++;
  } else if (direction === "prev" && searchCurrentPage > 1) {
    searchCurrentPage--;
  }
  startIndex = (searchCurrentPage - 1) * 10;
  renderSearchTab(startIndex); // Render the new jobs and pagination
}


const form = document.getElementById('register');
const password1 = document.getElementById('password');
const confirmPassword1 = document.getElementById('confirmPassword');

// Add event listener for form submission
form.addEventListener('submit', function (event) {


  // Prevent form submission if passwords don't match
  if (password1.value !== confirmPassword1.value) {
    confirmPassword1.setCustomValidity('Passwords do not match.');
  } else {
    confirmPassword1.setCustomValidity(''); // Clear the error if they match
  }

  // If the form is invalid, prevent submission and show validation messages
  if (!form.checkValidity()) {
    event.preventDefault(); // Stop submission
    form.reportValidity();  // Display built-in validation messages
    return; // Exit if invalid
  }

  // Collect input values only if form is valid
  const username = document.getElementById('username').value;
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const termsAccepted = document.getElementById('terms').checked;

  if (!termsAccepted) {
    alert('You must agree to the terms and conditions.');
    return; // Stop if terms are not accepted
  }

  const data = {
    username: username,
    email: email,
    password: password,
  };

  const loginData = {
    email: email,
    password: password,
  };

  // Create user request
  fetch('/reg_users', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
    .then(response => response.json())
    .then(data => {
      if (data.message === 'user created') {
        alert(`User ${username} created successfully.`);

        // Perform login after successful user creation
        return fetch('/sessions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(loginData),
        });
      } else {
        throw new Error(data.message); // Handle user creation failure
      }
    })
    .then(response => response.json())
    .then(data => {
      
      window.location.href = `/${data.session_id}/${true}`; 
    })
    .catch(error => console.error('Error:', error))
    .finally(() => {
      form.reset(); // Reset the form after submission
    });
});



 // Add an event listener to capture form submission
form.addEventListener('submit', function (event) {
  event.preventDefault(); // Prevents page reload

  
});

const closeButton = document.querySelector('.close-button');
closeButton.addEventListener('click', () => {
  document.querySelector('.popup').style.display = 'none';
});