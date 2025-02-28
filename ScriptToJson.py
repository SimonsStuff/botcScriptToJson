# Import required packages
import os
import sys

import cv2

def main(file):
    characters = ['Chef', 'Investigator', 'Undertaker', 'Fortune Teller', 'Ravenkeeper', 'Soldier', 'Virgin', 'Imp', 'Slayer', 'Poisoner', 'Spy', 'Scarlet Woman', 'Baron', 'Washerwoman', 'Librarian', 'Empath', 'Monk', 'Mayor', 'Butler', 'Saint', 'Recluse', 'Drunk', 'Tea Lady', 'Pacifist', 'Gambler', 'Gossip', 'Mastermind', 'Po', 'Moonchild', 'Tinker', 'Exorcist', 'Courtier', 'Fool', 'Assassin', 'Devil', 'Grandmother', 'Sailor', 'Chambermaid', 'Innkeeper', 'Professor', 'Minstrel', 'Goon', 'Lunatic', 'Godfather', 'Zombuul', 'Pukka', 'Shabaloth', 'Fang Gu', 'No Dashii', 'Vigormortis', 'Vortox', 'Pit-Hag', 'Witch', 'Cerenovus', 'Clockmaker', 'Dreamer', 'Snake Charmer', 'Mathematician', 'Flowergirl', 'Town Crier', 'Oracle', 'Savant', 'Seamstress', 'Philosopher', 'Artist', 'Juggler', 'Sage', 'Mutant', 'Sweetheart', 'Barber', 'Klutz', 'Evil Twin', 'Alchemist', 'Amnesiac', 'Atheist', 'Balloonist', 'Bounty Hunter', 'Cannibal', 'Choirboy', 'Cult Leader', 'Engineer', 'Farmer', 'Fisherman', 'General', 'High Priestess', 'Huntsman', 'King', 'Knight', 'Lycanthrope', 'Magician', 'Nightwatchman', 'Noble', 'Pixie', 'Poppy Grower', 'Preacher', 'Steward', 'Acrobat', 'Damsel', 'Golem', 'Heretic', 'Plague Doctor', 'Politician', 'Puzzlemaster', 'Snitch', 'Boomdandy', 'Fearmonger', 'Goblin', 'Harpy', 'Marionette', 'Mezepheles', 'Organ Grinder', 'Psychopath', 'Vizier', 'Widow', 'Al-Hadikhia', 'Legion', 'Leviathan', 'Lil', 'Lleech', 'Riot', 'Storm Catcher', 'Ferryman', 'Bootlegger', 'Gardener', 'Gangster']

    # Read image from which text needs to be extracted
    img = cv2.imread("a.png")

    # Preprocessing the image starts

    # Convert the image to gray scale

    height, width,_ = img.shape

    for i in range(height):
        for j in range(width):
            # img[i, j] is the RGB pixel at position (i, j)
            # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
            if img[i, j][0] == img[i,j][1] and img[i, j][0] == img[i,j][2]:
                img[i, j] = [255, 255, 255]
            if img[i,j][0] < 205 and img[i,j][2] < 205:
                img[i, j] = [255, 255, 255]
            if img[i,j][0] > 250 and img[i,j][2] > 250 and img[i,j][2] > 250:
                img[i, j] = [255, 255, 255]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for i in range(height):
        for j in range(width):
            # img[i, j] is the RGB pixel at position (i, j)
            # check if it's [0, 0, 0] and replace with [255, 255, 255] if so
            if gray[i, j] < 75:
                gray[i, j] = 255
    ret,thresh = cv2.threshold(gray,248,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    avgW = 0
    avgH = 0
    newContours = []
    avgArea = 0
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        newContours.append([x,y,w,h])
        avgW += w
        avgH += h
        avgArea += cv2.contourArea(c)
    avgArea = avgArea - (height*width)
    noContours = len(contours)
    newContours.sort(key=lambda x:x[2]*x[3],reverse=True)
    newContours = newContours[1:]
    newContours = newContours[0:20]

    for c in newContours:
        x,y,w,h = c
        if w > 40 or h > 40:
            if h < w*1.5:
                if w*h > avgArea/len(contours):
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255,255,255), 1)
            else:
                numChars = round(h/w*0.9)
                for chars in range(numChars):
                    cv2.rectangle(img, (x, y+int(chars*h/numChars)), (x + w, y+int(chars*h/numChars) + int(h/numChars)), (255,255,255), 1)

    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh2 = cv2.threshold(gray2,250,255,cv2.THRESH_BINARY)
    contours2, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    imgList = []
    im2 = img.copy()
    charsOnScript = []

    for c in contours2:
        x,y,w,h = cv2.boundingRect(c)
        if w > 10 and h > 10:
            if cv2.contourArea(c) > 10000:
                continue
            newImg = im2[y:y+h,x:x+w]
            newImg = cv2.resize(newImg,(50,50))
            grayNew = cv2.cvtColor(newImg, cv2.COLOR_BGR2GRAY)
            ret,threshNew = cv2.threshold(grayNew,235,255,cv2.THRESH_BINARY)
            flattenNew = threshNew.flatten()
            maxScore = 0
            bestMatch = ""
            for filename in os.listdir("Pictures"):
                checkImg = cv2.imread("Pictures/"+filename)

                checkImg = cv2.resize(checkImg,(50,50))

                grayCheck = cv2.cvtColor(checkImg, cv2.COLOR_BGR2GRAY)
                ret,threshCheck = cv2.threshold(grayCheck,245,255,cv2.THRESH_BINARY)

                flattenCheck = threshCheck.flatten()
                score = 0
                for i in range(len(flattenNew)):
                    if flattenCheck[i] == flattenNew[i]:
                        score+=1

                if score/len(flattenNew)>maxScore:
                    maxScore = score/len(flattenNew)

                    bestMatch = filename


            if maxScore > 0.75:
                newName = bestMatch.replace(" ", "_")
                newName = newName.replace("'", "")
                newName = newName.lower()
                charsOnScript.append(newName.split(".")[0])

            cv2.rectangle(img, (x, y), (x + w, y + h), (30,255,30), 1)

    jsonText = "[{\"id\":\"_meta\",\"author\":\"\",\"name\":\"\"}"
    charsOnScript.reverse()
    for charNames in charsOnScript:
        if jsonText.__contains__(charNames):
            continue
        jsonText = jsonText + ",{\"id\":\"" + charNames + "\"}"
    jsonText = jsonText + "]"
    f = open("jsonScript.json", "w")
    f.write(jsonText)
    f.close()

    cv2.imshow("Image",img)
    cv2.waitKey()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

if __name__ == '__main__':
    main(sys.argv[0])