# Shell script to run the start-up commands

echo "[+] Starting the recommender program ..."
echo "[+] Author: kudzaitsapo@gmail.com"

echo "==============================="
echo "[+] Starting docker ... make sure the daemon is running, and you have internet connection."
docker-compose up -d --build

if [ $? -eq 0 ]; then
    echo "[+] Running app migrations..."
    docker-compose exec web python manage.py migrate && echo "[+] Successfully migrated..." || exit 1
    docker-compose exec web python recommendations/books/import_data.py || exit 1
else
    echo "[-] Failed to start the docker container!"
fi