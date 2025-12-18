# Build stage
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install


# Copy source files
COPY . .

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "4000"]


