// MicButton.js
import React from 'react';

const MicButton = ({ onClick, isRecording }) => {
  return (
    <button className={`mic-button ${isRecording ? 'active' : ''}`} onClick={onClick}>
      <div id="iconContainer">
        {isRecording ? (
          <div className="red-dot"></div>
        ) : (
          <svg className="mic-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3s-3 1.34-3 3v6c0 1.66 1.34 3 3 3zm5-3c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
          </svg>
        )}
      </div>
    </button>
  );
};

export default MicButton;
