# =============================================================================
# Frontend Dockerfile - Next.js 16+ Development
# =============================================================================
# This Dockerfile creates a development environment for the Next.js frontend.
# It enables hot reload for rapid development iteration.
#
# Build: docker build -t todo-frontend .
# Run: docker run -p 3000:3000 -v $(pwd):/app todo-frontend
#
# Note: This is a DEVELOPMENT Dockerfile. For production, use multi-stage build.
# =============================================================================

FROM node:20-alpine

# Set working directory
WORKDIR /app

# Install dependencies for native modules (if needed)
RUN apk add --no-cache libc6-compat

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm ci

# Copy source code
# Note: In docker-compose, source is mounted as volume for hot reload
COPY . .

# Expose Next.js default port
EXPOSE 3000

# Set environment to development for hot reload
ENV NODE_ENV=development

# Start Next.js development server with hot reload
CMD ["npm", "run", "dev"]
