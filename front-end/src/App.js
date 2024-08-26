import React, { useState } from 'react';
import './App.css';

function App() {
  const [userInput, setUserInput] = useState('');
  const [intent, setIntent] = useState('');
  const [intentCategory, setIntentCategory] = useState('');
  const [customIntent, setCustomIntent] = useState('');
  const [customCategory, setCustomCategory] = useState('');
  const [isRecognized, setIsRecognized] = useState(false);

  const handleRecognition = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/recognize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userInput }),
    });

    const data = await response.json();
    setIntent(data.intent);
    setIntentCategory(data.intentCategory);
    setIsRecognized(true);
  };

  const handleSubmit = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/submit_custom', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        userInput,
        customIntent,
        customCategory,
      }),
    });

    const data = await response.json();
    alert(data.message);
  };

  return (
    <div className="App">
      <h1>User Intent Recognition</h1>

      <textarea
        value={userInput}
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Your input here"
        maxLength={1024}
        rows="4"
        cols="50"
      />
      
      <br />
      
      <button onClick={handleRecognition}>Recognition</button>

      {isRecognized && (
        <>
          <div className="output-row">
            <h3>Intent:</h3>
            <p>{intent}</p>
            <h3 style={{ marginLeft: '20px' }}>Intent Category:</h3>
            <p>{intentCategory}</p>
          </div>
          
          <div className="custom-intent-section">
            <p className="highlight-text">Not satisfied with the result? You could set your custom intent and intent category below:</p>
          </div>
          
          <div className="input-row">
            <h3>Custom Intent:</h3>
            <input
              type="text"
              value={customIntent}
              onChange={(e) => setCustomIntent(e.target.value)}
              placeholder="Enter your custom intent"
            />
          </div>
          
          <div className="input-row">
            <h3>Custom Intent Category:</h3>
            <input
              type="text"
              value={customCategory}
              onChange={(e) => setCustomCategory(e.target.value)}
              placeholder="Enter your custom category"
            />
          </div>
          
          <button onClick={handleSubmit} className="submit-button">Submit</button>
        </>
      )}
    </div>
  );
}

export default App;
