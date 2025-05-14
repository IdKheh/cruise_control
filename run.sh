echo "Stopping and removing containers..."
docker-compose down

echo "Rebuilding images without cache..."
docker-compose build --no-cache

echo "Starting containers..."
docker-compose up