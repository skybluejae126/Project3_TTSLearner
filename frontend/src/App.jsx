
import { useState, useRef } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // TTS State
  const [text, setText] = useState('안녕하세요, 제 목소리를 테스트해 보세요.');
  const [speaker, setSpeaker] = useState(11); // 1: female, 11: male
  const [speed, setSpeed] = useState(1.0);
  const [ttsAudioUrl, setTtsAudioUrl] = useState('');
  const [isLoadingTts, setIsLoadingTts] = useState(false);

  // RVC State
  const [modelFile, setModelFile] = useState(null);
  const [uploadedModelName, setUploadedModelName] = useState('');
  const [isLoadingUpload, setIsLoadingUpload] = useState(false);
  const [rvcAudioUrl, setRvcAudioUrl] = useState('');
  const [isLoadingRvc, setIsLoadingRvc] = useState(false);

  // Comparison State
  const [userRecording, setUserRecording] = useState(null);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [isLoadingCompare, setIsLoadingCompare] = useState(false);
  const userRecordingRef = useRef(null);

  // Global State
  const [error, setError] = useState('');

  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

  // 1. TTS Synthesis
  const handleSynthesize = async () => {
    if (!text.trim()) {
      setError('Please enter some text.');
      return;
    }
    setIsLoadingTts(true);
    setError('');
    setTtsAudioUrl('');

    try {
      const response = await axios.post(
        `${API_BASE_URL}/synthesize`,
        { text, speaker, speed },
        { responseType: 'blob' }
      );
      const url = URL.createObjectURL(new Blob([response.data], { type: 'audio/wav' }));
      setTtsAudioUrl(url);
    } catch (err) {
      handleApiError(err, 'TTS synthesis');
    } finally {
      setIsLoadingTts(false);
    }
  };

  // 2. RVC Model Upload
  const handleModelUpload = async () => {
    if (!modelFile) {
      setError('Please select a .pth model file.');
      return;
    }
    setIsLoadingUpload(true);
    setError('');

    const formData = new FormData();
    formData.append('file', modelFile);

    try {
      const response = await axios.post(`${API_BASE_URL}/upload-voice-model`, formData);
      setUploadedModelName(response.data.model_name);
    } catch (err) {
      handleApiError(err, 'model upload');
    } finally {
      setIsLoadingUpload(false);
    }
  };

  // 3. Synthesize with User Voice (RVC)
  const handleSynthesizeRvc = async () => {
    if (!text.trim() || !uploadedModelName) {
      setError('Please enter text and upload a voice model first.');
      return;
    }
    setIsLoadingRvc(true);
    setError('');
    setRvcAudioUrl('');

    try {
      const response = await axios.post(
        `${API_BASE_URL}/synthesize-user-voice`,
        { text, model_name: uploadedModelName, speaker, speed },
        { responseType: 'blob' }
      );
      const url = URL.createObjectURL(new Blob([response.data], { type: 'audio/wav' }));
      setRvcAudioUrl(url);
    } catch (err) {
      handleApiError(err, 'RVC synthesis');
    } finally {
      setIsLoadingRvc(false);
    }
  };
  
  // 4. Compare Pronunciation
  const handleCompare = async () => {
    if (!userRecording || !uploadedModelName) {
        setError('Please record or upload your voice, and ensure a reference TTS has been generated with an RVC model.');
        return;
    }
    setIsLoadingCompare(true);
    setError('');
    setComparisonResult(null);

    const formData = new FormData();
    formData.append('user_recording', userRecording);
    formData.append('reference_tts_id', uploadedModelName);

    try {
        const response = await axios.post(`${API_BASE_URL}/compare-voice`, formData);
        setComparisonResult(response.data);
    } catch (err) {
        handleApiError(err, 'voice comparison');
    } finally {
        setIsLoadingCompare(false);
    }
  };


  const handleApiError = (err, context) => {
    console.error(`Error during ${context}:`, err);
    const errorDetail = err.response?.data?.detail || `Failed during ${context}. Is the backend server running?`;
    setError(errorDetail);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Full-Stack Language Learning Tool</h1>
        {error && <p className="error-message">{error}</p>}
      </header>

      <main className="main-content">
        {/* Section 1: TTS Synthesis */}
        <section className="card">
          <h2>1. Text-to-Speech (TTS)</h2>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text here..."
            rows="3"
          />
          <div className="controls">
            <div className="control-group">
              <label>Speaker:</label>
              <select value={speaker} onChange={(e) => setSpeaker(Number(e.target.value))}>
                <option value={11}>Male</option>
                <option value={1}>Female</option>
              </select>
            </div>
            <div className="control-group">
              <label>Speed: {speed.toFixed(1)}</label>
              <input
                type="range"
                min="0.5"
                max="2.0"
                step="0.1"
                value={speed}
                onChange={(e) => setSpeed(parseFloat(e.target.value))}
              />
            </div>
          </div>
          <button onClick={handleSynthesize} disabled={isLoadingTts}>
            {isLoadingTts ? 'Synthesizing...' : 'Synthesize Base Voice'}
          </button>
          {ttsAudioUrl && <audio controls src={ttsAudioUrl} className="audio-player" />}
        </section>

        {/* Section 2: RVC Voice Conversion */}
        <section className="card">
          <h2>2. User Voice Conversion (RVC)</h2>
          <div className="control-group">
            <label>Upload .pth Model:</label>
            <input type="file" accept=".pth" onChange={(e) => setModelFile(e.target.files[0])} />
            <button onClick={handleModelUpload} disabled={!modelFile || isLoadingUpload}>
              {isLoadingUpload ? 'Uploading...' : 'Upload Model'}
            </button>
          </div>
          {uploadedModelName && <p className="success-message">Model ready: {uploadedModelName}</p>}
          
          <button onClick={handleSynthesizeRvc} disabled={isLoadingRvc || !uploadedModelName}>
            {isLoadingRvc ? 'Converting...' : 'Synthesize with My Voice'}
          </button>
          {rvcAudioUrl && <audio controls src={rvcAudioUrl} className="audio-player" />}
        </section>

        {/* Section 3: Pronunciation Practice */}
        <section className="card">
          <h2>3. Pronunciation Practice</h2>
          <div className="control-group">
            <label>Upload Your Voice (WAV):</label>
            <input type="file" accept="audio/wav" onChange={(e) => setUserRecording(e.target.files[0])} ref={userRecordingRef} />
          </div>
          <button onClick={handleCompare} disabled={isLoadingCompare || !userRecording || !rvcAudioUrl}>
            {isLoadingCompare ? 'Comparing...' : 'Compare Pronunciation'}
          </button>
          {comparisonResult && (
            <div className="results-grid">
              <div className="result-item score">
                <h3>Similarity Score</h3>
                <p>{comparisonResult.similarity_score.toFixed(2)} / 100</p>
              </div>
              <div className="result-item">
                <h3>Waveform</h3>
                <img src={`data:image/png;base64,${comparisonResult.waveform_plot}`} alt="Waveform Plot" />
              </div>
              <div className="result-item">
                <h3>Spectrogram</h3>
                <img src={`data:image/png;base64,${comparisonResult.spectrogram_plot}`} alt="Spectrogram Plot" />
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
