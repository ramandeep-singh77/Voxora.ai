import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [currentWord, setCurrentWord] = useState('')
  const [currentSentence, setCurrentSentence] = useState('')
  const [correctedText, setCorrectedText] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [lastLetter, setLastLetter] = useState('')
  const [confidence, setConfidence] = useState(0)

  // Update text from backend
  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const response = await fetch('http://localhost:5000/get_text')
        const data = await response.json()
        setCurrentWord(data.word || '')
        setCurrentSentence(data.sentence || '')
      } catch (error) {
        console.error('Error fetching text:', error)
      }
    }, 300)

    return () => clearInterval(interval)
  }, [])

  const addSpace = async () => {
    try {
      await fetch('http://localhost:5000/add_space', { method: 'POST' })
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const deleteLetter = async () => {
    try {
      await fetch('http://localhost:5000/delete_letter', { method: 'POST' })
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const correctSentence = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('http://localhost:5000/correct', { method: 'POST' })
      const data = await response.json()
      if (data.corrected) {
        setCorrectedText(data)
      } else {
        alert('No text to correct!')
      }
    } catch (error) {
      console.error('Error:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const resetText = async () => {
    if (window.confirm('Reset all text?')) {
      try {
        await fetch('http://localhost:5000/reset', { method: 'POST' })
        setCorrectedText(null)
      } catch (error) {
        console.error('Error:', error)
      }
    }
  }

  return (
    <div className="app-container">
      {/* Header */}
      <header className="app-header">
        <div className="logo">
          <span className="logo-icon">🤟</span>
          <h1>Voxora.AI</h1>
        </div>
        <p className="tagline">Real-time Sign Language Recognition</p>
      </header>

      {/* Main Content */}
      <div className="main-grid">
        {/* Video Section */}
        <section className="video-panel">
          <div className="panel-header">
            <h2>📹 Live Camera</h2>
            <span className="status-badge">● LIVE</span>
          </div>
          <div className="video-wrapper">
            <img 
              src="http://localhost:5000/video_feed" 
              alt="Video Stream" 
              className="video-feed"
            />
          </div>
          <div className="info-box">
            <p>💡 Hold each sign for 1 second</p>
            <p>👋 No hand = "nothing"</p>
          </div>
        </section>

        {/* Text Display Section */}
        <section className="text-panel">
          <div className="panel-header">
            <h2>📝 Recognized Text</h2>
          </div>
          
          <div className="text-box">
            <div className="text-row">
              <label>Current Word:</label>
              <div className="text-value word-value">
                {currentWord || '(empty)'}
              </div>
            </div>
            
            <div className="text-row">
              <label>Sentence:</label>
              <div className="text-value sentence-value">
                {currentSentence || '(empty)'}
              </div>
            </div>
          </div>

          {correctedText && (
            <div className="corrected-box">
              <h3>✨ AI Corrected</h3>
              <div className="corrected-content">
                <p><strong>Original:</strong> {correctedText.original}</p>
                <p><strong>Corrected:</strong> {correctedText.corrected}</p>
              </div>
            </div>
          )}

          {/* Control Buttons */}
          <div className="controls">
            <button className="control-btn primary" onClick={addSpace}>
              <span>➕</span> Space
            </button>
            <button className="control-btn danger" onClick={deleteLetter}>
              <span>⌫</span> Delete
            </button>
            <button 
              className="control-btn success" 
              onClick={correctSentence}
              disabled={isLoading}
            >
              <span>✨</span> {isLoading ? 'Correcting...' : 'Correct'}
            </button>
            <button className="control-btn warning" onClick={resetText}>
              <span>🔄</span> Reset
            </button>
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p>Powered by TensorFlow • MediaPipe • GPT-4</p>
      </footer>
    </div>
  )
}

export default App
