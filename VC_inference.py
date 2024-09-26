import os, shutil
import gradio as gr
import webbrowser
import configparser
import subprocess

def wav2lip_fn(source_video, source_audio):    
    videofilename = os.path.basename(source_video)
    video_path = os.path.join('uploads', videofilename)
    shutil.copy(source_video, video_path)
    
    audiofilename = os.path.basename(source_audio)
    audio_path = os.path.join('uploads', audiofilename)
    shutil.copy(source_audio, audio_path)
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('OPTIONS', 'video_file', video_path)
    config.set('OPTIONS', 'vocal_file', audio_path)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    result = subprocess.run(["python", "run.py"], capture_output=True, text=True)
    if result.returncode == 0:
        print(result.stdout)
        outlines = result.stdout.strip().split('\n')
        return outlines[-2]
    else:
        print(result.stderr)

if __name__ == "__main__":
    
    app = gr.Blocks()
    with app:
        with gr.Row():
            with gr.Column():
                source_video = gr.Video(label="Source video", sources="upload")
                source_audio = gr.Audio(label="Source audio", sources="upload", type="filepath")
            with gr.Column():
                video_output = gr.Video(label="Output video")
                btn = gr.Button("Generate!")
                btn.click(wav2lip_fn,
                          inputs=[source_video, source_audio],
                          outputs=[video_output])

    webbrowser.open("http://127.0.0.1:7860")
    app.queue()
    app.launch()            