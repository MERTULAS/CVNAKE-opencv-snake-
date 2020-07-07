import numpy as np
import cv2
import random
import time
import mysql.connector
conn = mysql.connector.connect(user='root', password='',
                              host='127.0.0.1',
                              database='GAMES')
c=conn.cursor()
health=cv2.imread("health.png")
health=cv2.resize(health,(150,75))
cvnake=cv2.imread("cvnake.png")
cvnake=cv2.resize(cvnake,(250,100))
python=cv2.imread("python.png")
python=cv2.resize(python,(100,100))
snack=cv2.imread("apple.png")
snack=cv2.resize(snack,(25,25))
barrier=cv2.imread("wall.png")
barrier=cv2.resize(barrier,(200,200))
x=0; y=0; control=0; control0=0; a=0; b=0;
font = cv2.FONT_HERSHEY_SIMPLEX
snake_body= [[775,475]]
snake_begin=[775,475]
score=0
life=3
lifemask=1475
k=50
maskbd=150
mask=np.ones(health.shape,dtype="uint8")*255
maxscore=0
print("""
********************************************************
****************                ************************
************    THE cvNAKE GAME     ********************
****************                ************************
********************************************************
""")
best=0
ttl_game_time=0
while True:
    nickname = input("ENTER YOUR NICKNAME:")
    nickname = nickname.upper()
    nickname_already_used = """SELECT nickname FROM cvnake WHERE nickname IN (%s) """
    c.execute(nickname_already_used,[nickname])
    nick_already_used = c.fetchall()
    if (nick_already_used!=[]):
        while True:
            password = input("WELCOME BACK " + nickname + " ENTER YOUR PASSWORD:")
            password_query_from_db = """SELECT password FROM cvnake WHERE password IN (%s) """
            c.execute(password_query_from_db,[password])
            password_confirmation = c.fetchall()
            if (password_confirmation!=[]):
                player_already_used = """SELECT nickname FROM cvnake WHERE nickname IN (%s) """
                c.execute(nickname_already_used, [nickname])
                nick_already_used = c.fetchall()
                is_best_score = """SELECT maxscore FROM cvnake WHERE nickname IN (%s)"""
                c.execute(is_best_score, [nickname])
                best_score = c.fetchall()
                best = best_score[0][0]
                print("The "+nickname+"'s best score: "+str(best))
                during_the_game_time = """SELECT play_time FROM cvnake WHERE nickname IN (%s)"""
                c.execute(during_the_game_time, [nickname])
                total_game_time = c.fetchall()
                ttl_game_time=total_game_time[0][0]
                print("The " + nickname + "'s"" game time: " + str(ttl_game_time))
                break
            else:
                print("YOUR PASSWORD IS INCORRECT!")
        break
    if (nick_already_used==[]):
        password = input("HEY NEW PLAYER! PLEASE CREATE YOUR PASSWORD:")
        add_player_account = """INSERT INTO cvnake(nickname,maxscore,password,play_time) VALUES(%s,%s,%s,%s)"""
        c.execute(add_player_account, (str(nickname), str(score),str(password),str("00:00:00")))
        conn.commit()
        ttl_game_time="00:00:00"
        break
start_time=time.time()
def read_scoreboard_from_database(scoreboard_area):
    query_from_db = """SELECT * FROM cvnake ORDER BY maxscore DESC LIMIT 3"""
    c.execute(query_from_db)
    champion = c.fetchall()
    for row in champion:
        cv2.rectangle(bground, (1348, 127), (1558, 350), (0, 0, 0), 2)
        cv2.putText(bground, str("TOP 3"),(1350,170), font, 1.4, (255, 0, 0), 2,cv2.LINE_AA)
        cv2.putText(bground, str(row[1])+" : "+str(row[3]), (1350, scoreboard_area), font, 1, (200, 0, 0), 2, cv2.LINE_AA)
        scoreboard_area+=50
        if scoreboard_area>350:
            scoreboard_area=230
def update_scoreboard_data_to_database(nickname,score):
    upt_nickname = """UPDATE cvnake SET maxscore = %s WHERE nickname = %s"""
    c.execute(upt_nickname, (str(score),str(nickname)))
    conn.commit()
def barriers():
    while True:
        a=random.randrange(125,775,25)
        b=random.randrange(25,1375,25)
        if (a<200 or a>500) or (b<500 or b>800): break
    return a,b
a,b=barriers()
def snacks(x,y,a,b):
    while True:
        x=random.randrange(125,975,25)
        y=random.randrange(25,1575,25)
        if ((x%50!=0) and (y%50!=0)) and ((x<a or x>a+200) and (y<b or y>b+200)):
            break
    return x,y
x, y=snacks(x,y,a,b)
def snake_eating_itself(snake_begin,snake_body):
    if snake_begin in snake_body[1:]:
        return 1
scoreboard_area=230
startcavex=745
startcavey=455
while True:
    bground = np.ones((1000, 1600, 3), dtype="uint8")
    bground[125:975,25:1575]=[0,255,0]
    bground[x:x+25,y:y+25]=snack
    mask[:,maskbd:150]=[0,0,0]
    health=cv2.bitwise_and(health,mask)
    bground[25:100,1375:1525]=health
    bground[15:115,650:900]=cvnake
    bground[15:115,900:1000]=python
    cv2.putText(bground,"YOUR SCORE:"+str(score), (25,65), font, 2, (0, 0, 255), 3, cv2.LINE_AA)
    bground[a:a+200, b:b+200] = barrier
    #cv2.putText(bground, "THE RECORD: "+str(champion_score)+" by "+str(champion_name), (25, 110), font, 0.9, (255, 0, 0), 2, cv2.LINE_AA)
    if score>=0:
        read_scoreboard_from_database(scoreboard_area)
        is_best_score = """SELECT maxscore FROM cvnake WHERE nickname IN (%s)"""
        c.execute(is_best_score, [nickname])
        best_score = c.fetchall()
        if (best_score[0][0]<score):
            update_scoreboard_data_to_database(nickname, score)
    for snake in snake_body:
        cv2.rectangle(bground,(snake[0], snake[1]), (snake[0] + 25, snake[1] + 25), (0, 0, 255), -1)
    if control==1:
        try:
            snake_begin[1]-=25
            control0=1
        except:pass
    elif control==2:
        try:
            snake_begin[1]+=25
            control0=2
        except: pass
    elif control==3:
        try:
            snake_begin[0]-=25
            control0=3
        except: pass
    elif control==4:
        try:
            snake_begin[0]+=25
            control0=4
        except: pass
    if snake_begin[0]==y and snake_begin[1]==x:
        x,y=snacks(x,y,a,b)
        bground[x:x+25,y:y+25]=snack
        snake_body.insert(0,list(snake_begin))
        score+=1
    else:
        snake_body.insert(0, list(snake_begin))
        snake_body.pop()
    if snake_begin[0]<25 or snake_begin[0]>1550 or snake_begin[1]<125 or snake_begin[1]>950 or snake_eating_itself(snake_begin,snake_body)==1 or \
            ((snake_begin[0]<b+200 and snake_begin[0]>b-25) and (snake_begin[1]>a-25 and snake_begin[1]<a+200)):
        life-=1
        control=1
        bground[25:100,lifemask:lifemask+k]=[0,0,0]
        for i in range(3):
            if (len(snake_body))==1:
                snake_body = [[775, 475]]
                break
            snake_body.pop()
        snake_begin=[775,475]
        lifemask-=50
        k+=50
        key=0
        maskbd-=50
        maxscore=score
        a,b=barriers()
        if life==0:
            cv2.putText(bground,"GAME OVER", (475, 550), font, 4, (255, 0, 0), 3, cv2.LINE_AA)
            cv2.imshow("CVNAKE GAME",bground)
            cv2.waitKey(0)
            time.sleep(2)
            break
        if score>=3:
            score-=3
            if best_score[0][0]<score+4:
                update_scoreboard_data_to_database(nickname, score)
        else: score=0
    cv2.imshow("CVNAKE GAME",bground)
    key = cv2.waitKey(10) & 0xFF
    if key==ord('1'): break
    elif key==ord('w') and control0!=2: control=1
    elif key==ord('s') and control0!=1: control=2
    elif key==ord('a') and control0!=4: control=3
    elif key==ord('d') and control0!=3: control=4
    elif key==ord('p'): control=0
stop_time = time.time()
if best > score:
    update_scoreboard_data_to_database(nickname, best)
play_time = stop_time - start_time
play_time = int(play_time)
timeParts = [int(s) for s in ttl_game_time.split(':')]
totalSecs = (timeParts[0] * 60 + timeParts[1]) * 60 + timeParts[2]
totalSecs += play_time
totalSecs, sec = divmod(totalSecs, 60)
hr, min = divmod(totalSecs, 60)
if (sec<10):
    sec = "0" + str(sec)
if (min<10):
    min = "0" + str(min)
if (hr<10):
    hr = "0" + str(hr)
timer=str(hr)+":"+str(min)+":"+str(sec)
upt_total_time = """UPDATE cvnake SET play_time = %s WHERE nickname = %s"""
c.execute(upt_total_time, (str(timer),str(nickname)))
conn.commit()
cv2.destroyAllWindows()
