import cv2
import sched, time
import datetime
from github import Github

# Github
g = Github("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")
repo = g.get_user().get_repo("HOBO")
all_files = []
try:
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
except: pass
git_file = 'VAISALA.jpg'

cap = cv2.videoCapture(0, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def get_data(sc):
    try:
        ret, frame = cap.read()
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
        cv2.imwrite("VAISALA.jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        
        # Github
        with open('VAISALA.jpg', 'r') as file: content = file.read()
        if git_file in all_files:
            contents = repo.get_contents(git_file)
            repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
        else:
            repo.create_file(git_file, "committing files", content, branch="master")
    
        sc.enter(60, 1, get_data, (sc,)) #600
    except Exception as e: print(e); get_data(sc)
  
now = datetime.now()
print(now.strftime("%m/%d/%Y-%H:%M")+"   VAISALA logging...")
s = sched.scheduler(time.time, time.sleep)
s.enter(60, 1, get_data, (s,))
s.run()