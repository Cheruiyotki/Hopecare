const contentDiv = document.getElementById('content');
const appointments = [];

// Render specific sections
function renderSection(section) {
    switch (section) {
        case 'profile':
            renderProfileSection();
            break;
        case 'doctors':
            renderDoctorsSection();
            break;
        case 'appointments':
            renderAppointmentsSection();
            break;
        case 'reports':
            renderReportsSection();
            break;
        default:
            contentDiv.innerHTML = '<p>Section not found.</p>';
    }
}

// Render profile section
function renderProfileSection() {
    contentDiv.innerHTML = `
        <h2>View Profile</h2>
        <div class="profile">
            <img src="profile-picture.jpg" alt="Profile Picture">
            <div class="profile-info">
                <p>Name: John Doe</p>
                <p>Age: 35</p>
                <p>Gender: Male</p>
                <!-- Add more profile details as needed -->
            </div>
        </div>
    `;
}

// Render doctors section
function renderDoctorsSection() {
    contentDiv.innerHTML = `
        <h2>Cancer Doctors at Hope Care</h2>
        <ul>
            <li>Dr. Jane Smith</li>
            <li>Dr. Michael Johnson</li>
            <li>Dr. Emily Davis</li>
            <!-- Add more doctors as needed -->
        </ul>
    `;
}

// Render appointments section
function renderAppointmentsSection() {
    contentDiv.innerHTML = `
        <h2>Manage Appointments</h2>
        <h3>Upcoming Appointments</h3>
        <ul id="upcomingAppointments">
            ${appointments.map(appointment => `
                <li>${appointment.doctor} on ${appointment.date} at ${appointment.time} <button onclick="cancelAppointment(${appointments.indexOf(appointment)})">Cancel</button></li>
            `).join('')}
        </ul>
        <h3>Make a New Appointment</h3>
        <form id="newAppointmentForm">
            <label for="doctor">Doctor:</label>
            <select id="doctor" name="doctor" required>
                <option value="">Select a doctor</option>
                <option value="dr-smith">Dr. Jane Smith</option>
                <option value="dr-johnson">Dr. Michael Johnson</option>
                <option value="dr-davis">Dr. Emily Davis</option>
                <!-- Add more doctors as needed -->
            </select>

            <label for="date">Date:</label>
            <input type="date" id="date" name="date" min="${new Date().toISOString().split('T')[0]}" required>

            <label for="time">Time:</label>
            <input type="time" id="time" name="time" required>

            <button type="submit">Make Appointment</button>
        </form>
    `;

    const newAppointmentForm = document.getElementById('newAppointmentForm');
    newAppointmentForm.addEventListener('submit', handleNewAppointment);
}
// Render reports section
function renderReportsSection() {
    contentDiv.innerHTML = `
        <h2>Download Medical Reports</h2>
        <ul>
            <li><a href="#" download>Medical Report - 01/01/2024</a></li>
            <li><a href="#" download>Medical Report - 02/15/2024</a></li>
            <!-- Add more reports as needed -->
        </ul>
    `;
}

// Handle new appointment form submission
function handleNewAppointment(event) {
    event.preventDefault();
    const doctor = document.getElementById('doctor').value;
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;
    const appointment = { doctor, date, time };
    appointments.push(appointment);
    renderAppointmentsList();
    event.target.reset();
}

// Render the list of appointments
function renderAppointmentsList() {
    const upcomingAppointmentsList = document.getElementById('upcomingAppointments');
    upcomingAppointmentsList.innerHTML = appointments.map(appointment => `
        <li>${appointment.doctor} on ${appointment.date} at ${appointment.time} <button onclick="cancelAppointment(${appointments.indexOf(appointment)})">Cancel</button></li>
    `).join('');
}

// Cancel an appointment
function cancelAppointment(index) {
    appointments.splice(index, 1);
    renderAppointmentsList();
}

// Event listeners for navigation links
const navLinks = document.querySelectorAll('nav a');
navLinks.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        const section = event.target.dataset.section;
        renderSection(section);
    });
});

// Initial render
renderSection('profile');