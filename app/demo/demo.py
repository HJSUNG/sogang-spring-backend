def demo_yawn(detection_detail_no, scenario_case='negative'):
    if scenario_case == 'positive':
        return {"predicted_label": "normal"}
    else:
        if detection_detail_no in [4,5,6,7,10,11,14,15,16,17,20,21,25,26,27,28,29,30,31,35,36,37]:
            return { "predicted_label": "yawn" }
        else:
            return { "predicted_label": "normal" }

def demo_eye_rubbing(detection_detail_no, scenario_case='negative'):
    if scenario_case == 'positive':
        return {"predicted_label": "normal"}
    else:
        if detection_detail_no in [4,5,6,7,10,11,14,15,16,17,20,21,25,26,27,28,29,30,31,35,36,37]:
            return { "predicted_label": "normal" }
        else:
            return { "predicted_label": "normal" }

def demo_sleeping(detection_detail_no, scenario_case='negative'):
    if scenario_case == 'positive':
        return {"predicted_label": "normal"}
    else:
        if detection_detail_no in [1,2,3]:
            return { "predicted_label": "C5" }
        else:
            return { "predicted_label": "C13" }

def demo_pose(detection_detail_no, scenario_case='negative'):
    if scenario_case == 'positive':
        return {"predicted_label": "normal"}
    else:
        if(detection_detail_no in [0,1,2]):
            return { "predicted_label": "normal" }
        elif(detection_detail_no in [3,4,5]):
            return { "predicted_label": "lean-left" }
        elif(detection_detail_no in [6,7]):
            return { "predicted_label": "normal" }
        elif(detection_detail_no in [8,9,10]):
            return { "predicted_label": "lean-right" }
        else:
            return { "predicted_label": "normal" }

def demo_facial_emotion(detection_detail_no, scenario_case='negative'):
    if scenario_case == 'positive':
        return {"predicted_label": "happy"}
    else:
        return {"predicted_label": "sad"}