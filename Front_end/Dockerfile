# Use the official Nginx image
FROM nginx:alpine

# Copy the Front_end directory content to Nginx's default HTML folder
COPY . /usr/share/nginx/html

# Copy Nginx config into container
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80
