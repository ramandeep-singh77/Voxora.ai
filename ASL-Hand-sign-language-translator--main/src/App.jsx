import { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  const videoRef = useRef(null)
  const [currentWord, setCurrentWord] = useState('')
  const [currentSentence, setCurrentSentence] = useState('')
  const [correctedText, setCorrectedText] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [cameraActive, setCameraActive] = useState(false)
  const [isProduction, setIsProduction] = useState(false)

  // Check if running on Vercel (production)
  useEffect(() => {
    const hostname = window.location.hostname
    setIsProduction(hostname !== 'localhost' && hostname !== '127.0.0.1')
  }, [])

  // Initialize browser camera for display
  useEffect(() => {
    const startCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { width: 640, height: 480 } 
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
          setCameraActive(true)
        }
      } catch (error) {
        console.error('Camera access denied:', error)
      }
    }

    if (isProduction) {
      startCamera()
    }

    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks()
        tracks.forEach(track => track.stop())
      }
    }
  }, [isProduction])

  // Update text from backend (only on localhost)
  useEffect(() => {
    if (isProduction) return

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
  }, [isProduction])

  const addSpace = async () => {
    if (isProduction) return
    try {
      await fetch('http://localhost:5000/add_space', { method: 'POST' })
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const deleteLetter = async () => {
    if (isProduction) return
    try {
      await fetch('http://localhost:5000/delete_letter', { method: 'POST' })
    } catch (error) {
      console.error('Error:', error)
    }
  }

  const correctSentence = async () => {
    if (isProduction) return
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
    if (isProduction) return
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
      {/* Disclaimer Banner - Only on Vercel */}
      {isProduction && (
        <div className="disclaimer-banner">
          <div className="disclaimer-content">
            <span className="warning-icon">⚠️</span>
            <div className="disclaimer-text">
              <strong>UI DEMO ONLY</strong> - This is a frontend showcase. 
              For full functionality with camera and AI recognition, 
              <a href="https://github.com/ramandeep-singh77/Voxora.ai" target="_blank" rel="noopener noreferrer"> install from GitHub</a> or 
              <a href="#demo-video"> watch our demo video below</a>.
            </div>
          </div>
        </div>
      )}

      {/* Demo Video Section - Only on Vercel */}
      {isProduction && (
        <section className="demo-video-section" id="demo-video">
          <div className="demo-video-container">
            <div className="demo-video-header">
              <h2>🎬 Demo Video - See Voxora.AI in Action!</h2>
              <p className="demo-subtitle">Watch how the full AI model recognizes sign language in real-time</p>
            </div>
            <div className="video-embed-wrapper">
              <iframe
                width="100%"
                height="400"
                src="https://www.youtube.com/embed/cvyST-QWqhw"
                title="Voxora.AI - Real-time Sign Language Recognition Demo"
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowFullScreen
                className="demo-video-iframe"
              ></iframe>
            </div>
            <div className="demo-video-info">
              <div className="demo-highlights">
                <h3>🌟 What You'll See in the Demo:</h3>
                <ul>
                  <li>✅ Real-time ASL sign recognition (96-99% accuracy)</li>
                  <li>✅ Automatic word and sentence formation</li>
                  <li>✅ AI-powered grammar correction with GPT-4</li>
                  <li>✅ 28 signs supported (A-Z, space, delete)</li>
                  <li>✅ Smooth 25-30 FPS performance</li>
                </ul>
              </div>
              <div className="demo-cta">
                <h3>🚀 Ready to Try the Full Version?</h3>
                <p>This demo shows the complete AI model in action. Install locally to experience the full functionality!</p>
                <div className="demo-buttons">
                  <a 
                    href="https://github.com/ramandeep-singh77/Voxora.ai" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="demo-btn primary"
                  >
                    📦 Download from GitHub
                  </a>
                  <a 
                    href="https://youtu.be/cvyST-QWqhw" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="demo-btn secondary"
                  >
                    🎥 Watch on YouTube
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>
      )}

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
            <span className={`status-badge ${cameraActive || !isProduction ? 'active' : ''}`}>
              ● {isProduction ? (cameraActive ? 'CAMERA ON' : 'CONNECTING...') : 'LIVE'}
            </span>
          </div>
          <div className="video-wrapper">
            {isProduction ? (
              <>
                <video 
                  ref={videoRef} 
                  autoPlay 
                  playsInline
                  muted
                  className="video-feed"
                />
                <div className="demo-overlay">
                  <div className="demo-message">
                    <h3>🎥 Camera Preview Only</h3>
                    <p>AI recognition requires local installation</p>
                    <a href="https://github.com/ramandeep-singh77/Voxora.ai" target="_blank" rel="noopener noreferrer" className="github-link">
                      📦 Get Full Version on GitHub
                    </a>
                  </div>
                </div>
              </>
            ) : (
              <img 
                src="http://localhost:5000/video_feed" 
                alt="Video Stream" 
                className="video-feed"
              />
            )}
          </div>
          <div className="info-box">
            <p>💡 Hold each sign for 1 second</p>
            <p>👋 No hand = "nothing"</p>
            {isProduction && (
              <p className="demo-note">⚠️ Recognition disabled in demo mode</p>
            )}
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
            <button className="control-btn primary" onClick={addSpace} disabled={isProduction}>
              <span>➕</span> Space
            </button>
            <button className="control-btn danger" onClick={deleteLetter} disabled={isProduction}>
              <span>⌫</span> Delete
            </button>
            <button 
              className="control-btn success" 
              onClick={correctSentence}
              disabled={isLoading || isProduction}
            >
              <span>✨</span> {isLoading ? 'Correcting...' : 'Correct'}
            </button>
            <button className="control-btn warning" onClick={resetText} disabled={isProduction}>
              <span>🔄</span> Reset
            </button>
          </div>

          {isProduction && (
            <div className="production-notice">
              <p>🔒 Controls disabled in demo mode</p>
              <p>Install locally for full functionality</p>
            </div>
          )}
        </section>
      </div>

      {/* Footer */}
      <footer className="app-footer">
        <p>Powered by TensorFlow • MediaPipe • GPT-4</p>
        {isProduction && (
          <p className="github-footer">
            <a href="https://github.com/ramandeep-singh77/Voxora.ai" target="_blank" rel="noopener noreferrer">
              ⭐ Star us on GitHub
            </a>
          </p>
        )}
      </footer>
    </div>
  )
}

export default App
