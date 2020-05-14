'''
## CONTROL -- game
Run one game with given mode and id, return if the score, and grade.

Inputs:
    mode: 0 for pass mode, 1 for training mode
    id: level number, to be appointed later
Outputs:
    score: num negative score of this round of game.
    grade: "A", "B", "C"; "F" for fail (in pass mode)

def game(mode: int, id: int) -> Tuple[int, str]:
    ...
    return score, grade
'''

import cv2
import time
import numpy as np

import pygame

## refactoring:

class Detector:
    def __init__(self, mode, in_width, in_height, threshold):

        if mode == "COCO":
            self.protoFile = "pose/coco/pose_deploy_linevec.prototxt"
            self.weightsFile = "pose/coco/pose_iter_440000.caffemodel"
            self.nPoints = 18
            self.POSE_PAIRS = [[1, 0], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7], [1, 8], [8, 9], [9, 10], [1, 11], [11, 12],
                               [12, 13], [0, 14], [0, 15], [14, 16], [15, 17]]   
        elif mode == "MPI":
            self.protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
            self.weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
            self.nPoints = 15
            self.POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 14], [14, 8], [8, 9], [9, 10], [14, 11],
                               [11, 12], [12, 13]]
        else:
            raise ValueError
        
        self.in_width = in_width
        self.in_height = in_height
        self.threshold = threshold

        self.net = cv2.dnn.readNetFromCaffe(self.protoFile, self.weightsFile)

    def __call__(self, frame):
        ''' 
        Pose detector. Input a frame, output keypoints.
        '''
        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (self.in_width, self.in_height), (0, 0, 0), swapRB=False, crop=False)
        self.net.setInput(inpBlob)
        output = self.net.forward()

        H = output.shape[2]
        W = output.shape[3]

        # Empty list to store the detected keypoints
        points = []

        for i in range(self.nPoints):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]

            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            # Scale the point to fit on the original image
            x = (frameWidth * point[0]) / W
            y = (frameHeight * point[1]) / H

            if prob > self.threshold:
                #cv2.circle(frame, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                #cv2.putText(frame, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, lineType=cv2.LINE_AA)
                # Add the point to the list if the probability is greater than the threshold
                points.append((int(x), int(y)))
            else:
                points.append(None)

        # logging
        print("detector: ", end=',')
        for i in points:
            #if i is not None:
                print(i,end=',')
        print()

        return points

class Grader:
    def __init__(self, mode, id):
        pass

    def evaluate(self, key_points, t):
        pass


    def get_final_grade(self, score):
        return "A"

class Visualiser:
    def raw(self, frame):
        return frame

    def show(self, frame):
        cv2.imshow('cam', frame)
        cv2.waitKey(1)

class OneTimeAudioPlayer:
    def __init__(self, sound_file):
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)

    def play(self):
        pygame.mixer.music.play()
    
    def stop(self):
        pygame.mixer.music.stop()
        #pygame.mixer.music.unload()

    

def game(mode, id):
    # mode define the mode(pass/training)
    # id define the level/training target
    # They are passed to game data feeders, and has nothing to do with this game controller

    # read info from game data 
        # dummy things for testing 
    music_file = './media/music_01.mp3'


        # end

    # control the cam
    cap = cv2.VideoCapture(0)

    # detector:
    detector = Detector(mode = "MPI", in_width = 128, in_height = 128, threshold = 0.1)

    # grader:
    grader = Grader(mode, id)

    # visualiser
    visualiser = Visualiser()

    # audio player
    music = OneTimeAudioPlayer(music_file)

    # time control
    t0 = time.time()

    music.play()

    # consider to add "ready to start": only when some certain set of points are detected then the game starts
    # or only when a "ready pose" gets enough score?

    while True:
        # time control for testing
        t = time.time() - t0
        print (t)
        if t >= 10:
            break

        # capture a frame
        hasFrame, frame = cap.read()
        frame = cv2.flip(frame,1)

        
        key_points = detector(frame)
        grader.evaluate(key_points, t)

        visualiser.show(frame)
        
    music.stop()

    score = 100
    grade = grader.get_final_grade(score)

    return (grade, score)




# dummy value for demo
grade = "A"
score = 100

def calculate():
    return grade

def game_(mode:int,id:int):
    # mode define the mode(pass/training)
    # id define the speed

    cap = cv2.VideoCapture(0)

    t0 = time.time()

    while(True):
        t = time.time()
        hasFrame, frame = cap.read()
        # make it mirroring
        frame = cv2.flip(frame,1)
        frameCopy = np.copy(frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if not hasFrame:
            cv2.waitKey()
            break
        print(t-t0)
        if t - t0 >= 10:
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        inpBlob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight),
                                        (0, 0, 0), swapRB=False, crop=False)
        net.setInput(inpBlob)
        output = net.forward()

        H = output.shape[2]
        W = output.shape[3]
        # Empty list to store the detected keypoints
        points = []
        # a time
        for i in range(nPoints):
            # confidence map of corresponding body's part.
            probMap = output[0, i, :, :]

            # Find global maxima of the probMap.
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            # Scale the point to fit on the original image
            x = (frameWidth * point[0]) / W
            y = (frameHeight * point[1]) / H

            if prob > threshold:
                cv2.circle(frameCopy, (int(x), int(y)), 8, (0, 255, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.putText(frameCopy, "{}".format(i), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2,
                            lineType=cv2.LINE_AA)
                # Add the point to the list if the probability is greater than the threshold
                points.append((int(x), int(y)))
            else:
                points.append(None)

        for i in points:
            if(i!=None):
                print(i,end='')
        # calculate
        calculate()
        # Draw Skeleton
        for pair in POSE_PAIRS:
            partA = pair[0]
            partB = pair[1]
            #print(points[partA],points[partB],end='')
            if points[partA] and points[partB]:
                cv2.line(frame, points[partA], points[partB], (0, 255, 255), 3, lineType=cv2.LINE_AA)
                cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.circle(frame, points[partB], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

        cv2.putText(frame,"time taken = {:.2f} sec".format(time.time() - t), (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8,
                    (255, 50, 0), 2, lineType=cv2.LINE_AA)
        cv2.imshow('Output-Skeleton', frame)

        # vid_writer.write(frame)
    # vid_writer.release()
    cv2.destroyAllWindows() 
    return (grade,score)

if __name__ == "__main__":
    print(game(1,1))

