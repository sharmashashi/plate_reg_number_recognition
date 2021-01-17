import os
import cv2


class Sorting:
    def coordinate_from_name(self, name):
        x = ''
        y = ''
        lockX = False
        lockY = True
        for char in name:
            if lockX == False:
                if(char != "_"):
                    x += char
                else:
                    lockX = True
                    lockY = False
            elif lockY == False:
                if(char != "."):
                    y += char
                else:
                    lockY = True

        return int(x), int(y)

    def bubbleSort(self, arr):
        n = len(arr)
        for i in range(n-1):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    def generatesortedrow(self, rowdirname):
        sortedimages = []
        for each in os.listdir(rowdirname):
            number = ""
            for char in each:
                if char != ".":
                    number = number + char
                else:
                    break
            sortedimages.append(int(number))
        # print(sortedimages)
        sortedimages = self.bubbleSort(sortedimages)
        # print(sortedimages)

        sortedimagefiles = []
        i = 0
        for each in sortedimages:
            img = cv2.imread(rowdirname+str(each) + ".png")
            os.remove(rowdirname+str(each)+".png")
            resized = cv2.resize(img,(32,32))
            cv2.imwrite(rowdirname+str(i)+".png", resized)
            i += 1

    def merge(self, firstpath, secondpath,finalpath):
        self.clearDir(finalpath)
        i = 0
        j = 0
        for each in os.listdir(firstpath):
            img = cv2.imread(firstpath+str(j)+".png")
            cv2.imwrite(finalpath+str(i)+".png", img)
            i += 1
            j += 1
        j = 0
        for each in os.listdir(secondpath):
            img = cv2.imread(secondpath+str(j)+".png")
            cv2.imwrite(finalpath+str(i)+".png", img)
            i += 1
            j += 1

    def clearDir(self, dirpath):
        for each in os.listdir(dirpath):
            os.remove(dirpath+each)

    def sort(self, imagepath, separator_y,finalpath):
        #
        self.clearDir("api/src/top_row/")
        self.clearDir("api/src/bottom_row/")
        #
        for each in os.listdir(imagepath):
            x, y = self.coordinate_from_name(each)
            if y <= separator_y:
                cv2.imwrite("api/src/top_row/"+str(x)+".png",
                            cv2.imread(imagepath+"/"+each))
            else:
                cv2.imwrite("api/src/bottom_row/"+str(x)+".png",
                            cv2.imread(imagepath+"/"+each))

        self.generatesortedrow("api/src/top_row/")
        self.generatesortedrow("api/src/bottom_row/")
        self.merge("api/src/top_row/", "api/src/bottom_row/",finalpath)
        return finalpath
