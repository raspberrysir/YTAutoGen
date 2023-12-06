from scraper import scraper
from tts import tts
from overlay import overlay
from upload import upload
from delete import delete

index = 10
tts(scraper(index))
overlay()
upload(index)
delete()