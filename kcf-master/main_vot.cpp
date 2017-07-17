#include <stdlib.h>

#include "kcf.h"
#include "vot.hpp"

int main()
{
    cv::VideoCapture capture(0);

    int init_x = 400, init_y = 100;
    int init_dx = 300, init_dy = 400;
  
    while (cv::waitKey(30) != 27)  
    {  
        cv::Mat frame;
        capture >> frame;

        cv::rectangle(frame,cvPoint(init_x,init_y),cvPoint(init_x+init_dx,init_y+init_dy),cv::Scalar(255,0,0),2,2,0);

        //cv::resize(frame, frame, cv::Size(frame.cols / 2, frame.rows / 2), 0, 0, cv::INTER_LINEAR);

        cv::imshow("camera", frame);
    }
    
    //load region, images and prepare for output
    //VOT vot_io("region.txt", "images.txt", "output.txt");

    KCF_Tracker tracker;
    cv::Mat image;
    capture >> image;

    //img = firts frame, initPos = initial position in the first frame
    cv::Rect init_rect(init_x, init_y, init_dx, init_dy);
    //vot_io.outputBoundingBox(init_rect);
    //vot_io.getNextImage(image);

    tracker.init(image, init_rect);

    BBox_c bb;
    //double avg_time = 0.;
    //int frames = 0;
    while (cv::waitKey(1) != 27){
        capture >> image;
        //double time_profile_counter = cv::getCPUTickCount();
        tracker.track(image);
        //time_profile_counter = cv::getCPUTickCount() - time_profile_counter;
        //std::cout << "  -> speed : " <<  time_profile_counter/((double)cvGetTickFrequency()*1000) << "ms. per frame" << std::endl;
        //avg_time += time_profile_counter/((double)cvGetTickFrequency()*1000);
        //frames++;

        bb = tracker.getBBox();
        //vot_io.outputBoundingBox(cv::Rect(bb.cx - bb.w/2., bb.cy - bb.h/2., bb.w, bb.h));

        cv::rectangle(image, cv::Rect(bb.cx - bb.w/2., bb.cy - bb.h/2., bb.w, bb.h), CV_RGB(0,255,0), 2);
        cv::imshow("output", image);
       // cv::waitKey();

//        std::stringstream s;
//        std::string ss;
//        int countTmp = frames;
//        s << "imgs" << "/img" << (countTmp/10000);
//        countTmp = countTmp%10000;
//        s << (countTmp/1000);
//        countTmp = countTmp%1000;
//        s << (countTmp/100);
//        countTmp = countTmp%100;
//        s << (countTmp/10);
//        countTmp = countTmp%10;
//        s << (countTmp);
//        s << ".jpg";
//        s >> ss;
//        //set image output parameters
//        std::vector<int> compression_params;
//        compression_params.push_back(CV_IMWRITE_JPEG_QUALITY);
//        compression_params.push_back(90);
//        cv::imwrite(ss.c_str(), image, compression_params);
    }

    //std::cout << "Average processing speed " << avg_time/frames <<  "ms. (" << 1./(avg_time/frames)*1000 << " fps)" << std::endl;

    return EXIT_SUCCESS;
}