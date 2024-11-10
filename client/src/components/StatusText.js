import React, { useState, useEffect } from 'react';

const StatusText = ({ isRecording }) => {
  const [dots, setDots] = useState('.');

  useEffect(() => {
    if (isRecording) {
      const interval = setInterval(() => {
        setDots((prev) => (prev.length === 5 ? '.' : prev + '.'));
      }, 500);

      return () => clearInterval(interval);
    } else {
      setDots('');
    }
  }, [isRecording]);

  return (
    <div className="status-text">
      {isRecording ? `${dots} Listening ${dots}` : 'Tap to Speak'}
    </div>
  );
};

export default StatusText;
