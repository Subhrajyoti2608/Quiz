import socket
from threading import Thread
import random

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IPAddress = "127.0.0.1"
port=8001
server.bind((IPAddress, port))
server.listen()
listOfClients=[]
print("Server is started!")

question={
    "What is the biggest megacity of India? \n a.Bengaluru\n b.Delhi\n c.Kolkata\n d.Mumbai"
    "Who invented Crescograph? \n a.Einstein\n b.Satyendranath Bose\n c.Jagadish Chandra Bose\n d.Charles Darwin"
    "What is the largest National Highway of India? \n a.NH12\n b.NH36\n c.NH44\n d.NH64"
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

def clientThread(conn):
  score=0
  conn.send("Welcome to this quiz game!".encode("UTF-8"))
  conn.send("You will recieve a question. The answer to that question should be one of a, b, c and d".encode("UTF-8"))
  conn.send("Good Luck!\n\n".encode("UTF-8"))

  index, question, answer = get_random_question_answer(conn)

  while True:
    try:
      message = conn.recv(2048).decode("UTF-8")
      if message:
        if message.lower() == answer:
          score+=1
          conn.send(f"Bravo! Your score is {score}\n\n".encode("UTF-8"))
        else:
          conn.send("Incorrect answer! Better luck next time!\n\n".encode("UTF-8"))
        remove_question(index)
        index, question, answer = get_random_question_answer(conn)
      else:
        remove(conn)
    except:
      continue

while True:
    conn, address = server.accept()
    listOfClients.append(conn)
    print(address[0]+"connected")
    newThread = Thread(target=clientThread, args=(conn, address))
    newThread.start()