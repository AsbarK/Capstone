import React from 'react';

const AIResponse = ({ response }) => {
  return (
    <div className="ai-response">
      <h3>AI Response:</h3>
      <p>{response}</p>
    </div>
  );
};

export default AIResponse;
