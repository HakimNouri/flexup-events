# FlexUp Events

A simple Django application that demonstrates secure event management without requiring traditional user logins or email confirmations.  

## Table of Contents
- [FlexUp Events](#flexup-events)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Usage](#usage)
    - [1. Creating a New Event (Organizer)](#1-creating-a-new-event-organizer)
    - [2. Guest RSVP](#2-guest-rsvp)
    - [3. Organizer/Admin Actions](#3-organizeradmin-actions)
  - [Technical Details](#technical-details)
  - [Technologies Used](#technologies-used)
  - [Contribution](#contribution)



## Description
This app allows users to create and manage events without the need for logins or emails. The goal is to provide a secure yet streamlined way for event organizers and participants to interact:

- **Organizer** creates events and shares a link with guests.
- **Guests** RSVP (confirm, maybe, or decline) without needing an account.
- **Organizer** has a unique link to edit the event and manage participants.
- **Guests** have a unique link to edit their own responses.



## Features
- **No User Accounts or Emails**  
  No login, password, or email verification required.
- **Unique Event and Response Links**  
  Each event and each participant response has a unique, secret link to enable secure editing.
- **Inline Editing**  
  Events and responses can be updated directly from the same page, leveraging HTMX for a smoother user experience.
- **Simple Sharing**  
  Share your event URL anywhere—email, social media, or messaging apps.
  


## Prerequisites
- [Python](https://www.python.org/downloads/) (3.8+ recommended)
- [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [uv](https://docs.astral.sh/uv/) (lightweight dependency manager)



## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/fabrizionastri/flexup-events
   cd flexup-events
   ```
2. **Sync dependencies**:
   ```bash
   uv sync
   ```
   This will create and activate a virtual environment and install all required packages.



## Running the Application
1. **Start the Django development server**:
   ```bash
   python manage.py runserver
   ```
2. **Access the application**:
   Open your browser and go to [http://localhost:8000/](http://localhost:8000/) (or the address indicated in your terminal).



## Usage
### 1. Creating a New Event (Organizer)
- Click on **"New event"** in the navigation bar.
- Fill out the form with event details.
- Click **"Create event"**.

You will receive **two links**:
1. **Registration link** (e.g., `events.flexup.org/event/<event_slug>/register`)  
   Share this link with guests.
2. **Admin link** (e.g., `events.flexup.org/event/<event_slug>/admin/<event_admin_code>`)  
   Keep this private; it allows you to edit the event and manage participants.
3. **Participant link** (e.g., `events.flexup.org/event/<event_slug>/participant/<participant_code>`)  
   Each participant gets his own secret link to edit their response.

### 2. Guest RSVP
- When guests follow the **registration link**, they see:
  1. **Event Details** (read-only)
  2. **Responses** (list of participants who have responded, read-only)
  3. **New Response Form** to submit their own RSVP  
     - Possible statuses: **Confirmed**, **Maybe**, or **Declined**  
     - Upon submitting, each guest is given a **unique link** to update their response in the future.

### 3. Organizer/Admin Actions
- Using the **admin link**, the organizer sees:
  1. **Event Details** (in view mode by default, but can toggle edit mode with the edit button)
  2. **Responses** (in view mode by default, but can toggle edit mode with an edit button for each participant)
  3. **New Response Form** (if the organizer wants to add participants on their behalf)  
- Admins only have all the status choices available to them: 
  - the basic ones available to participants: **Confirmed**, **Maybe**, **Declined**
  - additional ones, available only to admins: **Invited**, **Waiting list**



## Technical Details
1. **No Email or User Login**  
   - No user database or password management.
   - No email service integrated.
2. **Single Form Structure**  
   - Event and participant forms can switch between read-only and edit modes using HTMX and JavaScript.
   - The form’s read-only status is controlled by a `data-readonly` attribute and toggled in the browser.
   - The `data-readonly` variable controls:
     - the form's style
     - the input's attributes (disabled, readonly)
     - the visibility of the edit, save and cancel buttons
3. **Unique Links for Edit Authorization**  
   - Only users with the correct unique link can edit event details or participant responses.
   - Both front-end (hiding buttons) and back-end (checking links and IDs) enforce authorization.



## Technologies Used
- **Django** – Backend framework  
- **Django Templating Engine** – Render dynamic HTML  
- **HTMX** – Handling AJAX-like requests for partial page updates  
- **Bootstrap** – CSS framework for styling and layout  
- **JavaScript** – Client-side interactions and form handling  
- **SQLite** (default) or any other Django-compatible database  



## Contribution
Contributions and improvements are welcome!  
1. **Fork** the repository.  
2. Create a new branch:  
   ```bash
   git checkout -b feature-branch
   ```
3. Make and commit your changes:  
   ```bash
   git commit -m 'Add new feature'
   ```
4. Push to your branch:  
   ```bash
   git push origin feature-branch
   ```
5. Open a **Pull Request** describing your changes.
