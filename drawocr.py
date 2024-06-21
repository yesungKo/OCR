import os
import cv2
from paddleocr import draw_ocr
from PIL import Image

def draw_ocr_results(frame, result_screen, result_subtitle, frame_num, draw_output_folder):
    height, width, _ = frame.shape
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert('RGB')
    
    boxes_screen = [line[0] for line in result_screen[0]]
    txts_screen = [line[1][0] for line in result_screen[0]]
    scores_screen = [line[1][1] for line in result_screen[0]]
    im_show_screen = draw_ocr(image, boxes_screen, txts_screen, scores_screen, font_path='./NanumGothic-Regular.ttf')
    
    boxes_subtitle = [[(box[0][0], box[0][1] + int(height * 0.8)), 
                       (box[1][0], box[1][1] + int(height * 0.8)), 
                       (box[2][0], box[2][1] + int(height * 0.8)), 
                       (box[3][0], box[3][1] + int(height * 0.8))] for box in [line[0] for line in result_subtitle[0]]]
    
    txts_subtitle = [line[1][0] for line in result_subtitle[0]]
    scores_subtitle = [line[1][1] for line in result_subtitle[0]]
    im_show_subtitle = draw_ocr(image, boxes_subtitle, txts_subtitle, scores_subtitle, font_path='./NanumGothic-Regular.ttf')
    
    output_path_screen = os.path.join(draw_output_folder, f'result_screen_{frame_num}.png')
    Image.fromarray(im_show_screen).save(output_path_screen)
    
    output_path_subtitle = os.path.join(draw_output_folder, f'result_subtitle_{frame_num}.png')
    Image.fromarray(im_show_subtitle).save(output_path_subtitle)
    
    print(f'{output_path_screen} 저장 완료')
    print(f'{output_path_subtitle} 저장 완료')
