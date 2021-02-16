```plantuml
title Techs Wrappers 


class Manipulator{

    -view_manager: ViewObserver
    +handle(self, *argv): void
}


class DistanceEstimator implements Manipulator{
    -_prev_container: FrameContainer
    -_curr_container: FrameContainer
    -_focal_length:
    -_pp: 
    -_image: np.ndarray[81, 81, 3]
    -_is_first_frame: bool
    +Ctor(focal_length, pp): void 
    +prepare_data(*argv): void
    +execute(): 

}

class CandidatesFilter implements Manipulator{
    -_image: np.ndarray[81, 81, 3]
    -_green_candidates: List
    -_red_candidates: List
    +Ctor()
    +prepare_data(*argv): void
    +execute(): red_tfls[], green_tfls[]

}


class CandidatesDetector implements Manipulator{
    -_image: np.ndarray[81, 81, 3]
    +Ctor()
    +prepare_data(*argv): void
    +execute(): 

}


class FrameContainer{
    +Ctor(img): void
    -img: ndarray
    -traffic_light: []
    -traffic_lights_3d_location: []
    -EM: []
    -corresponding_ind:[]
    -valid: []
}


class ViewObserver{
    +Ctor(): void
    -_id_to_func: 
    -_id_to_func_args: Dict
    +notify(func_id, *argv): void
    +show(): void
    -{static}visualize_detector(argv): void

    
    -{static}visualize_filter(argv): void 

    -{static}visualize_estimator(curr_container): void
}

FrameContainer *-up- DistanceEstimator 
ViewObserver *-left- Manipulator


```