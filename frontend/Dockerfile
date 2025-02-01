# Use an official Node.js runtime as the base image
FROM node:latest

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json first to leverage Docker cache
COPY package*.json ./

# Copy the rest of the application files
COPY . .

# Install dependencies
RUN npm install

# Build the SvelteKit app
# RUN npm run build

# Expose a port (e.g., 3000 for a SvelteKit app)
# EXPOSE 3000

# Command to run the application
CMD ["npm", "run", "dev", "--"]
