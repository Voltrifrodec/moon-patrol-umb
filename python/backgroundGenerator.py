#? Used Libraries
from PIL import Image
import random




#? Function for generating background image for the game
def generateStarImage(starAmountMax: int, fileName: str, isPreviewNeeded: bool):
    
    # Image initialization
    img = Image.new('RGB', (800, 600))
    # img.paste((0, 0, 0), [0, 0, img.width, img.height])
    # img.show()
    
    # Generates random amount of stars
    starAmountMin = 50
    stars_count = random.randint(starAmountMin, starAmountMax)

    for i in range(0,stars_count):
        x = random.randint(10, img.width - 10)
        y = random.randint(10, img.height - 10)
        img.putpixel((x,y), (255, 255, 255))


    # Show (if needed, and )
    if(isPreviewNeeded) is (not None or not False):
        img.show()
    print('Saving in file: {}'.format(fileName))
    img.save(fileName)



#? Generate star images - Testing only!
for i in range(1,301):
    generateStarImage(random.randint(100, 300), 'assets/images/bg_stars-{}.png'.format('0' + (str(i)) if i < 10 else str(i)), False)