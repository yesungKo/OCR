import os
import cv2
import numpy as np
import pandas as pd
import json
import argparse
from paddleocr import PaddleOCR
from difflib import SequenceMatcher
from drawocr import draw_ocr_results
import time

def get_ocr_text(ocr_result):
    return ' '.join([line[1][0] for line in ocr_result[0]])

def get_ocr_boxes(ocr_result):
    return [line[0] for line in ocr_result[0]]

def is_similar(text1, text2, threshold=0.6):
    return SequenceMatcher(None, text1, text2).ratio() > threshold

def save_results(ocr_data, savefile_type, output_path):
    if savefile_type == 'csv':
        df = pd.DataFrame(ocr_data)
        df['screen_boxes'] = df['screen_boxes'].apply(lambda x: str(x))
        df['subtitle_boxes'] = df['subtitle_boxes'].apply(lambda x: str(x))
        df.to_csv(output_path, index=False, encoding='cp949')
    elif savefile_type == 'json':
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ocr_data, f, ensure_ascii=False, indent=4)
    elif savefile_type == 'txt':
        with open(output_path, 'w', encoding='utf-8') as f:
            for entry in ocr_data:
                f.write(f"Frame Filename: {entry['frame_filename']}\n")
                f.write(f"Screen OCR: {entry['screen_ocr']}\n")
                f.write(f"Screen Boxes: {entry['screen_boxes']}\n")
                f.write(f"Subtitle OCR: {entry['subtitle_ocr']}\n")
                f.write(f"Subtitle Boxes: {entry['subtitle_boxes']}\n")
                f.write("\n")

def main(video_path, output_folder_path, threshold=0.6, savefile_type='csv', draw_ocr_flag=False):
    start_time = time.time()
    ocr = PaddleOCR(lang="korean")
    
    csv_output_path = os.path.join(output_folder_path, f'ocr_results.{savefile_type}')
    os.makedirs(output_folder_path, exist_ok=True)
    
    if draw_ocr_flag:
        draw_output_folder = os.path.join(output_folder_path, 'drawocr')
        os.makedirs(draw_output_folder, exist_ok=True)
        
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f'FPS: {fps}, 총 프레임 수: {frame_count}')

    frame_num = 0
    ocr_texts_screen = []
    ocr_texts_subtitle = []
    ocr_data = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_num % int(fps) == 0:
            height, width, _ = frame.shape
            
            screen_roi = frame[:int(height*0.8), :]
            subtitle_roi = frame[int(height*0.8):, :]

            result_screen = ocr.ocr(np.array(cv2.cvtColor(screen_roi, cv2.COLOR_BGR2RGB)))
            result_subtitle = ocr.ocr(np.array(cv2.cvtColor(subtitle_roi, cv2.COLOR_BGR2RGB)))
            
            screen_text = get_ocr_text(result_screen)
            subtitle_text = get_ocr_text(result_subtitle)
            screen_boxes = get_ocr_boxes(result_screen)
            subtitle_boxes = get_ocr_boxes(result_subtitle)
            
            if any(is_similar(screen_text, existing_screen_text, threshold) and is_similar(subtitle_text, existing_subtitle_text, threshold)
                   for existing_screen_text, existing_subtitle_text in zip(ocr_texts_screen, ocr_texts_subtitle)):
                print(f"Frame {frame_num} is considered a duplicate and will be skipped.")
            else:
                ocr_texts_screen.append(screen_text)
                ocr_texts_subtitle.append(subtitle_text)
                
                frame_filename = os.path.join(output_folder_path, f'frame_{frame_num}.png')
                cv2.imwrite(frame_filename, frame)
                print(f'{frame_filename} 저장 완료')

                ocr_data.append({
                    'frame_filename': f'frame_{frame_num}.png',
                    'screen_ocr': screen_text,
                    'screen_boxes': screen_boxes,
                    'subtitle_ocr': subtitle_text,
                    'subtitle_boxes': subtitle_boxes
                })

                if draw_ocr_flag:
                    draw_ocr_results(frame, result_screen, result_subtitle, frame_num, draw_output_folder)
        
        frame_num += 1

    cap.release()
    save_results(ocr_data, savefile_type, csv_output_path)
    end_time= time.time()
    exec_time = end_time - start_time
    print(f"Execution time: {exec_time:.2f} seconds")
    return exec_time
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process video frames and perform OCR.")
    parser.add_argument('video_path', nargs='?', type=str, help='Path to the video file')
    parser.add_argument('output_path', nargs='?', type=str, help='Directory to save the output results')
    # parser.add_argument('--video_path', type=str, help='Path to the video file')
    # parser.add_argument('--output_path', type=str, help='Directory to save the output results')
    parser.add_argument('--threshold', type=float, default=0.6, help='Threshold for similarity comparison')
    parser.add_argument('--savefile_type', type=str, default='csv', choices=['csv', 'txt', 'json'], help='File type for saving results')
    parser.add_argument('--draw_ocr', action='store_true', help='Whether to draw OCR results on images')

    args = parser.parse_args()
    exec_time = main(args.video_path, args.output_path, args.threshold, args.savefile_type, args.draw_ocr)
    print(f"Total execution time: {exec_time:.2f} seconds")