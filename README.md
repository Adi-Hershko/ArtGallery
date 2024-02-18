# ArtGallery

Welcome to the ArtGallery repository! ArtGallery is a dynamic web application designed to showcase a curated collection of artworks. This application is structured into a frontend and backend, encapsulating the user interface and data management logic separately for better maintainability and scalability.

## Quick Start

To get ArtGallery up and running on your machine, ensure you have Docker installed and follow these steps:

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the Repository**

   First, clone the repository to your local machine:

   ```bash
   git clone https://github.com/Adi-Hershko/ArtGallery.git
   cd ArtGallery
   ```

2. **Build the Docker Images**

   Navigate to both the backend and frontend directories to build their respective Docker images:

   ```bash
   cd Backend
   docker build -t backend:latest .
   cd ../Frontend
   docker build -t frontend:latest .
   ```

   This will create the Docker images for both parts of the application.

3. **Run Docker Compose**

   Return to the root directory of the project and run Docker Compose to start the application:

   ```bash
   cd ..
   docker-compose up --build -d
   ```

   This command starts all the necessary services as defined in the `docker-compose.yml` file.

### Accessing the Application

After starting the services, the ArtGallery application should be accessible through your web browser:

- **Frontend:** http://localhost:5173
- **Backend:** http://localhost:8000

## Features

ArtGallery offers a range of features designed to enhance the experience of exploring and enjoying art, including:

- **Artwork Showcase:** Browse through a collection of artworks displayed in a user-friendly interface.
- **Artist Information:** Learn more about the artists behind the masterpieces.
- **Responsive Design:** Enjoy the gallery on any device, thanks to a responsive web design.

## Contributing

We welcome contributions to the ArtGallery project! If you have suggestions for improvements or encounter any issues, please feel free to open an issue or submit a pull request.

## Acknowledgments

A special thank you to all contributors and the open source community for making projects like this possible.
