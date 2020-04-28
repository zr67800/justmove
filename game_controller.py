'''
## CONTROL -- game
Run one game with given mode and id, return if the score, and grade.

Inputs:
    mode: 0 for pass mode, 1 for training mode
    id: level number, to be appointed later
Outputs:
    score: num negative score of this round of game.
    grade: "S", "A", "B", "C"; "F" for fail (in pass mode)

def game(mode: int, id: int) -> Tuple[int, str]:
    ...
    return score, grade
'''

import cv2
import time
import numpy as np

MODE = "MPI"

if MODE is "COCO":
    protoFile = "pose/coco/pose_deploy_linevec.prototxt"
    weightsFile = "pose/coco/pose_iter_440000.caffemodel"
    nPoints = 18
    POSE_PAIRS = [[1, 0], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7], [1, 8], [8, 9], [9, 10], [1, 11], [11, 12],
                  [12, 13], [0, 14], [0, 15], [14, 16], [15, 17]]

elif MODE is "MPI":
    protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
    nPoints = 15
    POSE_PAIRS = [[0, 1], [1, 2], [2, 3], [3, 4], [1, 5], [5, 6], [6, 7], [1, 14], [14, 8], [8, 9], [9, 10], [14, 11],
                  [11, 12], [12, 13]]

inWidth = 128
inHeight = 128
threshold = 0.1

# cap = cv2.VideoCapture(0)
# hasFrame, frame = cap.read()
# vid_writer = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10,
#                              (frame.shape[1], frame.shape[0]))

net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# dummy value for demo
grade = "A"
score = 100

def calculate():
    return grade

def game(mode:int,id:int):
    # mode define the mode(pass/training)
    # id define the speed

    cap = cv2.VideoCapture(0)

    t0 = time.time()

    while(True):
        t = time.time()
        hasFrame, frame = cap.read()
        # make it mirrowing
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
    print(game_controller(1,1))

