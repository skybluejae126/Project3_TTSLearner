import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSynthesize = async () => {
    if (!text.trim()) {
      setError('Please enter some text.');
      return;
    }
    setIsLoading(true);
    setError('');
    setAudioUrl('');

    try {
      const response = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL}/synthesize`,
        { text },
        { responseType: 'blob' }
      );

      const blob = new Blob([response.data], { type: 'audio/wav' });
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
    } catch (err) {
      console.error('Error synthesizing speech:', err);
      setError('Failed to synthesize speech. Make sure the backend server is running.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>TTS Language Learner</h1>
        <p>Enter text to synthesize speech</p>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter text here..."
          rows="4"
          cols="50"
          disabled={isLoading}
        />
        <br />
        <button onClick={handleSynthesize} disabled={isLoading}>
          {isLoading ? 'Synthesizing...' : 'Synthesize'}
        </button>

        {error && <p className="error">{error}</p>}

        {audioUrl && (
          <div className="audio-player">
            <h2>Generated Audio</h2>
            <audio controls src={audioUrl} />
            <br />
            <a href={audioUrl} download="synthesis.wav">
              Download Audio
            </a>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;