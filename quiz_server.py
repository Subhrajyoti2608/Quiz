import socket
from threading import Thread
import random

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IPAddress = "127.0.0.1"
port=8001
server.bind((IPAddress, port))
server.listen()
listOfClients=[]
nicknames=[]

print("Server is started!")

question={
    "What is the biggest megacity of India? \n a.Bengaluru\n b.Delhi\n c.Kolkata\n d.Mumbai",
    "Who invented Crescograph? \n a.Einstein\n b.Satyendranath Bose\n c.Jagadish Chandra Bose\n d.Charles Darwin",
    "What is the largest National Highway of India? \n a.NH12\n b.NH36\n c.NH44\n d.NH64",
    "On whose birthday we celebrate National Youth Day? \n a.Netaji Subhash Chandra Bose\n b.Bhagat Singh\n c.Shivaji\n d.Swami Vivekananda"
    
}

answer={"d","c","c","d"}

def get_random_question_answer(conn):
  random_index = random.randint(0,len(question)-1)
  random_question = question[random_index]
  random_answer=answer[random_index]
  conn.send(random_question.encode("UTF-8"))
  return random_index, random_question, random_answer 

def remove_question(index):
  question.pop(index)
  answer.pop(index)


def remove(conn):
  if conn in listOfClients:
    listOfClients.remove(conn)

def remove_nickname(nickname):
  if nickname in nicknames:
    nicknames.remove(nickname)

def clientThread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d!\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

while True:
    conn, address = server.accept()
    conn.send('NICKNAME'.encode("UTF-8"))
    nickname = conn.recv(2048).decode("UTF-8")
    listOfClients.append(conn)
    nicknames.append(nickname)
    print(nickname + "connected!")
    newThread = Thread(target=clientThread, args=(conn, nickname))
    newThread.start()