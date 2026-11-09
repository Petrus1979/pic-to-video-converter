import streamlit as st
import os
from PIL import Image
from moviepy.editor import ImageClip, AudioFileClip

# Set up a clean, ultra-simple phone layout
st.set_page_config(page_title="PicToVideo Converter", page_icon="🎬", layout="centered")

st.title("🎬 Free Image-to-Music Video Converter")
st.write("Convert any photo and audio track into a video file instantly!")
st.markdown("---")

# 1. User Upload Fields
uploaded_image = st.file_uploader("📸 Step 1: Upload your picture (.jpg, .png)", type=["jpg", "jpeg", "png"])
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Picture Preview", width=250)

uploaded_audio = st.file_uploader("🎵 Step 2: Upload your background music (.mp3)", type=["mp3"])

st.markdown("---")

# 2. Video Processing Logic
if uploaded_image and uploaded_audio:
    st.subheader("🚀 Step 3: Generate Your Video")
    
    if st.button("🎬 Convert & Build Video Now"):
        with st.spinner("Processing video... Please wait while your download links prepare."):
            try:
                # Ensure temporary directories exist
                os.makedirs("temp", exist_ok=True)
                
                # Save uploaded items to temporary local files
                temp_img_path = os.path.join("temp", uploaded_image.name)
                temp_aud_path = os.path.join("temp", uploaded_audio.name)
                output_video_path = os.path.join("temp", "output_music_video.mp4")
                
                with open(temp_img_path, "wb") as f:
                    f.write(uploaded_image.getbuffer())
                with open(temp_aud_path, "wb") as f:
                    f.write(uploaded_audio.getbuffer())
                
                # Open audio to dynamically calculate its exact length
                audio_clip = AudioFileClip(temp_aud_path)
                audio_duration = audio_clip.duration
                
                # Create a video clip matching the exact length of the audio track
                image_clip = ImageClip(temp_img_path).set_duration(audio_duration)
                video_clip = image_clip.set_audio(audio_clip)
                
                # Render and write out the final video file
                video_clip.write_videofile(
                    output_video_path, 
                    fps=24, 
                    codec="libx262", 
                    audio_codec="aac",
                    logger=None
                )
                
                # Close the media elements to free up memory
                audio_clip.close()
                video_clip.close()
                
                # Provide the finished video download button to the user
                st.balloons()
                st.success("🎉 Video successfully generated!")
                with open(output_video_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Your Finished Video",
                        data=file,
                        file_name="my_created_video.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error("An error occurred during video creation. Please ensure your audio file is not corrupted.")

else:
    st.info("Please upload both a picture and a music track above to unlock the conversion button.")

# 3. Automated Passive Income Revenue Section
st.markdown("<br><br><br><hr>", unsafe_allow_html=True)
st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center; border: 1px dashed #cccccc;">
        <p style="color: #888888; font-size: 12px; margin: 0;">ADVERTISEMENT SPONSOR</p>
        <h4 style="color: #444444; margin: 5px 0;">Google AdSense Banner Integration Space</h4>
        <p style="color: #666666; font-size: 14px; margin: 0;">(Earn passive revenue from traffic automatically while videos compile above.)</p>
    </div>
""", unsafe_allow_html=True)
