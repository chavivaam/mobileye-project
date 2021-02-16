```plantuml
title integration_entities


class Controller{
    +Ctor(): void
    -_tfl_manager: TflManager
    -_extract_metadata: TflMetadata
    +static {static}extract_frame_id(frame_path): int
    +run(): void
}

class TflManager{
    +Ctor(TflMetadata): void
    -_tfl_metadata: TflMetadata
    -_candidate_detector: CandidatesDetector
    -_candidate_filter: CandidatesFilter
    -_distance_estimator: DistanceEstimator
    -view_manager: ViewObserver
    +handle_frame(img): void 
}



class Manipulator{
}

class DistanceEstimator implements Manipulator{
}

class CandidatesFilter implements Manipulator{
}

class CandidatesDetector implements Manipulator{
}


DistanceEstimator *-- TflManager 
CandidatesFilter *-- TflManager 
CandidatesDetector *-- TflManager 


TflManager *-left- Controller

```