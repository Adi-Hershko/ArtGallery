# Use an official Node runtime as a parent image
FROM node:16

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install any needed packages
RUN npm install

# Bundle app source
COPY . .

# Expose the port that Vite runs on
EXPOSE 5173

# Define command to run the app using Vite
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

