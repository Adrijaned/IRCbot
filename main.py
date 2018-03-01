import socket
import re
import random
import time
import responses
import regexes
import urllib.parse

run = True
irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "chat.freenode.net"
bot_name = "Adrij"
channel = "#destination-sol"
admin_name = "Adrijaned"
timezone_string = "UTC-01:00"
gooey_name = "gooey-bridge"

new_remembers = []
remember_file_name = "/home/adrijaneddebian/remember"
remember_delimiter = "--------------------------------------------------------"

with open(remember_file_name, mode="a") as file:
    file.write(remember_delimiter)


def join_channel(channel=channel):
    irc_socket.send(bytes("JOIN " + channel + "\n", "UTF-8"))
    irc_message = ""
    while "nd of " not in irc_message:
        irc_message = irc_socket.recv(2048).decode()
        irc_message = irc_message.strip("\n\r")
        print(irc_message)


def ping():
    irc_socket.send((bytes("PONG :pingis\n", "UTF-8")))
    print("PONG")


def send_message(message: str, target=channel):
    irc_socket.send(bytes("PRIVMSG " + target + " :" + str(message) + "\n",
                          "UTF-8"))


def quit():
    irc_socket.send(bytes("QUIT \n", "UTF-8"))
    global run
    run = False


def responder(name: str, message: str, bridged: bool):
    if regexes.greeter.match(message):
        if name == "Zweihander" and not bridged:
            name = "Suraj"
        send_message(name + ": Hello to you too!")
    elif regexes.ping.match(message):
        send_message("PONG")
    elif regexes.exit.match(message):
        if name == admin_name and not bridged:
            send_message(responses.disconnect_approved)
            for temp in new_remembers:
                send_message(temp, "Adrijaned")
            quit()
        else:
            send_message(responses.disconnect_rejected)
    elif regexes.random_float.match(message):
        send_message(random.random())
    elif regexes.random_dice.match(message):
        send_message(random.randint(1, 6))
    elif regexes.timezone.match(message):
        send_message(timezone_string)
    elif regexes.time.match(message):
        send_message(time.asctime(time.localtime(time.time())))
    elif regexes.the_rules.match(message):
        for line in responses.the_rules:
            send_message(line)
    elif regexes.help.match(message):
        send_message(responses.help_url)
    elif regexes.remember.match(message):
        with open(remember_file_name, mode="a") as file:
            note = regexes.remember.match(message).group("note")
            file.write(note + "\n")
            new_remembers.append(note)
            file.flush()
        send_message("Will try :)")
    elif regexes.say.match(message):
        matcher = regexes.say.match(message)
        send_message(matcher.group("nick") + ": " + matcher.group("msg"))
    elif regexes.loop.match(message) and regexes.loop_iterations_passed < 10:
        regexes.loop_iterations_passed += 1
        send_message(responses.loop)
    elif regexes.retrieve.match(message):
        item = int(regexes.retrieve.match(message).group("num"))
        with open(remember_file_name, mode='r') as file:
            while item > 0:
                temp = file.readline()
                if temp != remember_delimiter:
                    item -= 1
            send_message(file.readline())
    elif regexes.google.search(message):
        msg = regexes.google.search(message).group("msg")
        msg = urllib.parse.quote_plus(msg)
        send_message(name + ": http://lmgtfy.com/?q=" + msg)
    elif regexes.issue.search(message):
        issue = regexes.issue.search(message).group("num")
        send_message("https://github.com/MovingBlocks/DestinationSol/pull/" +
                     issue)
    elif re.match(regexes.bot_prefix, message):
        send_message(responses.not_recognized)


irc_socket.connect((server, 6667))
irc_socket.send(bytes("USER " + bot_name + " " + bot_name + " " + bot_name +
                      " " + bot_name + "\n", "UTF-8"))
irc_socket.send(bytes("NICK " + bot_name + "\n", "UTF-8"))

join_channel()
while run:
    irc_message = irc_socket.recv(2048).decode()
    irc_message = irc_message.strip("\n\r")
    print(irc_message)
    if "PRIVMSG" in irc_message:
        name = irc_message.split("!", 1)[0][1:]
        message = irc_message[1:].split(":", 1)[1]
        print("------------\n" + message + "\n-------------")
        if len(name) < 17:
            # for when someone performs an ACTION
            if message.startswith("ACTION"):
                continue
            if name == gooey_name:
                name = re.match(regexes.gooey_prefix, message).group("nick")
                message = regexes.gooey_preprocessor.match(message).group("msg")
                responder(name, message, True)
            elif message != "":
                responder(name, message, False)

    if "PING" in irc_message:
        ping()
