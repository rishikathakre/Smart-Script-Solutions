import streamlit as st
from streamlit_player import st_player

from fetch_transcript import fetch_transcript
from model import Engine
from preprocessing import create_similarity_text, create_result_url

# Set page configuration
st.set_page_config(
    page_title="YouTube Q&A Search",
    page_icon=":movie_camera:",
    layout="wide",
)

# Add background image and styled title with YouTube logo
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://static.vecteezy.com/system/resources/previews/008/070/564/original/gradient-background-with-two-colors-yellow-blue-smooth-gradient-suitable-for-backgrounds-web-design-banners-illustrations-and-others-free-vector.jpg');
        background-size: cover;
        background-position: center;
    }

    .gradient-text {
        background-image: linear-gradient(to right, #272626, #272626, #272626, #272626, #191350, #191350, #191350, #45002b, #45002b, #45002b);
        -webkit-background-clip: text;
        color: transparent;
        font-size: 55px;
        font-family: 'monospace', monospace;
        padding-bottom: 50px;
        display: center;
    }

    .white-text {
        color: white;
        font-family: 'Arial', monospace;
    }

    .guide {
        padding: 20px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    }

    .guide h3 {
        background-image: linear-gradient(to right, #272626, #272626, #272626, #272626, #191350, #191350, #191350, #45002b, #45002b, #45002b);
        color: white;
        font-size: 24px;
        margin: 10px;
        padding-left:10px;
        font-weight: bold;
    }

    .guide ol {
        list-style-type: decimal;
        padding-left: 20px;
    }

    .guide p {
        font-size: 16px;
        margin-bottom: 5px;
    }

    .guide li {
        margin-bottom: 10px;
        font-weight: bold;
    }

    .guide li p {
        margin-bottom: 5px;
        font-weight: bold;
    }

    .guide li:before {
        font-weight: bold;
        border-radius: 50%;
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #ffe100;
        margin-right: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Add styled title with YouTube logo
st.markdown(
    """
    <h1 style='text-align: center;font-family: cursive;font-style: italic;color: navy;'>SMART SCRIPT SOLUTIONS</h1>
    """,
    unsafe_allow_html=True,
)

# Main content area
with st.container():
    st.markdown("<h5 class='white-text' id='tool' style='text-align: center;'>Revolutionize Your Video Content with Seamless Transcripts and Instant Q&A</h5>", unsafe_allow_html=True)

    # Input fields and buttons
    url_input = st.text_input(label='Video URL', placeholder='Enter YouTube Video URL')
    question_input = st.text_input(label='Question', placeholder='Enter Your Question')

    # Create three buttons
    # Create a flex layout for the buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        get_answer_btn = st.button("Get Answer")

    with col2:
        summary_btn = st.button("Summary")

    with col3:
        full_transcript_btn = st.button("Full Transcript")

    if url_input and question_input:
        with st.spinner('Loading your video...'):
            # Fetch transcript and initialize the model
            transcript = fetch_transcript(url_input)
            if not transcript:
                st.error("Could not fetch transcript. Please check the video URL.")
                st.stop()
            
            model = Engine(transcript)

        if get_answer_btn:
            with st.spinner('Finding an answer...'):
                # Ask the model the user's question
                answer = model.ask(question_input)
                similarity_text = create_similarity_text(question_input, answer)
                groups, timestamps = model.find_similar(similarity_text)
                url = create_result_url(url_input, timestamps[0])

            st.write('---')
            # Display extracted answer
            st.subheader("Extracted Answer:")
            st.write(answer)

            st.write('---')
            # Display video
            st.write("<h3>Video</h3>", unsafe_allow_html=True)
            st_player(url)

        elif summary_btn:
            with st.spinner('Generating summary...'):
                # Generate video summary
                video_summary = model.summarize_video()
            
            st.write('---')
            # Display summary
            st.write("<h3>Short Summary</h3>", unsafe_allow_html=True)
            st.write(video_summary)

        elif full_transcript_btn:
            st.write('---')
            # Display full transcript
            st.write("<h3>Long Summary</h3>", unsafe_allow_html=True)
            full_transcript = "\n".join([f"{item['text']}" for item in transcript])
            st.write(full_transcript)

    st.write("---")

    # Benefits section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("<h3 style='text-align: center;'>No Installations or Setup</h3>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>“Copy the URL from the address bar of your web browser or right-click the video and select “Copy Video URL”</p>", unsafe_allow_html=True)

    with col2:
        st.write("<h3 style='text-align: center;'>Probably Won't Fail</h3>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>“The meeting transcripts are generated live without any note-taking bots and with 100% accurate speaker identification”</p>", unsafe_allow_html=True)

    with col3:
        st.write("<h3 style='text-align: center;'>Easy to Use</h3>", unsafe_allow_html=True)
        st.write("<p style='text-align: center;'>“Use one-click AI prompts to generate a summary, Extracted Answer, Video time stamp from your given youtube link”</p>", unsafe_allow_html=True)

    st.write("---")

    # How to Get the Transcript of a YouTube Video
    st.markdown(
        """
        <div class='guide'>
            <h3>User Guide - How To Get The Transcript Of A YouTube Video?</h3>
            <ol>
                <li><p>Copy the YouTube URL</p></li>
                    <p>Copy the URL from the address bar of your web browser or right-click the video and select “Copy Video URL”.</p>
                <li><p>Paste the URL above</p></li>
                    <p>Simply paste the copied YouTube video URL one the given address bar "Enter Youtube VIdeo URL".</p>
                <li><p>Write the Question related to Youtube URL</p></li>
                    <p>Once you have write the question related to Youtube URL, the transcription will automatically begin and the open transcript will be ready within minutes.</p>
                <li><p>Click "Get Answer" to View the Answer with Time Stamp</p></li>
                    <p>The transcript will include timestamps of each sentence and a full written extracted answer related to question of the YouTube video.</p>
                <li><p>Click "Summary" to View the Summary Transcript</p></li>
                    <p>Then you will see the YouTube video summary to quickly grasp the core points of the video. Without watching the full video, you can judge whether it's worth your time to study.</p>
                <li><p>Click "Full Transcript" to View the Full Transcript</p></li>
                    <p>Then you will see the full transcript pop up from the given youtube video URL. Copy the text from the transcript and paste it wherever you need to download it.</p>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("---")

    # Frequently Asked Questions
    st.markdown(
        """
        <div class='guide'>
            <h3>Frequently Asked Questions</h3>
            <ol>
                <li><p>Is YouTube Video Transcript Available for Free?</p></li>
                    <p>Yes, YouTube video transcripts are available for free. YouTube transcripts are generated using automatic speech recognition technology. This means they are not always 100% accurate, but they are usually good enough for general purposes.</p>
                <li><p>What is a YouTube transcript?</p></li>
                    <p>Transcripts are literal word-for-word transcription of the audio in a video. They are typically displayed below the video player but can also be downloaded as a text file. Transcripts are helpful for people who want to read along with the audio or who need to access the content of the video in a different format, such as text-to-speech.</p>
                <li><p>How do I get a YouTube transcript?</p></li>
                    <p>Go to YouTube and open the video that you want transcribed. Click the three dots below the video, next to the Share and Save buttons. Select “Show transcript” from the menu. Note that the transcript might not be available for every video.</p>
            </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )
