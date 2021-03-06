#2016-2017 PERSONAL PROJECTS: TurtleChat!
#AMIR SADI (AKA JESUS)

#####################################################################################
#                                   IMPORTS                                         #
#####################################################################################
#import the turtle module
#import the Client class from the turtle_chat_client module
#Finally, from the turtle_chat_widgets module, import two classes: Button and TextInput
#####################################################################################

import turtle
from turtle_chat_client import Client
from turtle_chat_widgets import Button , TextInput

#####################################################################################

#####################################################################################
#                                   TextBox                                         #
#####################################################################################
#Make a class called TextBox, which will be a subclass of TextInput.
#Because TextInput is an abstract class, you must implement its abstract
#methods.  There are two:
#
#draw_box
#write_msg
#
#Hints:
#1. in draw_box, you will draw (or stamp) the space on which the user's input
#will appear.
#
#2. All TextInput objects have an internal turtle called writer (i.e. self will
#   have something called writer).  You can write new text with it using code like
#
#   self.writer.write(a_string_variable)
#
#   and you can erase that text using
#
#   self.writer.clear()
#
#3. If you want to make a newline character (i.e. go to the next line), just add
#   \r to your string.  Test it out at the Python shell for practice
#####################################################################################

class TextBox(TextInput):
    def draw_box(self):
        turtle.hideturtle()
        self.drawer = turtle.clone()
        self.drawer.pu()
        self.drawer.goto(self.pos)
        pos = self.drawer.position()
        self.drawer.pendown()
        self.drawer.setx(pos[0]+ self.width/2)
        self.drawer.sety(pos[1]+ self.height)
        self.drawer.setx(pos[0] - self.width/2)
        self.drawer.sety(pos[1])
        self.drawer.setx(pos[0])

    def write_msg(self):
        self.writer.clear()
        self.writer.write(self.new_msg)

#####################################################################################

#####################################################################################
#                                  SendButton                                       #
#####################################################################################
#Make a class called SendButton, which will be a subclass of Button.
#Button is an abstract class with one abstract method: fun.
#fun gets called whenever the button is clicked.  It's jobs will be to
#
# 1. send a message to the other chat participant - to do this,
#    you will need to call the send method of your Client instance
# 2. update the messages that you see on the screen
#
#HINT: You may want to override the __init__ method so that it takes one additional
#      input: view.  This will be an instance of the View class you will make next
#      That class will have methods inside of it to help
#      you send messages and update message displays.
#####################################################################################

class SendButton(Button):
    def __init__(self,my_turtle=None,shape=None,pos=(0,-260),view = None):
        super(SendButton,self).__init__(my_turtle,shape,pos)
        self.view = view
    def fun(self,x=None,y=None):
        self.view.send_msg()
        
            

#####################################################################################


##################################################################
#                             View                               #
##################################################################
#Make a new class called View.  It does not need to have a parent
#class mentioned explicitly.
#
#Read the comments below for hints and directions.
##################################################################
##################################################################
class View:
    _MSG_LOG_LENGTH=10 #Number of messages to retain in view
    _SCREEN_WIDTH=500
    _SCREEN_HEIGHT=800
    _LINE_SPACING=50
    _GAME_SPOT = (1200,-300)    
    scroll_shift = 0 


    def __init__(self,username='Me',partner_name='Partner'):
        '''
        :param username: the name of this chat user
        :param partner_name: the name of the user you are chatting with
        '''
        ###
        #Store the username and partner_name into the instance.
        ###

        self.username = username
        self.partner_name = partner_name

        ###
        #Make a new Client object and store it in this instance of View
        #(i.e. self).  The name of the instance should be my_client
        ###

        self.my_client = Client()

        ###
        #Set screen dimensions using turtle.setup
        #You can get help on this function, as with other turtle functions,
        #by typing
        #
        #   import turtle
        #   help(turtle.setup)
        #
        #at the Python shell.
        ###

        turtle.setup(self._SCREEN_WIDTH,self._SCREEN_HEIGHT)

        ###
        #This list will store all of the messages.
        #You can add strings to the front of the list using
        #   self.msg_queue.insert(0,a_msg_string)
        #or at the end of the list using
        #   self.msg_queue.append(a_msg_string)
        ###

        self.msg_queue=[]

        ###
        #Create one turtle object for each message to display.
        #You can use the clear() and write() methods to erase
        #and write messages for each
        ###
        
        self.turty = turtle.clone()
        self.turty.penup()
        self.turty.hideturtle()

        ###
        #Create a TextBox instance and a SendButton instance and
        #Store them inside of this instance
        ###
        
        self.textbox = TextBox()
        self.send_button = SendButton(view = self)

        ###
        #Call your setup_listeners() function, if you have one,
        #and any other remaining setup functions you have invented.
        ###
        self.setup_listeners()

    def game(self):
        self.game_turt = turtle.clone()
        self.game_turt.ht()
        self.game_turt.pu()
        self.game_turt.goto(-200,300)
        pos = self.game_turt.position()
        self.game_turt.pd()
        self.game_turt.goto(pos[0] + 400,pos[1])
        self.game_turt.goto(pos[0] + 400,pos[1] - 500)
        self.game_turt.goto(pos[0],pos[1] - 500)
        self.game_turt.goto(pos[0],pos[1])
        self.game_turt.pu()

    def send_msg(self):
        '''
        You should implement this method.  It should call the
        send() method of the Client object stored in this View
        instance.  It should also update the list of messages,
        self.msg_queue, to include this message.  It should
        clear the textbox text display (hint: use the clear_msg method).
        It should call self.display_msg() to cause the message
        display to be updated.
    '''

##      print(self.textbox.new_msg) #aha
        
        if(self.textbox.new_msg == "/start game"):
            self.textbox.new_msg = "game started!"
            self.game()

        if len(self.textbox.new_msg) > 0:
            self.textbox.new_msg = "You:\r" + self.textbox.new_msg
            self.msg_queue.insert(0,self.textbox.new_msg)                                                                                                                                                
            self.my_client.send(self.textbox.new_msg)
            self.textbox.clear_msg()
            self.display_msg()

    def get_msg(self):
        return self.textbox.get_msg()


    def setup_listeners(self):
        '''
        Set up send button - additional listener, in addition to click,
        so that return button will send a message.
        To do this, you will use the turtle.onkeypress function.
        The function that it will take is
        self.send_btn.fun
        where send_btn is the name of your button instance

        Then, it can call turtle.listen()
        '''

        #SCROLL
        turtle.onkeypress( self.up_arrow, 'Up' )
        turtle.onkeypress( self.down_arrow, 'Down' )
        

    def up_arrow(self):
##        print("up")
        if self.scroll_shift < len(self.msg_queue) - 1:
            self.scroll_shift += 1
            self.display_msg(self.scroll_shift)

    def down_arrow(self):
##        print("down")
        if self.scroll_shift > 0:
            self.scroll_shift -= 1
            self.display_msg(self.scroll_shift)
        
        
        self.send_button.fun()
        turtle.listen()

        

    def msg_received(self,msg):
        '''
        This method is called when a new message is received.
        It should update the log (queue) of messages, and cause
        the view of the messages to be updated in the display.

        :param msg: a string containing the message received
                    - this should be displayed on the screen
        '''
        print(msg) #Debug - print message
        show_this_msg=self.partner_name+' says:\r'+ msg
        #Add the message to the queue either using insert (to put at the beginning)
        #or append (to put at the end).


        self.msg_queue.insert(0,show_this_msg)
        self.display_msg()

        #Then, call the display_msg method to update the display


    def display_msg(self, scroll = 0):
        '''
        This method should update the messages displayed in the screen.
        You can get the messages you want from self.msg_queue
        
        '''
        pos = (-150,-230)

        self.turty.clear()

        for i in range(scroll,len(self.msg_queue)):
            print(" i === " + str(i) + "  scroll === " + str(scroll))
            if len(self.msg_queue) >= i+scroll :
                print(i)
                print(scroll)
                self.turty.goto(pos[0],pos[1] + self._LINE_SPACING * (i - scroll +1))
                self.turty.write(self.msg_queue[i])
##            print(self.msg_queue)
##            print(self.msg_queue_turts)
        
    def get_client(self):
        return self.my_client
##############################################################
##############################################################


#########################################################
#Leave the code below for now - you can play around with#
#it once you have a working view, trying to run you chat#
#view in different ways.                                #
#########################################################
if __name__ == '__main__':
    my_view=View()
    _WAIT_TIME=200 #Time between check for new message, ms
    def check() :
        #msg_in=my_view.my_client.receive()
        msg_in=my_view.get_client().receive()
        if not(msg_in is None):
            if msg_in==Client._END_MSG:
                print('End message received')
                sys.exit()
            else:
                my_view.msg_received(msg_in)
        turtle.ontimer(check,_WAIT_TIME) #Check recursively
    check()
    turtle.mainloop()
