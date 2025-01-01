# 📚 Light Novel Reader Website

Welcome to the **Light Novel Reader Website**! This platform allows users to upload their favorite light novels in PDF format, read them directly on the site, and share them with others. Users can also participate in **genre-based forums** or discussions about specific series. Additionally, there is a **search feature** to find books by title.

---

## 🌟 Key Features

- **PDF Upload and Reading** 📄: Users can upload PDFs of light novels, which will be stored in the database and made available for reading online.
- **Forums** 🗣️: Genre-specific or series-specific forums where users can discuss their favorite books.
- **Search Functionality** 🔍: Users can search for light novels by title.
- **User Profiles** 👤: Users can create and manage profiles to track their reading history and favorite books.

---

## 🛠️ Technologies Used

- **Frontend**: React, HTML, CSS, JavaScript
- **Backend**: Django, Django Rest Framework (DRF)
- **Database**: PostgreSQL
- **File Storage**: AWS S3 (or local file storage if preferred)
- **Authentication**: JWT-based authentication (Django Rest Framework JWT)

---

## 🔧 Project Breakdown: Steps to Focus On

### 1. **User Authentication and Profiles** 🔒

#### Features:
- User registration, login, and logout (using JWT).
- Ability to view and update user profiles.
- Allow users to track books they’ve read or are currently reading.

#### Steps:
- Set up Django’s **authentication system** with JWT for secure API access.
- Create user models with necessary fields (username, email, password, reading history).
- Design frontend components for registration, login, and profile management using React.
- Implement protected routes to ensure only logged-in users can upload books, post in forums, etc.

---

### 2. **PDF Upload and Reader** 📄

#### Features:
- Users can upload PDF files of light novels.
- PDFs are stored on the server or external storage (AWS S3).
- A built-in **PDF reader** for users to read the books directly on the website.

#### Steps:
- **Backend**:
  - Create a model for light novels with fields like title, author, PDF file, genre, etc.
  - Set up file storage for PDFs (either local storage or AWS S3).
  - Create a Django API endpoint to handle **file uploads** and store metadata in the database.
- **Frontend**:
  - Build a **file upload** component in React that allows users to upload PDFs.
  - Integrate a **PDF viewer** library (e.g., `react-pdf` or `pdf.js`) to display the uploaded PDFs on the website.
- **File Handling**:
  - Ensure files are securely uploaded and accessible for users to read.
  - Implement pagination or chapters for better readability of large PDFs.

---

### 3. **Search Functionality** 🔍

#### Features:
- Users can search for books by title.

#### Steps:
- **Backend**:
  - Implement a search API endpoint using Django’s ORM to filter books by title.
  - Ensure the search query matches partial titles and is case-insensitive.
- **Frontend**:
  - Create a search bar in React where users can enter book titles.
  - Display search results dynamically as the user types (real-time search).
  - Use **React hooks** to manage the search state and display results.

---

### 4. **Forum for Genre/Series Discussions** 💬

#### Features:
- Users can participate in forums for specific genres or series.
- Forums allow text-based discussions with threaded replies.

#### Steps:
- **Backend**:
  - Create a **Forum model** for different genres or series.
  - Each forum can have multiple threads, and each thread can have multiple replies.
  - Set up Django API endpoints to create, read, update, and delete forum posts.
- **Frontend**:
  - Build a **forum UI** where users can select a genre or series and post new threads.
  - Display threads with options to reply.
  - Allow users to upvote or downvote threads or posts to encourage quality discussions.

---

### 5. **User Interaction and Community Building** 👫

#### Features:
- Users can upvote/downvote posts or threads in the forum.
- Ability to mark favorite books or threads to create personalized recommendations.

#### Steps:
- **Backend**:
  - Add an **upvote/downvote** system for posts and threads in the forum using Django models.
  - Implement a **favorites** feature where users can mark light novels or threads as favorites.
- **Frontend**:
  - Build upvoting/downvoting components in React.
  - Add UI elements for users to mark light novels or threads as favorites.

---

### 6. **Deployment** 🚀

#### Features:
- Deploy the website on a platform like **Heroku**, **Vercel**, or **AWS**.
- Set up production-level databases and storage solutions.

#### Steps:
- Set up a **Heroku** or **AWS** account for deployment.
- Configure the backend for **production**, including settings for the database (PostgreSQL) and file storage (AWS S3).
- Deploy the frontend (React) to **Vercel** or **Netlify**.
- Make sure your **CORS** settings are correctly configured to allow the frontend to communicate with the backend.

---
