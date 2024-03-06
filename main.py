from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import cv2
import time
import threading
import os

# Your existing initialization code for MTCNN, InceptionResnetV1, dataset, and embeddings
mtcnn0 = MTCNN(image_size=240, margin=0, keep_all=False, min_face_size=40)
mtcnn = MTCNN(image_size=240, margin=0, keep_all=True, min_face_size=40)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

dataset = datasets.ImageFolder('photos')
idx_to_class = {i: c for c, i in dataset.class_to_idx.items()}

# Load saved data for embeddings and names
load_data = torch.load('data.pt')
embedding_list, name_list = load_data

min_distance_threshold = 0.9

person_records = {}
last_seen = {}

def camera_feed_process(camera_index):
    cam = cv2.VideoCapture(camera_index)
    window_name = f"Camera {camera_index}"  # Dynamic window name based on camera index
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # Create a window for each camera
    while True:
        ret, frame = cam.read()
        if not ret:
            print(f"Failed to grab frame from camera {camera_index}, try again")
            break

        img = Image.fromarray(frame)
        img_cropped_list, prob_list = mtcnn(img, return_prob=True)

        # Display the original frame before any face processing
        cv2.imshow(window_name, frame)

        current_seen_names = []

        if img_cropped_list is not None:
            boxes, _ = mtcnn.detect(img)

            for i, (img_cropped, prob) in enumerate(zip(img_cropped_list, prob_list)):
                if prob > 0.95:
                    emb = resnet(img_cropped.unsqueeze(0)).detach()

                    dist_list = []
                    for idx, emb_db in enumerate(embedding_list):
                        dist = torch.dist(emb, emb_db).item()
                        dist_list.append(dist)

                    min_dist = min(dist_list)
                    min_dist_idx = dist_list.index(min_dist)
                    name = name_list[min_dist_idx]

                    current_seen_names.append(name)

                    box = boxes[i]

                    frame = cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                    cv2.putText(frame, name, (int(box[0]), int(box[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

                    if min_dist < min_distance_threshold:
                        if name not in person_records or (name in person_records and person_records[name]['exit_time'] is not None):
                            person_records[name] = {'entry_time': time.time(), 'exit_time': None}
                            print(f'{name} entered at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
                        last_seen[name] = 0

        for name in list(last_seen.keys()):
            if name not in current_seen_names:
                last_seen[name] += 1
                if last_seen[name] > 30:
                    if name in person_records and person_records[name]['exit_time'] is None:
                        person_records[name]['exit_time'] = time.time()
                        print(f'{name} exited at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
                    del last_seen[name]
            else:
                last_seen[name] = 0

        cv2.imshow(window_name, frame)
        k = cv2.waitKey(1)
        if k % 256 == 27:  # ESC key
            print(f'Esc pressed, closing camera {camera_index}...')
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    available_indices = [index for index in range(5) if cv2.VideoCapture(index).isOpened()]

    threads = []
    for index in available_indices:
        thread = threading.Thread(target=camera_feed_process, args=(index,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
