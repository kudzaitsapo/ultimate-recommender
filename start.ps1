Write-Host "[+] Starting the recommender program ..."
Write-Host "[+] Author: kudzaitsapo@gmail.com`r`n"

Write-Host "========================================"

try {
    Write-Host "[+] Starting docker ... make sure the daemon is running, and you have internet connection."
    docker-compose up -d --build

    Write-Host "[+] Running app migrations..."
    docker-compose exec web python manage.py migrate

    docker-compose exec web python recommendations/books/import_data.py

    Write-Host "[+] Rebuilding elasticsearch haystack index..."
    docker-compose exec web ./manage.py rebuild_index --noinput
}
catch {
    Write-Host "[-] Error: $($_.Exception.Message)"
	exit 1
}