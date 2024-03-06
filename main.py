from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from torchvision import datasets
from torch.utils.data import DataLoader
from PIL import Image
import cv2
import time
import os

# initializing MTCNN and InceptionResnetV1
mtcnn0 = MTCNN(image_size=240, margin=0, keep_all=False, min_face_size=40)  # keep_all=False
mtcnn = MTCNN(image_size=240, margin=0, keep_all=True, min_face_size=40)  # keep_all=True
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Read data from folder
dataset = datasets.ImageFolder('photos')  # photos folder path
idx_to_class = {i: c for c, i in dataset.class_to_idx.items()}  # accessing names of people from folder names

def collate_fn(x):
    return x[0]

loader = DataLoader(dataset, collate_fn=collate_fn)

name_list = []  # list of names corresponding to cropped photos
embedding_list = []  # list of embedding matrix after conversion from cropped faces to embedding matrix using resnet

for img, idx in loader:
    face, prob = mtcnn0(img, return_prob=True)
    if face is not None and prob > 0.92:
        emb = resnet(face.unsqueeze(0))
        embedding_list.append(emb.detach())
        name_list.append(idx_to_class[idx])

# Save data
data = [embedding_list, name_list]
torch.save(data, 'data.pt')  # saving data.pt file

# Using webcam to recognize faces
load_data = torch.load('data.pt')
embedding_list = load_data[0]
name_list = load_data[1]

# Set a minimum distance threshold for recognition
min_distance_threshold = 0.9

# Maintain records of entry and exit times
person_records = {}
last_seen = {}  # Dictionary to track the last frame a person was seen
load_data = torch.load('data.pt')
embedding_list = load_data[0]
name_list = load_data[1]

min_distance_threshold = 0.9
person_records = {}
last_seen = {}

available_indices = []

for index in range(5):

    cap = cv2.VideoCapture(index)

    if cap.isOpened():

        print(f"Camera index {index} is opened.")

        available_indices.append(index)

        cap.release()

    else:

        print(f"Camera index {index} is not available.")



# Initialize cameras
laptop_cam = cv2.VideoCapture(0)  # Usually, 0 is the laptop's built-in camera
external_cam = cv2.VideoCapture(1)  # Assumes 1 is the first external camera connected

def process_and_display_frame(cam, window_name):
    ret, frame = cam.read()
    if not ret:
        print(f"Failed to grab frame from {window_name}")
        return
    
    img = Image.fromarray(frame)
    img_cropped_list, prob_list = mtcnn(img, return_prob=True)
    current_seen_names = []

    if img_cropped_list is not None:
        boxes, _ = mtcnn.detect(img)
        for i, (img_cropped, prob) in enumerate(zip(img_cropped_list, prob_list)):
            if prob > 0.95:
                emb = resnet(img_cropped.unsqueeze(0)).detach()
                dist_list = [torch.dist(emb, emb_db).item() for emb_db in embedding_list]
                min_dist = min(dist_list)
                if min_dist < min_distance_threshold:
                    min_dist_idx = dist_list.index(min_dist)
                    name = name_list[min_dist_idx]
                    current_seen_names.append(name)

                    box = boxes[i]
                    frame = cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                    cv2.putText(frame, name, (int(box[0]), int(box[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
                    
                    # Update entry time and reset exit time
                    if name not in person_records:
                        person_records[name] = {'entry_time': time.time(), 'exit_time': None}
                        print(f"{name} entered at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
                    else:
                        if person_records[name]['exit_time'] is not None:
                            person_records[name]['entry_time'] = time.time()
                            person_records[name]['exit_time'] = None
                            print(f"{name} re-entered at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
                    last_seen[name] = 0

    # Check for exits
    for name in list(last_seen.keys()):
        if name not in current_seen_names:
            last_seen[name] += 1
            # Mark as exited after 30 frames of absence
            if last_seen[name] > 30:
                if person_records[name]['exit_time'] is None:
                    person_records[name]['exit_time'] = time.time()
                    print(f"{name} exited at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}")
        else:
            last_seen[name] = 0  # Reset last seen counter if currently seen

    cv2.imshow(window_name, frame)

# Main loop
while True:
    process_and_display_frame(laptop_cam, "Laptop Camera")
    process_and_display_frame(external_cam, "External Camera")

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit loop if 'q' is pressed
        break

# Cleanup
laptop_cam.release()
external_cam.release()
cv2.destroyAllWindows()