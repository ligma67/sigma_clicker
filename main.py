import pygame
import time
from copy import copy

pygame.init()

mpos = (0, 0)
#жесть
clotheshas = []
things = [
    [
        [{'e0': 20}, 'Скибиди стул', 'Присядь, +1 к клику', 'click', {'e0': 1}, 'imageslol/0_0.jpg', 0],
        [{'e0': 100}, 'Мышь Defender', 'Дает +1 в сек', "auto", {'e0':1}, 'imageslol/0_1.jpg', 0],
        [{'e0': 250}, 'Улучшенный щелк', 'Всего +10 к клику', 'click', {'e0':10}, 'imageslol/0_2.png', 0],
        [{'e0':500}, 'ChatGPT 2.0', 'Прибавляет по +10 в сек', 'auto', {'e0':10}, 'imageslol/0_3.png', 0]
    ],
    [
        [{'e0':0, 'e3': 1}, 'Кожаная броня', 'Не густо... +25 к клику', 'click wear', {'e0': 25}, 'imageslol/1_0.jpg', 0, ['imageslol/leather_chest.png', 'imageslol/leather_helmet.png']],
        [{'e0':0, 'e3': 20}, 'Я.Музыка (торрент)', 'Послушай музыку, +200/сек', "auto music", {'e0':200}, 'imageslol/1_1.jpg', 0, ['bgmusic.mp3']],
        [{'e0':0, 'e3':50}, 'Взросление', 'Закрой магазин, нажми -->', 'image', {'e0':10}, 'imageslol/1_2.jpg', 0, ['sigmabuttongigachad.jpg'], 1],
        [{'e0':0, 'e3': 100}, 'ChatGPT 3.0', 'Для людей. +1к/клик', 'click', {'e3':1}, 'imageslol/0_3.png', 0]
    ],
    [
        [{'e0':0, 'e3': 500}, '/god', 'Купил админку, +30e3 к кл', 'click', {'e3': 30}, 'imageslol/2_0.jpg', 0],
        [{'e0':0, "e3":0, 'e6': 1}, 'Душ', 'Пока сходи в душ, +10e3 в сек', "auto", {'e3':10}, 'imageslol/2_1.jpg', 0],
        [{'e0':0, 'e3': 0, 'e6': 50}, 'Свой бизнес.', 'Миллионер. В секунду', 'auto', {'e6':1}, 'imageslol/2_2.png', 0],
        [{'e0':0,  'e3': 0, 'e6':100}, 'Раз в жизни', 'Удваивает твою силу клика.', 'x2cl', {'e0':10}, 'imageslol/2_3.jpg', 0, [], 1]
    ]

]
#существует megaupgr, жесткая вещь. не ставить в 4 слот
clock = pygame.time.Clock()
FPS = 60
w = 1366
h = 768
screen = pygame.display.set_mode([w, h])
pygame.display.set_caption('Мульти-Сигма-Кликер')
#переменныепросто
bgisimageorcolor = 'image'
bgcolor = [255, 255, 255]
bgimage = pygame.image.load('bgimage.jpg')
sigmabuttonimage = pygame.image.load('sigmabutton.jpg')
shopbuttonimage = pygame.image.load('shopbutton1.png')
upgradebuttonimage = pygame.image.load('upgradesbutton.png')
screentype = 'clicker'
wearssmth = True
wearswhat = []
volume = 0.4
musicact = True
musics = ['bgmusic.mp3']
sigmabuttonimageshas = ['sigmabutton.jpg']
sigmabuttonimagecount = 0
pygame.mixer.music.load(musics[0])
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(loops=-1)
#переменные для объектов
bgx = 0
bgflag = 0.5
bgspeed = 1
page = 0
sigmabuttonx = w / 2 - sigmabuttonimage.get_width() // 2
sigmabuttony = h / 2 - sigmabuttonimage.get_height() // 2
shopbuttony = -1000
shopbuttonx = -1000
upgradebuttonx = w - upgradebuttonimage.get_width() * 1.25
upgradebuttony = 10
upgrademenuopen = False
upgrmegaactive = False

#text
textforpoints = pygame.font.Font('fontpoints.ttf', 65)
textforppc = pygame.font.Font('fontpoints.ttf', 40)
textforappc = pygame.font.Font('fontpoints.ttf', 40)

#длясигма
pointstextx = w / 2 - sigmabuttonimage.get_width() / 2 - textforpoints.get_height()
ppctext = (50, 600)
appctext = (50, 675)

#поинты


pointsperclick = {'e0':1}
autopointsperclick = {'e0': 0}


#функции
def pointstextoret(pointss):
    pointss = pointconvert(pointss)
    a = ''
    b = 'e0'
    for i in reversed(pointss):
        if pointss[i] >= 1:
            a += str(pointss[i])
            b = i
            break

    if b == 'e0':
        return a
    elif len(pointss) == 1 and pointss['e0'] == 0:
        return a
    elif pointss[b[0] + str((int(b[1:]) - 3))] < 10:
        a += '.00'
        a += str(pointss[b[0] + str((int(b[1:]) - 3))])
        a += ' ' + b
        return a
    elif pointss[b[0] + str((int(b[1:]) - 3))] < 100:
        a += '.0'
        if pointss[b[0] + str((int(b[1:]) - 3))] % 10 == 0:
            a += str(pointss[b[0] + str((int(b[1:]) - 3))] // 10)
        else:
            a += str(pointss[b[0] + str((int(b[1:]) - 3))])
        a += ' ' + b

        return a
    elif pointss[b[0] + str((int(b[1:]) - 3))] < 1000:
        if pointss[b[0] + str((int(b[1:]) - 3))] % 10 == 0:
            if pointss[b[0] + str((int(b[1:]) - 3))] % 100 == 0:
                a += '.' + str(pointss[b[0] + str((int(b[1:]) - 3))] // 100)
            else:
                a += '.' + str(pointss[b[0] + str((int(b[1:]) - 3))] // 10)
        else:
            a += '.' + str(pointss[b[0] + str((int(b[1:]) - 3))])
        a += ' ' + b

        return a


def pointconvert(pointss):
    abcde = copy(pointss)
    for i in pointss:
        if abcde[i] >= 1000:
            howmany = abcde[i] // 1000
            abcde[i] -= abcde[i] // 1000 * 1000
            if i[0] + str((int(i[1:]) + 3)) in abcde:
                abcde[i[0] + str((int(i[1:]) + 3))] += howmany
            else:
                abcde[i[0] + str((int(i[1:]) + 3))] = howmany


    return copy(abcde)

def bigprice(price):
    adv = copy(price)
    adv = {key:adv[key] for key in sorted(adv)}



    infff = ''
    infff2 = ''
    summofzeros = 0
    for esq in reversed(adv):
        infff = esq
        break
    for esq2 in adv:
        infff2 = esq2
        break
    for thinges in adv:
        if adv[thinges] == 0:
            summofzeros += 1
    howmany = 0
    if len(adv) == 1:
        if infff == 'e0':
            adv[infff] = round(1.15 * adv[infff])
            return adv
        else:

            howmany = adv[infff[0]+str(int(infff[1:]))]
            adv[infff[0] + str(int(infff[1:]))] -= howmany

            adv[infff[0] + str(int(infff[1:]) - 3)] = howmany


    if len(adv) >= 2:
        if infff == infff2:
            howmany = adv[infff2[0] + str(int(infff[1:]) + 3)]
            adv[infff2[0] + str(int(infff2[1:]) + 3)] -= howmany
            adv[infff2] += (howmany * 1000 * 1.15)

            return pointconvert(adv)
        else:
            stop = int(infff[1:])
            start = int(infff2[1:])
            for i in range(stop, start, -3):
                iconvert = 'e'+str(i)
                iconvert2 = 'e'+str(i-3)
                howmany = adv[iconvert]
                adv[iconvert] -= howmany
                adv[iconvert2] += howmany*1000
            adv['e'+str(start)] = round(1.15*adv['e'+str(start)])

            return pointconvert(adv)









def pointsadd(pointsforclick, pointss):
    for i in pointsforclick:
        if i in pointss:
            pointss[i] += pointsforclick[i]
        else:
            pointss[i] = pointsforclick[i]
    return pointss


def fltoint(thedict):
    for i in thedict:
        thedict[i] = int(thedict[i])
    return thedict

def sendwhat(points, ppc, appc, type):
    if 'click' in type:
        return [ppc, points]
    elif "auto" in type:
        return [appc, points]
    elif 'image' in type:
        return [ppc, points]
    elif 'megaupgr' in type or 'x2cl' in type:
        return [ppc, points]


def makeapointlist(pointss):
    maxpoint = 'e0'
    for i in reversed(pointss):
        maxpoint = i
        break
    for i in range(0, int(maxpoint[1]), 3):
        if not 'e' + str(i) in pointss:
            pointss['e' + str(i)] = 0
    pointconvert(pointss)
    return pointss

def x2(pointsperclick):
    for i in pointsperclick:
        pointsperclick[i]*=2
    return pointconvert(pointsperclick)

def _sort_dict(d):
    def _by_num(key):
        return int(key[1:])

    return dict(sorted(d.items(), key=lambda x: _by_num(x[0])))


def buycheck(pointss, pricee, check=False):
    howmuch = len(pricee)

    price = _sort_dict(copy(pricee))

    pointss = _sort_dict(makeapointlist(pointconvert(copy(pointss))))

    truetimes = 0
    mad = 0
    summ = 0
    if len(price) != -1:
        for i in price:

            if i in pointss:

                whiche = i

                if pointss[whiche] >= price[whiche]:
                    pointss[whiche] -= price[whiche]
                    truetimes += 1
                    pointconvert(pointss)

                elif pointss[whiche] < price[whiche]:

                    lastpoint = 'e'
                    for eshkere in reversed(price):
                        lastpoint = eshkere
                        break

                    has = 0
                    whereeee = 'e'

                    if whiche != lastpoint or len(price) == 1:

                        for qe in pointss:

                            if int(qe[1:]) > int(i[1:]) and pointss[qe] >= 1 and int(qe[1:]) != int(i[1:]):
                                has = 1
                                whereeee = qe

                                break

                        if has != 0 and whereeee != 'e':

                            for bla in range(int(whereeee[1:]), int(i[1:]), -3):  # ОШИБКА ЗДЕСЬ

                                whattt = 'e' + str(bla)
                                whattt2 = 'e' + str(bla - 3)
                                if whattt2 == 'e-3':
                                    truetimes -= 1
                                    break

                                pointss[whattt] -= 1
                                pointss[whattt2] += 1000
                                pointss[whattt2] -= price[whiche]
                            truetimes += 1
                    else:

                        ane = i[0]
                        numba = int(i[1:])
                        numb2 = -1
                        has = False
                        where = ''
                        for wja in reversed(pointss):
                            ane1 = wja[0]
                            numb2 = int(wja[1:])

                            break

                        for bbb in range(numba + 3, numb2 + 1, 3):
                            dictname = 'e' + str(bbb)

                            if dictname in pointss:
                                if pointss[dictname] >= 1:
                                    has = True
                                    where = dictname

                                    break

                        if has:
                            for exc in range(int(where[1:]), numba, -3):
                                idagain = 'e' + str(exc)

                                minusedid = 'e' + str(exc - 3)
                                if pointss[idagain] >= 1:
                                    pointss[idagain] -= 1
                                    pointss[minusedid] += 1000
                                    pointss[whiche] -= price[whiche]

                                else:

                                    break

                            truetimes += 1

                pointconvert(pointss)

    if truetimes + mad == len(price):

        return [True, pointconvert(pointss), pointconvert(price)]
    else:

        return [False, pointconvert(points), pointconvert(price)]



points = {'e0': 0}
ppctextnotx = textforppc.render(f'Сигм за клик: {pointstextoret(pointsperclick)}', False, [255, 255, 255])
appctextnotx = textforppc.render(f'Сигм в сек: {pointstextoret(autopointsperclick)}', False, [255, 255, 255])

# 'e3':0}
class Thinginshop():
    def __init__(self, x, y, isactive):
        self.image = pygame.Surface((500, 500))
        self.image.fill((10, 100, 20))
        self.status = isactive
        self.upgr1 = None
        self.upgr2 = None
        self.upgr3 = None
        self.upgr4 = None

        self.txt = pygame.font.Font("numberfont.ttf", 50)
        self.pagetxt = self.txt.render(f'Страница: {page+1}/{len(things)}', False, (255, 255, 255))

        self.x = x
        self.y = y
        self.posforsmth = 75
        self.posforprice = (275, 10)

    def blitme(self):
        screen.blit(self.image, [self.x, self.y])

    def generateitems(self):
        self.upgr1 = Upgrade(*things[page][0])
        self.upgr2 = Upgrade(*things[page][1])
        self.upgr3 = Upgrade(*things[page][2])
        self.upgr4 = Upgrade(*things[page][3])
        self.displaythings(page, self.upgr1.screenn, self.upgr2.screenn, self.upgr3.screenn, self.upgr4.screenn)

    def displaythings(self, page, item1scr, item2scr, item3scr, item4scr):
        self.image.fill((10, 100, 20))

        self.image.blit(item1scr, [10, 10])
        self.image.blit(item2scr, [10, 120])
        self.image.blit(item3scr, [10, 230])
        self.image.blit(item4scr, [10, 340])
        self.pagetxt = self.txt.render(f'Страница: {page+1}/{len(things)}', False, (255, 255, 255))
        self.image.blit(self.pagetxt, [175, 430])
        pygame.display.update()


class Upgrade():
    def __init__(self, price, name, descr, type, howmuch, image, activated, addclothes=[],  activations=100):
        self.posforsmth = 82
        self.screenn = pygame.Surface((480, 90))
        self.screenn.fill((0, 0, 0))
        self.pricee = makeapointlist(price)
        self.photo = pygame.image.load(image)
        self.addclothes = addclothes
        self.activated = activated
        self.activations = activations
        self.txt = pygame.font.Font('fontpoints.ttf', 22)
        self.namefont = pygame.font.Font('fontdescr.ttf', 30)
        self.descrfont = pygame.font.Font('fontdescr.ttf', 25)
        self.nametxt = self.namefont.render(name, False, (255, 255, 255))
        self.descrtxt = self.descrfont.render(descr, False, (255, 255, 255))

        if activated < activations:
            self.pricetxt = self.txt.render(pointstextoret(makeapointlist(self.pricee)), False, (0, 255, 0))
            self.abletobuytxt = self.txt.render(f'{activated}/{activations}', False, (0, 0, 255))
        else:
            self.pricetxt = self.txt.render('', False, (0, 255, 255))
            self.abletobuytxt = self.txt.render('Sold out', False, (255, 0, 0))
        self.type = type  #click, auto, other
        self.howmuch = howmuch  #what you get, if other then ' '
        self.screenn.blit(self.nametxt, (self.posforsmth, 20))
        self.screenn.blit(self.descrtxt, (self.posforsmth, 55))
        self.screenn.blit(self.pricetxt, (325, 15))
        self.screenn.blit(self.photo, (5, 10))
        self.screenn.blit(self.abletobuytxt, (350, 60))

    def whenbought(self, pointsperclick, pointsss, numb, image = ''):
        if self.activated < self.activations:
            a = buycheck(copy(points), copy(self.pricee))
            if a[0] == False:
                return [a[1]]
            else:
                self.pricee = fltoint(copy(bigprice(a[2])))
                self.activated = self.activated + 1
                self.screenn.fill((0, 0, 0))
                self.screenn.blit(self.nametxt, (self.posforsmth, 10))
                self.screenn.blit(self.descrtxt, (self.posforsmth, 40))
                self.pricetxt = self.txt.render(pointstextoret(makeapointlist(self.pricee)), False, (255, 255, 255))
                self.screenn.blit(self.pricetxt, (275, 10))
                self.screenn.blit(self.photo, (2, 2))
                things[page][numb][0] = copy(self.pricee)
                things[page][numb][6] = self.activated
                pygame.display.update()
                if 'click' in self.type:
                    if 'wear' in self.type:
                        if self.activated <= 1:
                            for i in self.addclothes:
                                wearssmth = True
                                clotheshas.append(i)
                                wearswhat.append(i)



                    return [pointsadd(self.howmuch, pointsperclick), a[1]]
                elif 'auto' in self.type:
                    if 'music' in self.type:
                        for i in self.addclothes:
                            musics.append(i)

                    return [pointsadd(self.howmuch, makeapointlist(autopointsperclick)), a[1]]
                elif 'image' in self.type:
                    image = self.addclothes[0]
                    screen.blit(sigmabuttonimage, [sigmabuttonx-100, sigmabuttony])
                    return [image, a[1]]
                elif 'megaupgr' in self.type:
                    return [pointsperclick, a[1]]
                elif 'x2cl' in self.type:
                    return x2(pointsperclick)
        else:
            return [False]



upgradesmenu = Thinginshop(w - 525, 150, False)
pointstext = textforpoints.render(f'Сигм: {pointstextoret(points)}', False, [255, 255, 255])
musicflag = True
timer_interval = 1000
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, timer_interval)
captionacts = 2

runs = True

while runs:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            pygame.quit()
            runs = False
        elif i.type == timer_event:
            pointsadd(autopointsperclick, points)
            pointstext = textforpoints.render(f'Сигм: {pointstextoret(points)}', False, [255, 255, 255])


        if screentype == 'clicker':
            if i.type == pygame.MOUSEBUTTONDOWN:
                if i.button == 1 or i.button == 3:
                    mpos = pygame.mouse.get_pos()
                    if upgradesmenu.status == False:
                        if sigmabuttonx < mpos[0] < sigmabuttonx + sigmabuttonimage.get_width() and sigmabuttony < mpos[
                            1] < sigmabuttony + sigmabuttonimage.get_height():
                            points = pointsadd(pointsperclick, points)
                            if upgrmegaactive:
                                pointsperclick = pointconvert(x2(pointsperclick))
                            pointstext = textforpoints.render(f'Сигм: {pointstextoret(points)}', False, [255, 255, 255])
                    elif upgradesmenu.status == True:
                        if sigmabuttonx - 100 < mpos[
                            0] < sigmabuttonx - 100 + sigmabuttonimage.get_width() and sigmabuttony < mpos[
                            1] < sigmabuttony + sigmabuttonimage.get_height():
                            points = pointsadd(pointsperclick, points)
                            if upgrmegaactive:
                                pointsperclick = pointconvert(x2(pointsperclick))
                            pointstext = textforpoints.render(f'Сигм: {pointstextoret(points)}', False, [255, 255, 255])
                        if mpos[0] in range(upgradesmenu.x, upgradesmenu.x + 400) and mpos[1] in range(upgradesmenu.y,
                                                                                                       upgradesmenu.y + 400):
                            #if mpos[0] in range(upgradesmenu.item1())
                            if captionacts >= 1:
                                pygame.display.set_caption('НАЖИМАЙ НА ЦИФРЫ (1, 2, 3, 4)')
                                captionacts -= 1
                                time.sleep(2)
                                pygame.display.set_caption('Мульти-Сигма-Кликер')


                            #СДЕЛАТЬ
                    if shopbuttonx < mpos[0] < shopbuttonx + shopbuttonimage.get_width() and shopbuttony < mpos[
                        1] < shopbuttony + shopbuttonimage.get_height():
                        screentype = 'shop'
                        pygame.display.set_caption('Магазин')
                        bgimage = pygame.image.load('bgimage2.jpg')
                        screen.blit(bgimage, [bgx, 0])
                    if upgradebuttonx < mpos[0] < upgradebuttonx + upgradebuttonimage.get_width() and upgradebuttony < \
                            mpos[1] < upgradebuttony + upgradebuttonimage.get_height():
                        upgradesmenu.status = not upgradesmenu.status
            elif i.type == pygame.KEYDOWN:
                if upgradesmenu.status:

                    if i.key == pygame.K_1:
                        try:
                            what = sendwhat(points, pointsperclick, autopointsperclick, upgradesmenu.upgr1.type)
                            b1 = upgradesmenu.upgr1.whenbought(what[0], what[1], 0)
                            if len(b1) == 1:
                                print('nuh uh')
                            else:
                                if 'click' in upgradesmenu.upgr1.type:
                                    var = pointsperclick == b1[0]
                                    points = b1[1]
                                elif 'auto' in upgradesmenu.upgr1.type:
                                    var = autopointsperclick == b1[0]
                                    points = b1[1]


                        except KeyError as aooaoo:

                            print(aooaoo, "KEYERROR, YOU DONT HAVE THIS YET")
                    elif i.key == pygame.K_2:
                        try:
                            what = sendwhat(points, pointsperclick, autopointsperclick, upgradesmenu.upgr2.type)
                            b2 = upgradesmenu.upgr2.whenbought(what[0], what[1], 1)
                            if len(b2) == 1:
                                print('nuh uh')
                            else:
                                if 'click' in upgradesmenu.upgr2.type:
                                    var = pointsperclick == b2[0]
                                    points = b2[1]
                                elif 'auto' in upgradesmenu.upgr2.type:
                                    var = autopointsperclick == b2[0]
                                    points = b2[1]
                        except KeyError as aooaoo:
                            print(aooaoo, "KEYERROR, YOU DONT HAVE THIS YET")
                    elif i.key == pygame.K_3:
                        try:
                            what = sendwhat(points, pointsperclick, autopointsperclick, upgradesmenu.upgr3.type)
                            b3 = upgradesmenu.upgr3.whenbought(what[0], what[1], 2)
                            if len(b3) == 1:
                                if upgradesmenu.upgr3.type != 'image':
                                    print('nuh uh')


                            else:
                                if 'click' in upgradesmenu.upgr3.type:
                                    var = pointsperclick == b3[0]
                                    points = b3[1]
                                elif 'auto' in upgradesmenu.upgr3.type:
                                    var = autopointsperclick == b3[0]
                                    points = b3[1]
                                elif "image" in upgradesmenu.upgr3.type:
                                    if b3[0] != False:
                                        sigmabuttonimageshas.append(b3[0])

                                        points = b3[1]


                        except KeyError as aooaoo:
                            print(aooaoo, "KEYERROR, YOU DONT HAVE THIS YET")
                    elif i.key == pygame.K_4:
                        try:
                            what = sendwhat(points, pointsperclick, autopointsperclick, upgradesmenu.upgr4.type)
                            b4 = upgradesmenu.upgr4.whenbought(what[0], what[1], 3)
                            if len(b4) == 1:
                                print('nuh uh')
                            else:
                                if 'click' in upgradesmenu.upgr4.type:
                                    var = pointsperclick == b4[0]
                                    points = b4[1]
                                elif 'auto' in upgradesmenu.upgr4.type:
                                    var = autopointsperclick == b4[0]
                                    points = b4[1]
                                elif 'megaupgr' in upgradesmenu.upgr4.type:
                                    upgrmegaactive = True

                        except KeyError as aooaoo:
                            print(aooaoo, "KEYERROR, YOU DONT HAVE THIS YET")

                    elif i.key == pygame.K_RIGHT:
                        if page < len(things)-1:
                            page += 1

                            upgradesmenu.generateitems()
                    elif i.key == pygame.K_LEFT:
                        if page >= 1:
                            page -= 1

                            upgradesmenu.generateitems()
                else:
                    if i.key == pygame.K_RIGHT:
                        if sigmabuttonimagecount < len(sigmabuttonimageshas)-1:
                            sigmabuttonimagecount += 1
                        sigmabuttonimage = pygame.image.load(sigmabuttonimageshas[sigmabuttonimagecount])
                    elif i.key == pygame.K_LEFT:
                        if sigmabuttonimagecount > 0:
                            sigmabuttonimagecount -= 1
                        sigmabuttonimage = pygame.image.load(sigmabuttonimageshas[sigmabuttonimagecount])

                if i.key == pygame.K_SPACE:
                    musicflag = not musicflag
                    if musicflag:
                        pygame.mixer.music.unpause()
                    else:
                        pygame.mixer.music.pause()



    screen.blit(bgimage, [bgx, 0])


    bgx -= bgspeed * bgflag
    if -(bgimage.get_width() - w) > bgx or bgx > 1.1:
        bgflag *= -1

    if screentype == 'clicker':
        screen.blit(shopbuttonimage, [shopbuttonx, shopbuttony])
        screen.blit(upgradebuttonimage, [upgradebuttonx, upgradebuttony])
        if upgradesmenu.status == False:
            screen.blit(sigmabuttonimage, [sigmabuttonx, sigmabuttony])
            screen.blit(pointstext, [pointstextx, 60])
            screen.blit(ppctextnotx, ppctext)
            screen.blit(appctextnotx, appctext)
            if len(wearswhat) > 1:
                screen.blit(pygame.image.load(wearswhat[0]), [sigmabuttonx, sigmabuttony])
                screen.blit(pygame.image.load(wearswhat[1]), [sigmabuttonx, sigmabuttony])
        elif upgradesmenu.status == True:

            screen.blit(sigmabuttonimage, [sigmabuttonx - 100, sigmabuttony])
            if len(wearswhat) > 1:
                screen.blit(pygame.image.load(wearswhat[0]), [sigmabuttonx-100, sigmabuttony])
                screen.blit(pygame.image.load(wearswhat[1]), [sigmabuttonx-100, sigmabuttony])
            screen.blit(pointstext, [pointstextx - 100, 60])
            screen.blit(ppctextnotx, ppctext)
            screen.blit(appctextnotx, appctext)
            upgradesmenu.blitme()

            upgradesmenu.generateitems()



    elif screentype == 'shop':
        pass



    pointconvert(points)
    pointstext = textforpoints.render(f'Сигм: {pointstextoret(points)}', False, [255, 255, 255])
    ppctextnotx = textforppc.render(f'Сигм за клик: {pointstextoret(pointsperclick)}', False, [255, 255, 255])
    appctextnotx = textforppc.render(f'Сигм в сек: {pointstextoret(autopointsperclick)}', False, [255, 255, 255])
    screen.blit(ppctextnotx, ppctext)
    screen.blit(appctextnotx, appctext)
    pygame.display.update()
    clock.tick(FPS)

