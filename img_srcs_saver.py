import urllib.request
import csv


# csv를 열고 해당 값들을 불러오는 함수
def openCsv(path, fileName):
    imgsUrl = []

    f = open(f'{path}{fileName}.csv', 'r')
    csvReader = csv.reader(f)
    for l in csvReader:
        if l:
            imgsUrl.append(l[0])

    return imgsUrl

# url을 바탕으로 해당 이미지를 저장해주는 함수
def saveImgs(imgsUrl, targetName):
    count = 1

    opener = urllib.request.build_opener()

    """ browser header setting """
    header = "Mozilla/5.0 Chrome/118.0.5993.70"
    opener.addheaders = [(header)]
    urllib.request.install_opener(opener)

    for imgUrl in imgsUrl:
        try:
            urllib.request.urlretrieve(imgUrl, f'./img_srcs/{targetName}/{targetName}{str(count)}.jpg')
        except Exception as e:
            print(f'error {count}th :', e)
            pass

        count = count + 1


""" custom this place """
fileName = "가을"

# csv를 열고 해당 값들을 불러오기
path = f"./img_urls/{fileName}/"
imgsUrl = openCsv(path, fileName)

# url을 바탕으로 해당 이미지를 저장하기
saveImgs(imgsUrl, fileName)
