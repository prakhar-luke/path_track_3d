# path_track_3d
Reconstruct path in 3d for a detected object in 2d 

# Dir structure :
.
├── camera_calib
│   └── calib_cam.py
├── data_points
│   ├── data_cords.csv
│   └── xyr_cords.csv
├── data_prep
│   └── xywh_to_xyr.py
├── models
│   └── 2best.pt
├── object_detect
│   └── detect_xyr.py
├── plots
│   └── 3d_path.py
├── README.md
├── requirements.txt
└── test_vids
    └── recorded_video_0.avi


# Work-flow : 
(Model) ----> obj_detection ----> data_cords.csv ----> xywh_2_xyr ----> xyr_cords.csv ---> 3d_plot
   