const AUTH_URL = "http://127.0.0.1:5000/api/me";

async function checkLogin() {
    try {
        const response = await fetch(AUTH_URL, {
            credentials: "include"
        });

        if (!response.ok) {
            window.location.href = "login.html";
            return false;
        }

        return true;

    } catch (error) {
        console.error("Authentication error:", error);
        window.location.href = "login.html";
        return false;
    }
}
const API_URL = "http://127.0.0.1:5000/api/applications";

const searchInput = document.getElementById("search-input");
const statusFilter = document.getElementById("status-filter");
const sortFilter = document.getElementById("sort-filter");
async function loadApplications() {
    try {
        const response = await fetch(API_URL, {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error("Failed to fetch applications");
        }

        const applications = await response.json();
        const searchTerm = searchInput.value.toLowerCase();
        const selectedStatus = statusFilter.value;

        const filteredApplications = applications.filter(application => {
            const matchesSearch =
                application.company.toLowerCase().includes(searchTerm) ||
                application.position.toLowerCase().includes(searchTerm);

            const matchesStatus =
                selectedStatus === "All" ||
                application.status === selectedStatus;

            return matchesSearch && matchesStatus;
        });

        filteredApplications.sort((a, b) => {
    const dateA = new Date(a.date_applied || "1900-01-01");
    const dateB = new Date(b.date_applied || "1900-01-01");

    if (sortFilter.value === "newest") {
        return dateB - dateA;
    } else {
        return dateA - dateB;
    }
});
        displayApplications(filteredApplications);
        updateDashboard(applications);
        displayFollowUps(applications);
        updateAnalytics(applications);

    } catch (error) {
        console.error("Error:", error);

        document.getElementById("applications-container").innerHTML =
            "<p>Unable to load applications.</p>";
    }
}
function getFollowUpStatus(followUpDate) {
    if (!followUpDate) {
        return "";
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const followUp = new Date(followUpDate + "T00:00:00");

    const difference = followUp - today;
    const days = Math.round(
        difference / (1000 * 60 * 60 * 24)
    );

    if (days < 0) {
        return "⚠️ Overdue";
    }

    if (days === 0) {
        return "📅 Due today";
    }

    if (days === 1) {
        return "⏳ 1 day remaining";
    }

    return `⏳ ${days} days remaining`;
}
function displayFollowUps(applications) {
    const container = document.getElementById("follow-up-list");

    const applicationsWithFollowUps = applications
        .filter(application => application.follow_up_date)
        .sort((a, b) => {
            const dateA = new Date(a.follow_up_date + "T00:00:00");
            const dateB = new Date(b.follow_up_date + "T00:00:00");

            return dateA - dateB;
        });

    if (applicationsWithFollowUps.length === 0) {
        container.innerHTML = "<p>No upcoming follow-ups.</p>";
        return;
    }

    container.innerHTML = applicationsWithFollowUps.map(application => `
        <div class="follow-up-item">

            <div>
                <h3>${application.company}</h3>
                <p>${application.position}</p>
            </div>

            <div class="follow-up-date">
                <strong>${application.follow_up_date}</strong>
                <span>${getFollowUpStatus(application.follow_up_date)}</span>
            </div>

        </div>
    `).join("");
}

function displayApplications(applications) {
    const container = document.getElementById("applications-container");

    if (applications.length === 0) {
        container.innerHTML = "<p>No applications yet.</p>";
        return;
    }

container.innerHTML = applications.map(application => `
    <div class="application-card">

        <div class="application-header">
            <div>
                <h3>${application.company}</h3>
                <p class="application-position">${application.position}</p>
            </div>

            <span class="status status-${application.status.toLowerCase()}">
                ${application.status}
            </span>
        </div>

        <div class="application-details">

            <p>
                <strong>Location</strong>
                <span>${application.location || "Not specified"}</span>
            </p>

            <p>
                <strong>Date Applied</strong>
        <span>${application.date_applied || "Not specified"}</span>
    </p>
	${application.follow_up_date
    ? `<p>
        <strong>Follow-Up</strong>
        <span>
            ${application.follow_up_date}
            <br>
            ${getFollowUpStatus(application.follow_up_date)}
        </span>
       </p>`
    : ""
}
            ${application.salary
                ? `<p><strong>Salary:</strong> ${application.salary}</p>`
                : ""
            }

            ${application.job_url
                ? `<p><strong>Job Posting:</strong>
                    <a href="${application.job_url}" target="_blank">View Job</a>
                   </p>`
                : ""
            }

            ${application.notes
                ? `<p><strong>Notes:</strong> ${application.notes}</p>`
                : ""
            }

            <div class="application-actions">
                <button onclick="editApplication(${application.id})">
                    Edit
                </button>

                <button onclick="deleteApplication(${application.id})">
                    Delete
                </button>
            </div>
        </div>
    `).join("");
}

function updateDashboard(applications) {
    document.getElementById("total-applications").textContent =
        applications.length;

    document.getElementById("interview-count").textContent =
        applications.filter(app => app.status === "Interview").length;

    document.getElementById("offer-count").textContent =
        applications.filter(app => app.status === "Offer").length;

    document.getElementById("rejected-count").textContent =
        applications.filter(app => app.status === "Rejected").length;

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    let followUpCount = 0;

    applications.forEach(application => {
        if (!application.follow_up_date) {
            return;
        }

        const followUpDate = new Date(
            application.follow_up_date + "T00:00:00"
        );

        if (followUpDate <= today) {
            followUpCount++;
        }
    });

    document.getElementById("follow-up-count").textContent =
        followUpCount;

    const interviewCount =
        applications.filter(app => app.status === "Interview").length;

    const offerCount =
        applications.filter(app => app.status === "Offer").length;

    const completedApplications =
        applications.filter(app =>
            app.status === "Interview" ||
            app.status === "Offer" ||
            app.status === "Rejected"
        ).length;

    const successfulApplications =
        interviewCount + offerCount;

    const successRate =
        completedApplications > 0
            ? Math.round(
                (successfulApplications / completedApplications) * 100
            )
            : 0;

    document.getElementById("success-rate").textContent =
        `${successRate}%`;
}


function updateAnalytics(applications) {
    const applied = applications.filter(
        app => app.status === "Applied"
    ).length;

    const interviews = applications.filter(
        app => app.status === "Interview"
    ).length;

    const offers = applications.filter(
        app => app.status === "Offer"
    ).length;

    const rejected = applications.filter(
        app => app.status === "Rejected"
    ).length;

    document.getElementById("analytics-applied").textContent =
        applied;

    document.getElementById("analytics-interview").textContent =
        interviews;

    document.getElementById("analytics-offer").textContent =
        offers;

    document.getElementById("analytics-rejected").textContent =
        rejected;
}

const addButton = document.getElementById("add-application-btn");
const applicationForm = document.getElementById("application-form");
const cancelButton = document.getElementById("cancel-btn");
const addApplicationForm = document.getElementById("add-application-form");

addButton.addEventListener("click", () => {
    applicationForm.classList.remove("hidden");
});

cancelButton.addEventListener("click", () => {
    applicationForm.classList.add("hidden");
    addApplicationForm.reset();
    delete addApplicationForm.dataset.editingId;
    document.getElementById("form-title").textContent = "Add Application";
    document.getElementById("submit-btn").textContent = "Save Application";
});

addApplicationForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const application = {
        company: document.getElementById("company").value,
        position: document.getElementById("position").value,
        location: document.getElementById("location").value,
        status: document.getElementById("status").value,
        date_applied: document.getElementById("date_applied").value || null,
        follow_up_date: document.getElementById("follow_up_date").value || null,
        job_url: document.getElementById("job_url").value || null,
        salary: document.getElementById("salary").value || null,
        notes: document.getElementById("notes").value || null
    };

    const editingId = addApplicationForm.dataset.editingId;

    try {
        let response;

        if (editingId) {
            response = await fetch(`${API_URL}/${editingId}`, {
                method: "PUT",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(application)
            });
        } else {
            response = await fetch(API_URL, {
                method: "POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(application)
            });
        }

        if (!response.ok) {
            throw new Error("Failed to save application");
        }

	addApplicationForm.reset();
	delete addApplicationForm.dataset.editingId;

	document.getElementById("form-title").textContent = "Add Application";
	document.getElementById("submit-btn").textContent = "Save Application";

	applicationForm.classList.add("hidden");
        await loadApplications();
    } catch (error) {
        console.error("Error:", error);
        alert("Unable to save application.");
    }
});

async function editApplication(id) {
    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "GET",
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error("Failed to get application");
        }

        const application = await response.json();

        document.getElementById("company").value = application.company || "";
        document.getElementById("position").value = application.position || "";
        document.getElementById("location").value = application.location || "";
        document.getElementById("status").value = application.status || "";
        document.getElementById("date_applied").value = application.date_applied || "";
        document.getElementById("follow_up_date").value = application.follow_up_date || "";
        document.getElementById("job_url").value = application.job_url || "";
        document.getElementById("salary").value = application.salary || "";
        document.getElementById("notes").value = application.notes || "";
	
	addApplicationForm.dataset.editingId = id;

	document.getElementById("form-title").textContent = "Edit Application";
	document.getElementById("submit-btn").textContent = "Update Application";

	applicationForm.classList.remove("hidden");
    } catch (error) {
        console.error("Error:", error);
        alert("Unable to load application.");
    }
}

async function deleteApplication(id) {
    const confirmed = confirm(
        "Are you sure you want to delete this application?"
    );

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE",
            credentials: "include"
        });

        if (!response.ok) {
            throw new Error("Failed to delete application");
        }

        await loadApplications();
    } catch (error) {
        console.error("Error:", error);
        alert("Unable to delete application.");
    }
}

searchInput.addEventListener("input", () => {
    console.log("SEARCH IS WORKING");
    loadApplications();
});
statusFilter.addEventListener("change", loadApplications);
sortFilter.addEventListener("change", loadApplications);
checkLogin().then(isLoggedIn => {
    if (isLoggedIn) {
        loadApplications();
    }
});
const logoutButton = document.getElementById("logout-btn");

logoutButton.addEventListener("click", async () => {
    try {
        await fetch("http://127.0.0.1:5000/api/logout", {
            method: "POST",
            credentials: "include"
        });

        window.location.href = "login.html";

    } catch (error) {
        console.error("Logout error:", error);
    }
});