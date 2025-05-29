# Use the official NGINX image from the Docker Hub
FROM nginx:latest

# Expose port 8080 to access the container externally
EXPOSE 8083

# Replace the default NGINX configuration with your custom one (if needed)
# COPY ./nginx.conf /etc/nginx/nginx.conf

# If you have a custom website, copy the site files into the NGINX container
# COPY ./html /usr/share/nginx/html

# By default, NGINX listens on port 80, so we need to update it to listen on port 8080
RUN sed -i 's/listen 80;/listen 8080;/g' /etc/nginx/conf.d/default.conf

# Start NGINX when the container runs
CMD ["nginx", "-g", "daemon off;"]
