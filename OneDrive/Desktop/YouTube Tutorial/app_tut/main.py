import pygame, pygamereq as pyreq, mysql.connector, random, time as t, datetime, winsound
from pygame.locals import *; from pygame import *

whatsappbool = True

if whatsappbool:
    import pywhatkit

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mandaveli7531",
    database="cscproj"
)

cursordb = database.cursor()

carimg = pygame.image.load("car.png")

screen, clock = pyreq.init('Parking lot management App', 0, carimg)

class Button:
    def __init__(self, rect, color1, color2, text, border = (0, 0, 0)):
        self.rect = rect
        self.color1 = color1; self.color2 = color2
        self.text = text
        self.border = border
    def show(self, mouse):
        if not self.rect.collidepoint(mouse):
            pygame.draw.rect(screen.surf, self.border, (self.rect.x - 4, self.rect.y - 4, self.rect.w + 8, self.rect.h + 8))
            pygame.draw.rect(screen.surf, self.color1, self.rect)
        else:
            pygame.draw.rect(screen.surf, self.border, (self.rect.x - 10, self.rect.y - 10, self.rect.w + 20, self.rect.h + 20))
            pygame.draw.rect(screen.surf, self.color2, (self.rect.x - 6, self.rect.y - 6, self.rect.w + 12, self.rect.h + 12))
        pyreq.write(screen.surf, self.text, (self.rect.x + 10, self.rect.centery - 14), int((len(self.text)*(self.rect.w/len(self.text))/8)))

button1 = Button(Rect(screen.rect.centerx - 300, 200, 200, 100), (255, 0, 0), (255, 200, 200), "Administrator")
button2 = Button(Rect(screen.rect.centerx + 100, 200, 200, 100), (0, 255, 0), (200, 255, 200), "Customer")

plist = []

class Particle:
    def __init__(self, pos, color, shape, size):
        self.pos = list(pos)
        self.color = color
        self.shape = shape
        self.size = size
    def update(self, dim):
        if dim == "x-":
            self.pos[0] -= 2
            self.pos[1] += random.randint(-2, 2)
        if dim == "x+":
            self.pos[0] += 2
            self.pos[1] += random.randint(-2, 2)
        if dim == "y-":
            self.pos[1] -= 2
            self.pos[0] += random.randint(-2, 2)
        if dim == "y+":
            self.pos[1] += 2
            self.pos[0] += random.randint(-2, 2)
    def show(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.size)

def dust(surface, pos, color=(200, 200, 255), limit=0, dim='x-'):
    if random.randint(0, 6) == 0:
        plist.append(Particle(pos, color, 'circle', 3))
    for bubble in plist:
        bubble.update(dim)
        bubble.show(surface)
    if len(plist) > 1:
        if dim == "x-":
            if plist[0].pos[0] < limit:
                plist.pop(0)
        if dim == "x+":
            if plist[0].pos[0] > limit:
                plist.pop(0)
        if dim == "y-":
            if plist[1].pos[1] < limit:
                plist.pop(0)
        if dim == "y+":
            if plist[1].pos[1] > limit:
                plist.pop(0)

def resetdust():
    global plist
    plist = []

def startapp():
    iter = 0
    iter2 = 0
    x, y = screen.w/2 - 100, screen.h/2 - 10
    while True:
        pygame.display.flip(); clock.tick(10)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
        screen.surf.fill((200, 200, 255))
        dust(screen.surf, (x+10, y+30), (20, 180, 255), screen.rect.h, 'y+')
        dust(screen.surf, (x+70, y+30), (20, 180, 255), screen.rect.h, 'y+')
        dust(screen.surf, (x+130, y+30), (20, 180, 255), screen.rect.h, 'y+')
        if int(iter) == 0:
            pyreq.write(screen.surf, "Starting App.", (x, y), 20)
        if int(iter) == 1:
            pyreq.write(screen.surf, "Starting App..", (x, y), 20)
        if int(iter) == 2:
            pyreq.write(screen.surf, "Starting App...", (x, y), 20)
        iter += 0.5
        if iter > 2:
            iter = 0
            iter2 += 1
        if iter2 > 3:
            resetdust()
            break

def showdatabase():
    running = True
    scroll = [20, 40]
    cursordb.execute("SELECT * FROM parking_users")
    dblist = cursordb.fetchall()
    while running:
        pygame.display.flip(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    running = False
                if ev.key == K_DOWN and scroll[1] > -1000:
                    scroll[1] -= 20
                if ev.key == K_UP and scroll[1] < 0:
                    scroll[1] += 20
        keys = pygame.key.get_pressed()
        if keys[K_DOWN] and scroll[1] > -1000:
            scroll[1] -= 2
        elif keys[K_UP] and scroll[1] < 0:
            scroll[1] += 2
        if keys[K_LEFT] and scroll[0] < 20:
            scroll[0] += 4
        elif keys[K_RIGHT] and scroll[0] > -850:
            scroll[0] -= 4
        screen.surf.fill((40, 140, 240))
        pyreq.write(screen.surf, "Parking Lot Database", (screen.rect.centerx - 220, scroll[1] + 20), 44, bgcolor=(60, 200, 180))
        if scroll[1] >= -200:
            scrolly = scroll[1]
        else:
            scrolly = -200
        for y in range(len(dblist)):
            pyreq.write(screen.surf, str(dblist[y][0]), (scroll[0], scroll[1] + (y+3) * 100), 30)
            pyreq.write(screen.surf, str(dblist[y][1]), (scroll[0] + 400, scroll[1] + (y+3) * 100), 30)
            pyreq.write(screen.surf, str(dblist[y][2]), (scroll[0] + 600, scroll[1] + (y+3) * 100), 30)
            pyreq.write(screen.surf, str(dblist[y][3]), (scroll[0] + 900, scroll[1] + (y+3) * 100), 30)
            pyreq.write(screen.surf, str(dblist[y][4]), (scroll[0] + 1200, scroll[1] + (y+3) * 100), 30)
            pyreq.write(screen.surf, str(dblist[y][5]), (scroll[0] + 1300, scroll[1] + (y+3) * 100), 30)
            if dblist[y][6]:
                msg = "True"
            else:
                msg = "False"
            pyreq.write(screen.surf, msg, (scroll[0] + 1500, scroll[1] + (y+3) * 100), 30)
            pyreq.write(screen.surf, str(dblist[y][7]), (scroll[0] + 1650, scroll[1] + (y+3) * 100), 30)
            pyreq.write(screen.surf, str(dblist[y][8]), (scroll[0] + 1740, scroll[1] + (y+3) * 100), 30)
        pyreq.write(screen.surf,
        "Name                                        Phno                Plate                           Aadhaar                     Hours  Date                 Ban           Slot     Time ",
        (scroll[0], scrolly + 200), 30, bgcolor=(200, 140, 40))

def showbanuser():
    running = True
    iterate = False
    successmsg = False
    aadhaar_no = ""
    aadhaartext = "Enter aadhaar number : " + aadhaar_no
    while running:
        pygame.display.flip(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
            if ev.type == KEYDOWN:
                winsound.Beep(10000, 3)
                iterate = False
                successmsg = False
                if ev.key == K_ESCAPE:
                    running = False
                else:
                    if ev.key != K_RETURN:
                        aadhaar_no += ev.unicode
                    if ev.key == K_BACKSPACE:
                        aadhaar_no = aadhaar_no[:-2]
                if ev.key == K_RETURN:
                    winsound.Beep(30000, 30)
                    cursordb.execute("SELECT aadhaar_number, parking_slot, penalty, phone_number FROM parking_users")
                    dblist = cursordb.fetchall()
                    for no in dblist:
                        if no[0] == int(aadhaar_no):
                            phno = no[3]
                            banbool = not no[2]
                            successmsg = True
                            cursordb.execute(
                                "UPDATE parking_users SET penalty = " + str(banbool) + " WHERE (parking_slot = " + str(no[1]) + ") and (aadhaar_number = " + aadhaar_no + ");"
                                )
                            database.commit()
                    iterate = True
        aadhaartext = "Enter aadhaar number : " + aadhaar_no
        screen.surf.fill((240, 140, 40))
        pyreq.write(screen.surf, "Ban/Unban User", (screen.rect.centerx - 180, 200), 44, bgcolor=(60, 200, 180))
        pyreq.write(screen.surf, aadhaartext, (100, 400), 36)
        if iterate:
            if successmsg:
                rtime = t.localtime()
                current_time = t.strftime("%H:%M:%S", rtime)
                h, m = int(current_time[0:2]), int(current_time[3:5])
                if banbool:
                    pyreq.write(screen.surf, "User successfully banned.", (200, 600), 30, (0, 255, 0))
                    if whatsappbool:
                        pywhatkit.sendwhatmsg("+91" + str(phno), "*Your account has been banned for not following the time limit.*", h, m+1, 7)
                else:
                    pyreq.write(screen.surf, "User successfully unbanned.", (200, 600), 30, (0, 255, 0))
                    if whatsappbool:
                        pywhatkit.sendwhatmsg("+91" + str(phno), "*Your account has been lifted from banned state (No Ban).*", h, m+1, 7)
            else:
                pyreq.write(screen.surf, "Aadhaar number is incorrect. Try again.", (160, 600), 30, (255, 0, 0))
            aadhaar_no = ""

def showoutuser():
    running = True
    iterate = False
    successmsg = False
    aadhaar_no = ""
    aadhaartext = "Enter aadhaar number : " + aadhaar_no
    while running:
        pygame.display.flip(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
            if ev.type == KEYDOWN:
                winsound.Beep(10000, 3)
                iterate = False
                successmsg = False
                if ev.key == K_ESCAPE:
                    running = False
                else:
                    if ev.key != K_RETURN:
                        aadhaar_no += ev.unicode
                    if ev.key == K_BACKSPACE:
                        aadhaar_no = aadhaar_no[:-2]
                if ev.key == K_RETURN:
                    winsound.Beep(30000, 30)
                    cursordb.execute("SELECT aadhaar_number, parking_slot, phone_number, parking_time, duration_hours FROM parking_users")
                    dblist = cursordb.fetchall()
                    for no in dblist:
                        if no[0] == int(aadhaar_no):
                            phno = no[2]
                            successmsg = True
                            hours = no[4]
                            print(no[3][0:2])
                            tiime = int(no[3])
                            cursordb.execute("UPDATE parking_lots SET occupied_bool = FALSE WHERE (parking_slot = " + str(no[1]) + ");")
                            cursordb.execute("DELETE FROM parking_users WHERE (parking_slot = '" + str(no[1]) + "') and (aadhaar_number = '" + aadhaar_no + "');")
                            database.commit()
                    iterate = True
        aadhaartext = "Enter aadhaar number : " + aadhaar_no
        screen.surf.fill((240, 140, 40))
        pyreq.write(screen.surf, "User - OUT TIME", (screen.rect.centerx - 180, 200), 44, bgcolor=(60, 200, 180))
        pyreq.write(screen.surf, aadhaartext, (100, 400), 36)
        if iterate:
            if successmsg:
                pyreq.write(screen.surf, "User's OUT TIME successful.", (200, 600), 30, (0, 255, 0))
                if whatsappbool:
                    rtime = t.localtime()
                    current_time = t.strftime("%H:%M:%S", rtime)
                    h, m = int(current_time[0:2]), int(current_time[3:5])
                    if h > hours + tiime:
                        pywhatkit.sendwhatmsg("+91" + str(phno),
                        f"*Your have to pay the extra price of {(h - (hours + tiime))*10} before taking back the vehicle for arriving {h - (hours + tiime)} hours late.*",
                        h, m+1, 7)
            else:
                pyreq.write(screen.surf, "Aadhaar number is incorrect. Try again.", (160, 600), 30, (255, 0, 0))
            aadhaar_no = ""

def administrator2():
    buttondb = Button(Rect(screen.rect.centerx - 400, 300, 200, 100), (255, 0, 0), (255, 200, 200), "View Database")
    buttondel = Button(Rect(screen.rect.centerx - 100, 300, 200, 100), (20, 200, 255), (200, 200, 255), "User-OUT TIME")
    buttonban = Button(Rect(screen.rect.centerx + 200, 300, 200, 100), (0, 255, 0), (200, 255, 200), "Ban User")
    running = True
    while running:
        pygame.display.flip(); clock.tick(60)
        mouse = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    running = False
        screen.surf.fill((255, 100, 100))
        buttondb.show(mouse[0])
        buttonban.show(mouse[0])
        buttondel.show(mouse[0])
        if buttondb.rect.collidepoint(mouse[0]) and mouse[1][0]:
            winsound.Beep(30000, 30)
            showdatabase()
        elif buttonban.rect.collidepoint(mouse[0]) and mouse[1][0]:
            winsound.Beep(30000, 30)
            showbanuser()
        elif buttondel.rect.collidepoint(mouse[0]) and mouse[1][0]:
            winsound.Beep(30000, 30)
            showoutuser()

def administrator1():
    username, password = "Admin", "123456"
    inusername = inpassword = ""
    selection = 0
    usernametext = "Username : " + inusername
    passwordtext = "Password : " + inpassword
    running = True
    errormsg = False
    while running:
        pygame.display.flip(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
            if ev.type == KEYDOWN:
                winsound.Beep(10000, 3)
                if ev.key == K_ESCAPE:
                    running = False
                if selection == 0:
                    if ev.key != K_RETURN:
                        inusername += ev.unicode
                    if ev.key == K_BACKSPACE:
                        inusername = inusername[:-2]
                if selection == 1:
                    if ev.key != K_RETURN:
                        inpassword += ev.unicode
                    if ev.key == K_BACKSPACE:
                        inpassword = inpassword[:-2]
                if ev.key == K_RETURN:
                    if selection == 0:
                        selection = 1
                    elif selection == 1:
                        if inusername == username and inpassword == password:
                            winsound.Beep(30000, 30)
                            administrator2()
                        else:
                            inusername = inpassword = ""
                            selection = 0
                            errormsg = True
        usernametext = "Username : " + inusername
        passwordtext = "Password : " + "X"*len(inpassword)
        screen.surf.fill((160, 160, 180))
        pyreq.write(screen.surf, "Admin Login", (screen.rect.centerx - 180, 200), 44, bgcolor=(60, 200, 180))
        pyreq.write(screen.surf, usernametext, (100, 400), 36)
        pyreq.write(screen.surf, passwordtext, (100, 500), 36)
        if errormsg:
            pyreq.write(screen.surf, "Username or Password is incorrect. Try again.", (160, 600), 30, (255, 0, 0))

def customer2():
    running = True
    while running:
        pygame.display.flip(); clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    running = False
        screen.surf.fill((100, 255, 100))
        pyreq.write(screen.surf, f"Please park in slot number {lastval}.", (screen.rect.centerx - 420, 300), 40, (80, 0, 0))

def customer1():
    global lastval
    selection = 0
    pressed = False
    blocked = False
    cname = phno = numplate = aadhaarno = duration = ""
    interrormsg1 = False
    interrormsg2 = False
    running = True
    mbuttonbool = False
    mbutton = Button(Rect(400, screen.rect.h - 120, 140, 100), (255, 80, 80), (255, 140, 140), "Pay Re. 30", (100, 0, 0))
    cnametext =     "Customer's Name           : " + cname
    phnotext =      "Phone Number                 : " + phno
    numplatetext =  "Number Plate value         : " + numplate
    aadhaarnotext = "Aadhaar Card Number     : " + aadhaarno
    durationtext =  "Parking duration(in hours, max 6) : " + duration
    while running:
        pygame.display.flip(); clock.tick(60)
        mouse = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        if interrormsg1:
            selection = 0
            cname = phno = numplate = aadhaarno = duration = ""
            interrormsg1 = False
        for ev in pygame.event.get():
            if ev.type == QUIT:
                pyreq.quitapp()
            if ev.type == KEYDOWN:
                winsound.Beep(10000, 3)
                if ev.key == K_ESCAPE:
                    running = False
                if selection == 0:
                    if ev.key != K_RETURN:
                        cname += ev.unicode
                    if ev.key == K_BACKSPACE:
                        cname = cname[:-2]
                if selection == 1:
                    if ev.key != K_RETURN:
                        phno += ev.unicode
                    if ev.key == K_BACKSPACE:
                        phno = phno[:-2]
                if selection == 2:
                    if ev.key != K_RETURN:
                        numplate += ev.unicode
                    if ev.key == K_BACKSPACE:
                        numplate = numplate[:-2]
                if selection == 3:
                    if ev.key != K_RETURN:
                        aadhaarno += ev.unicode
                    if ev.key == K_BACKSPACE:
                        aadhaarno = aadhaarno[:-2]
                if selection == 4:
                    if ev.key != K_RETURN:
                        duration += ev.unicode
                    if ev.key == K_BACKSPACE:
                        duration = duration[:-2]
                cnametext =     "Customer's Name           : " + cname
                phnotext =      "Phone Number                 : " + phno
                numplatetext =  "Number Plate value         : " + numplate
                aadhaarnotext = "Aadhaar Card Number     : " + aadhaarno
                durationtext =  "Parking duration(in hours, max 6) : " + duration
                if ev.key == K_RETURN:
                    if selection == 4:
                        if cname == "" or phno == "" or numplate == "" or aadhaarno == "" or duration == "" or float(duration) > 6 or len(numplate) != 10 or len(phno) != 10 or len(aadhaarno) != 12:
                            interrormsg1 = True
                            interrormsg2 = True
                        else:
                            for i in cname:
                                if i.isdigit():
                                    interrormsg1 = True
                                    interrormsg2 = True
                            for i in phno:
                                if not i.isdigit():
                                    interrormsg1 = True
                                    interrormsg2 = True
                            for i in numplate:
                                if not i.isupper() and not i.isdigit():
                                    interrormsg1 = True
                                    interrormsg2 = True
                            for i in aadhaarno:
                                if not i.isdigit():
                                    interrormsg1 = True
                                    interrormsg2 = True
                            for i in duration:
                                if not i.isdigit():
                                    interrormsg1 = True
                                    interrormsg2 = True
                            if not interrormsg1:
                                interrormsg2 = False
                                mbuttonbool = True
                    selection += 1
        screen.surf.fill((200, 200, 200))
        if interrormsg2:
            pyreq.write(screen.surf, "Entered detail(s) incorrect. Try again.", (160, 700), 30, (255, 0, 0))
        pyreq.write(screen.surf, "Customer Register", (screen.rect.centerx - 200, 60), 44, bgcolor=(60, 200, 180))
        pyreq.write(screen.surf, cnametext, (100, 200), 36)
        pyreq.write(screen.surf, phnotext, (100, 300), 36)
        pyreq.write(screen.surf, numplatetext, (100, 400), 36)
        pyreq.write(screen.surf, aadhaarnotext, (100, 500), 36)
        pyreq.write(screen.surf, durationtext, (100, 600), 36)
        if mbuttonbool:
            mbutton.show(mouse[0])
            if mbutton.rect.collidepoint(mouse[0]) and mouse[1][0] and not pressed:
                pressed = True
                winsound.Beep(30000, 30)
                rtime = t.localtime()
                current_time = t.strftime("%H:%M:%S", rtime)
                h, m = int(current_time[0:2]), int(current_time[3:5])
                cdate = datetime.date.today()
                cursordb.execute("SELECT * FROM parking_users")
                dblist = cursordb.fetchall()
                cursordb.execute("SELECT * FROM parking_lots")
                dblist2 = cursordb.fetchall()
                for lot in dblist2:
                    if not lot[1]:
                        lastval = lot[0]
                        break
                if len(dblist) < 20:
                    for i in dblist:
                        for j in dblist:
                            if i != j and i[3] == j[3]:
                                blocked = True
                    cursordb.execute("SELECT * FROM parking_users")
                    dblist = cursordb.fetchall()
                    iteration = False
                    for id_ in dblist:
                        if dblist[-1][3] == id_[3] and id_[6]:
                            blocked = True
                        if not blocked:
                            if not iteration:
                                if m < 10:
                                    m = f"0{m}"
                                cursordb.execute(f'INSERT INTO parking_users VALUES("{cname}", "{phno}", "{numplate}", {aadhaarno}, {duration}, "{cdate}", FALSE, {lastval}, {int(f"{h}{m}")});')
                                cursordb.execute("UPDATE parking_lots SET occupied_bool = TRUE WHERE (parking_slot = " + str(lastval) + ");")
                                database.commit()
                                iteration = True
                            if whatsappbool:
                                pywhatkit.sendwhatmsg("+91" + phno, "*Thank you for using Janardan's Parking Systems :D*", h, m+1, 7)
                    if blocked:
                        if whatsappbool:
                            pywhatkit.sendwhatmsg("+91" + phno, "*Your entry is blocked due to pending payments.*", h, m+1, 7)
                else:
                    if whatsappbool:
                        pywhatkit.sendwhatmsg("+91" + phno, "*Your entry is blocked due to filled slots.*", h, m+1, 7)
                customer2()

def menu():
    while True:
        pygame.display.flip(); clock.tick(60)
        mouse = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        for ev in pygame.event.get():
            if ev.type == QUIT or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                pyreq.quitapp()
        screen.surf.fill((200, 255, 230))
        pyreq.write(screen.surf, "Parking-Lot Management System", (screen.rect.centerx - 424, 58), 51, (80, 180, 220))
        pyreq.write(screen.surf, "Parking-Lot Management System", (screen.rect.centerx - 420, 60), 50, (80, 0, 0))
        pyreq.write(screen.surf, "Project made by ~ A. S. Janaardhan Ram", (screen.rect.centerx - 300, 650), 30)
        dust(screen.surf, (screen.rect.centerx - 56, screen.rect.centery + 30), (255, 200, 30), screen.rect.centerx - 180)
        screen.surf.blit(carimg, (screen.rect.centerx - 64, screen.rect.centery - random.randint(63, 65)))
        button1.show(mouse[0])
        button2.show(mouse[0])
        if button1.rect.collidepoint(mouse[0]) and mouse[1][0]:
            winsound.Beep(30000, 30)
            administrator1()
        elif button2.rect.collidepoint(mouse[0]) and mouse[1][0]:
            winsound.Beep(30000, 30)
            customer1()

if __name__ == '__main__':
    startapp()
    menu()