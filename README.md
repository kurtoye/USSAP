## 🚀 University Student Support Backend (Flask + Firebase + Google Cloud)

A lightweight backend for managing student inquiries, support requests, and document uploads, built using Flask, Firestore, and Firebase Authentication.
Designed as part of my final-year university project — clean, modular, and deployable on Google Cloud.

## 🎥 2-Minute Demo Video

Watch the full walkthrough:
👉 https://youtu.be/wK3k1t7LBTo

This shows login, signup, document uploads, and the backend workflow end-to-end.

## 🏗️ What This Backend Does
📩 Inquiries System

* Students can submit support inquiries.
* Admins can view, filter, update, or delete them.
* (Implemented in inquiries_service.py)

## 📝 Requests System

* Students can create formal support requests (e.g., documents, academic help).
* Admins can filter by type/status and manage them.
* (Implemented in requests_service.py)

## 🧠 Clean Data Models

Simple structured Python models that convert directly to Firestore documents:

* Inquiry

* Request

## 🌐 Flask API Structure

Blueprint-based and organised cleanly:

* /inquiries

* /requests

* Root health endpoint (/)

## 🔧 Tools & Technologies Used
☁️ Google Cloud Platform

* Hosting

* IAM service accounts

* Firestore database access

🔐 Firebase Authentication

* Handles login/signup

* Secure user identity and access control

🗄️ Firestore Database

* Stores user activity, inquiries, and requests in a clean NoSQL structure.

📁 Firebase Storage

* Used for student document uploads (e.g., forms, evidence).

🧪 Postman
Used to test:

* POST/GET/PUT/DELETE routes

* Auth tokens

* Firestore writes

* Error handling

## 🧱 Architecture Overview
Flask API
*  ├── /inquiries   → Inquiry submission + admin management
*  ├── /requests    → Request creation + admin management
*  ├── Firestore    → stores all inquiry/request data
*  └── Firebase Auth → controls user identity

## 🧑‍💻 My Responsibilities

I was responsible for the entire backend:

* Architecting the Flask API

* Building services, models, and route blueprints

* Integrating Firebase Authentication

* Connecting Firestore database to all endpoints

* Handling admin workflows

* Testing the full system in Postman

* Ensuring Docker + Cloud compatibility
