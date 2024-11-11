import React, { useState } from 'react';
import MicButton from './MicButton';
import StatusText from './StatusText';
import Watermark from './Watermark';
import FooterWatermark from './FooterWatermark';

const AudioRecorder = () => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioContext, setAudioContext] = useState(null);
  const [mediaStream, setMediaStream] = useState(null);
  const [inputMode, setInputMode] = useState('audio');
  const [audioBuffer, setAudioBuffer] = useState([]);
  const [audioProcessor, setAudioProcessor] = useState(null);
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const submitVal = () => {
    if (inputValue.trim()) {
      fetch('http://127.0.0.1:5000/submit-text', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: inputValue }), // Send input value in the request body
      })
        .then((response) => response.text())
        .then((result) => {
          console.log(result); // Log the response from Flask
          alert(result.message || "Text submitted successfully!");
        })
        .catch((error) => {
          console.error('Error:', error);
          alert('Error submitting text');
        });

      setInputValue('');
    } else {
      alert("Input cannot be empty!");
    }
  };

  const handleMicButtonClick = async () => {
    if (!isRecording) {
      // Clear the audio buffer to start a new recording
      setAudioBuffer([]);

      // Start a new recording session
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const context = new AudioContext();
      const processor = context.createScriptProcessor(2048, 1, 1);

      const source = context.createMediaStreamSource(stream);
      source.connect(processor);
      processor.connect(context.destination);

      processor.onaudioprocess = (e) => {
        const inputData = e.inputBuffer.getChannelData(0);
        setAudioBuffer((prev) => [...prev, new Float32Array(inputData)]);
      };

      setAudioContext(context);
      setMediaStream(stream);
      setAudioProcessor(processor);
      setIsRecording(true);
    } else {
      // Stop recording and send to backend
      mediaStream.getTracks().forEach((track) => track.stop());
      audioProcessor.disconnect();
      audioContext.close();
      setIsRecording(false);
      sendWavToBackend();
    }
  };

  const sendWavToBackend = () => {
    const pcmData = new Int16Array(audioBuffer.length * 2048);
    let index = 0;

    for (let i = 0; i < audioBuffer.length; i++) {
      const data = audioBuffer[i];
      for (let j = 0; j < data.length; j++) {
        pcmData[index++] = Math.max(-1, Math.min(1, data[j])) * 0x7FFF;
      }
    }

    const wavData = encodeWav(pcmData, 44100, 1); // 44.1kHz, Mono
    const wavBlob = new Blob([wavData], { type: 'audio/wav' });

    // Send to backend
    const formData = new FormData();
    formData.append('audio', wavBlob, 'recording.wav');

    fetch(' http://127.0.0.1:5000/upload-audio', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.text())
      .then((result) => {
        console.log(result); // Log the response from Flask
        alert('Audio file uploaded successfully!');
      })
      .catch((error) => {
        console.error('Error uploading file:', error);
        alert('Error uploading audio');
      });
  };

  const encodeWav = (pcmData, sampleRate, channels) => {
    const buffer = new ArrayBuffer(44 + pcmData.length * 2);
    const view = new DataView(buffer);

    // WAV Header
    writeString(view, 0, 'RIFF');
    view.setUint32(4, 36 + pcmData.length * 2, true);
    writeString(view, 8, 'WAVE');
    writeString(view, 12, 'fmt ');

    view.setUint32(16, 16, true); // PCM format
    view.setUint16(20, 1, true); // PCM format
    view.setUint16(22, channels, true); // Mono channel
    view.setUint32(24, sampleRate, true); // Sample rate
    view.setUint32(28, sampleRate * channels * 2, true); // Byte rate
    view.setUint16(32, channels * 2, true); // Block align
    view.setUint16(34, 16, true); // Bits per sample
    writeString(view, 36, 'data');
    view.setUint32(40, pcmData.length * 2, true);

    // PCM Data
    for (let i = 0; i < pcmData.length; i++) {
      view.setInt16(44 + i * 2, pcmData[i], true);
    }

    return buffer;
  };

  const writeString = (view, offset, str) => {
    for (let i = 0; i < str.length; i++) {
      view.setUint8(offset + i, str.charCodeAt(i));
    }
  };

  const handleInputModeToggle = () => {
    setInputMode(inputMode === 'audio' ? 'text' : 'audio');
  };

  return (
    <div className="container">
      <Watermark />
      {inputMode === 'audio' ? (
        <>
          <MicButton onClick={handleMicButtonClick} isRecording={isRecording} />
          <StatusText isRecording={isRecording} />
        </>
      ) : (
        <>
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Type your input..."
            className="text-input" // Keeping your original class name for styling
          />
          <button name="submit" onClick={submitVal} className="mode-toggle-button">
            Submit
          </button>
        </>
      )}
      <button onClick={handleInputModeToggle} className="mode-toggle-button">
        Switch to {inputMode === 'audio' ? 'Text' : 'Audio'} Input
      </button>
      <FooterWatermark />
    </div>
  );
};

export default AudioRecorder;
