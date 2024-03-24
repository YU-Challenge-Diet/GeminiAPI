import React, { useRef, useState, useCallback, useEffect } from 'react';
import './../css/Snap.css';
import Webcam from 'react-webcam';
import {
  BrowserRouter as Router,
  Route,
  Routes,
  useLocation,
} from 'react-router-dom';
import axios from 'axios';
function Snap() {
  const location = useLocation();
  const webcamRef = useRef(null);
  const [pictureTaken, setPictureTaken] = useState(false);
  const [imgSrc, setImgSrc] = useState(null);
  const [response, setResponse] = useState(null);
  const base64StringToBlob = (base64String) => {
    const byteCharacters = atob(base64String.split(',')[1]);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: 'image/png' });
  };

  useEffect(() => {}, [webcamRef]);
  const submitForm = async () => {
    const text =
      'This is most likely an image of a dish, I want you to purely reply with the following information: the name of the dish (or an estimate), the ingredients necessary to make said dish, the number of calories within this dish, and the portion size (although this can be a rough estimate)';

    const formData = new FormData();
    formData.append('image', imgSrc);
    formData.append('text', text);

    try {
      const response = await axios.post(
        'http://35.188.128.72:5000/upload/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      setResponse(response);
      console.log(response);
    } catch (error) {
      console.log(error);
    }
  };
  // create a capture function
  const capture = useCallback(() => {
    const imageSrc = webcamRef.current.getScreenshot();
    setPictureTaken(true);
    const blob = base64StringToBlob(imageSrc);
    setImgSrc(blob); // Store the Blob in your state
  }, [webcamRef]);
  useEffect(() => {
    if (imgSrc !== null) {
      submitForm();
    }
  });
  return (
    <div className="screen2">
      <h1 className="header">
        Capture <br /> your <br />
        {location.state.mode ? 'food' : 'fridge'}.
      </h1>

      {imgSrc && response !== null ? (
        <>
          <p>{response.data.message}</p>
        </>
      ) : (
        <>
          <div className="container">
            <Webcam
              ref={webcamRef}
              height={600}
              width={600}
              screenshotFormat="image/png"
            />
          </div>
          <div className="btn-container">
            <button onClick={capture}>Capture photo</button>
          </div>
        </>
      )}
    </div>
  );
}

export default Snap;
