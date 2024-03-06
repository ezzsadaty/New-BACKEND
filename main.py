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
frame_count = {}
# Check available camera indices
available_indices = []
for index in range(5):
    cap = cv2.VideoCapture(index)
    if cap.isOpened():
        print(f"Camera index {index} is opened.")
        available_indices.append(index)
        cap.release()
    else:
        print(f"Camera index {index} is not available.")

# Open the webcam
if available_indices:
    cam = cv2.VideoCapture(available_indices[0])  # Use the first available camera index
else:
    print("No camera available. Exiting.")
    exit()

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to grab frame, try again")
        break

    img = Image.fromarray(frame)
    img_cropped_list, prob_list = mtcnn(img, return_prob=True)

    # Display the original frame before any face processing
    cv2.imshow("IMG", frame)

    current_seen_names = []  # List to keep track of names seen in the current frame

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

                # Draw the bounding box and the name above it
                frame = cv2.rectangle(frame, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
                cv2.putText(frame, name, (int(box[0]), int(box[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

                if min_dist < min_distance_threshold:
                    # Person recognized
                    if name not in person_records or (name in person_records and person_records[name]['exit_time'] is not None):
                        person_records[name] = {'entry_time': time.time(), 'exit_time': None}
                        print(f'{name} entered at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
                    last_seen[name] = 0  # Reset or initialize last seen frame count for this person

    # Update last seen counters and check for exits
    for name in list(last_seen.keys()):
        if name not in current_seen_names:
            last_seen[name] += 1  # Increment the frame counter if not seen in the current frame
            # Check if the person has not been seen for a while and mark them as exited
            if last_seen[name] > 30:  # Assuming 30 frames as the threshold for someone having exited
                if name in person_records and person_records[name]['exit_time'] is None:
                    person_records[name]['exit_time'] = time.time()
                    print(f'{name} exited at {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}')
                del last_seen[name]  # Remove from last seen to avoid memory leak
        else:
            last_seen[name] = 0  # Reset counter if seen in the current frame

    # Assume the rest of your frame processing and display logic remains unchanged
    cv2.imshow("IMG", frame)
    k = cv2.waitKey(1)
    if k % 256 == 27:  # ESC key
        print('Esc pressed, closing...')
        break

# After the loop
cam.release()
cv2.destroyAllWindows()