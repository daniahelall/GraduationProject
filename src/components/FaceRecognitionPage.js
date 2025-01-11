// src/components/FaceRecognitionPage.js
import React, { useEffect } from 'react';
import "./FaceRecognition.css";

const FaceRecognitionPage = () => {
    useEffect(() => {
       
        const videoElement = document.getElementById("video-feed");
        videoElement.src = "http://localhost:5000/video_feed"; // Point to Flask server
    }, []);

    return (
        <div className="face-recognition-container">
            <h1>Campus Identity Recognition System</h1>
            <img
                id="video-feed"
                width="1080"
                height="480"
                alt="Video feed"
                style={{ display: 'block' }}
            />
            <div id="status">Initializing...</div>
            <button
            className="dashboard-btn"
            onClick={() => window.location.href = "/dashboard"}
        >
            Go to Dashboard
        </button>
        </div>
    );
};

export default FaceRecognitionPage;
