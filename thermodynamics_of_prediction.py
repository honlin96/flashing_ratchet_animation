# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np
import random as rd
from tkinter import *
#-------------define transition probability for each protocol-----------------#
probA = 1/2
probB = 9/10
probC = 1/10
global potentialA,potentialB,forward_trans_A,forward_trans_B
potentialA = np.array([[0,probA,1-probA],[1-probA,0,probA],[probA,1-probA,0]])
potentialB = np.array([[0,probB,1-probB],[1-probC,0,probC],[probC,1-probC,0]])

forward_trans_A = np.array([[0,probA,0],[0,0,probA],[probA,0,0]])
backward_trans_A = potentialA - forward_trans_A

forward_trans_B = np.array([[0,probB,0],[0,0,probC],[probC,0,0]])
backward_trans_B = potentialB - forward_trans_B

#------------define initial state ------------------#
initial_state = np.array([1,0,0])

def prob_going_forward(state):
    #return the probability of going forward and the new state given the current state
    forward_prob_A = state*forward_trans_A
    forward_prob_B = state*forward_trans_B
    return forward_prob_A, forward_prob_B

def which_potential(state,forward_prob_A,forward_prob_B):
    #return which potential to use
    ispotentialA = False
    if forward_prob_A>forward_prob_B:
        ispotentialA = True
        newstate,isgoingforward = execute_potential(state,ispotentialA,forward_prob_A)
    else:
        newstate,isgoingforward = execute_potential(state,ispotentialA,forward_prob_B)
    return newstate,ispotentialA,isgoingforward

def execute_potential(state,ispotentialA,forward_prob):
    #execute the potential
    isgoingforward = False
    if ispotentialA:
        if forward_prob > rd.uniform(0,1):
        #execute the potential based on the probability
            newstate = state*forward_trans_A
            isgoingforward = True
        else:
            newstate = state*(potentialA - forward_trans_A)
    else:
        if forward_prob > rd.uniform(0,1):
            newstate = state*forward_trans_B
            isgoingforward = True
        else:
            newstate = state*(potentialB - forward_trans_B)
    return newstate,isgoingforward
        

def main():
    # Create the entire GUI program
    program = MolecularMotor()
    # Start the GUI event loop
    program.window.mainloop()

class MolecularMotor:
    CANVAS_WIDTH = 260
    CANVAS_HEIGHT = 130
    MOTOR_POSN_X = 120 # x position of box containing the ball (bottom)
    MOTOR_POSN_Y = 88 # y position of box containing the ball (left edge)
    MOTOR_WIDTH = 12 # size of ball – width (x-dimension)
    MOTOR_HEIGHT = 12 # size of ball – height (y-dimension)
    MOTOR_COLOR = "violet" # color of the ball
    def __init__(self):#window
         self.window = tk.Tk()
         self.window.title("Flashing Ratchet Animation")
         self.canvas_frame,self.widget_frame = self.createFrames()
         self.chart1 = self.createCanvas()
    
    def createFrames(self):
        canvas_frame = tk.Frame(self.window, bg='lightgreen', width=300, height=300)
        canvas_frame.grid(row=1, column=1)

        widget_frame = tk.Frame(self.window, bg='lightblue', width=100, height=300)
        widget_frame.grid(row=1, column=2)
        return canvas_frame,widget_frame         
         
    def createCanvas(self):
        chart1 = Canvas(self.canvas_frame, width=MolecularMotor.CANVAS_WIDTH, height=MolecularMotor.CANVAS_HEIGHT, background="white")
        chart1.grid(row=0, column=0)
        #create motor
        chart1.create_oval(MolecularMotor.MOTOR_POSN_X, MolecularMotor.MOTOR_POSN_Y, MolecularMotor.MOTOR_POSN_X + + MolecularMotor.MOTOR_WIDTH, MolecularMotor.MOTOR_POSN_Y + MolecularMotor.MOTOR_HEIGHT, fill=MolecularMotor.MOTOR_COLOR)
        #create track
        Track_Num = int(MolecularMotor.CANVAS_WIDTH/20)
        for i in np.linspace(0,MolecularMotor.CANVAS_WIDTH,Track_Num+1):
            coordinate = 0+i, MolecularMotor.MOTOR_POSN_Y, 20+i, MolecularMotor.MOTOR_POSN_Y + 10  
            chart1.create_rectangle(coordinate,fill = self.COLORS(int(i)))
        return chart1
    
    def moveMotor(self):
        #make the Motor jump
        cycle_period = 2000 # time between fresh positions of the ball (milliseconds).
        shift_up = 5
        coordinate = MolecularMotor.MOTOR_POSN_X, MolecularMotor.MOTOR_POSN_Y + shift_up, MolecularMotor.MOTOR_POSN_X + MolecularMotor.MOTOR_WIDTH , MolecularMotor.MOTOR_POSN_Y + MolecularMotor.MOTOR_HEIGHT + shift_up
        shift_down = -5
        coordinate = MolecularMotor.MOTOR_POSN_X, MolecularMotor.MOTOR_POSN_Y + shift_down, MolecularMotor.MOTOR_POSN_X + MolecularMotor.MOTOR_WIDTH , MolecularMotor.MOTOR_POSN_Y + MolecularMotor.MOTOR_HEIGHT + shift_down
        
        #create motor
        self.chart1.after(cycle_period)
        self.chart1.create_oval(coordinate, fill=MolecularMotor.MOTOR_COLOR)
        self.chart1.update()
        self.chart1.after(cycle_period)
        
        self.chart1.create_oval(coordinate, fill=MolecularMotor.MOTOR_COLOR)
        self.chart1.update()
        
    def COLORS(self,which_color):
        COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']
        if which_color < 480 and which_color >= 0:
            return COLORS[which_color]
        else:
            which_color = rd.randit(0,479)
            print("Color number is not in the range 0, 479. Return random color")
            return COLORS[which_color]
if __name__ == "__main__":
    main()