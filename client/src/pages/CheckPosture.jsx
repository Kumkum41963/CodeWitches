import React, { useRef, useState } from 'react';
import Webcam from 'react-webcam';
import axios from 'axios';
import imageCompression from 'browser-image-compression'; 
import './CheckPosture.css'; // Import the CSS file

const CheckPosture = () => {
  const webcamRef = useRef(null);
  const [processedImages, setProcessedImages] = useState([]); // Store all processed images
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [captureInterval, setCaptureInterval] = useState(null);
  const [frameCount, setFrameCount] = useState(0); // Track the number of frames

  const convertBlobToBase64 = (blob) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(blob);
    });
  };

  const captureFrame = async () => {
    if (!webcamRef.current) return;

    const frame = webcamRef.current.getScreenshot(); // Capture the frame from the webcam
    if (frame && isProcessing) {
      try {
        // Convert base64 to Blob for better handling
        const byteString = atob(frame.split(',')[1]);
        const arrayBuffer = new ArrayBuffer(byteString.length);
        const uintArray = new Uint8Array(arrayBuffer);
        for (let i = 0; i < byteString.length; i++) {
          uintArray[i] = byteString.charCodeAt(i);
        }
        const blob = new Blob([uintArray], { type: 'image/jpeg' });

        // Compress the image using the browser-image-compression library
        const compressedImage = await imageCompression(blob, {
          maxWidthOrHeight: 640, // Resize image
          useWebWorker: true,
          initialQuality: 0.7, // Reduce quality
        });

        // Create a new base64 string from the compressed image
        const compressedBase64 = await convertBlobToBase64(compressedImage);

        // Check the size of the compressed image
        const sizeInKB = compressedBase64.length / 4 / 1024; // Calculate size in KB
        if (sizeInKB > 5000) {
          alert("Frame size is still too large. Please capture a smaller frame.");
          return;
        }

        // Send the base64 string to the backend
        const response = await axios.post('http://localhost:5000/process', {
          frame: frame.split(',')[1], // Remove base64 prefix
        }, {
          headers: {
            'Content-Type': 'application/json',
          },
        });

        // Generate a unique name for the frame
        const newFrameName = `frame${frameCount + 1}`;

        // Add the processed frame to the list of processed images with a new name
        const processedImage = `data:image/jpeg;base64,${response.data.frame}`;

        setProcessedImages((prevImages) => {
          // Increment frame count and add the new frame
          setFrameCount(frameCount + 1);
          return [...prevImages, { name: newFrameName, data: processedImage }];
        });
      } catch (err) {
        console.error('Error processing frame:', err);
        alert('Error processing frame. Please check your server or try again later.');
      }
    } else {
      console.log('Processing is on hold');
    }
  };

  const toggleCameraAndProcessing = () => {
    if (!isCameraOn) {
      // Start the camera and processing
      setIsCameraOn(true);
      setIsProcessing(true);
      setCaptureInterval(setInterval(captureFrame, 1000)); // Capture frame every 500ms
    } else {
      // Just stop the camera but keep processed images and feed container
      setIsCameraOn(false);
      setCaptureInterval(null); // Clear the interval but keep processing images
    }
  };

  return (
    <div className="check-posture-container">
      {/* Heading */}
      <h1 className="heading">Posture Detection</h1>

      {/* Main Content Container */}
      <div className="main-container">
        {/* Left: Live Camera Feed */}
        <div className="camera-feed-container">
          <div className={`camera-feed ${isCameraOn ? "" : "black-screen"}`}>
            {isCameraOn && (
              <Webcam
                ref={webcamRef}
                audio={false}
                className="camera-view"
                screenshotFormat="image/jpeg"
              />
            )}
          </div>
        </div>

        {/* Right: Processed Image Grid */}
        <div className="processed-grid">
          <div className="processed-images">
            {processedImages.map((imageObj, index) => (
              <img
                key={index}
                src={imageObj.data}
                alt={imageObj.name}
                className="processed-image"
              />
            ))}
          </div>
        </div>
      </div>

      {/* Buttons */}
      <div className="button-container">
        <button className="toggle-button" onClick={toggleCameraAndProcessing}>
          {isCameraOn ? 'Stop' : 'Start'}
        </button>
        {isCameraOn && (
          <button className="capture-button" onClick={captureFrame}>
            Process
          </button>
        )}
      </div>
    </div>
  );
};

export default CheckPosture;