//
//  main.cpp
//  LuckyYou
//
//  Created by DJ Lee on 2/13/16.
//  Copyright © 2016 DJ Lee. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <string>
#include <opencv2/opencv.hpp>

using namespace std;
using namespace cv;

#define IMG_WIDTH	300
#define IMG_HEIGHT	300
#define IMG_COLS	6
#define MAX_STDS	200
#define NUM_DINGS   12

Mat Photos, Individual;
int Num_Stds, Student, nPicked;
int Picked[MAX_STDS], Active[MAX_STDS], Presence[MAX_STDS];
char LastName[MAX_STDS][128], FirstName[MAX_STDS][128], StudentID[MAX_STDS][128];

void onClear(int, void*);
void onPresence(int, void*);
void onClick(int, void*);

int main(int argc, const char * argv[])
{
// Read names from roster file
    ifstream RosterFile ("..//..//..//Roster.txt");
    Num_Stds = 0;
    if (RosterFile.is_open()) {
        while (RosterFile >> LastName[Num_Stds] >> FirstName[Num_Stds] >> StudentID[Num_Stds]) {
            // cout << LastName[Num_Stds] << FirstName[Num_Stds] << StudentID[Num_Stds] << endl;
            Num_Stds++;
        }
        // cout << Num_Stds << endl;
        RosterFile.close();
    } else {
        cout << "Missing roster file! Exie program";
        return -1;
    }
// Read records
    ifstream RecordFile ("..//..//..//Record.txt");
    nPicked = 0;
    int id, index = 0;
    if (RecordFile.is_open()) {
        while (RecordFile >> id >> Active[index] >> Picked[index] >> Presence[index] >> LastName[index] >> FirstName[index] >>StudentID[index]) {
            index++;
        }
        RecordFile.close();
    } else {  // create the record file the first time
        for (int i = 0; i < Num_Stds; i++) {
            Active[i] = 1;
            Picked[i] = 0;
            Presence[i] = 0;
        }
    }
    
    namedWindow("LuckyYou", WINDOW_AUTOSIZE);
    
//  createButton("Clear", onClear, NULL, QT_PUSH_BUTTON, false);
//  createButton("Presence", onPresence, NULL, QT_PUSH_BUTTON, false);
//  createButton("Click", onClick, NULL, QT_PUSH_BUTTON, false);
  
    Photos = imread("..//..//..//photos.bmp", CV_LOAD_IMAGE_UNCHANGED);
    
    Num_Stds = 20;

    
//    imshow("LuckyYou", Individual);
    waitKey();
    return 0;
}

    
void onClear(int, void*) {
    for (int i = 0; i < Num_Stds; i++) {
        nPicked = 0;
        Picked[i] = 0;
    }
}

void onPresence(int, void*) {
    Presence[Student]++;
}

    
void onClick(int, void*)
{
    Rect	ROI;
    int		i, j, Delay, rand_Student;
    // char	Msg[128];
    
    // if (First) First = FALSE;
    ROI.width = IMG_WIDTH;
    ROI.height = IMG_HEIGHT;
    for (i=0; i<NUM_DINGS; i++) {
        Delay = (int)(150*sqrt(sqrt(double(i+5)))+0.5);
        usleep(Delay*1000);
        rand_Student = rand() % Num_Stds;
        Student = -1;
        for (j = rand_Student; j<rand_Student + Num_Stds; j++) {
            //if (!Picked[j%Num_Stds] && Active[j%Num_Stds]) {
                Student = j%Num_Stds;
                //break;
            //}
        }
        if (Student >= 0) {
            ROI.x = (Student % IMG_COLS)*IMG_WIDTH;
            ROI.y = (Student / IMG_COLS)*IMG_HEIGHT;
            Individual = Photos(ROI);
            
            // sprintf_s(Msg, "%s, %s", LastName[Student], FirstName[Student]);

            // sprintf_s(Msg, "%2d", nPicked);

            
            
            // PlaySound(TEXT("Ding.wav"), 0, SND_ASYNC);
        }
    }
    if (Student >= 0) {
        nPicked++;
        Picked[Student] = 1;
    }
}

