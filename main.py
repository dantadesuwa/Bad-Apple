import asyncio
from pyscript import document, window
from pyodide.http import pyfetch

screen = document.getElementById('screen')
overlay = document.getElementById('overlay')
audio = document.getElementById('bg-music')
start_btn = document.getElementById('start-btn')
status_text = document.getElementById('status-text')

video_data = None
last_rendered_frame = -1
FPS = 30

def update_scaling(event=None):
    """Dynamically applies CSS based on the user's screen shape."""
    if not video_data: return
    
    font_aspect = 0.6
    cols = video_data['cols']
    rows = video_data['rows']
    
    if window.innerHeight > window.innerWidth:
        # MOBILE (Portrait Mode): Fit width perfectly, leave space at top/bottom
        screen.style.fontSize = f"calc(100vw / ({cols} * {font_aspect}))"
        screen.style.lineHeight = "1em"
    else:
        # DESKTOP (Landscape Mode): Stretch fully to all edges (Classic mode)
        screen.style.fontSize = f"calc(100vw / ({cols} * {font_aspect}))"
        screen.style.lineHeight = f"calc(100vh / {rows})"

# Listen for the user resizing the window or rotating their phone
window.onresize = update_scaling

async def load_and_prep():
    global video_data
    
    try:
        status_text.innerHTML = "Python Engine Booted!<br>Downloading JSON data..."
        
        response = await pyfetch('./frames.json')
        video_data = await response.json()
        
        # Trigger our smart scaling math immediately
        update_scaling()

        status_text.innerHTML = "Data loaded.<br>Buffering audio..."
        
        while audio.readyState < 3:
            await asyncio.sleep(0.1)

        status_text.style.display = 'none'
        start_btn.innerText = "Click to Start"
        start_btn.classList.add("ready")
        
    except Exception as e:
        status_text.innerHTML = f"<span style='color:red'>Error loading files:<br>{str(e)}</span>"
        print(f"Error: {e}")

def start_playback(event):
    if "ready" in start_btn.classList:
        overlay.style.display = 'none'
        audio.play()
        asyncio.create_task(update_frame())

start_btn.onclick = start_playback

async def update_frame():
    global last_rendered_frame
    
    while True:
        if not audio.paused and video_data:
            current_time = audio.currentTime
            current_frame_index = int(current_time * FPS)
            
            if current_frame_index != last_rendered_frame and current_frame_index < len(video_data['frames']):
                screen.innerText = video_data['frames'][current_frame_index]
                last_rendered_frame = current_frame_index
        
        await asyncio.sleep(1 / 60)

asyncio.ensure_future(load_and_prep())