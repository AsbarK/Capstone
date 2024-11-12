import React from 'react';

const HadoopScriptComponent = ({script}) => {
//   const script = `iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1')); SET "PATH=%PATH%;%ALLUSERSPROFILE%\\chocolatey\\bin"; choco install hadoop -y`;

  const copyToClipboard = () => {
    navigator.clipboard.writeText(script);
    alert('Script copied to clipboard!');
  };

  return (
    <div style={{ fontFamily: 'Arial', margin: '20px', maxWidth: '600px' }}>
      <h2>Generated Script</h2>
      <pre
        style={{
          padding: '10px',
          borderRadius: '5px',
          overflowX: 'auto',
          whiteSpace: 'pre-wrap'
        }}
      >
        {script}
      </pre>
      <button 
        onClick={copyToClipboard} 
        style={{
          marginTop: '10px',
          padding: '8px 16px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        Copy to Clipboard
      </button>
    </div>
  );
};

export default HadoopScriptComponent;
