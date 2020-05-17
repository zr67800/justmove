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
import shelve

import pygame

from game_data import GameDataLoader

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
        #print("detector: ", end='  ')
        #for i in points:
            #if i is not None:
                print(i,end=',')
        #print()

        return points

## NOTE: it works only when Detector is configured as "MPI"
class Grader:
    def __init__(self, game_data):
        self.actions = game_data.actions
        self.target_dict = game_data.target_dict

        self.scores = [[] for i in self.actions]
        self.score = None

        for key in self.target_dict:
            self.target_dict[key] = self._normalise(list(self.target_dict[key]))

    def _find(self, t):
        for idx, action in enumerate(self.actions):
            #print(f"_find: t = {t}, time slot = {action[0]}, {action[0]+action[1]}")
            if t >= action[0] and t < action[0]+action[1]:
                return idx
        #assert False
        return None

    def evaluate(self, key_points, t):
        action_idx = self._find(t)
        print(f"grader: action_seq_idx = {action_idx}")
        if action_idx is not None:
            print(f"grader: t = {t}, action = {self.actions[action_idx][3]}")
            score = self._evaluate_frame(key_points, self.target_dict[self.actions[action_idx][3]])
            self.scores[action_idx].append(score)
            return score
        return None

    def _normalise(self, points):
        '''normalise the points. point[14] relocates to (0,0) and dist of point 0 and point 14 is 1'''
        if points[0] is None or points[14] is None:
            return None

        dx, dy = points[14]
        for i,p in enumerate(points):
            if p is not None:
                points[i] = list(p)
                points[i][0] -= dx
                points[i][1] -= dy
        
        dist = ((points[0][0])**2 + (points[0][1])**2) ** 0.5
        for i,p in enumerate(points):
            if p is not None:
                p[0] /= dist
                p[1] /= dist
        return points

    def _evaluate_frame(self,key_points, targets):
        # TODO
        key_points = self._normalise(key_points)

        if key_points is None: #cannot be normalised
            #print("_evaluate_frame: cannot normalise")
            return 0
        #print("_evaluate_frame: normalise success! ")
        #print(f"    {key_points}")
        #print(f"    {targets}")
        points_in_use = [0,1,2,3,4,5,6,7,8,10,11,12,14]
        n = len(points_in_use)

        frame_score = 0
        for i in points_in_use:
            target = targets[i]
            user_point = key_points[i]
            if target is not None and user_point is not None:
                dist = ((target[0]-user_point[0])**2 + (target[1]-user_point[1])**2) ** 0.5
                frame_score += 10 * 2**(-dist)

        return frame_score/n

    def get_target(self, t):
        action_idx = self._find(t)
        if action_idx is not None:
            print(f"get_target: t = {t}, action = {self.actions[action_idx][3]}")
            target = self.target_dict[self.actions[action_idx][3]]
            return target
        return None


    def get_score(self):
        score = 0
        for i, action in enumerate(self.actions):
            if len(self.scores[i])>0:
                if action[2] == 0:
                    score += max(self.scores[i])
                else:
                    score += sum(self.scores[i])/len(self.scores[i])
        self.score = score
        return int(score)
    
    def get_grade(self):
        n = len(self.actions)
        if self.score >= n*9:
            return "A"
        elif self.score >= n*5:
            return "B"
        elif self.score >= n*2:
            return "C"
        else:
            return "F"

class VideoProcessor:
    def __init__(self, pose_pairs):
        self.camera = cv2.VideoCapture(0)
        self.current_frame = None
        
        self.POSE_PAIRS = pose_pairs
        self.backSub = cv2.createBackgroundSubtractorMOG2()
    
    def capture(self):
        hasFrame, frame = self.camera.read()
        frame = cv2.flip(frame,1)
        self.current_frame = frame
        return self.current_frame

    def draw(self, points, is_target):
        if points is None:
            return

        frame = self.current_frame
        screen_x, screen_y = 1280, 720
        scale_factor = screen_y//8*3

        if is_target == True:
            colour = (200, 200, 200)
            points_ = []
            for p in points:
                if p is not None:
                    points_.append((int(p[0]*scale_factor + screen_x//2), int(p[1]*scale_factor + screen_y//2)))
                else:
                    points_.append(None)
            points = points_
        else:
            colour = (200, 200, 0)

        for pair in self.POSE_PAIRS:
            partA = pair[0]
            partB = pair[1]
            #print(points[partA],points[partB],end='')
            if points[partA] and points[partB]:
                cv2.line(frame, points[partA], points[partB], colour, 3, lineType=cv2.LINE_AA)
                cv2.circle(frame, points[partA], 8, colour, thickness=-1, lineType=cv2.FILLED)
                cv2.circle(frame, points[partB], 8, colour, thickness=-1, lineType=cv2.FILLED)
        self.current_frame = frame

    def _bg_remove(self):
        #not in use
        mask = self.backSub.apply(self.current_frame)
        self.current_frame = cv2.bitwise_or(self.current_frame, self.current_frame, mask=mask)

    def show(self):
        cv2.imshow('cam', self.current_frame)
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

    print("GAME",mode, id)
    # read info from game data:
    game_data = GameDataLoader(mode, id)

    # detector:
    detector = Detector(mode = "MPI", in_width = 128, in_height = 128, threshold = 0.05)

    # grader:
    grader = Grader(game_data)

    # video processor
    video = VideoProcessor(pose_pairs = detector.POSE_PAIRS)

    # audio player
    music = OneTimeAudioPlayer(game_data.music)

    # time control
    t0 = time.time()

    music.play()

    # consider to add "ready to start": only when some certain set of points are detected then the game starts
    # or only when a "ready pose" gets enough score?

    while True:
        # time control
        t = time.time() - t0
        print (t)
        if t >  game_data.max_time:
            break

        # capture a frame
        frame = video.capture()
        video.draw(grader.get_target(t),True)
        
        key_points = detector(frame)
        video.draw(key_points, False)
        grader.evaluate(key_points, t)

        video.show()
    

    music.stop()

    score = grader.get_score()
    grade = grader.get_grade()
    print(grader.scores)

    cv2.destroyAllWindows()

    return (grade, score)


if __name__ == "__main__":
    print(game(1,1))

